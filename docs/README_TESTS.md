# Running Tests

## Setup

Make sure you have installed all dependencies:

```bash
cd backend
pip install -r requirements.txt
```

## Running All Tests

```bash
pytest
```

## Running Specific Test Files

```bash
pytest tests/test_download.py
pytest tests/test_parse.py
pytest tests/test_settings.py
pytest tests/test_logs.py
pytest tests/test_run_full.py
pytest tests/test_rate_limiter.py
pytest tests/test_database.py
```

## Running with Verbose Output

```bash
pytest -v
```

## Running with Coverage

```bash
pip install pytest-cov
pytest --cov=app --cov-report=html
```

## Test Structure

- `test_health.py` - Health check endpoint tests
- `test_download.py` - Download endpoint tests (including rate limiting)
- `test_parse.py` - Parse endpoint tests
- `test_settings.py` - Settings endpoint tests
- `test_logs.py` - Logs endpoint tests
- `test_run_full.py` - Full automation endpoint tests
- `test_rate_limiter.py` - Rate limiter unit tests
- `test_database.py` - Database service tests

## Notes

- Tests use temporary directories and databases
- Rate limiter tests may take a few seconds due to timing
- Some download tests may fail if NSE URLs are inaccessible (expected)

