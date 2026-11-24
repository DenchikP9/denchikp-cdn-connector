import json
import sys
import urllib.error
import urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://cdnapi.denchikp.com").rstrip("/")
UA = {"User-Agent": "denchikp-cdn-connector-check/1.0"}
failed = 0


def request(method, path, body=None, headers=None):
    data = json.dumps(body).encode() if body is not None else None
    h = {**UA, **(headers or {})}
    if data is not None:
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


def check(ok, label, detail=""):
    global failed
    print(("PASS " if ok else "FAIL ") + label + (f": {detail}" if detail and not ok else ""))
    failed += 0 if ok else 1


s, h, b = request("GET", "/.well-known/oauth-protected-resource/mcp")
meta = json.loads(b) if s == 200 else {}
check(s == 200 and meta.get("resource") == BASE + "/mcp", "protected resource metadata (RFC 9728)", f"HTTP {s}")
check(meta.get("authorization_servers") == [BASE], "authorization server is listed")

s, h, b = request("GET", "/.well-known/oauth-authorization-server")
asm = json.loads(b) if s == 200 else {}
check(s == 200 and asm.get("issuer") == BASE, "authorization server metadata (RFC 8414)", f"HTTP {s}")
check("S256" in asm.get("code_challenge_methods_supported", []), "PKCE S256")
check("refresh_token" in asm.get("grant_types_supported", []), "refresh tokens")
check(bool(asm.get("registration_endpoint")), "dynamic client registration (RFC 7591)")

s, h, b = request("POST", "/mcp/oauth/register", {"client_name": "connector check", "redirect_uris": ["http://localhost:8976/callback"]})
check(s == 201 and json.loads(b).get("client_id"), "client registration works", f"HTTP {s}")
s, h, b = request("POST", "/mcp/oauth/register", {"client_name": "bad", "redirect_uris": ["https://example.com/callback"]})
check(s == 400, "unknown redirect URIs are rejected", f"HTTP {s}")

s, h, b = request("POST", "/mcp", {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25"}})
wa = {k.lower(): v for k, v in h.items()}.get("www-authenticate", "")
check(s == 401 and "resource_metadata=" in wa, "unauthenticated MCP request returns 401 with resource_metadata", f"HTTP {s}")

s, h, b = request("GET", "/mcp")
check(s == 405, "GET /mcp answers 405 (no SSE stream)", f"HTTP {s}")

print(f"\n{'All checks passed' if not failed else f'{failed} check(s) failed'}")
sys.exit(1 if failed else 0)
