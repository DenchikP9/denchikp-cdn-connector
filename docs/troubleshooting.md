# Troubleshooting

| Symptom | Cause and fix |
|---|---|
| The consent page does not accept the key | Use your main DenchikP CDN API key, not a `dpt_…` token. Keys with a list of allowed IP addresses cannot be used: create a separate key without an IP list for the connector. |
| "This confirmation page has expired" | The consent page is valid for 15 minutes. Go back to the assistant and connect again. |
| The assistant asks to connect again | The token was deleted in the panel, the API key was disabled, or the connector was not used for more than a year. Connect it once more. |
| "A file with this name already exists" | The connector never overwrites files. Choose another file name or upload without `keep_filename` to get a unique name. |
| "Rate limit reached" | The token's limit of 120 requests per minute was exceeded. Wait for the time in the message or raise the token's limit in the panel. |
| "Access denied by DenchikP CDN" | The token or key is limited to some domains, or the key was disabled. Check the key and its domains in the panel. |
| A new tool does not appear | Disable and enable the connector in the assistant's settings, or refresh the tool list. |
| Images are not shown | `cdn_view_image` shows jpg, png, webp and gif. SVG is text: read it with `cdn_read_text_file`. |
| Connection fails behind a firewall | Claude connects from `160.79.104.0/21`, ChatGPT from the egress ranges published by OpenAI. The server must be reachable from these addresses. |

Check the server from your computer:

```sh
python scripts/check_server.py
```

If nothing helps, write to support@denchikp.com with the time of the problem and the assistant you use. Never send your API key or tokens.
