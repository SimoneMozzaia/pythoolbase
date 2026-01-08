# pytoolbase

A small, Windows-first toolbox of reusable utilities for scripts and probes.

## Goals

- PEP8 compliant, pythonic code
- Fail-fast behavior (exceptions, no silent best-effort)
- Optional dependencies via `extras`
- Usable from both NAS paths and Git repos

## Installation

From a NAS path:

```powershell
pip install \\NAS\share\pytoolbase
```

With extras:

```powershell
pip install "pytoolbase[excel,db]"
```

## Directory conventions

Set `PYTOOLBASE_ROOT` to a folder that contains (by convention):

- `env/` (dotenv files)
- `secrets/` (credentials, tokens)
- `queries/` (SQL files)
- `logs/` (log files)

`PathContext` will *not* create any folder automatically.

## Environment keys (general `.env`)

- `jdbc_driver`
- `jdbc_url_prefix`
- `jt400_jar_path`

Country env file naming:

- `.<COUNTRY>-<ENV>-env` (e.g. `.IT-prod-env`)

Country env keys typically include:

- `db_host`
- `db_user`
- `db_password`
