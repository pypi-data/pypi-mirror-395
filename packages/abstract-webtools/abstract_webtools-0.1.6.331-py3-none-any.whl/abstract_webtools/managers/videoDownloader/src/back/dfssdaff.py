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

def run_js(js_code,fn,  s):
    import tempfile, subprocess

    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".js") as f:
        f.write(js_code)
        temp_path = f.name

    out = subprocess.check_output(
        ["node", "decrypt.js", temp_path, fn, s],
        stderr=subprocess.STDOUT
    )

    return out.decode().strip()
# ---------------------------------------------------------
# BASIC HTML FETCH
# ---------------------------------------------------------
def fetch_watch_html(url: str) -> str:
    r = S.get(url, timeout=15)
    r.raise_for_status()
    return r.text


def extract_player_response(html: str) -> dict:
    m = re.search(r"ytInitialPlayerResponse\s*=\s*(\{.+?\});", html, re.S)
    if not m:
        m = re.search(r"var\s+ytInitialPlayerResponse\s*=\s*(\{.+?\});", html, re.S)
    if not m:
        raise RuntimeError("Could not find ytInitialPlayerResponse")
    return json.loads(m.group(1))


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
##
def fetch_js(url: str) -> str:
    r = S.get(url, timeout=15)
    r.raise_for_status()
    return r.text

def decipher_signature(js: str, s: str) -> str:
    # find fn name, ops, apply
    i=1
    j = 1000
    lines =str(js).split(';')
    funames = []
    for i,line in enumerate(lines):
        if 'function' in line:
            funame = {}
            fnLine =  [eatAll(part,[' ','\n','\t','','=']) for part in line.split('function')]
            bef = fnLine[0]
            aft = fnLine[1]
            
            name = aft.split('(')[0]
            if len(name) == 0:
                name = bef.split(' ')[-1]
 
        
            funame["name"]=name
            funame["vars"] = eatAll(get_enclosed(aft,'(',')'),[' ','\n','\t',''])    
            fn_rest = ['function'.join(bef[1:])]
            rest = ';'.join(fn_rest+lines[i+1:])
            fun = eatAll(get_enclosed(rest),[' ','\n','\t',''])
            funame["fun"] = fun 
            if '.split' in fun or '.slice' in fun or '.join' in fun or '.reverse' in fun or '.swap' in fun:
                funames.append(funame)

    return funames
# ---------------------------------------------------------
# RUN THE REAL JS IN PYTHON (CORRECT DECIPHER!!)
# ---------------------------------------------------------
def run_js_decipher(js_code: str, fn_name: str, s: str) -> str:
    ctx = js2py.EvalJs()
    ctx.execute(js_code)
    return ctx.eval(f"{fn_name}('{s}')")

def fnames_in_kinds(all_declared,file):
    contents_js = all_declared["scripts"][file]
    kinds = contents_js.get('kinds')
    fnames = all_declared.get('fnames')
    for fname,fname_values in fnames.items():
        variables = list(kinds.keys())
        if fname_values.get('file') == None and fname in variables:
            all_declared["fnames"][fname]['file'] = file
            all_declared["fnames"][fname]['aliases'] = make_all_aliases(kinds,fname_values.get('aliases'))
            contents_js["fnames"].append(fname)
    all_declared["scripts"][file] = contents_js   
    return all_declared
def get_all_func_names(data=None,json_path=None,all_declared=None):
    all_declared= all_declared or {"fnames":{},"scripts":{},"kinds":{},"types":{}}
    data = data or safe_read_from_json(json_path)
    dirname = os.path.dirname(json_path)
    dirs,sub_files = get_files_and_dirs(directory,allowed_exts='.ts')
    declared_fnames = all_declared.get('fnames')
    fnames = list(data.keys())
    for fname in fnames:
        if fname not in all_declared['fnames']:
            vals = make_list(data.get(fname) or fname)
            all_declared['fnames'][fname]={"file":None,"aliases":vals}
    for file in sub_files:
        contents = read_from_file(file)
        kinds = decl_kinds(contents)
        types = roll_types(kinds)
        all_declared["kinds"].update(kinds)
        all_declared["scripts"][file] = {"kinds":kinds,"types":{},"fnames":[]}
        for key,values in types.items():
            if key not in all_declared["types"]:
                all_declared["types"][key] = []
            all_declared["types"][key] = update_list_value(all_declared["types"][key],values)    
        all_declared = fnames_in_kinds(all_declared,file)
    return all_declared
