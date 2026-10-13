# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | yes       |
| 0.5.x   | security only |
| < 0.5   | no        |

## Reporting a vulnerability

Email `security@ai-headshot-studio.dev` with a description, reproduction
steps, and the affected version. We aim to respond within 72 hours.

Do **not** open public issues for security reports.

## Scope

In scope:
- Arbitrary code execution through a malicious style pack or LoRA file.
- Path traversal in the output writer or project loader.
- Unsafe deserialization of `.ahsproj` project files.
- Credential leakage from `config/secrets.local.yaml`.

Out of scope:
- Model output quality or "deepfake" concerns — this is a rendering tool.
- Issues that require an already-compromised local account.

## Handling of user photos

Reference photos are processed locally. The optional cloud renderer
(`services/cloud_render.py`) uploads only when explicitly enabled and
only to the endpoint configured in `config/settings.yaml`.