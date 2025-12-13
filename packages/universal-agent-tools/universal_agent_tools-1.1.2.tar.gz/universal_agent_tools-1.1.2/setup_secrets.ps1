# Script to copy PyPI secrets from nexus repo to tools repo
# Note: You'll need to manually enter the token values when prompted

Write-Host "Setting up PyPI secrets for universal_agent_tools repository..."
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path ".github/workflows/publish.yml")) {
    Write-Host "Error: Must run from universal_agent_tools directory"
    exit 1
}

# Create environments if they don't exist
Write-Host "Creating GitHub environments..."
try {
    $envBody = '{"wait_timer":0}'
    gh api repos/mjdevaccount/universal_agent_tools/environments/testpypi -X PUT --input - <<< $envBody 2>&1 | Out-Null
    gh api repos/mjdevaccount/universal_agent_tools/environments/pypi -X PUT --input - <<< $envBody 2>&1 | Out-Null
    Write-Host "✓ Environments created"
} catch {
    Write-Host "Environments may already exist (this is OK)"
}

Write-Host ""
Write-Host "Now you need to set the secrets. You can either:"
Write-Host ""
Write-Host "Option 1: Set secrets interactively (will prompt for values):"
Write-Host "  gh secret set TEST_PYPI_API_TOKEN --repo mjdevaccount/universal_agent_tools"
Write-Host "  gh secret set PYPI_API_TOKEN --repo mjdevaccount/universal_agent_tools"
Write-Host ""
Write-Host "Option 2: If you have the tokens in environment variables:"
Write-Host "  gh secret set TEST_PYPI_API_TOKEN --repo mjdevaccount/universal_agent_tools --body `$env:TEST_PYPI_API_TOKEN"
Write-Host "  gh secret set PYPI_API_TOKEN --repo mjdevaccount/universal_agent_tools --body `$env:PYPI_API_TOKEN"
Write-Host ""
Write-Host "To get the token values, check your password manager or PyPI account:"
Write-Host "  TestPyPI: https://test.pypi.org/manage/account/token/"
Write-Host "  Production PyPI: https://pypi.org/manage/account/token/"
Write-Host ""

