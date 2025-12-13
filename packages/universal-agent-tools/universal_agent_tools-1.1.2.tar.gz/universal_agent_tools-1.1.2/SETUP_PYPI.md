# PyPI Publishing Setup

This document describes how to set up PyPI publishing for `universal-agent-tools`.

## Required Secrets

The GitHub Actions workflows require two secrets to be configured:

1. **PYPI_API_TOKEN** - API token for production PyPI
2. **TEST_PYPI_API_TOKEN** - API token for TestPyPI

## Setup Steps

### 1. Create GitHub Environments

The workflows use GitHub Environments for deployment protection. Create them via GitHub web UI or CLI:

```bash
# Create testpypi environment
gh api repos/mjdevaccount/universal_agent_tools/environments/testpypi -X PUT -f '{"wait_timer":0}'

# Create pypi environment  
gh api repos/mjdevaccount/universal_agent_tools/environments/pypi -X PUT -f '{"wait_timer":0}'
```

### 2. Set Repository Secrets

Copy the secrets from the nexus repo. You can set them interactively:

```bash
# Set TestPyPI token (will prompt for value)
gh secret set TEST_PYPI_API_TOKEN --repo mjdevaccount/universal_agent_tools

# Set PyPI token (will prompt for value)
gh secret set PYPI_API_TOKEN --repo mjdevaccount/universal_agent_tools
```

Or set them from environment variables if you have them:

```bash
# If you have the tokens in environment variables
$env:TEST_PYPI_API_TOKEN = "your-testpypi-token"
$env:PYPI_API_TOKEN = "your-pypi-token"

gh secret set TEST_PYPI_API_TOKEN --repo mjdevaccount/universal_agent_tools --body "$env:TEST_PYPI_API_TOKEN"
gh secret set PYPI_API_TOKEN --repo mjdevaccount/universal_agent_tools --body "$env:PYPI_API_TOKEN"
```

### 3. Set Environment Secrets (Optional but Recommended)

For better security, you can also set secrets at the environment level:

```bash
# Set TestPyPI environment secret
gh secret set TEST_PYPI_API_TOKEN --repo mjdevaccount/universal_agent_tools --env testpypi

# Set PyPI environment secret
gh secret set PYPI_API_TOKEN --repo mjdevaccount/universal_agent_tools --env pypi
```

## Publishing

Once secrets are configured, publishing can be triggered by:

1. **Creating a GitHub Release** - Automatically publishes to production PyPI
2. **Manual Workflow Dispatch** - Go to Actions → Publish to PyPI → Run workflow
   - Choose `testpypi` to test first
   - Choose `pypi` for production release

## Getting PyPI API Tokens

If you need to create new tokens:

1. **TestPyPI**: https://test.pypi.org/manage/account/token/
2. **Production PyPI**: https://pypi.org/manage/account/token/

Create a new API token with "Upload packages" scope.

