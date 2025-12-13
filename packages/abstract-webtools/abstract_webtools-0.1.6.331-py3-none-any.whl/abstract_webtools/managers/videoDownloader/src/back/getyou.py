from abstract_webtools import *

import re
import json
import requests
import urllib.parse
from typing import Tuple, List, Dict, Any
from nops import *
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
S = requests.Session()
S.headers.update({"User-Agent": USER_AGENT})
from abstract_utilities import *
from abstract_react import *
def split_caps(string):
    alphs_lower = 'abcdefghijklmnopqrstuvwxyz'
    alphs_upper = alphs_lower.upper()
    spl_chars = ''
    for char in string:
        if char in alphs_upper:
            char=f"_{char.lower()}"
        spl_chars+=char
    return spl_chars
def make_all_aliases(kinds,aliases):
    return_aliases = []
    
    for alias in aliases:
        return_aliases.append(alias)
        if '_' not in alias:
            alias = split_caps(alias)
        alias_spl = [al.lower() for al in alias.split('_') if al]
        alias_lower = ''.join(alias_spl)
        return_aliases.append(alias_lower)
        for i,alias_ap in enumerate(alias_spl):
            if i != 0:  
                alias_ap = capitalize(alias_ap)
            alias_spl[i] = alias_ap
        alias_upper = ''.join(alias_spl)
        return_aliases.append(alias_upper)
    return list(set([alias for alias in return_aliases if alias not in kinds]))
def are_equal(*nums):
    prev_num = None
    for num in nums:
        if prev_num == None:
            prev_num = num
        elif prev_num != num:
            return False
    return True
def get_full_args(string,fname):
    string_parts = {"fname":fname,"args":None,"returns":None}
    chars_js = {"(":1,")":0}
    string_spl = string.split('(')
    string_parts["fname"] = string_spl[0].split(' ')[-1]
    string_part = '('.join(string_spl[1:])
    for i,char in enumerate(string_part):
        if char in chars_js:
            chars_js[char]+=1
        values = chars_js.values()
        if are_equal(*values):
           
           string_parts["args"] = eatAll(string_part[:i],[')',' ','\n','\t','('])
           returns = string_part[i:].split('{')[0]
           
           string_parts["returns"] = eatAll(returns,['(',')',':',' ','\t','\n']) if [ret for ret in returns.split(' ') if ret] else None
           return string_parts
def create_alias_funcs(string,fname,aliases):
    full_args = get_full_args(string,fname)
    for i,alias in enumerate(aliases):
        args = full_args.get('args')
        input_args = ','.join([arg.split(':')[0] for arg in args.split(',') if ':' in arg])
        returns = full_args.get('returns')
        
        returns = f":{returns}" if returns else ""
        aliases[i] = f"\nexport function {alias}(\n\t{args}\n\t){returns} {{\n\t\treturn {fname}({input_args});\n\t}}\n"
    return aliases
def roll_types(kinds):
    types={}
    for key,value in kinds.items():
        if value not in types:
            types[value] = []
        if key not in types[value]:
            types[value].append(key)
    return types
def update_list_value(*lists):
    nu_list = []
    for li in lists:
        nu_list+=li
    return list(set(li))


def run_decipher(js_code: str, s: str) -> str:
    # 1) Find signature function name
    m = re.search(r'([A-Za-z0-9_$]{2,})=function\(a\)\{', js_code)
    if not m:
        m = re.search(r'function\s+([A-Za-z0-9_$]{2,})\(a\)\{', js_code)
    if not m:
        raise RuntimeError("Could not find decipher function")

    fn_name = m.group(1)

    # 2) Extract complete function (including helpers)
    #    We take the WHOLE base.js because helpers may be elsewhere
    context = js2py.EvalJs()
    context.execute(js_code)

    # 3) Call the decipher function
    result = context.eval(f"{fn_name}('{s}')")
    return result
    
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

####directory = "/var/www/modules/packages/abstract-utilities/src"
####dirs,json_paths = get_files_and_dirs(directory,allowed_patterns='alias_map')
####all_declared={}
####for json_path in json_paths:
####    all_declared = get_all_func_names(json_path,all_declared=all_declared)
####    all_declared_scripts = all_declared.get("scripts")
####    all_declared_fnames = all_declared.get('fnames')
####    
####    for sub_file,values in all_declared_scripts.items():
####        
####        
####        for fname in all_declared_fnames:
####            contents = read_from_file(sub_file)
####      
####            fname_values = all_declared_fnames.get(fname)
####            aliases = fname_values.get('aliases')
####            
####            all_aliases = []
####            lines = contents.split('\n')
####            aliases = list(set([alias for alias in fname_values.get('aliases') if alias not in decl_kinds(contents)]))
####            for i,line in enumerate(lines):
####                if line.startswith(f'export function {fname}'):
####                    string = '\n'.join(lines[i:])
####                
####                    
####                    alias_funcs = create_alias_funcs(string,fname,aliases)
####                    all_aliases+=alias_funcs
####            if all_aliases:
####                all_aliases = [contents]+all_aliases
####                contents = '\n'.join(all_aliases)
####                
####                write_to_file(contents=contents,file_path=sub_file)
####                


