import argparse
import json
import re
import struct
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "chatgpt-plugin"
DIST = ROOT / "dist"
LIMITS = {"displayName": 30, "shortDescription": 30, "longDescription": 4000, "developerName": 80}
URLS = ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL")
FORBIDDEN = ("test_credentials", "reviewer_instructions", "clientSecret", "headers", "hooks", "apps")


def png_size(path: Path):
    head = path.read_bytes()[:24]
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit(f"{path.name}: not a PNG file")
    return struct.unpack(">II", head[16:24])


def walk_keys(obj, found):
    if isinstance(obj, dict):
        for k, v in obj.items():
            found.add(k)
            walk_keys(v, found)
    elif isinstance(obj, list):
        for v in obj:
            walk_keys(v, found)


def validate(plugin: dict, mcp: dict):
    errors = []
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", plugin.get("name", "")) or len(plugin["name"]) > 64:
        errors.append("name: lowercase letters, numbers and single hyphens, up to 64 characters")
    if not re.fullmatch(r"\d+\.\d+\.\d+", plugin.get("version", "")):
        errors.append("version: semver like 1.0.0")
    ui = plugin.get("extensions", {}).get("com.openai", {}).get("interface", {})
    for k, n in LIMITS.items():
        if not ui.get(k):
            errors.append(f"interface.{k} is required")
        elif len(ui[k]) > n:
            errors.append(f"interface.{k}: {len(ui[k])} characters, limit {n}")
    for k in URLS:
        if not str(ui.get(k, "")).startswith("https://"):
            errors.append(f"interface.{k} must be an https URL")
    prompts = ui.get("defaultPrompt", [])
    if len(prompts) > 3 or any(len(p) > 128 for p in prompts):
        errors.append("interface.defaultPrompt: up to 3 prompts, 128 characters each")
    if len(ui.get("capabilities", [])) > 20 or any(len(c) > 120 for c in ui.get("capabilities", [])):
        errors.append("interface.capabilities: up to 20 items, 120 characters each")
    for k in ("brandColor", "brandColorDark"):
        if k in ui and not re.fullmatch(r"#[0-9A-Fa-f]{6}", ui[k]):
            errors.append(f"interface.{k} must look like #RRGGBB")
    for k in ("logo", "composerIcon", "logoDark", "composerIconDark"):
        if k in ui:
            p = SRC / ui[k]
            if not ui[k].startswith("./") or not p.is_file():
                errors.append(f"interface.{k}: file {ui[k]} not found")
            else:
                w, h = png_size(p)
                if w != h or w < 48 or w > 4096 or p.stat().st_size > 5 * 1024 * 1024:
                    errors.append(f"interface.{k}: must be square, 48-4096 px, up to 5 MiB (got {w}x{h})")
    review = plugin.get("extensions", {}).get("com.openai", {}).get("review", {})
    cases = review.get("test_cases", {})
    if len(cases.get("positive", [])) != 5 or len(cases.get("negative", [])) != 3:
        errors.append("review.test_cases: exactly 5 positive and 3 negative cases")
    for c in cases.get("positive", []):
        if not all(c.get(k) for k in ("description", "prompt", "tools_triggered", "expected_behavior")):
            errors.append(f"positive case {c.get('description')!r}: description, prompt, tools_triggered and expected_behavior are required")
    servers = mcp.get("mcpServers", {})
    if len(servers) != 1:
        errors.append("mcp.json: exactly one MCP server")
    for name, s in servers.items():
        if not str(s.get("url", "")).startswith("https://"):
            errors.append(f"mcp.json {name}: url must be https")
        if s.get("type") != "streamable-http":
            errors.append(f"mcp.json {name}: type must be streamable-http")
    keys = set()
    walk_keys(plugin, keys)
    walk_keys(mcp, keys)
    for k in FORBIDDEN:
        if k in keys:
            errors.append(f"{k} must not be in the package")
    return errors


def main():
    ap = argparse.ArgumentParser(description="Validate and pack the DenchikP CDN plugin for the ChatGPT app directory")
    ap.add_argument("--demo-url", help="Public URL of the demo video for reviewers (demo_recording_url)")
    ap.add_argument("--check-only", action="store_true", help="Only validate, do not build the ZIP")
    a = ap.parse_args()
    plugin = json.loads((SRC / "plugin.json").read_text(encoding="utf-8"))
    mcp = json.loads((SRC / "mcp.json").read_text(encoding="utf-8"))
    if a.demo_url:
        if not a.demo_url.startswith("https://"):
            raise SystemExit("--demo-url must be an https URL")
        plugin["extensions"]["com.openai"]["review"]["demo_recording_url"] = a.demo_url
    errors = validate(plugin, mcp)
    if errors:
        print("Problems:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    if a.check_only:
        print("plugin.json and mcp.json are valid")
        return
    if not a.demo_url:
        print("Warning: no --demo-url. ChatGPT review needs a demo video: add it here or in the dashboard before submitting.")
    DIST.mkdir(exist_ok=True)
    out = DIST / f"{plugin['name']}-chatgpt-{plugin['version']}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("plugin.json", json.dumps(plugin, ensure_ascii=False, indent=2) + "\n")
        z.writestr("mcp.json", json.dumps(mcp, ensure_ascii=False, indent=2) + "\n")
        for p in sorted((SRC / "assets").iterdir()):
            if p.is_file():
                z.write(p, f"assets/{p.name}")
    print(f"Built {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
