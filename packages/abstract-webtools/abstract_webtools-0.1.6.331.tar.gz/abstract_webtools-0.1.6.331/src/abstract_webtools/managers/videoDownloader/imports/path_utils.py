from .imports import *
_LOCK = threading.RLock()
VIDEO_ENV_KEY = "DATA_DIRECTORY"
# near your helpers
YT_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
# Full schema
VIDEO_SCHEMA = {
    "video_path": "video.mp4",
    "info_path": "info.json",
    "audio_path": "audio.wav",
    "whisper_path": "whisper.json",
    "captions_path": "captions.srt",
    "metadata_path": "metadata.json",
    "thumbnail_path": "thumb.jpg",
    "thumbnails_path": "thumbnails.json",
    "total_info_path": "total_info.json",
    "total_aggregated_path": "total_aggregated.json",
    "aggregated_directory": "aggregated",
    "aggregated_dir": {
        "aggregated_json_path": "aggregated.json",
        "aggregated_metadata_path": "aggregated_metadata.json",
        "best_clip_path": "best_clip.txt",
        "hashtags_path": "hashtags.txt",
    },
    "thumbnails_directory": "thumbnails",
    "thumbnails_dir": {
        "frames": "{video_id}_frame_{i}.jpg",  # pattern
    }
}
def check_create_logs(string):
    stri = string.split('==')[1]
    directory = eatAll(stri,[' ','\t'])
    if directory.lower() == directory:
        logger.info(f"this is the directory fudd\n\n\n{string}")
    

def generate_video_id(path_or_title: str, max_length: int = 50) -> str:
    base = os.path.splitext(os.path.basename(path_or_title))[0]
    if base == 'video':
        base = os.path.basename(os.path.dirname(path_or_title)) or base
    # 👇 preserve case for YouTube-like IDs
    if YT_ID_RE.match(base):
        return base

    # keep the rest as "slug"
    base = get_normalize_ascii(base)          # NOTE: no .lower() here
    base = re.sub(r'[^a-zA-Z0-9]+', '-', base).strip('-')
    base = re.sub(r'-{2,}', '-', base)
    if len(base) > max_length:
        h = get_sha12(base)
        base = f"{base[:max_length - len(h) - 1].rstrip('-')}-{h}"
    return base or get_sha12(path_or_title)
def get_temp_id(url):
    url = str(url)
    url_length = len(url)
    len_neg = 20
    len_neg = len_neg if url_length >= len_neg else url_length
    temp_id = re.sub(r'[^\w\d.-]', '_', url)[-len_neg:]
    return temp_id
def get_temp_file_name(url):
    temp_id = get_temp_id(url)
    temp_filename = f"temp_{temp_id}.mp4"
    return temp_filename
def get_display_id(info):
    display_id = info.get('display_id') or info.get('id')
    return display_id

def get_safe_title(title):
    re_str = r'[^\w\d.-]'
    safe_title = re.sub(re_str, '_', title)
    return safe_title
def download_image(url, save_path=None):
    """
    Downloads an image from a URL and saves it to the specified path.
    
    Args:
        url (str): The URL of the image to download
        save_path (str, optional): Path to save the image. If None, uses the filename from URL
        
    Returns:
        str: Path where the image was saved, or None if download failed
    """
    try:
        # Send GET request to the URL
        response = requests.get(url, stream=True)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Set decode_content=True to automatically handle Content-Encoding
            response.raw.decode_content = True
            
            # If no save_path provided, extract filename from URL
            if save_path is None:
                # Get filename from URL
                filename = url.split('/')[-1]
                save_path = filename
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # Write the image content to file
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            print(f"Image successfully downloaded to {save_path}")
            return save_path
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {str(e)}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None
def get_thumbnails(directory,info):
    thumbnails_dir = os.path.join(directory,'thumbnails')
    os.makedirs(thumbnails_dir, exist_ok=True)
    thumbnails = info.get('thumbnails',[])
    for i,thumbnail_info in enumerate(thumbnails):
        thumbnail_url = thumbnail_info.get('url')
        thumbnail_base_url = thumbnail_url.split('?')[0]
        baseName = os.path.basename(thumbnail_base_url)
        fileName,ext = os.path.splitext(baseName)
        baseName = f"{fileName}{ext}"
        resolution = info['thumbnails'][i].get('resolution')
        if resolution:
            baseName = f"{resolution}_{baseName}"
        img_id = info['thumbnails'][i].get('id')
        if img_id:
            baseName = f"{img_id}_{baseName}"
        thumbnail_path = os.path.join(thumbnails_dir,baseName)
        info['thumbnails'][i]['path']=thumbnail_path
        download_image(thumbnail_url, save_path=thumbnail_path)
    return info

