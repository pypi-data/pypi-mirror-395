# pip-audit-extra [![codecov](https://codecov.io/gh/Kirill-Lekhov/pip-audit-extra/graph/badge.svg?token=KBUU5XZ982)](https://codecov.io/gh/Kirill-Lekhov/pip-audit-extra)
Extended version of [pip-audit](https://pypi.org/project/pip-audit/).

## Features
* Viewing vulnerabilities of project dependencies along with severities.

## Installation
```sh
pip install pip-audit-extra
```

## Usage
```sh
cat requirements.txt | pip-audit-extra
```

Poetry
```sh
poetry export -f requirements.txt | pip-audit-extra
# or
poetry run pip-audit-extra --local
```

UV
```sh
uv export --format requirements-txt | pip-audit-extra
# or
uv run pip-audit-extra --local
```

### Severity filter
If necessary, you can filter vulnerabilities by severity.
By default, the filter selects vulnerabilities with the specified severity AND SEVERITIES WITH A HIGHER PRIORITY.
It only affects the vulnerability table.
```sh
cat requirements.txt | pip-audit-extra --severity CRITICAL
```

To select only the specified level, add the prefix `~`, for example:
```sh
cat requirements.txt | pip-audit-extra --severity ~CRITICAL
```

### Fail level
You can set severity of vulnerability from which the audit will be considered to have failed.
```sh
cat requirements.txt | pip-audit-extra --fail-level HIGH
```
In this example, the audit will be considered failed if vulnerabilities of CRITICAL or HIGH severity are found.

### Caching
Caching is used to speed up re-auditing by maintaining the severity of vulnerabilities.

By default, cached record is valid for a day from the moment of saving.
You can control the lifetime of entries in the cache.

```sh
# (default) 1 day
cat requirements.txt | pip-audit-extra --cache-lifetime 1d

# disable cache
cat requirements.txt | pip-audit-extra --cache-lifetime 0

# 1 minute
cat requirements.txt | pip-audit-extra --cache-lifetime 60

# 1 weak
cat requirements.txt | pip-audit-extra --cache-lifetime 604800

# 15 seconds
cat requirements.txt | pip-audit-extra --cache-lifetime 15s

# 30 minutes
cat requirements.txt | pip-audit-extra --cache-lifetime 30m

# 12 hours
cat requirements.txt | pip-audit-extra --cache-lifetime 12h

# 1 weak
cat requirements.txt | pip-audit-extra --cache-lifetime 7d
```

#### Custom cache path
You can use the `PAE_CACHE_DIR` environment variable to specify path to the cache folder.

```sh
PAE_CACHE_DIR="/tmp/pae/" pip-audit-extra --local
```

### Local packages check
You can check packages which installed in the current local environment without installing dependencies in isolated environment.

```sh
pip-audit-extra --local
```

### Disable pip
You can skip isolated environment building (only if requirements.txt file contains hashes) to speedup audit.

```sh
cat requirements.txt | pip-audit-extra --disable-pip
```

#### ⛔Limitations⛔
There are certain types of dependencies that are not supported by pip-audit
(for example, dependencies installed directly from github with a specific hash).
