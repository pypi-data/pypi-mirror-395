country-iso2ify
====================

A lightweight Python library for converting **free-form country names** into standardized **ISO-3166 alpha-2** codes.Designed for real-world datasets, APIs, and AWS Lambda — with **no database**, **no external APIs**, and **safe fallback logic**.

Features
--------

*   🔍 **Accurate ISO resolution** using pycountry
    
*   🎛 **Custom alias layer** for outliers (e.g., _Kosovo → XK_, _Ivory Coast → CI_)
    
*   ⚡ **Fully in-memory**, Lambda-friendly, fast lookups
    
*   🧠 Optional **validated fuzzy matching**
    
*   🔧 Easily extend with add\_alias()
    
*   🗂 Includes curated default aliases
    

Installation
------------

```
   pip install country-iso2ify
```

Or include in your Lambda layer / requirements.

Usage
-----
```
  from country_iso2ify import get_resolver

  resolver = get_resolver()

  resolver.resolve("United States")     # "US"
  resolver.resolve("Ivory Coast")       # "CI"
  resolver.resolve("Kosovo")            # "XK"
  resolver.resolve("Republic of Korea") # "KR"
```

### Add aliases dynamically

```   
  resolver.add_alias("Mainland China", "CN")
```

### Load aliases from S3

```
  resolver.load_custom_aliases_from_s3(
      bucket="my-bucket",
      key="configs/custom_alias.csv",
      skip_if_unchanged=True,  # default: compares ETag/LastModified before downloading
  )
```

The CSV should contain either a header row with columns like `alias` / `name`
and `alpha2` / `alpha_2` / `code`, or simply two columns without headers
(alias in the first column, ISO alpha-2 code in the second). Additional
columns are ignored.

By default the resolver issues a cheap `HeadObject` call and skips the
download if the ETag/Last-Modified matches the last loaded version. Pass
`skip_if_unchanged=False` if you always want to re-fetch the file.

### Enable safe fuzzy matching

```
  from country_iso2ify import CountryResolver

  resolver = CountryResolver(allow_fuzzy=True)
  resolver.resolve("Unted Sttes")  # "US"
```

### Slack notifications for unresolved names

Set the `COUNTRY_LOOKUP_SLACK_WEBHOOK` environment variable to a Slack
incoming-webhook URL to receive alerts whenever the resolver fails to map an
input country name. Each unique unresolved name is reported once per process
to avoid noisy repeats. You can optionally override the requests timeout
(default `2.0` seconds) via `COUNTRY_LOOKUP_SLACK_TIMEOUT`.

Why this library?
-----------------

*   Works **offline**
    
*   Handles **non-standard names**
    
*   Deterministic, safe, and fast
    
*   Perfect for ETL pipelines, APIs, and Lambda workloads
    

License
-------

MIT License.