def get_html(url):
    request = requestManager(url)
    return request.source_code
def get_all_js(url=None,html=None):
    if not html:
        html = get_html(url)
    all_js = []
    for line in html.split('.js'):
        all_js.append(f"""{line.split('"')[-1]}.js""")
    return all_js

def fetch_watch_html(video_id: str) -> str:
    url = f"https://www.youtube.com/watch?v={video_id}"
    r = S.get(url, timeout=15)
    r.raise_for_status()
    return r.text


def extract_yt_initial_player_response(html: str) -> dict:
    # common pattern
    m = re.search(r"ytInitialPlayerResponse\s*=\s*(\{.+?\});", html, re.S)
    if not m:
        # fallback: "var ytInitialPlayerResponse = {...};"
        m = re.search(r"var\s+ytInitialPlayerResponse\s*=\s*(\{.+?\});", html, re.S)
    if not m:
        raise RuntimeError("Could not find ytInitialPlayerResponse in page")
    return json.loads(m.group(1))


def find_player_js_url(html: str) -> str:
    # find the base.js/player url - many variants exist; try some common ones
    # look for "jsUrl": "/s/player/....base.js" in the page JSON or script tags
    m = re.search(r'"jsUrl":"(?P<u>[^"]+base\.js)"', html)
    if m:
        u = m.group("u").replace("\\/", "/")
        return urllib.parse.urljoin("https://www.youtube.com", u)
    # fallback: search script tags for /s/player/.../base.js
    m = re.search(r'(/s/player/[\w\d\-_/.]+/base\.js)', html)
    if m:
        return urllib.parse.urljoin("https://www.youtube.com", m.group(1))
    raise RuntimeError("Could not find player base.js URL")


def parse_streaming_data(player_response: dict) -> List[Dict[str, Any]]:
    sd = player_response.get("streamingData", {}) or {}
    formats = sd.get("formats", []) + sd.get("adaptiveFormats", [])
    return formats


# ---------- signature deciphering helpers ----------
def fetch_js(url: str) -> str:
    r = S.get(url, timeout=15)
    r.raise_for_status()
    return r.text


def find_decipher_function_name(js: str) -> str:
    input(get_all_func_names(js))
    # search for something like: a.set("signature", somefunc(s)) OR "sig||somefunc(s)"
    # common patterns: "functionName=function(a){a=a.split(\"\");...}"
    m = re.search(r"\b([a-zA-Z0-9$]{2,})\s*=\s*function\(\w\)\s*\{\w=\w\.split\(\"\"\)", js)
    if m:
        return m.group(1)
    # other pattern: function abc(a){a=a.split("");
    m = re.search(r"function\s+([a-zA-Z0-9$]{2,})\s*\(\w\)\s*\{\w=\w\.split\(\"\"\)", js)
    if m:
        return m.group(1)
    # newer pattern: e.g. var T7=function(a){a=a.split("");
    m = re.search(r"var\s+([A-Za-z0-9$]{2,})\s*=\s*function\(\w\)\s*\{\w=\w\.split\(\"\"\)", js)
    if m:
        return m.group(1)
##    raise RuntimeError("Decipher function name not found")