def optimize_video_for_safari(input_file, reencode=False):
    """
    Optimizes an MP4 file for Safari by moving the 'moov' atom to the beginning.
    Optionally, re-encodes the video for maximum compatibility.
    
    Args:
        input_file (str): Path to the original MP4 file.
        reencode (bool): If True, re-encode the video for Safari compatibility.
        
    Returns:
        str: Path to the optimized MP4 file.
    """
    tmp_dir = tempfile.mkdtemp()
    try:
        local_input = os.path.join(tmp_dir, os.path.basename(input_file))
        shutil.copy2(input_file, local_input)
        
        base, ext = os.path.splitext(local_input)
        local_output = f"{base}_optimized{ext}"
        
        if reencode:
            # Re-encoding command for maximum Safari compatibility
            command = [
                "ffmpeg", "-i", local_input,
                "-c:v", "libx264", "-profile:v", "baseline", "-level", "3.0", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "128k",
                "-movflags", "faststart",
                local_output
            ]
        else:
            # Simple faststart with stream copy
            command = [
                "ffmpeg", "-i", local_input,
                "-c", "copy", "-movflags", "faststart",
                local_output
            ]
        
        try:
            subprocess.run(command, check=True)
            shutil.copy2(local_output, input_file)
            print(f"Optimized video saved as {input_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error during optimization: {e}")
        return input_file
    finally:
        shutil.rmtree(tmp_dir)




def dl_video(url, download_directory=None, output_filename=None,
             get_info=None, download_video=None, ydl_opts=None):
    mgr = get_video_info(
        url,
        download_directory=download_directory,
        output_filename=output_filename,
        get_info=get_info,
        download_video=download_video,
        ydl_opts=ydl_opts,  # pass through
    )
    return get_video_info_from_mgr(mgr)
def for_dl_video(url,download_directory=None,output_filename=None,get_info=None,download_video=None):
    get_info = bool_or_default(get_info,default=True)
    download_video =bool_or_default(download_video,default=True)
    video_mgr = dl_video(url,download_directory=download_directory,output_filename=output_filename,get_info=get_info,download_video=download_video)
    if get_video_info_from_mgr(video_mgr):
        return video_mgr
    videos = soupManager(url).soup.find_all('video')
    for video in videos:
        src = video.get("src")
        video_mgr = dl_video(src,download_directory=download_directory,output_filename=output_filename,download_video=download_video)
        if get_video_info_from_mgr(video_mgr):
            return video_mgr
def downloadvideo(
    url,
    directory=None,
    output_filename=None,          # kept for API compat; not used for final name
    rename_display=None,           # kept for API compat; final file is always video.mp4
    thumbnails=None,
    audio=None,
    safari_optimize=None,
    download_video=None,
    flat_layout: bool = False,
    *args, **kwargs,
):
    """
    Download a video and save alongside info.json and other schema files.

    Rules:
      - Final file is ALWAYS <video_dir>/video.mp4
      - Only ONE canonical video_dir is used
      - No extra folders derived from 'display_id' are created
    """
    # normalize flags
    rename_display   = bool_or_default(rename_display)          # no-op for file name
    thumbnails       = bool_or_default(thumbnails)
    audio            = bool_or_default(audio, default=False)
    safari_optimize  = bool_or_default(safari_optimize, default=True)
    download_video   = bool_or_default(download_video, default=True)

    # Kick off fetch/download via your existing flow
    # (keeps your yt-dlp + registry logic intact)
    _tmp_name = output_filename or get_temp_file_name(url)
    video_mgr = for_dl_video(
        url,
        download_directory=directory,
        output_filename=_tmp_name,
        download_video=download_video,
    )
    info = get_video_info_from_mgr(video_mgr) or {}

    # Decide canonical id & base root
    video_id   = info.get("video_id") or info.get("id") or get_temp_id(url)
    # If caller passed a root directory, respect it; otherwise use what the registry established
    base_root  = directory or info.get("directory") or get_video_root(None)

    # Decide the single canonical directory to use
    video_dir  = base_root if flat_layout else os.path.join(base_root, video_id)
    logger.info(f"making this downloadvideo == {video_dir} == get_video_directory line 246")
    os.makedirs(video_dir, exist_ok=True)

    # Where the final file must live
    final_path = os.path.join(video_dir, "video.mp4")

    # If a file was downloaded somewhere else, move it into place
    cur_path = info.get("file_path") or info.get("video_path")
    if cur_path and os.path.isfile(cur_path):
        if os.path.abspath(cur_path) != os.path.abspath(final_path):
            final_dir = os.path.dirname(final_path)
            logger.info(f"making this downloadvideo == {final_dir} == get_video_directory line 251")
            os.makedirs(final_dir, exist_ok=True)
            try:
                shutil.move(cur_path, final_path)
            except Exception:
                # If move fails (e.g. cross-device), copy+remove
                shutil.copy2(cur_path, final_path)
                os.remove(cur_path)
    else:
        # If yt-dlp already wrote video.mp4 at the canonical spot, keep it.
        # Otherwise, try to find any video-like file in video_dir and rename it.
        if not os.path.isfile(final_path):
            candidates = []
            for name in os.listdir(video_dir):
                p = os.path.join(video_dir, name)
                if os.path.isfile(p) and os.path.splitext(name)[1].lower() in {".mp4", ".m4v", ".mov", ".webm", ".mkv"}:
                    candidates.append(p)
            if candidates:
                # choose the largest as the likely full file
                best = max(candidates, key=lambda p: os.path.getsize(p))
                if os.path.abspath(best) != os.path.abspath(final_path):
                    shutil.move(best, final_path)

    # Safari faststart (moov up front) if we have a proper mp4
    if os.path.isfile(final_path) and final_path.lower().endswith(".mp4") and safari_optimize:
        try:
            optimize_video_for_safari(final_path, reencode=safari_optimize)
        except Exception as e:
            print(f"Safari optimization skipped: {e}")

    # Update info with canonical paths
    info["video_id"]  = video_id
    info["directory"] = video_dir
    info["file_path"] = final_path
    info["video_path"]= final_path

    # Thumbnails / audio (optional)
    if thumbnails:
        try:
            info = get_thumbnails(video_dir, info)
        except Exception as e:
            print(f"Thumbnail fetch failed: {e}")
    if audio:
        try:
            info = download_audio(video_dir, info)  # your helper
        except Exception:
            info["audio_path"] = None

    # Write info.json next to the video
    info_path = os.path.join(video_dir, "info.json")
    info["info_path"] = info_path
    info["json_path"] = info_path
    safe_dump_to_file(info, info_path)

    # Attach the rest of the schema INSIDE the already-chosen video_dir
    info = ensure_standard_paths(info, video_dir, flat_layout=True)
    return info

    return info


