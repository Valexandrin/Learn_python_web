# Celery(+redis) start on Windows

## One-time action

```bash
poetry install celery[redis]
poetry install eventlet
```

## Usage

```bash
celery -A <mymodule> worker -l info -P eventlet
```