# ---------------------------------------------------------
# OPTIONAL: FIX "n" PARAM THROTTLING (REQUIRED FOR HD)
# ---------------------------------------------------------
def apply_n_param(js: str, url: str) -> str:
    """Extract the 'n' transform function and apply it."""
    m = re.search(r'\.get\("n"\)\)&&\(a=([A-Za-z0-9_$]{2,})\(', js)
    if not m:
        return url  # No throttling function found

    n_func_name = m.group(1)

    ctx = js2py.EvalJs()
    ctx.execute(js)

    parsed = urllib.parse.urlparse(url)
    q = urllib.parse.parse_qs(parsed.query)

    if "n" not in q:
        return url

    n_val = q["n"][0]
    new_n = ctx.eval(f"{n_func_name}('{n_val}')")

    q["n"] = new_n
    new_query = urllib.parse.urlencode(q, doseq=True)

    return urllib.parse.urlunparse(parsed._replace(query=new_query))
import re

def find_decipher_function(js: str):
    """
    STEP 1:
    Find the EXACT function that performs a = a.split("").
    Return its name and its full function body as a string.
    """
    functions = []
    # 1) patterns for: fnName = function(a){ ... a=a.split("") ... }
    patterns = [
        r'([A-Za-z0-9_$]{2,})\s*=\s*function\s*\(\w\)\s*\{([^}]+split\(""\)[^}]*)\}',
        r'function\s+([A-Za-z0-9_$]{2,})\s*\(\w\)\s*\{([^}]+split\(""\)[^}]*)\}',
        r'var\s+([A-Za-z0-9_$]{2,})\s*=\s*function\s*\(\w\)\s*\{([^}]+split\(""\)[^}]*)\}',
    ]
    
    for pat in patterns:
        m = re.search(pat, js, re.S)
        if m:
            fn_name = m.group(1)
            body = m.group(2)
            functions.append([fn_name, body])
    return functions
    return None, None
from abstract_react import *
VALUES_FILE_PATH = os.path.join(get_caller_dir(),'js_file.txt')
# ---------------------------------------------------------
# BUILD DIRECT URL
# ---------------------------------------------------------
def get_direct_url(url: str):
    if not os.path.isfile(VALUES_FILE_PATH):
        html = fetch_watch_html(url)
        player_response = extract_player_response(html)

        # Find base.js
        player_js_url = find_player_js_url(html)
        js = fetch_js(player_js_url)
        values = {"url":url,"player_url":player_js_url,"js":js,"html":html,"player_response":player_response}
        safe_dump_to_file(data=values,file_path=VALUES_FILE_PATH)
    data = safe_load_from_json(VALUES_FILE_PATH)
    values =data.get("values")
    js =data.get("js")
    player_js_url =data.get("player_js_url")
    player_response =data.get("player_response")
    html = data.get("html")

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
        body = decipher_signature(str(js),s)
        for key in body:
            
                
                    signature = run_js(js, key.get('name'), s)
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


# ---------------------------------------------------------
# DOWNLOAD
def download(url: str, output: str = "video.mp4") -> str:
    ua_mgr = UserAgentManager(randomAll=True)
    headers = {
        "User-Agent": ua_mgr.generate_for_url("https://www.youtube.com")["User-Agent"],
        "Accept": "*/*",
        "Accept-Encoding": "identity",
        "Connection": "keep-alive",
        "Range": "bytes=0-",
        "Referer": "https://www.youtube.com/",
        "Origin": "https://www.youtube.com",
    }

    print(f"Downloading:\n{url}\n→ {output}")

    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(output, "wb") as f:
            for chunk in r.iter_content(64 * 1024):
                if chunk:
                    f.write(chunk)

    print("Download complete.")
    return output

url = 'https://www.youtube.com/shorts/6vP02wYh4Ds'
get_direct_url(url)
