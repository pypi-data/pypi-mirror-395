from __future__ import annotations

import csv
import io
import json
import os
import re
import unicodedata
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Dict, Optional

import requests

import boto3
import pycountry
from botocore.exceptions import ClientError

from .default_aliases import DEFAULT_CUSTOM_ALIASES

_SLACK_WEBHOOK_ENV = "COUNTRY_LOOKUP_SLACK_WEBHOOK"
_SLACK_WEBHOOK_URL = os.getenv(_SLACK_WEBHOOK_ENV)


def _parse_float_env(name: str, default: float) -> float:
    raw = os.getenv(name)
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


_SLACK_TIMEOUT = _parse_float_env("COUNTRY_LOOKUP_SLACK_TIMEOUT", 2.0)


def _post_slack_message(original: str, normalized_key: str) -> None:
    """
    Fire-and-forget Slack webhook notification for unresolved lookups.
    """
    if not _SLACK_WEBHOOK_URL:
        return

    if len(original) <= 200:
        truncated_original = original
    else:
        truncated_original = f"{original[:197]}..."
    payload = {
        "text": (
            ":warning: country_iso2ify unresolved lookup\n"
            f"*input*: `{truncated_original}`\n"
            f"*normalized*: `{normalized_key}`"
        )
    }
    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}

    try:
        requests.post(
            _SLACK_WEBHOOK_URL,
            data=data,
            headers=headers,
            timeout=_SLACK_TIMEOUT,
        )
    except requests.RequestException:
        # Swallow network issues rather than breaking resolution flows.
        return