def expand_schema(video_id: str, folder: str, schema: dict[str, Any], flat_layout: bool = False) -> dict[str, Any]:
    """
    Expand VIDEO_SCHEMA into concrete paths (recursively).
    - Replaces {video_id} placeholder with the actual ID.
    - If flat_layout=True, do NOT create a <video_id> subdir.
    """
    result = {}
    for key, rel in schema.items():
        if isinstance(rel, dict):
            dirname = key.replace("_dir", "").replace("_directory", "")
            # If flat, stay in current folder
            subfolder = folder if flat_layout else os.path.join(folder, dirname)
            check_create_logs(f"making this directory == {subfolder} == expand_schema line 323")
            os.makedirs(subfolder, exist_ok=True)
            result[f"{dirname}_directory"] = subfolder
            result[key] = expand_schema(video_id, subfolder, rel, flat_layout=flat_layout)
        elif isinstance(rel, str):
            rel = rel.format(video_id=video_id, i="{i}")
            path = os.path.join(folder, rel)
            if key.endswith("_dir"):
                os.makedirs(path, exist_ok=True)
            result[key] = path
    return result


def ensure_standard_paths(info: dict, video_root: str,video_path: str =None, flat_layout: bool = False,) -> dict:
    """
    Ensure standard paths exist inside <video_root>/ or <video_root>/<video_id>/.
    Controlled by flat_layout.
    """
    vid = info.get("video_id") or info.get("id")
    if not vid:
        return info

    dirbase = video_root if flat_layout else os.path.join(video_root, vid)
    check_create_logs(f"making this directory == {dirbase} == ensure_standard_paths line 347")
    os.makedirs(dirbase, exist_ok=True)
    info["directory"] = dirbase

    schema_paths = expand_schema(vid, dirbase, VIDEO_SCHEMA, flat_layout=flat_layout)

    # flatten for convenience
    def flatten(d, parent_key="", sep="_"):
        flat = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                flat.update(flatten(v, new_key, sep))
            else:
                flat[new_key] = v
        return flat

    flat_paths = flatten(schema_paths)
    for k, v in flat_paths.items():
        if not info.get(k):
            info[k] = v

    info["schema_paths"] = schema_paths
    return info


def get_video_folder(video_id, envPath=None, flat_layout: bool = False):
    """Return the canonical video folder (with optional flat layout)."""
    root = get_video_directory(envPath=envPath)
    dir_path = root if flat_layout else os.path.join(root, video_id)
    check_create_logs(f"making this directory == {dir_path} == ensure_standard_paths line 377")
    os.makedirs(dir_path, exist_ok=True)
    return dir_path


