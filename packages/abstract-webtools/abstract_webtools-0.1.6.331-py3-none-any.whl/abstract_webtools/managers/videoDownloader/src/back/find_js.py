from abstract_webtools import *
from abstract_utilities import *
from abstract_react import *

import re
import json
import urllib.parse
import requests

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120 Safari/537.36"
)

S = requests.Session()
S.headers.update({"User-Agent": USER_AGENT})
def fetch_js(url: str) -> str:
    r = S.get(url, timeout=15)
    r.raise_for_status()
    return r.text

# ============================
# Run decrypt in NodeJS
# ============================
##def run_js_decipher(js_code: str, fn: str, sig: str) -> str:
    # Write JS code to temp file
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".js") as f:
            f.write(js_code.encode())
            temp_js_path = f.name

        # Call Node
        out = subprocess.check_output(
            ["node", "decrypt.js", temp_js_path, fn, sig],
            text=True
        )
        return out.strip()
    except Exception as e:
        print(f"{e}")
def get_all_enclosed(s: str, open_char='{', close_char='}'):
    blocks = []
    depth = 0
    start = None

    for i, ch in enumerate(s):
        if ch == open_char:
            if depth == 0:
                start = i
            depth += 1
        elif ch == close_char and depth > 0:
            depth -= 1
            if depth == 0 and start is not None:
                blocks.append(s[start:i+1])
                start = None

    return blocks
def is_all_shape(string,last=0):
    shape_length = len([key for key in ['reverse','slice','swap','splice'] if key in string])
    if shape_length > last:
        return string,shape_length
    return False,last
    
def get_readable(string,start,end):
   
    str_len = len(string)
    if start>str_len:
        return False
    if end>str_len:
        end = str_len
    return string[start:end]
            
def read_js(js: str) -> str:
    # find fn name, ops, apply
    i=1
    j = 1000

    string = str(js)
    lines =string.split('{')
    for i,line in enumerate(lines):
        strin = '{'+('{'.join(lines[i:]))
        all_enclosed = get_all_enclosed(strin, open_char='{', close_char='}')
        input(strin)
    funames = []
    while True:
        c = i*j
        k = c-j
        readable = get_readable(string,k,c)
        if readable == False:
            break
##        print(readable)
##        input()
        i+=1
    all_enclosed = get_enclosed(string, open_char='{', close_char='}')
    last = 0
    for func in all_enclosed:
        input(func)
        func,last = is_all_shape(str(func),last=last)
        if func:
          input(string.split(func)[0])
          
#    for i,line in enumerate(lines):
def get_enclosed(s: str, open_char='{', close_char='}'):
    """
    Returns the FIRST balanced {...} block INCLUDING the braces.
    Supports nested braces.
    If no balanced block is found, returns None.
    """
    start = s.find(open_char)
    if start == -1:
        return None

    depth = 0
    for i in range(start, len(s)):
        if s[i] == open_char:
            depth += 1
        elif s[i] == close_char:
            depth -= 1
            if depth == 0:
                return s[start:i+1]

    return None

# ============================
# Extract initialPlayerResponse
# ============================
def extract_player_response(html: str) -> dict:
    m = re.search(r"ytInitialPlayerResponse\s*=\s*(\{.+?\});", html, re.S)
    if not m:
        raise RuntimeError("Could not find ytInitialPlayerResponse")
    return json.loads(m.group(1))
# ---------------------------------------------------------
# BASIC HTML FETCH
# ---------------------------------------------------------
def fetch_watch_html(url: str) -> str:
    r = S.get(url, timeout=15)
    r.raise_for_status()
    return r.text
# ---------------------------------------------------------
# FIND PLAYER BASE.JS
# ---------------------------------------------------------
def find_player_js_url(html: str) -> str:
    m = re.search(r'"jsUrl":"(?P<u>[^"]+base\.js)"', html)
    if m:
        url = m.group("u").replace("\\/", "/")
        return urllib.parse.urljoin("https://www.youtube.com", url)

    m = re.search(r'(/s/player/[\w\d\-_/.]+/base\.js)', html)
    if m:
        return urllib.parse.urljoin("https://www.youtube.com", m.group(1))

    raise RuntimeError("player base.js URL not found")