def _normalize_whitespace(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = re.sub(r"\s+", " ", value).strip()
    return normalized or None


def _normalize_for_lookup(value: str) -> str:
    """
    Aggressive normalization:
    - lowercase
    - remove accents
    - replace non-alphanumeric with space
    - collapse spaces
    """
    value = value.strip().lower()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def _detect_delimiter(value: str | None) -> str | None:
    if not value:
        return None
    if "," in value:
        return ","
    if "|" in value:
        return "|"
    return None


def _strip_accents(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    return "".join(ch for ch in value if not unicodedata.combining(ch))


def _pick_csv_field(
    fieldnames: list[str],
    candidates: list[str],
) -> str | None:
    lowered = {name.lower(): name for name in fieldnames}
    for candidate in candidates:
        if candidate in lowered:
            return lowered[candidate]
    return None


@dataclass
class CountryResolver:
    """
    Self-contained, DB-free country resolver.

    Priority per input string:
        1. pycountry alpha-2 / alpha-3 codes (O(1) lookups)
        2. Custom aliases (outliers, political cases, colloquial names)
        3. pycountry exact-style lookups (lookup, name, official_name)
        4. Optional pycountry fuzzy search with validation

    All data is in-memory, suitable for Lambda and other stateless
    environments.
    """

    allow_fuzzy: bool = False
    fuzzy_min_score: float = 0.86  # strict threshold to avoid bad matches
    _alpha2_set: set[str] = field(
        init=False,
        repr=False,
        default_factory=set,
    )
    _alpha3_map: Dict[str, str] = field(
        init=False,
        repr=False,
        default_factory=dict,
    )
    _name_map: Dict[str, str] = field(
        init=False,
        repr=False,
        default_factory=dict,
    )
    _custom_aliases: Dict[str, str] = field(
        init=False,
        repr=False,
        default_factory=dict,
    )
    _cache: Dict[str, Optional[str]] = field(
        init=False,
        repr=False,
        default_factory=dict,
    )
    _s3_alias_meta: Dict[tuple[str, str], Dict[str, str]] = field(
        init=False,
        repr=False,
        default_factory=dict,
    )

    def __post_init__(self) -> None:
        self._load_pycountry_data()
        self._load_custom_aliases(DEFAULT_CUSTOM_ALIASES)

    # ---------- Initialization helpers ----------

    def _load_pycountry_data(self) -> None:
        """
        Load pycountry data into in-memory structures.
        Called once per resolver instance (per process / Lambda cold start).
        """
        for c in pycountry.countries:
            alpha2 = getattr(c, "alpha_2", None)
            alpha3 = getattr(c, "alpha_3", None)

            if alpha2:
                alpha2_u = alpha2.upper()
                self._alpha2_set.add(alpha2_u)

                for attr in ("name", "official_name"):
                    val = getattr(c, attr, None)
                    if val:
                        key = _normalize_for_lookup(val)
                        if key and key not in self._name_map:
                            self._name_map[key] = alpha2_u

            if alpha2 and alpha3:
                self._alpha3_map[alpha3.upper()] = alpha2_u

    def _load_custom_aliases(self, aliases: Dict[str, str]) -> None:
        """
        Load custom alias -> alpha2 mapping, normalizing keys.
        """
        for raw_name, alpha2 in aliases.items():
            if not alpha2:
                continue
            key = _normalize_for_lookup(raw_name)
            if not key:
                continue
            self._custom_aliases[key] = alpha2.upper()

    def load_custom_aliases_from_s3(
        self,
        bucket: str,
        key: str,
        *,
        encoding: str = "utf-8",
        delimiter: str = ",",
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
        aws_session_token: str | None = None,
        region_name: str | None = None,
        skip_if_unchanged: bool = True,
    ) -> int:
        """
        Download a CSV file from S3 and merge its aliases.

        The CSV should contain two columns (alias/name and alpha2/code). A
        header row is recommended but not required. Returns the number of
        aliases ingested.
        """
        client_kwargs = {}
        for key_name, value in [
            ("aws_access_key_id", aws_access_key_id),
            ("aws_secret_access_key", aws_secret_access_key),
            ("aws_session_token", aws_session_token),
            ("region_name", region_name),
        ]:
            if value:
                client_kwargs[key_name] = value

        s3_client = boto3.client("s3", **client_kwargs)
        meta_key = (bucket, key)
        cached_meta = self._s3_alias_meta.get(meta_key)
        etag = None
        last_modified = None

        if skip_if_unchanged:
            try:
                head = s3_client.head_object(Bucket=bucket, Key=key)
                etag = head.get("ETag")
                last_modified = head.get("LastModified")
                if last_modified is not None:
                    last_modified = last_modified.isoformat()
            except ClientError:
                head = None
            if cached_meta:
                if etag and cached_meta.get("etag") == etag:
                    return 0
                if (
                    not etag
                    and last_modified
                    and cached_meta.get("last_modified") == last_modified
                ):
                    return 0

        response = s3_client.get_object(Bucket=bucket, Key=key)
        csv_bytes = response["Body"].read()
        csv_text = csv_bytes.decode(encoding)
        aliases = self._parse_alias_csv(csv_text, delimiter=delimiter)
        if not aliases:
            return 0
        self._load_custom_aliases(aliases)
        # Purge cache entries that may be affected.
        for raw_name in aliases.keys():
            norm = _normalize_for_lookup(raw_name)
            if norm in self._cache:
                del self._cache[norm]

        response_etag = response.get("ETag") or etag
        response_last_modified = response.get("LastModified")
        if response_last_modified is not None:
            response_last_modified = response_last_modified.isoformat()
        if response_last_modified is None:
            response_last_modified = last_modified

        self._s3_alias_meta[meta_key] = {
            "etag": response_etag or "",
            "last_modified": response_last_modified or "",
        }
        return len(aliases)

    def _parse_alias_csv(
        self,
        csv_text: str,
        *,
        delimiter: str = ",",
    ) -> Dict[str, str]:
        """
        Parse CSV text into a name -> alpha2 mapping. Supports header-based
        files and header-less files (first two columns).
        """
        buffer = io.StringIO(csv_text)
        reader = csv.DictReader(buffer, delimiter=delimiter)
        aliases: Dict[str, str] = {}

        if reader.fieldnames:
            alias_field = _pick_csv_field(
                [name for name in reader.fieldnames if name],
                ["alias", "name"],
            )
            code_field = _pick_csv_field(
                [name for name in reader.fieldnames if name],
                ["alpha2", "alpha_2", "code"],
            )
            if alias_field and code_field:
                for row in reader:
                    alias_val = row.get(alias_field, "")
                    code_val = row.get(code_field, "")
                    if alias_val and code_val:
                        aliases[alias_val] = code_val
                if aliases:
                    return aliases

        # Fallback: treat as a simple two-column CSV
        buffer.seek(0)
        plain_reader = csv.reader(buffer, delimiter=delimiter)
        for idx, row in enumerate(plain_reader):
            if not row or len(row) < 2:
                continue
            first, second = row[0], row[1]
            if idx == 0 and first.strip().lower() in {"alias", "name"}:
                # Skip header row when parsing without DictReader support.
                continue
            if first and second:
                aliases[first] = second

        return aliases

    # ---------- Public API ----------

    def resolve(self, country_name: str | None) -> Optional[str]:
        """
        Resolve input string to ISO alpha-2 code, or None if unresolved.
        Supports comma- or pipe-separated lists, returning a string that
        preserves the original separator formatting.
        """
        normalized_ws = _normalize_whitespace(country_name)
        if not normalized_ws:
            return None

        delimiter = _detect_delimiter(country_name)
        if delimiter:
            return self._resolve_delimited(country_name, delimiter)

        return self._resolve_single(normalized_ws, already_normalized=True)

    def add_alias(self, name: str, alpha2: str) -> None:
        """
        Dynamically add an alias for this process.
        (If you want persistence, you handle writing out configs yourself.)
        """
        key = _normalize_for_lookup(name)
        if not key:
            return
        self._custom_aliases[key] = alpha2.upper()
        if key in self._cache:
            del self._cache[key]

    # ---------- Core (uncached) resolution logic ----------

    def _resolve_single(
        self,
        value: str,
        *,
        already_normalized: bool = False,
    ) -> Optional[str]:
        normalized_ws = (
            value if already_normalized else _normalize_whitespace(value)
        )
        if not normalized_ws:
            return None

        key = _normalize_for_lookup(normalized_ws)
        if key in self._cache:
            return self._cache[key]

        alpha2 = self._resolve_uncached(normalized_ws, norm_key=key)
        alpha2 = alpha2.upper() if alpha2 else None
        if alpha2 is None:
            _post_slack_message(normalized_ws, key)
        if alpha2 is not None or key not in self._cache:
            self._cache[key] = alpha2
        return alpha2

    def _resolve_delimited(self, raw_value: str, delimiter: str) -> str:
        """
        Resolve each element separated by the given delimiter.
        """
        tokens = raw_value.split(delimiter)
        resolved_tokens = [
            self._resolve_single(token) for token in tokens
        ]
        return delimiter.join(
            token if token is not None else "None"
            for token in resolved_tokens
        )

    def _resolve_uncached(
        self,
        value: str,
        *,
        norm_key: Optional[str] = None,
    ) -> Optional[str]:
        """
        Internal resolver without caching. `value` is whitespace-normalized.
        """
        upper = value.upper()

        # 1) pycountry fast-path: alpha-2 codes
        if len(upper) == 2 and upper in self._alpha2_set:
            return upper

        # 2) alpha-3 codes -> alpha-2 via pycountry
        if len(upper) == 3 and upper in self._alpha3_map:
            return self._alpha3_map[upper]

        norm_key = norm_key or _normalize_for_lookup(value)

        # 3) pycountry name/official_name map (exact-ish, normalized)
        if norm_key in self._name_map:
            return self._name_map[norm_key]

        # 4) Custom aliases (your override layer)
        if norm_key in self._custom_aliases:
            return self._custom_aliases[norm_key]

        # 5) pycountry.lookup() on original + accent-stripped
        alpha2 = self._lookup_pycountry_exact(value)
        if alpha2:
            return alpha2

        # 6) Optional fuzzy search with validation
        if self.allow_fuzzy:
            alpha2 = self._lookup_pycountry_fuzzy(value)
            if alpha2:
                return alpha2

        return None

    # ---------- pycountry exact & fuzzy helpers ----------

    def _lookup_pycountry_exact(self, value: str) -> Optional[str]:
        """
        Use pycountry.countries.lookup() for exact-style matches.
        This covers alpha2, alpha3, numeric, name, official_name, etc.
        Try both original and accent-stripped versions.
        """
        candidates = [value, _strip_accents(value)]
        seen = set()
        for v in candidates:
            if not v or v in seen:
                continue
            seen.add(v)
            try:
                c = pycountry.countries.lookup(v)
                if not c:
                    if "-" in v:
                        c = pycountry.countries.lookup(v.replace("-", " "))
                    if v.lower().startswith("the "):
                        c = pycountry.countries.lookup(v[4:])
            except LookupError:
                continue
            alpha2 = getattr(c, "alpha_2", None)
            if alpha2:
                return alpha2.upper()
        return None

    def _lookup_pycountry_fuzzy(self, value: str) -> Optional[str]:
        """
        pycountry.search_fuzzy() with similarity validation to avoid
        bad matches (e.g., 'Kosovo' -> 'RS', 'Niger' -> 'Nigeria').
        """
        value = value.strip()
        if len(value) < 3:
            return None

        try:
            matches = pycountry.countries.search_fuzzy(value)
        except LookupError:
            return None

        if not matches:
            return None

        top = matches[0]
        alpha2 = getattr(top, "alpha_2", None)
        if not alpha2:
            return None

        query_norm = _normalize_for_lookup(value)
        cand_names = [
            getattr(top, "name", "") or "",
            getattr(top, "official_name", "") or "",
        ]
        cand_norms = [_normalize_for_lookup(n) for n in cand_names if n]

        best_score = 0.0
        for cand in cand_norms:
            score = SequenceMatcher(None, query_norm, cand).ratio()
            if score > best_score:
                best_score = score

        if best_score < self.fuzzy_min_score:
            return None

        return alpha2.upper()
