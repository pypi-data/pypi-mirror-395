from imports.src.abstract_webtools.managers.videoDownloader import *
from urllib.parse import urlparse, parse_qs
import os
import mimetypes
import yt_dlp
import os
video_url = "https://www.instagram.com/reel/DRS6A9yEnA_"
def get_all_from_source(video_url):
    call_keys = ["get_video_info","download_video","get_video_whisper_result","get_video_metadata","get_all_data"]
    for endpoint in call_keys:
        sub_endpoint = "hugpy"
        url = f"https://typicallyoutliers.com/{sub_endpoint}"
        data={"url":video_url}
        result = postRequest(url,endpoint=endpoint,data=data)
        all_js = {}
        if endpoint == 'get_video_info':
            for key in ['paths','video_path','audio_path','webpage_url',"thumbnails","ext","fulltitle"]:
               
                all_js[key]=find_paths_to_key(result,key)
        input(result)
DOWNLOAD_FOLDER = "/var/www/media/DATA/videos"  # ← CHANGE THIS
ARCHIVE_FILE = os.path.join(DOWNLOAD_FOLDER, "archive.txt")
get_all_from_source(video_url)
# Create the base folder if it doesn't exist
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_video_silently(url: str):
    ydl_opts = {
        'download_archive': ARCHIVE_FILE,
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mkv',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(id)s/%(id)s.%(ext)s',

        # THIS IS THE MAGIC PART — TOTAL SILENCE
        'quiet': True,                  # suppress almost everything
        'no_warnings': False,         # hide warnings too
        'no_progress': True,            # no progress bars at all
        'progress_hooks': [],           # disable any custom progress output
        
        # Only show real problems
        'ignoreerrors': False,          # stop and show error if something breaks
        
        # Still recommended options
        'concurrent_fragments': 8,
        'retries': 10,
        'writethumbnail': True,
        'writeinfojson': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Example
if __name__ == "__main__":
    download_video_silently("https://www.facebook.com/reel/835367642535780")


input()
YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "youtu.be"}
VIMEO_HOSTS = {"vimeo.com", "www.vimeo.com"}
TIKTOK_HOSTS = {"tiktok.com", "www.tiktok.com"}
TWITTER_HOSTS = {"twitter.com", "x.com", "www.twitter.com", "www.x.com"}
DIRECT_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg",
    ".mp4", ".mov", ".mkv", ".avi",
    ".mp3", ".wav", ".ogg",
    ".pdf", ".zip", ".rar", ".7z", ".gz",
}

def _clean_url(url: str) -> str:
    """ normalize scheme + strip weird fragments """
    if not url:
        return ""
    url = url.strip()
    if url.startswith("//"):
        url = "https:" + url
    return url

# -----------------------------------------------------
# PLATFORM EXTRACTORS
# -----------------------------------------------------

def detect_youtube(parsed, query):
    netloc = parsed.netloc.lower()
    if netloc not in YOUTUBE_HOSTS:
        return None

    # video id
    if "v" in query:
        return {
            "downloadable": True,
            "kind": "video",
            "provider": "youtube",
            "id": query.get("v", [None])[0],
            "direct": False,
        }

    # youtu.be short links
    if parsed.netloc == "youtu.be":
        vid = parsed.path.strip("/")
        return {
            "downloadable": True,
            "kind": "video",
            "provider": "youtube",
            "id": vid,
            "direct": False,
        }

    # playlists
    if "list" in query:
        return {
            "downloadable": True,
            "kind": "playlist",
            "provider": "youtube",
            "id": query.get("list", [None])[0],
            "direct": False,
        }

    return {
        "downloadable": False,
        "kind": None,
        "provider": "youtube",
        "id": None,
        "direct": False,
    }


def detect_vimeo(parsed):
    if parsed.netloc.lower() not in VIMEO_HOSTS:
        return None
    vid = parsed.path.strip("/")
    if vid.isdigit():
        return {
            "downloadable": True,
            "kind": "video",
            "provider": "vimeo",
            "id": vid,
            "direct": False
        }
    return {"downloadable": False, "provider": "vimeo"}


def detect_tiktok(parsed):
    if parsed.netloc.lower() not in TIKTOK_HOSTS:
        return None

    parts = parsed.path.split("/")
    # /@user/video/123456
    if "video" in parts:
        idx = parts.index("video")
        vid = parts[idx + 1] if idx + 1 < len(parts) else None
        return {
            "downloadable": True,
            "kind": "video",
            "provider": "tiktok",
            "id": vid,
            "direct": False,
        }
    return {"downloadable": False, "provider": "tiktok"}


def detect_twitter(parsed, query):
    if parsed.netloc.lower() not in TWITTER_HOSTS:
        return None

    parts = parsed.path.split("/")
    # /username/status/ID
    if "status" in parts:
        idx = parts.index("status")
        tid = parts[idx + 1] if idx + 1 < len(parts) else None
        return {
            "downloadable": True,
            "kind": "video",
            "provider": "twitter",
            "id": tid,
            "direct": False,
        }
    return {"downloadable": False, "provider": "twitter"}


# -----------------------------------------------------
# DIRECT FILE DETECTION
# -----------------------------------------------------

def detect_direct_file(parsed):
    ext = os.path.splitext(parsed.path)[1].lower()
    if ext in DIRECT_EXTS:
        return {
            "downloadable": True,
            "kind": mimetypes.guess_type(parsed.path)[0] or "file",
            "provider": None,
            "id": None,
            "direct": True,
        }
    return None


# -----------------------------------------------------
# MAIN ENTRY POINT
# -----------------------------------------------------

def get_downloadable_info(url: str):
    url = _clean_url(url)
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    # 1. Direct file
    direct = detect_direct_file(parsed)
    if direct:
        direct["url"] = url
        return direct

    # 2. YouTube
    yt = detect_youtube(parsed, query)
    if yt:
        yt["url"] = url
        return yt

    # 3. Vimeo
    vimeo = detect_vimeo(parsed)
    if vimeo:
        vimeo["url"] = url
        return vimeo

    # 4. TikTok
    tiktok = detect_tiktok(parsed)
    if tiktok:
        tiktok["url"] = url
        return tiktok

    # 5. Twitter/X
    tw = detect_twitter(parsed, query)
    if tw:
        tw["url"] = url
        return tw

    # fallback
    return {
        "downloadable": False,
        "kind": None,
        "provider": None,
        "id": None,
        "direct": False,
        "url": url,
    }
import requests

def download(url, output=None):
    output = output or 'video.mp4'
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(output, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


corrected_url= get_corrected_url(video_url)
url_mgr = urlManager(video_url)
name = url_mgr.parsed.get('name')
name = url_mgr.parsed.get('name')
domain = url_mgr.parsed.get('domain')
query = url_mgr.parsed.get('query')
v = query.get('v')
if name == 'youtube':
    video_url = f'https://www.{domain}/watch?v={v}'
input(get_youtube_parsed_dict(url=video_url))
url_mgr = urlManager(DOMAIN)



