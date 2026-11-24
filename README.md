# DenchikP CDN connector for Claude and ChatGPT

[Русская версия](README.ru.md)

A remote [Model Context Protocol](https://modelcontextprotocol.io) server that connects AI assistants to [DenchikP CDN](https://cdn.denchikp.com), a file storage and content delivery service. With it Claude, ChatGPT and other MCP clients can check quotas, find, read and view files, upload new files and create share links.

**Server URL:** `https://cdnapi.denchikp.com/mcp`

This repository contains the public documentation of the connector, the machine-readable tool list, the package for the ChatGPT app directory and scripts that check the live server. The server itself is part of the DenchikP CDN API and is not published here.

## What the connector can do

- Show the plan, quotas, usage and the domains you can upload to
- Find files by name, folder or extension; show links, sizes and dates
- Read text files (html, css, js, json, md) and look at images (jpg, png, webp, gif)
- Upload new files from text, base64 or a public link, or up to 20 text files at once
- Build links to resized or converted images (webp, avif) and temporary signed links
- Create share links with a password, expiry and download limit
- Show statistics, expiring files, the trash, duplicates, checksums and antivirus results

It **cannot** delete, overwrite, rename or change existing files. All 22 tools have `destructiveHint: false`. See [docs/tools.md](docs/tools.md) for every tool and parameter.

## Connect

### Claude (claude.ai, Desktop, mobile)

1. Open **Settings → Connectors** and find **DenchikP CDN** in the directory. If it is not listed, choose **Add custom connector** and enter `https://cdnapi.denchikp.com/mcp`.
2. On the DenchikP CDN consent page enter your API key (or confirm the key of your panel session) and click **Allow**.
3. Enable the connector in a chat and ask, for example, "How much space is left on my CDN?"

### Claude Code

```sh
claude mcp add --transport http denchikp-cdn https://cdnapi.denchikp.com/mcp
```

Then run `/mcp` and sign in in the browser.

### ChatGPT

Install **DenchikP CDN** from the ChatGPT app directory. Until it is listed, add it in developer mode: **Settings → Apps and connectors → Advanced settings → Developer mode**, then **Create**, name `DenchikP CDN`, URL `https://cdnapi.denchikp.com/mcp`, authentication **OAuth**.

### Other MCP clients

Any client that supports remote servers over Streamable HTTP with OAuth 2.1 (PKCE S256 and dynamic client registration) can connect to the same URL. Loopback redirect URIs (`http://localhost:<port>/...`, `http://127.0.0.1:<port>/...`) are accepted on any port.

## Example prompts

- "How much space is left on my CDN and which domains can I upload to?"
- "Publish this page (index.html, style.css and app.js) to my domain and send me the link."
- "What is shown in the images in the img folder of example.com?"
- "Give me a link to logo.png 400 px wide in webp."
- "Create a password-protected download link for report.pdf that expires in 7 days."
- "Find duplicate files on my domain."

## Authentication and permissions

- OAuth 2.1 with PKCE (S256), dynamic client registration (RFC 7591), refresh tokens with rotation, revocation (RFC 7009), `iss` in the authorization response (RFC 9207).
- Your API key is used once on the consent page and is never stored. The assistant receives its own token with the `read`, `upload` and `share` permissions only.
- The access token lives 90 days and is renewed automatically with a refresh token while the connector is in use.
- You can revoke access at any time by deleting the "Claude (MCP)" or "ChatGPT (MCP)" token in the DenchikP CDN panel.

Details: [docs/authentication.md](docs/authentication.md).

## Data and privacy

The connector receives only the arguments of the tools that are called and returns their results. It has no access to your conversations, the assistant's memory or other files. See the [privacy policy](https://cdn.denchikp.com/privacy/?lang=en) (section 2.8) and [terms of service](https://cdn.denchikp.com/terms/?lang=en).

## Check the server

```sh
python scripts/check_server.py
```

The script checks OAuth discovery, client registration and the 401 challenge of the live server. It needs only Python 3.9+ and no credentials. The same check runs weekly in GitHub Actions.

## ChatGPT app directory package

```sh
python scripts/build_chatgpt_plugin.py --check-only
python scripts/build_chatgpt_plugin.py --demo-url https://example.com/demo.mp4
```

The package source is in [chatgpt-plugin](chatgpt-plugin). The ZIP is written to `dist/`. See [docs/directory-listing.md](docs/directory-listing.md) for the submission steps.

## Troubleshooting

See [docs/troubleshooting.md](docs/troubleshooting.md) or the [guide](https://cdn.denchikp.com/guide/?lang=en#claude-connector-trouble).

## Support

- Email: support@denchikp.com
- Issues: [GitHub issues](https://github.com/DenchikP9/denchikp-cdn-connector/issues)
- Security reports: see [SECURITY.md](SECURITY.md)

## License

The documentation, manifests and scripts in this repository are released under the [MIT License](LICENSE).
