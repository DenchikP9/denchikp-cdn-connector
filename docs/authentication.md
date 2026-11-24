# Authentication

The connector is an OAuth 2.1 protected MCP resource. Clients discover everything from the server; nothing has to be configured by hand.

## Discovery

| Endpoint | Purpose |
|---|---|
| `GET /.well-known/oauth-protected-resource/mcp` | Protected resource metadata (RFC 9728) |
| `GET /.well-known/oauth-authorization-server` | Authorization server metadata (RFC 8414) |
| `POST /mcp/oauth/register` | Dynamic client registration (RFC 7591), public clients only |
| `GET /mcp/oauth/authorize` | Consent page |
| `POST /mcp/oauth/token` | `authorization_code` and `refresh_token` grants |
| `POST /mcp/oauth/revoke` | Token revocation (RFC 7009) |

An unauthenticated `POST /mcp` returns `401` with
`WWW-Authenticate: Bearer resource_metadata="https://cdnapi.denchikp.com/.well-known/oauth-protected-resource/mcp", scope="read upload share offline_access"`.
An expired or revoked token gets the same answer with `error="invalid_token"`, which makes the client refresh the token or start the flow again.

## Flow

1. The client registers itself with its redirect URIs. Allowed: `https://claude.ai/api/mcp/auth_callback`, `https://claude.com/api/mcp/auth_callback`, ChatGPT connector callbacks on `https://chatgpt.com/`, and loopback addresses on any port.
2. The user opens the consent page, enters a DenchikP CDN API key (or confirms the key of an open panel session) and clicks **Allow**. Keys restricted to a list of IP addresses are refused, because the assistant connects from its vendor's addresses.
3. The client exchanges the authorization code (valid 5 minutes, single use) with its PKCE `code_verifier`.
4. The response contains `access_token` (`dpt_…`, 90 days), `refresh_token` (`dpr_…`, one year) and `scope` `read upload share`.
5. Before the access token expires, or after a 401, the client calls the token endpoint with `grant_type=refresh_token`. The access token and the refresh token are both replaced; the old access token stops working. Repeating the same refresh request within 2 minutes returns the same new pair, so parallel refreshes do not break the connection.

## Permissions

| Scope | Allows |
|---|---|
| `read` | All read-only tools |
| `upload` | Creating new files. Existing files are never overwritten |
| `share` | Creating public share links |

There is no scope for deleting or changing files, and no tool that does it.

## Revoking access

- In the DenchikP CDN panel, tokens section: delete the "Claude (MCP)" or "ChatGPT (MCP)" token. The next refresh answers `invalid_grant` and the assistant asks to connect again.
- In the assistant: disconnect the connector. Clients that support RFC 7009 also revoke the token on the server.
- Each assistant keeps up to 5 connections per API key (for example claude.ai and Claude Code). A sixth connection replaces the oldest one.

## Limits

- 120 requests per minute per token; above that the tools answer with a clear "Rate limit reached" error and the wait time.
- Uploads through the connector: up to 8 MB per call (base64 or text), up to 500 MB with `cdn_upload_from_url`.
- A tool call is stopped after 200 seconds with an explanatory error.
- Results longer than 100,000 characters are shortened: lists are cut and the response is marked `truncated`.