def get_video_paths(video_id, envPath=None, flat_layout: bool = False):
    """Return dict of canonical paths for this video_id."""
    folder = get_video_folder(video_id, envPath=envPath, flat_layout=flat_layout)
    return expand_schema(video_id, folder, VIDEO_SCHEMA, flat_layout=flat_layout)

def get_video_env(key=None, envPath=None):
    """Pull video directory from env file or environment variables."""
    key = key or VIDEO_ENV_KEY
    return get_env_value(key=key, path=envPath)

def get_video_root(video_root=None):
    """Fallback root directory if no env override is found."""
    home = os.path.expanduser("~")
    candidates = [
        video_root,
        os.path.join(home, "videos"),
        os.path.join(home, "Videos"),
        os.path.join(home, "Downloads"),
        os.path.join(home, "downloads"),
        home,
    ]
    for directory in candidates:
        if directory and os.path.isdir(directory):
            return directory
    return home  # last resort

def get_video_directory(key=None, envPath=None):
    """Assure that a valid video directory exists and return its path."""
    video_directory = get_video_env(key=key, envPath=envPath)
    if not video_directory:
        video_directory = get_video_root()
    check_create_logs(f"making this directory == {dir_path} == get_video_directory line 413")
    os.makedirs(video_directory, exist_ok=True)
    return video_directory

def get_video_folder(video_id, envPath=None):
    """Return the canonical per-video folder and ensure subdirs exist."""
    root = get_video_directory(envPath=envPath)
    dir_path = os.path.join(root, video_id)
    os.makedirs(dir_path, exist_ok=True)

    # Ensure schema directories exist
    for key, rel in VIDEO_SCHEMA.items():
        if rel.endswith("/") or "dir" in key:
            os.makedirs(os.path.join(dir_path, rel), exist_ok=True)

    return dir_path

def get_video_paths(video_id, envPath=None):
    """Return dict of canonical paths for this video_id."""
    folder = get_video_folder(video_id, envPath=envPath)
    return {key: os.path.join(folder, rel) for key, rel in VIDEO_SCHEMA.items()}


##def generate_video_id(path: str, max_length: int = 50) -> str:
##    # 1. Take basename (no extension)
##    file_parts = get_file_parts(path)
##    base= file_parts.get("filename")
##    if base == 'video':
##        base = file_parts.get("dirbase")
##    # 2. Normalize Unicode → ASCII
##    base = unicodedata.normalize('NFKD', base).encode('ascii', 'ignore').decode('ascii')
##    # 3. Lower-case
##    base = base.lower()
##    # 4. Replace non-alphanumeric with hyphens
##    base = re.sub(r'[^a-z0-9]+', '-', base).strip('-')
##    # 5. Collapse duplicates
##    base = re.sub(r'-{2,}', '-', base)
##    # 6. Optionally truncate & hash for uniqueness
##    if len(base) > max_length:
##        h = hashlib.sha1(base.encode()).hexdigest()[:8]
##        base = base[: max_length - len(h) - 1].rstrip('-') + '-' + h
##    return base
def _get_video_info(url=None,file_path=None, ydl_opts=None,output_filename=None, cookies_path=None):
    from yt_dlp import YoutubeDL
    
    
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }

    if cookies_path and os.path.exists(cookies_path):
        ydl_opts['cookiefile'] = cookies_path

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        print(f"Failed to extract video info: {e}")
        return None

def get_sha12(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:12]

def get_atomic_write(path: str, data: dict):
    tmp = f"{path}.tmp"
    safe_dump_to_file(data, tmp)
    os.replace(tmp, path)

def get_normalize_ascii(s: str) -> str:
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')



def make_video_info(filepath: str) -> dict:
    import json as _json
    import subprocess as _sub
    cmd = [
        "ffprobe","-v","quiet","-print_format","json",
        "-show_format","-show_streams", filepath
    ]
    probe = _sub.check_output(cmd)
    data = _json.loads(probe)
    info = {
        "id": generate_video_id(filepath),
        "title": os.path.splitext(os.path.basename(filepath))[0],
        "upload_date": datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%Y%m%d"),
        "duration": float(data["format"].get("duration", 0.0)),
        "streams": data.get("streams", []),
        "format": data.get("format", {}),
        "file_path": os.path.abspath(filepath),
    }
    return info

def get_yt_dlp_info(url: str, ydl_opts: dict | None = None) -> dict | None:
    from yt_dlp import YoutubeDL
    opts = {'quiet': True, 'skip_download': True}
    if ydl_opts:
        opts.update(ydl_opts)
    try:
        with YoutubeDL(opts) as ydl:
            return ydl.extract_info(url, download=False)
    except Exception:
        return None