# ---------------------------------------------------------
# EXTRACT DECIPHER FUNCTION NAME
# ---------------------------------------------------------
def find_decipher_function_name(js: str) -> str:
    # Look for functionName=function(a){a=a.split("")
    patterns = [
        r'([A-Za-z0-9_$]{2,})=function\(a\)\{a=a\.split\(""\)',
        r'function\s+([A-Za-z0-9_$]{2,})\(a\)\{a=a\.split\(""\)',
        r'var\s+([A-Za-z0-9_$]{2,})\s*=\s*function\(a\)\{a=a\.split\(""\)'
    ]
    for p in patterns:
        m = re.search(p, js)
        if m:
            return m.group(1)
    raise RuntimeError("Could not find decipher function name")
def decipher_signatures(js: str) -> str:
    # find fn name, ops, apply
    i=1
    j = 1000
    lines =str(js).split(';')
    funames = []
    for i,line in enumerate(lines):
        if 'function' in line:
            funame = {}
            fnLine =  [eatAll(part,[' ','\n','\t','']) for part in line.split('function')]
            bef = fnLine[0]
            aft = fnLine[1]
            name = aft.split('(')[0]
            if bef[-1] == '=':
                name = bef.split(' ')[-1].split('=')[0]
            funame["name"]=name
            funame["vars"] = eatAll(get_enclosed(aft,'(',')'),[' ','\n','\t',''])    
            fn_rest = ['function'.join(bef[1:])]
            rest = ';'.join(fn_rest+lines[i+1:])
            fun = eatAll(get_enclosed(rest),[' ','\n','\t',''])
            funame["fun"] = fun 
            if '.split' in fun or '.slice' in fun or '.join' in fun or '.reverse' in fun or '.swap' in fun:
                funames.append(funame)
    return funames
def get_direct_url(url: str):
    html = fetch_watch_html(url)
    player_response = extract_player_response(html)

    # Find base.js
    player_js_url = find_player_js_url(html)
    js = fetch_js(player_js_url)
    read_js(js)
    fnames = decipher_signatures(js)
    
    formats = (
        player_response
        .get("streamingData", {})
        .get("formats", [])
        + player_response
        .get("streamingData", {})
        .get("adaptiveFormats", [])
    )

    # First: direct URL formats
    for fmt in formats:
        if fmt.get("url"):
            direct = apply_n_param(js, fmt["url"])
            return direct, fmt.get("qualityLabel", "unknown")

    # Second: formats requiring signature decipher
    for fmt in formats:
        cipher = fmt.get("signatureCipher") or fmt.get("cipher")
        if not cipher:
            continue

        data = urllib.parse.parse_qs(cipher)
        s = data.get("s", [""])[0]
        base_url = data.get("url", [""])[0]
        sp = data.get("sp", ["signature"])[0]
        
        # Find decipher function name
        print(f"s == {s}")
        for fname in fnames:
            name = fname.get('name')
            function = fname.get('fun')
            signature = run_js_decipher(js, name, s)
            if signature:
                input(signature)
        # Run real JS decrypt


        # Append decrypted signature
        parsed = urllib.parse.urlparse(base_url)
        q = urllib.parse.parse_qs(parsed.query)
        q[sp] = signature
        new_query = urllib.parse.urlencode(q, doseq=True)
        final = urllib.parse.urlunparse(parsed._replace(query=new_query))

        # Apply n-param throttling
        final = apply_n_param(js, final)

        return final, fmt.get("qualityLabel", "unknown")

    raise RuntimeError("No usable video URL found.")
url = 'https://www.youtube.com/shorts/6vP02wYh4Ds'
result = get_direct_url(url)
input(result)