def extract_operations(js: str, fn_name: str) -> List[Tuple[str, int]]:
    """
    Find object that contains helper methods and then the function body calling them.
    We'll try to map common ops to ('swap', n), ('reverse', None), ('slice', n) etc.
    """
    input(f"extract_operations == {fn_name}")
    if fn_name:
        # find the function body for fn_name
        pattern = re.compile(rf"{re.escape(fn_name)}\s*=\s*function\(\w\)\s*\{{(.*?)\}}", re.S)
        
        m = pattern.search(js)
        body = None
        if m:
            body = m.group(1)
        else:
            # try function fn_name(a){...}
            pattern2 = re.compile(rf"function\s+{re.escape(fn_name)}\(\w\)\s*\{{(.*?)\}}", re.S)
            mm = pattern2.search(js)
            if mm:
                body = mm.group(1)
    ##    if not body:
    ##        raise RuntimeError("Could not extract function body for decipher fn")

        # find helper object name in body, e.g. var bR={swap:function(a,b){...},reverse:...}; then calls like bR.qd(a,3)
        obj_match = re.search(r"([A-Za-z0-9$]{2,})\.(?:[A-Za-z0-9$]{2,})\(\w,(\d+)\)", body)
        helper_obj = None
        if obj_match:
            helper_obj = obj_match.group(1)

        ops: List[Tuple[str, int]] = []

        # If helper object exists, find its definition and method mapping
        helper_body = ""
        if helper_obj:
            # match object definition: var X={ad:function(a,b){a.splice(0,b);},rd:function(a){a.reverse();},...};
            obj_pattern = re.compile(rf"var\s+{re.escape(helper_obj)}\s*=\s*\{{(.*?)\}};", re.S)
            om = obj_pattern.search(js)
            if om:
                helper_body = om.group(1)
            else:
                # sometimes assigned as X={...}; or X={...}; function calls still use it.
                om2 = re.search(rf"{re.escape(helper_obj)}\s*=\s*\{{(.*?)\}};", js, re.S)
                if om2:
                    helper_body = om2.group(1)

        # Build short mapping of helper method names to operation type by heuristics
        method_map = {}
        if helper_body:
            # find each method: abc:function(a,b){a.splice(0,b)}
            for m in re.finditer(r"([A-Za-z0-9$]{2,})\s*:\s*function\([^\)]*\)\s*\{([^\}]+)\}", helper_body):
                name, code = m.group(1), m.group(2)
                code = code.strip()
                if "reverse" in code:
                    method_map[name] = ("reverse", None)
                elif ".splice" in code or ".slice" in code:
                    # splice likely for removing first n; slice for slicing
                    # capture numeric argument from the call site if possible later
                    method_map[name] = ("splice", None)
                elif re.search(r"[a-z]\[0\]\s*=\s*[a-z]\[b%[a-z]\.length\]", code) or "var c=" in code and "a[0]" in code:
                    method_map[name] = ("swap", None)
                elif "var c=a[0];a[0]=a[b%a.length];a[b%a.length]=c" in code or "var c" in code and "a[b%a.length]" in code:
                    method_map[name] = ("swap", None)
                else:
                    # fallback
                    method_map[name] = ("unknown", None)

        # now scan the body for calls like X.ab(a,3) or a=a.slice(3)
        calls = re.finditer(rf"(?:{re.escape(helper_obj)}\.)?([A-Za-z0-9$]{{2,}})\(\w,?(\d+)?\)", body) if helper_obj else re.finditer(r"([A-Za-z0-9$]{2,})\(\w,?(\d+)?\)", body)
        for c in calls:
            meth = c.group(1)
            num = c.group(2)
            op = method_map.get(meth)
            if op:
                opname, _ = op
                if opname == "splice":
                    ops.append(("slice", int(num) if num else 0))
                elif opname == "reverse":
                    ops.append(("reverse", None))
                elif opname == "swap":
                    ops.append(("swap", int(num) if num else 0))
                else:
                    # unknown mapped - treat as noop or try numeric arg
                    if num:
                        ops.append(("slice", int(num)))
                    else:
                        ops.append(("unknown", None))
            else:
                # direct calls (a=a.split("");a.reverse();a=a.slice(3))
                # check common text around meth name in body
                segment = body
                if re.search(rf"\.{re.escape(meth)}\(", segment):
                    # try detect by literal words
                    if "reverse" in segment:
                        ops.append(("reverse", None))
                    elif "slice" in segment or "splice" in segment:
                        # find number
                        n = c.group(2)
                        ops.append(("slice", int(n) if n else 0))
                    else:
                        ops.append(("unknown", None))

        # If still empty, try to extract inline ops: .reverse(), .slice(N), swap pattern
        if not ops:
            if "reverse()" in body:
                ops.append(("reverse", None))
            for m in re.finditer(r"\.slice\((\d+)\)", body):
                ops.append(("slice", int(m.group(1))))
            for m in re.finditer(r"var\s+[a-z]=\w\[0\];\w\[0\]=\w\[(\d+)%\w\.length\];\w\[\1\]=[a-z];", js):
                ops.append(("swap", int(m.group(1))))

    ##    if not ops:
    ##        raise RuntimeError("Could not determine decipher operations")

        return ops


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


def run_js_decipher(js_code: str, fn: str, s: str) -> str:
    # write base.js to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".js") as f:
        f.write(js_code.encode())
        temp_path = f.name

    # run node decrypt.js temp.js fn signature
    out = subprocess.check_output(
        ["node", "decrypt.js", temp_path, fn, s],
        text=True
    )
    return out.strip()

