# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in miniflux-tui-py, please **do not** create a public GitHub issue. Instead, please report it privately by emailing:

**[peter@reuteras.net](mailto:peter@reuteras.net)**

Please include:
1. A description of the vulnerability
2. Steps to reproduce the issue
3. Potential impact
4. Any suggested fixes (if you have them)

We will acknowledge your email within 48 hours and provide updates on our progress in fixing the vulnerability.

## Security Guidelines

### API Keys and Configuration

- **Never** commit your API key to the repository
- **Never** share your Miniflux API key publicly
- Keep your configuration file (`config.toml`) private and secure
- Use strong API keys generated from your Miniflux server

### Certificate Validation

By default, miniflux-tui-py validates SSL certificates:

```toml
allow_invalid_certs = false  # Keep this as the default
```

Only set `allow_invalid_certs = true` for local development with self-signed certificates. **Never** use this in production.

### Updates

Keep miniflux-tui-py updated to receive security patches:

```bash
pip install --upgrade miniflux-tui-py
```

## Dependency Security

We use:
- [Dependabot](https://dependabot.com/) to monitor for vulnerable dependencies
- Pre-commit hooks to catch common security issues
- Regular security audits

## Known Security Considerations

### Local Storage of Credentials

The application stores your Miniflux API key in the configuration file. Ensure your system:
- Has restricted file permissions on the config directory
- Is protected with a password/lockscreen
- Keeps the file on an encrypted filesystem when possible

### Miniflux Server

The security of your miniflux-tui-py installation depends on:
- Your Miniflux server's security
- The security of your network connection to the server
- The strength of your API key

## Responsible Disclosure

We follow responsible disclosure practices and ask that you:
1. Give us reasonable time to fix the vulnerability before public disclosure
2. Do not publicly disclose the vulnerability until a fix is available
3. Do not access data beyond what's necessary to confirm the vulnerability
4. Do not disrupt service availability

## Security Contact

- **Email**: [peter@reuteras.net](mailto:peter@reuteras.net)
- **Response Time**: We aim to acknowledge reports within 48 hours

Thank you for helping keep miniflux-tui-py and its users secure!
