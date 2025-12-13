# Security Policy

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.4.x   | :white_check_mark: |
| 0.3.x   | :white_check_mark: |
| < 0.3   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in the Itential Python SDK, please report it responsibly:

1. **Do not** create a public GitHub issue
2. Email security details to the maintainers
3. Include steps to reproduce the vulnerability
4. Provide any relevant technical details

We will respond to security reports within 48 hours and provide regular updates on our progress.

## Security Best Practices

### Authentication and Credentials

- **Never hardcode credentials** in your source code
- Use environment variables or secure credential management systems
- Rotate authentication tokens regularly
- Use OAuth with client credentials flow when available (Platform connections)
- Store credentials with appropriate file permissions (600 or restrictive)

```python
# Good: Use environment variables
import os
from ipsdk import platform_factory

client = platform_factory(
    host=os.getenv("ITENTIAL_HOST"),
    username=os.getenv("ITENTIAL_USERNAME"),
    password=os.getenv("ITENTIAL_PASSWORD")
)

# Bad: Hardcoded credentials
client = platform_factory(
    host="https://production.example.com",
    username="admin",
    password="secret123"
)
```

### TLS and Certificate Verification

- **Always use HTTPS** in production environments
- **Never disable certificate verification** unless absolutely necessary for development
- Use proper CA certificates and validate certificate chains
- Configure appropriate TLS versions (1.2+)

```python
# Good: Secure TLS configuration
client = platform_factory(
    host="https://itential.example.com",
    username=username,
    password=password,
    verify_certs=True,  # Default: always verify certificates
    timeout=30
)

# Bad: Disabled certificate verification
client = platform_factory(
    host="https://itential.example.com",
    username=username,
    password=password,
    verify_certs=False  # Only for development/testing
)
```

### Network Security

- Use network segmentation and firewalls to restrict access
- Implement proper timeout values to prevent hanging connections
- Use connection pooling appropriately
- Monitor and log API access patterns

### Error Handling and Information Disclosure

- Handle exceptions properly without exposing sensitive information
- Sanitize error messages before logging or displaying
- Use structured logging with appropriate log levels
- Avoid logging sensitive data (credentials, tokens, personal information)

```python
import logging
from ipsdk import logger

# Configure logging securely
logger.set_level("INFO")  # Avoid DEBUG in production

try:
    response = client.get("/api/data")
except Exception as e:
    # Good: Log error without sensitive details
    logging.error("API request failed: %s", str(e))

    # Bad: Don't log full request details that might contain secrets
    # logging.error("Request failed: %s", request.json)
```

### Input Validation and Sanitization

- Validate all input parameters
- Sanitize data before sending to APIs
- Use parameterized queries and avoid string concatenation
- Implement rate limiting for API calls

```python
# Good: Validate input parameters
def get_user_data(user_id):
    if not isinstance(user_id, (int, str)) or not user_id:
        raise ValueError("Invalid user_id")

    # Sanitize user_id if needed
    safe_user_id = str(user_id).strip()

    return client.get(f"/users/{safe_user_id}")
```

### Dependency Management

- Regularly update dependencies to patch security vulnerabilities
- Use dependency scanning tools in CI/CD pipeline
- Pin dependency versions in production
- Monitor security advisories for httpx and other dependencies

```bash
# Check for security vulnerabilities
uv run bandit -r src/ipsdk --configfile pyproject.toml
make security

# Keep dependencies updated
uv sync --upgrade
```

### Development Security

- Use pre-commit hooks to catch potential security issues
- Run security scans in CI/CD pipeline
- Implement code review processes
- Use static analysis tools (bandit, ruff security rules)

```bash
# Install pre-commit hooks
uv run pre-commit install

# Run security analysis
make security
make premerge  # Includes security checks
```

### Async Security Considerations

When using async connections:

- Properly manage async context managers and resource cleanup
- Use appropriate timeout values for async operations
- Handle async exceptions properly
- Avoid blocking the event loop with synchronous operations

```python
# Good: Proper async resource management
async def secure_async_call():
    async with gateway_factory(
        host=host,
        username=username,
        password=password,
        want_async=True
    ) as client:
        response = await client.get("/api/data")
        return response
```

### Production Deployment

- Use secrets management systems (Kubernetes secrets, AWS Secrets Manager, etc.)
- Implement proper monitoring and alerting
- Use least-privilege access principles
- Regularly audit access logs and API usage
- Implement circuit breakers and retry mechanisms with backoff

### Code Quality and Security

Our CI/CD pipeline includes security checks:

- **Bandit**: Static security analysis for Python code
- **Ruff**: Includes security-focused linting rules (S rule set)
- **Pre-commit hooks**: Catch security issues before commits
- **Dependency scanning**: Monitor for vulnerable dependencies

## Security Testing

When testing the SDK:

- Use test credentials and isolated test environments
- Never use production credentials in tests
- Implement security-focused unit tests
- Test authentication failure scenarios
- Validate TLS certificate handling

## Compliance and Standards

The Itential Python SDK follows security best practices including:

- Secure defaults (TLS verification enabled, appropriate timeouts)
- Principle of least privilege
- Defense in depth
- Input validation and sanitization
- Secure error handling and logging
