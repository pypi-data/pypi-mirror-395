# Security Policy

## Supported Versions

We actively support the latest major version of python-opendota. Security updates will be applied to:

| Version | Supported          |
| ------- | ------------------ |
| 26.x.x  | :white_check_mark: |
| < 26.0  | :x:                |

## Reporting a Vulnerability

We take the security of python-opendota seriously. If you have discovered a security vulnerability, please follow these steps:

### 1. Do NOT Create a Public Issue

Security vulnerabilities should **never** be reported through public GitHub issues.

### 2. Report Privately

Please report security vulnerabilities by emailing the maintainers directly or through GitHub's private vulnerability reporting:

1. Go to the Security tab of the repository
2. Click on "Report a vulnerability"
3. Provide detailed information about the vulnerability

### 3. Information to Include

When reporting a vulnerability, please include:

- **Description**: Clear description of the vulnerability
- **Impact**: What can an attacker achieve with this vulnerability?
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Affected Versions**: Which versions are affected
- **Suggested Fix**: If you have suggestions for fixing the issue

### 4. Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 5 business days
- **Fix Timeline**: Depending on severity:
  - Critical: Within 7 days
  - High: Within 14 days
  - Medium: Within 30 days
  - Low: Next regular release

## Security Best Practices for Users

### API Key Security

1. **Never commit API keys to version control**
   ```python
   # BAD - Never do this
   client = OpenDota(api_key="your-actual-key-here")
   
   # GOOD - Use environment variables
   client = OpenDota(api_key=os.getenv("OPENDOTA_API_KEY"))
   ```

2. **Use environment variables or secure vaults**
   ```bash
   export OPENDOTA_API_KEY="your-api-key"
   ```

3. **Rotate API keys regularly**

4. **Use minimal permissions when possible**

### Dependency Security

1. **Keep dependencies updated**
   ```bash
   uv sync --upgrade
   ```

2. **Review dependency changes**
   ```bash
   uv pip list --outdated
   ```

3. **Use dependency scanning tools**

### Network Security

1. **Always use HTTPS** (the library enforces this by default)

2. **Be cautious with untrusted data**
   ```python
   # Validate data from API responses before processing
   if not isinstance(match_id, int):
       raise ValueError("Invalid match ID")
   ```

3. **Implement rate limiting** to avoid API abuse

## Disclosure Policy

- Security issues will be disclosed publicly after a fix is available
- We will credit reporters who responsibly disclose vulnerabilities
- A security advisory will be published for critical vulnerabilities

## Security Updates

Security updates will be released as patch versions (e.g., 26.0.1) and will be clearly marked in the CHANGELOG.

## Contact

For sensitive security matters, contact the maintainers directly through:
- GitHub Security Advisory feature
- Direct message to repository maintainers

Thank you for helping keep python-opendota and its users safe!