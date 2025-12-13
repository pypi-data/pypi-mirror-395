import re
import json
import requests
import tempfile
import subprocess
import urllib.parse

# ============================
# Session + Headers
# ============================
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120 Safari/537.36"
)

S = requests.Session()
S.headers.update({"User-Agent": USER_AGENT})


# ============================
# Extract HTML
# ============================
def get_html(url: str) -> str:
    r = S.get(url)
    r.raise_for_status()
    return r.text


# ============================
# Extract initialPlayerResponse
# ============================
def extract_player_response(html: str) -> dict:
    m = re.search(r"ytInitialPlayerResponse\s*=\s*(\{.+?\});", html, re.S)
    if not m:
        raise RuntimeError("Could not find ytInitialPlayerResponse")
    return json.loads(m.group(1))


# ============================
# Find base.js URL
# ============================
def find_player_js_url(html: str) -> str:
    # Look for "/s/player/.../base.js"
    m = re.search(r'(/s/player/[^"]+/base\.js)', html)
    if not m:
        raise RuntimeError("Could not find player JS URL")
    return urllib.parse.urljoin("https://www.youtube.com", m.group(1))


# ============================
# Find signature decipher function name
# ============================
def find_decipher_function_name(js: str) -> str:
    # yt-dlp stable pattern
    m = re.search(r'\.sig\|\|([a-zA-Z0-9$]{2,})\(', js)
    if m:
        return m.group(1)

    # fallback patterns
    m = re.search(r'([a-zA-Z0-9$]{2,})=function\(a\)\{a=a\.split', js)
    if m:
        return m.group(1)

    m = re.search(r'function\s+([a-zA-Z0-9$]{2,})\(a\)\{a=a\.split', js)
    if m:
        return m.group(1)

    raise RuntimeError("Could not locate decipher function")


# ============================
# Run decrypt in NodeJS
# ============================
def run_js_decipher(js_code: str, fn: str, sig: str) -> str:
    # Write JS code to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".js") as f:
        f.write(js_code.encode())
        temp_js_path = f.name

    # Call Node
    out = subprocess.check_output(
        ["node", "decrypt.js", temp_js_path, fn, sig],
        text=True
    )
    return out.strip()


# ============================
# Build final direct URL
# ============================
def get_direct_url(url: str):
    html = get_html(url)
    player_resp = extract_player_response(html)
    formats = player_resp.get("streamingData", {}).get("formats", []) + \
              player_resp.get("streamingData", {}).get("adaptiveFormats", [])

    # 1st: return any direct url (no signature needed)
    for f in formats:
        if f.get("url"):
            return f["url"], f.get("qualityLabel") or "unknown"

    # 2nd: decrypt signatureCipher
    js_url = find_player_js_url(html)
    js_code = requests.get(js_url).text

    for f in formats:
        cipher = f.get("signatureCipher") or f.get("cipher")
        if not cipher:
            continue

        qs = urllib.parse.parse_qs(cipher)
        sig = qs["s"][0]
        base_url = qs["url"][0]
        sp = qs.get("sp", ["signature"])[0]

        fn = find_decipher_function_name(js_code)

        # RUN ACTUAL JS FUNCTION
        dec_sig = run_js_decipher(js_code, fn, sig)

        # Rebuild final URL
        parsed = urllib.parse.urlparse(base_url)
        q = urllib.parse.parse_qs(parsed.query)
        q[sp] = dec_sig
        new_query = urllib.parse.urlencode(q, doseq=True)

        final_url = urllib.parse.urlunparse(parsed._replace(query=new_query))
        return final_url, f.get("qualityLabel") or "unknown"

    raise RuntimeError("Could not extract any valid stream URL")


# ============================
# Download video
# ============================
def download(url: str, output="video.mp4"):
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "*/*",
        "Accept-Encoding": "identity",
        "Referer": "https://www.youtube.com/",
        "Origin": "https://www.youtube.com",
        "Range": "bytes=0-",
        "Connection": "keep-alive",
    }

    print(f"Downloading:\n{url}\n-> {output}")

    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(output, "wb") as f:
            for chunk in r.iter_content(chunk_size=64 * 1024):
                if chunk:
                    f.write(chunk)

    print("Done:", output)
    return output


# ============================
# MAIN
# ============================
if __name__ == "__main__":
    url = "https://www.youtube.com/shorts/6vP02wYh4Ds"
    direct, quality = get_direct_url(url)
    download(direct, "video.mp4")
    print("Quality:", quality)
