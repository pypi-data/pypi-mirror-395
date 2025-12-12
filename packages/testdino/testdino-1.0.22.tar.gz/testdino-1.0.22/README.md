# testdino

[![PyPI version](https://badge.fury.io/py/testdino.svg)](https://pypi.org/project/testdino/)
[![Python](https://img.shields.io/pypi/pyversions/testdino.svg)](https://pypi.org/project/testdino/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **TestDino CLI** - Cache test metadata and upload Playwright test reports to TestDino platform

## Quick Start

> **⚠️ Important:** The `testdino upload` command requires a JSON report to be generated during test execution. Make sure to:
> 1. Install required plugins: `pip install pytest-playwright-json pytest-html`
> 2. Run your tests with `--playwright-json` flag: `pytest --playwright-json=test-results/report.json`
> 3. Optionally generate HTML reports: `pytest --html=test-results/index.html --self-contained-html`



### Cache Command
```bash
# Cache test execution metadata after Playwright runs
testdino cache --token="your-api-token"

# With custom directory (recommended when test results are in a specific folder)
testdino cache --working-dir test-results --token="your-api-token"

# With verbose logging
testdino cache --working-dir test-results --verbose --token="your-api-token"
```

### Last Failed Command
```bash
# Get last failed test cases for Playwright reruns
testdino last-failed --token="your-api-token"

# Run only last failed tests
pytest $(testdino last-failed --token="your-api-token")
```

### Upload Command
```bash
# Upload test reports with attachments
testdino upload ./test-results --token="your-api-token"

# Upload all attachments
testdino upload ./test-results --token="your-api-token" --upload-full-json
```

## Features

- **Test Metadata Caching** - Store test execution metadata after Playwright runs
- **Last Failed Tests** - Retrieve and rerun only failed tests for faster CI/CD pipelines
- **Zero Configuration** - Auto-discovers Playwright reports and configuration
- **Smart Shard Detection** - Automatically detects Playwright shard information
- **CI/CD Ready** - Works seamlessly with GitHub Actions, GitLab CI, Jenkins, Azure DevOps
- **Secure Authentication** - Token-based API authentication

## Commands

### Cache Command

Store test execution metadata after Playwright runs.

```bash
# Basic usage
testdino cache --token="your-token"

# With custom working directory
testdino cache --working-dir ./test-results --token="your-token"

# With verbose logging
testdino cache --verbose --token="your-token"
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--working-dir <path>` | Directory to scan for test results | Current directory |
| `--cache-id <value>` | Custom cache ID override | Auto-detected |
| `-t, --token <value>` | TestDino API token | Required |
| `-v, --verbose` | Enable verbose logging | `false` |

### Last Failed Command

Retrieve cached test failures for intelligent reruns.

```bash
# Basic usage
testdino last-failed --token="your-token"

# Run only last failed tests
pytest $(testdino last-failed --token="your-token")

# With custom branch and commit
testdino last-failed --branch="main" --commit="abc123" --token="your-token"
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--cache-id <value>` | Custom cache ID override | Auto-detected |
| `--branch <value>` | Custom branch name override | Auto-detected |
| `--commit <value>` | Custom commit hash override | Auto-detected |
| `-t, --token <value>` | TestDino API token | Required |
| `-v, --verbose` | Enable verbose logging | `false` |

### Upload Command

Upload test reports with attachments.

> **⚠️ Important:** The `testdino upload` command requires a JSON report to function. You must:
> 1. Install required plugins: `pip install pytest-playwright-json pytest-html`
> 2. Run your tests with the `--playwright-json` flag: `pytest --playwright-json=test-results/report.json`
> 3. Optionally generate HTML reports: `pytest --html=test-results/index.html --self-contained-html`

```bash
# Basic upload
testdino upload ./test-results --token="your-token"

# Upload with attachments
testdino upload ./test-results --token="your-token" --upload-images --upload-videos

# Upload all attachments
testdino upload ./test-results --token="your-token" --upload-full-json
```

**Options:**

| Option | Description |
|--------|-------------|
| `<report-directory>` | Directory containing Playwright reports (required) |
| `-t, --token <value>` | TestDino API token (required) |
| `--upload-images` | Upload image attachments |
| `--upload-videos` | Upload video attachments |
| `--upload-html` | Upload HTML reports |
| `--upload-traces` | Upload trace files |
| `--upload-files` | Upload file attachments (.md, .pdf, .txt, .log) |
| `--upload-full-json` | Upload all attachments |
| `-v, --verbose` | Enable verbose logging |

### Environment Variables

```bash
export TESTDINO_TOKEN="your-api-token"
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Playwright Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pytest pytest-playwright pytest-playwright-json pytest-html testdino
          playwright install chromium --with-deps

      - name: Run tests
        run: |
          pytest \
            --playwright-json=test-results/report.json \
            --html=test-results/index.html \
            --self-contained-html

      - name: Cache rerun metadata
        if: always()
        run: testdino cache --working-dir test-results --token="${{ secrets.TESTDINO_TOKEN }}" -v

      - name: Upload test reports
        if: always()
        run: testdino upload ./test-results --token="${{ secrets.TESTDINO_TOKEN }}" --upload-full-json
```

### GitLab CI

```yaml
image: python:3.11

stages:
  - test

playwright-tests:
  stage: test
  script:
    - pip install pytest pytest-playwright pytest-playwright-json pytest-html testdino
    - playwright install chromium --with-deps
    - pytest --playwright-json=test-results/report.json --html=test-results/index.html --self-contained-html
    - testdino upload ./test-results --token="$TESTDINO_TOKEN" --upload-full-json
  when: always
```

### Jenkins

```groovy
pipeline {
    agent any

    environment {
        TESTDINO_TOKEN = credentials('testdino-token')
    }

    stages {
        stage('Test') {
            steps {
                sh 'pip install pytest pytest-playwright pytest-playwright-json pytest-html testdino'
                sh 'playwright install chromium --with-deps'
                sh 'pytest --playwright-json=test-results/report.json --html=test-results/index.html --self-contained-html'
                sh 'testdino upload ./test-results --token="$TESTDINO_TOKEN" --upload-full-json'
            }
        }
    }
}
```

## Authentication

### Getting Your Token

1. Sign up at [TestDino](https://app.testdino.com)
2. Navigate to **Settings** > **API Tokens**
3. Generate a new token
4. Store it securely in your CI/CD secrets

**Token Format:**
```
trx_{environment}_{64-character-hex-string}
```

**Security Best Practices:**
- Never commit tokens to version control
- Use environment variables or CI/CD secrets
- Rotate tokens regularly

## Examples

### Basic Workflow

```bash
# Run tests with JSON and HTML reports
pytest \
  --playwright-json=test-results/report.json \
  --html=test-results/index.html \
  --self-contained-html

# Cache metadata (specify directory where test results are located)
testdino cache --working-dir test-results --token="your-token"
```

### Intelligent Test Reruns

```bash
# Run tests with JSON and HTML reports, then cache results
pytest \
  --playwright-json=test-results/report.json \
  --html=test-results/index.html \
  --self-contained-html
testdino cache --working-dir test-results --token="your-token"

# On next run, execute only previously failed tests
pytest $(testdino last-failed --token="your-token")
```

### Complete CI/CD Workflow

```bash
# Run all tests with JSON and HTML reports
pytest \
  --playwright-json=test-results/report.json \
  --html=test-results/index.html \
  --self-contained-html

# Cache test metadata (specify directory where test results are located)
testdino cache --working-dir test-results --token="$TESTDINO_TOKEN"

# Rerun only failed tests
if [ $? -ne 0 ]; then
  FAILED=$(testdino last-failed --token="$TESTDINO_TOKEN")
  [ -n "$FAILED" ] && pytest $FAILED
fi
```

## Support

- **Documentation**: [docs.testdino.com](https://docs.testdino.com)
- **Issues**: [GitHub Issues](https://github.com/testdino-inc/testdino-cli/issues)
- **Email**: support@testdino.com

---

**Made with love by the [TestDino](https://testdino.com) team**
