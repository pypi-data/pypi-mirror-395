import re
import urllib.parse
# ------------------------------------------------------------
#  YOUTUBE N-PARAM DECIPHERING (YouTube throttle bypass)
# ------------------------------------------------------------

def find_n_function_name(js: str) -> str | None:
    """
    Extracts the name of the 'n' transform function from player.js.
    YouTube typically uses something like: 
        .get("n").then(nu)  → so we find "nu"
    """
    # Look for code that defines the n transform function object.
    # Example js snippet: 
    #   a.set("n",function(b){return Xy(b)})
    m = re.search(r'\.get\(?"n"\)?\.then\((?P<fn>[A-Za-z0-9$]{2,})\)', js)
    if m:
        return m.group("fn")

    # fallback: search assignment
    m = re.search(r'(?P<fn>[A-Za-z0-9$]{2,})=function\(a\)\{a=a\.split', js)
    if m:
        return m.group("fn")

    return None


def extract_n_operations(js: str, fn_name: str):
    """
    Inspect the function implementation and extract the sequence of operations.
    Similar to signature decoding: reverse, slice, swap.
    """
    # Find fn_name:function(a){ ... }
    pat = re.compile(rf'{re.escape(fn_name)}=function\(a\)\{{(.*?)\}}', re.S)
    m = pat.search(js)
    if not m:
        return []

    body = m.group(1)

    # Find helper object used inside this function
    helper = re.search(r'([A-Za-z0-9$]{2,})\.[A-Za-z0-9$]{2,}\(a,\d+\)', body)
    helper_obj = helper.group(1) if helper else None

    ops = []

    # Inline reverse()
    if "reverse()" in body:
        ops.append(("reverse", None))

    # inline slice(n)
    sl = re.findall(r'\.slice\((\d+)\)', body)
    for s in sl:
        ops.append(("slice", int(s)))

    # If helper object exists, extract from the helper definition
    if helper_obj:
        obj_pat = re.compile(rf'var {re.escape(helper_obj)}=\{{(.*?)\}};', re.S)
        mm = obj_pat.search(js)
        if mm:
            helper_body = mm.group(1)
            # map methods to op types
            method_map = {}
            for k, v in re.findall(r'([A-Za-z0-9$]{2,}):function\(a,b\)\{([^}]+)\}', helper_body):
                code = v.strip()
                if "reverse" in code:
                    method_map[k] = "reverse"
                elif "splice" in code or "slice" in code:
                    method_map[k] = "slice"
                elif "var c=a[0]" in code:
                    method_map[k] = "swap"

            # Now find calls in body
            for call, num in re.findall(rf'{helper_obj}\.([A-Za-z0-9$]{{2,}})\(a,?(\d+)?\)', body):
                op = method_map.get(call)
                if op == "reverse":
                    ops.append(("reverse", None))
                elif op == "slice":
                    ops.append(("slice", int(num)))
                elif op == "swap":
                    ops.append(("swap", int(num)))

    return ops


def apply_n_ops(n_value: str, ops):
    """Apply the decoded throttle operations."""
    arr = list(n_value)
    for op, val in ops:
        if op == "reverse":
            arr.reverse()
        elif op == "slice":
            arr = arr[val:]
        elif op == "swap":
            i = val % len(arr)
            arr[0], arr[i] = arr[i], arr[0]
    return "".join(arr)


def decrypt_n_param(js: str, n_value: str) -> str:
    """
    Fully decode YouTube 'n=' throttle parameter.
    """
    fn_name = find_n_function_name(js)
    if not fn_name:
        return n_value  # can't decode, fallback

    ops = extract_n_operations(js, fn_name)
    if not ops:
        return n_value  # fallback

    return apply_n_ops(n_value, ops)
