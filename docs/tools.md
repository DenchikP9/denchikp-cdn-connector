# Tools

All 22 tools of the DenchikP CDN connector. None of them can delete, overwrite or modify existing files (`destructiveHint: false` for every tool). The machine-readable list is in [`tools.json`](../tools.json).

| Tool | Title | Access | Read-only | Open world | What it does |
|---|---|---|---|---|---|
| `cdn_account` | Account and quotas | `read` | yes | no | Returns the API key name, plan, storage and traffic quotas, current usage and the domains this connector can upload to. Call it first to learn the available domains. |
| `cdn_list_files` | List files | `read` | yes | no | Lists files uploaded with this API key, newest first, with optional search by name and filters by domain, folder and extension. Returns links, sizes and dates. |
| `cdn_browse_domain` | Browse a domain | `read` | yes | no | Lists files stored on disk for a domain, including files uploaded by other keys of the same domain owner. Returns up to 200 files. |
| `cdn_file_info` | File details | `read` | yes | no | Returns metadata of one file: size, content type, whether it exists on disk, upload date and expiry. |
| `cdn_read_text_file` | Read a text file | `read` | yes | no | Returns the contents of a text file (html, css, js, json, md, txt, svg and similar) up to 2 MB. |
| `cdn_stats` | Usage statistics | `read` | yes | no | Uploads, downloads and views for this API key over a period, optionally for one domain. |
| `cdn_signed_link` | Temporary link | `read` | yes | no | Creates a signed link to a file that stops working after the given time. Useful for private files. Does not change the file. |
| `cdn_upload_text` | Upload a text file | `upload` | no | no | Creates a new file from text (html, css, js, json, md, txt and so on) and returns its public link. Existing files are never overwritten. |
| `cdn_upload_base64` | Upload a file (base64) | `upload` | no | no | Creates a new file from base64 data (images, PDFs, archives and other binary files, up to 8 MB) and returns its public link. Existing files are never overwritten. |
| `cdn_upload_from_url` | Upload from a link | `upload` | no | yes | The server downloads a file from a public http or https link and stores it as a new file in the CDN (up to 500 MB). Returns the new link. |
| `cdn_upload_text_batch` | Upload several text files | `upload` | no | no | Uploads up to 20 text files in one call (for example the html, css and js of a web page), 8 MB in total. File names are kept by default; existing files are never overwritten. Returns a link or an error for every file. |
| `cdn_view_image` | View an image | `read` | yes | no | Returns an image stored in the CDN (jpg, png, webp or gif) so it can be looked at, described or compared. Large images are scaled down. |
| `cdn_image_url` | Resized image link | `read` | yes | no | Builds a public link to a resized, cropped or converted version of an image (webp, avif, jpeg, png) for use on a website. The original file is not changed. |
| `cdn_list_folders` | Domain folders | `read` | yes | no | Lists the folders of a domain with the number of files and total size in each. |
| `cdn_file_hash` | File checksum | `read` | yes | no | Calculates a checksum of a file: sha256 (default), sha1 or md5. |
| `cdn_find_duplicates` | Find duplicates | `read` | yes | no | Finds files with identical content among the files of this API key. Report only: nothing is deleted. |
| `cdn_expiring_files` | Expiring files | `read` | yes | no | Lists files that are scheduled to be deleted automatically, with the time of deletion. |
| `cdn_trash` | Trash | `read` | yes | no | Lists files in the trash and when the trash will be emptied. View only: restoring is done in the DenchikP CDN panel. |
| `cdn_list_shares` | Share links | `read` | yes | no | Lists public share links created with this API key: expiry, password protection and download counts. |
| `cdn_create_share` | Create a share link | `share` | no | no | Creates a public download page for a file (https://cdn.denchikp.com/s/<code>) with an optional password, expiry and download limit. The file itself is not changed. |
| `cdn_check_url` | Check a link | `read` | yes | yes | Checks whether an http or https link opens and, for DenchikP CDN links, splits it into domain, folder and file name. |
| `cdn_scan_file` | Antivirus scan | `read` | yes | no | Scans a file with the ClamAV antivirus and reports the result. The file is not changed or deleted. |

## Parameters

### `cdn_account`

No parameters.

### `cdn_list_files`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | no | Part of the file name |
| `domain` | string | no | Domain the file belongs to, for example example.com, or public. See cdn_account for the list. |
| `folder` | string | no | Folder: img, css, js, fonts, video, audio, docs or files |
| `extension` | string | no | Extension without the dot, for example png |
| `limit` | integer | no | How many items to return, 1-200, default 50 |
| `offset` | integer | no | How many items to skip, for paging |

### `cdn_browse_domain`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domain` | string | yes | Domain the file belongs to, for example example.com, or public. See cdn_account for the list. |
| `folder` | string | no | Folder: img, css, js, fonts, video, audio, docs or files |
| `name_filter` | string | no | Part of the file name |

### `cdn_file_info`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `url` | string | yes | Full file link: https://cdn.denchikp.com/<domain>/<folder>/<file> |

### `cdn_read_text_file`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `url` | string | yes | Full file link: https://cdn.denchikp.com/<domain>/<folder>/<file> |

### `cdn_stats`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `period` | string (day, week, month, year) | no | Period, default month |
| `domain` | string | no | Domain the file belongs to, for example example.com, or public. See cdn_account for the list. |

### `cdn_signed_link`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `url` | string | yes | Full file link: https://cdn.denchikp.com/<domain>/<folder>/<file> |
| `ttl_seconds` | integer | no | Lifetime in seconds, 10 seconds to 30 days, default 3600 |
| `download` | boolean | no | Make the browser download the file instead of opening it |

### `cdn_upload_text`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `filename` | string | yes | File name with extension, for example index.html |
| `content` | string | yes | File contents, UTF-8 text, up to 8 MB |
| `domain` | string | no | Domain the file belongs to, for example example.com, or public. See cdn_account for the list. |
| `keep_filename` | boolean | no | Keep the file name exactly as given. By default the file gets a random unique name. If the name is taken, the upload is rejected. |
| `expires_in_seconds` | integer | no | Optional: delete the file automatically after this many seconds |

### `cdn_upload_base64`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `filename` | string | yes | File name with extension, for example logo.png |
| `content_base64` | string | yes | File contents encoded as base64 |
| `domain` | string | no | Domain the file belongs to, for example example.com, or public. See cdn_account for the list. |
| `keep_filename` | boolean | no | Keep the file name exactly as given. By default the file gets a random unique name. If the name is taken, the upload is rejected. |
| `expires_in_seconds` | integer | no | Optional: delete the file automatically after this many seconds |

### `cdn_upload_from_url`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `source_url` | string | yes | Public http or https link to the file |
| `domain` | string | no | Domain the file belongs to, for example example.com, or public. See cdn_account for the list. |
| `folder` | string | no | Folder: img, css, js, fonts, video, audio, docs or files |

### `cdn_upload_text_batch`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `files` | array | yes | Files to upload |
| `domain` | string | no | Domain the file belongs to, for example example.com, or public. See cdn_account for the list. |
| `keep_filename` | boolean | no | Keep file names as given (default true) |
| `expires_in_seconds` | integer | no | Optional: delete the files automatically after this many seconds |

### `cdn_view_image`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `url` | string | yes | Full file link: https://cdn.denchikp.com/<domain>/<folder>/<file> |
| `max_width` | integer | no | Longest side in pixels, 64-1568, default 1024 |

### `cdn_image_url`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `url` | string | yes | Full file link: https://cdn.denchikp.com/<domain>/<folder>/<file> |
| `width` | integer | no | Width in pixels |
| `height` | integer | no | Height in pixels |
| `fit` | string (scale-down, contain, cover) | no | How to fit into width and height |
| `format` | string (auto, webp, avif, jpeg, png) | no | Output format |
| `quality` | integer | no | Quality 1-100, default 80 |

### `cdn_list_folders`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domain` | string | yes | Domain the file belongs to, for example example.com, or public. See cdn_account for the list. |

### `cdn_file_hash`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `url` | string | yes | Full file link: https://cdn.denchikp.com/<domain>/<folder>/<file> |
| `algorithm` | string (sha256, sha1, md5) | no | Hash algorithm, default sha256 |

### `cdn_find_duplicates`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domain` | string | no | Domain the file belongs to, for example example.com, or public. See cdn_account for the list. |
| `min_size` | integer | no | Ignore files smaller than this many bytes |

### `cdn_expiring_files`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domain` | string | no | Domain the file belongs to, for example example.com, or public. See cdn_account for the list. |
| `limit` | integer | no | How many items to return, 1-500, default 100 |

### `cdn_trash`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domain` | string | no | Domain the file belongs to, for example example.com, or public. See cdn_account for the list. |
| `limit` | integer | no | How many items to return, 1-500, default 100 |
| `offset` | integer | no | How many items to skip, for paging |

### `cdn_list_shares`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domain` | string | no | Domain the file belongs to, for example example.com, or public. See cdn_account for the list. |
| `limit` | integer | no | How many items to return, 1-500, default 100 |

### `cdn_create_share`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `url` | string | yes | Full file link: https://cdn.denchikp.com/<domain>/<folder>/<file> |
| `name` | string | no | Optional label for the link |
| `password` | string | no | Optional password, 4-128 characters |
| `expires_in_seconds` | integer | no | Optional lifetime of the link in seconds |
| `max_downloads` | integer | no | Optional maximum number of downloads |

### `cdn_check_url`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `url` | string | yes | Any http or https link |

### `cdn_scan_file`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `url` | string | yes | Full file link: https://cdn.denchikp.com/<domain>/<folder>/<file> |