def get_readable(string,start,end):
    print(start,end)
    str_len = len(string)
    if start>str_len:
        return False
    if end>str_len:
        end = str_len
    return string[start:end]
            
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
            response = run_js_decipher(js_code=js, fn=name, s=s)
            input(response)
            funame["name"]=name
            funame["vars"] = eatAll(get_enclosed(aft,'(',')'),[' ','\n','\t',''])    
            fn_rest = ['function'.join(bef[1:])]
            rest = ';'.join(fn_rest+lines[i+1:])
            fun = eatAll(get_enclosed(rest),[' ','\n','\t',''])
            funame["fun"] = fun 
            if '.split' in fun or '.slice' in fun or '.join' in fun or '.reverse' in fun or '.swap' in fun:
                funames.append(funame)
                apply_ops(s, fun)
                
##    while True:
##        c = j*i
##        k = c-j
##        readable = get_readable(lines,k,c)
##        i+=1
##        if readable==False:
##            break
##        input(readable)

    ops = extract_operations(js, fn)
    return 


# ---------- main flow ----------
def get_direct_url_for_video(url: str) -> Tuple[str, str]:
    html=get_html(url) 
    all_js = get_all_js(url=url,html=html)
   
    player_response = extract_yt_initial_player_response(html)
    formats = parse_streaming_data(player_response)

    
    # prefer formats with direct url
    for fmt in formats:
        if fmt.get("url"):
            return fmt["url"], fmt.get("qualityLabel") or fmt.get("quality") or fmt.get("mimeType")

    # otherwise parse signatureCipher entries
    # signatureCipher has form: "s=ENC&sp=signature&url=ENCURL" or "cipher=..."
    for fmt in formats:
        sc = fmt.get("signatureCipher") or fmt.get("cipher")
        if not sc:
            continue
        # parse query-string style
        parsed = urllib.parse.parse_qs(sc)
        s = parsed.get("s", [None])[0]
        url = parsed.get("url", [None])[0]
        sp = parsed.get("sp", ["signature"])[0]
        if not s or not url:
            continue

        # fetch player js
        player_js_url = find_player_js_url(html)
        js = fetch_js(player_js_url)
        
        
        # try to decipher
     
        signature = decipher_signature(js, s)

        # append signature param to url
        parsed_url = urllib.parse.urlparse(url)
        q = urllib.parse.parse_qs(parsed_url.query)
        q[sp] = signature
        new_query = urllib.parse.urlencode({k: v if isinstance(v, str) else v for k, v in q.items()}, doseq=True)
        final_url = urllib.parse.urlunparse(parsed_url._replace(query=new_query))
        return final_url, fmt.get("qualityLabel") or fmt.get("mimeType")

    raise RuntimeError("No usable direct URL found (and signature decipher failed)")
def download(url: str, output: str = "video.mp4") -> str:
    ua_mgr = UserAgentManager(randomAll=True)
    base_headers = ua_mgr.generate_for_url("https://www.youtube.com")

    # --- ABSOLUTELY REQUIRED FOR YOUTUBE CDN ----
    yt_overrides = {
        "User-Agent": base_headers["User-Agent"],  # MUST be string, not dict
        "Accept": "*/*",
        "Accept-Encoding": "identity",   # CRITICAL FIX
        "Connection": "keep-alive",
        "Referer": "https://www.youtube.com/",
        "Origin": "https://www.youtube.com",
        "Range": "bytes=0-",             # CRITICAL FIX
    }

    # Merge: browser headers + YouTube overrides
    headers = {**base_headers, **yt_overrides}

    print(f"Downloading:\n{url}\n-> {output}")

    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()

        with open(output, "wb") as f:
            for chunk in r.iter_content(chunk_size=64 * 1024):
                if chunk:
                    f.write(chunk)

    print(f"Done! Saved to: {output}")
    return output
def run_js_decipher(js_code: str, fn: str, s: str) -> str:
    # write base.js to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".js") as f:
        f.write(js_code.encode())
        temp_path = f.name

    # run node decrypt.js temp.js fn signature
    out = subprocess.check_output(
        ["node", "decrypt.js", temp_path, fn, s],
        text=True
    )
    return out.strip()

# Example usage:
if __name__ == "__main__":
    vid = "0XFudmaObLI"
    url = 'https://www.youtube.com/shorts/6vP02wYh4Ds'
    
    direct_url, quality = get_direct_url_for_video(url)
    result = download(direct_url)
    print("Direct URL:", direct_url)
    print("Quality:", quality)

