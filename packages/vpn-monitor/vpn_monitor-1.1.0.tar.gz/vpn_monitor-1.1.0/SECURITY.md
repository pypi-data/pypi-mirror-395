# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version  | Supported          |
| -------- | ------------------ |
| Latest   | :white_check_mark: |
| < Latest | :x:                |

## Reporting a Vulnerability

Please report (suspected) security vulnerabilities by creating a private security advisory at:

**https://github.com/henrykp/vpn_status_monitor/security/advisories/new**

Alternatively, you can open a regular issue and label it as a security concern, though a security advisory is preferred for sensitive vulnerabilities.

You will receive a response within 48 hours. If the issue is confirmed, we will release a patch as soon as possible depending on complexity but historically within a few days.

## Security Considerations

This application:

- Queries external services (ip-api.com) to determine your public IP and location
- Stores configuration locally (allowed country, allowed_ips.txt file)
- Requires network access to function
- Uses Windows-specific APIs for process monitoring
- Does not transmit or store any personal data beyond your public IP address

### Known Security Limitations

- The application queries ip-api.com over HTTP (not HTTPS) - this is a limitation of the free tier service
- The `allowed_ips.txt` file is stored in plain text without encryption
- No authentication is required to modify configuration files
- The application runs with the same privileges as the user

## Security Best Practices

When using this application:

1. Keep the application updated to the latest version
2. Regularly review the `allowed_ips.txt` file if you use it
3. Be aware that the application queries external services to check your IP
4. Ensure your system has appropriate security measures in place
