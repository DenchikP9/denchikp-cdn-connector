# Directory listings

Texts and steps for submitting the connector to the Claude Connectors Directory and the ChatGPT app directory.

## Common facts

| Field | Value |
|---|---|
| Name | DenchikP CDN |
| Server URL | `https://cdnapi.denchikp.com/mcp` |
| Transport | Streamable HTTP (JSON responses, no SSE stream) |
| Authentication | OAuth 2.1, PKCE S256, dynamic client registration, refresh tokens |
| Documentation | https://cdn.denchikp.com/guide/?lang=en#claude-connector |
| Privacy policy | https://cdn.denchikp.com/privacy/?lang=en |
| Terms of service | https://cdn.denchikp.com/terms/?lang=en |
| Support | support@denchikp.com |
| Website | https://cdn.denchikp.com |
| Data | First-party API: the connector calls only the DenchikP CDN API of the same company. No health data, no sponsored content |
| Tools | 22, see [tools.md](tools.md). Read and write, no destructive tools |

## Claude Connectors Directory

Submit at https://claude.ai/directory/manage → **Submit new** → **MCP connector** (needs a paid Claude plan).

**One-liner** (up to 200 characters):

> Find, read, view and upload files in your DenchikP CDN storage, build image links and create share links. Existing files are never deleted or overwritten.

**Description** (up to 2,000 characters):

> DenchikP CDN is a file storage and content delivery service for websites, apps and screenshots. The connector lets Claude work with your storage: check your plan, quotas and domains; find files by name, folder or extension; read text files such as html, css, js, json and md; look at images and describe or compare them; upload new files from text, base64 or a public link, including a whole web page in one call; build links to resized or converted images (webp, avif) and temporary signed links; create share links with a password, expiry and download limit; and review statistics, expiring files, the trash, duplicates, checksums and antivirus results.
>
> The connector is safe by design: it cannot delete, overwrite, rename or change existing files, and uploads with a name that is already taken are rejected. You sign in once with your DenchikP CDN API key on our consent page; the key is not stored and Claude gets its own token with read, upload and share permissions, which renews automatically and can be revoked at any time in the DenchikP CDN panel.

**Categories:** Productivity, Developer tools, File storage (choose the closest ones offered by the portal).

**Use cases:**

1. Publish a web page or text file and get its public link.
2. Find files and get their links, sizes and dates.
3. Look at images stored in the CDN and describe or compare them.
4. Prepare image links in the right size and format for a website.
5. Share a file with a password, expiry and download limit.

**What users need before connecting:** a DenchikP CDN account and an API key without an IP allow-list (https://cdn.denchikp.com/account/).

**Read/write:** both. Read-only tools have `readOnlyHint: true`; upload and share tools have `readOnlyHint: false` and `destructiveHint: false`.

**Authentication requirement:** required. **Method:** OAuth with dynamic client registration (`oauth_dcr`).

**Test & launch:** every tool was run through the custom connector in Claude and the automated test suite. For a Verified review, create a separate demo API key with sample files and send it to the reviewer by email; never put credentials in the portal.

**Icon:** [chatgpt-plugin/assets/logo.png](../chatgpt-plugin/assets/logo.png) (512×512 PNG).

## ChatGPT app directory

1. Verify the developer identity at https://platform.openai.com/settings/organization/general (individual or business).
2. Record a short demo video that shows connecting the app and running the five positive test cases, upload it somewhere reviewers can open, and build the package:

   ```sh
   python scripts/build_chatgpt_plugin.py --demo-url https://…/demo.mp4
   ```

3. In the OpenAI dashboard create a plugin, upload `dist/denchikp-cdn-chatgpt-1.0.0.zip`, connect the MCP server with OAuth and run **Scan Tools**.
4. Domain verification: the dashboard gives a token that must be served as plain text at `https://cdnapi.denchikp.com/.well-known/openai-apps-challenge`. Save it as the only line of `openai-apps-challenge.txt` in the API folder; it is served immediately, without a restart.
5. In **Review details** give reviewers a demo API key with sample files and no MFA. Do not put credentials in the ZIP.
6. Submit for review.

The test cases (5 positive, 3 negative), listing texts and icons are in [chatgpt-plugin/plugin.json](../chatgpt-plugin/plugin.json).
