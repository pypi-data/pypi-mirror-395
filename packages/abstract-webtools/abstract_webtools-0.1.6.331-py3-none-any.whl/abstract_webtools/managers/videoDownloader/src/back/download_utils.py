from .imports import *
from .path_utils import *
from abstract_utilities import make_list,get_any_value
_LOCK = threading.RLock()
# ---------------- Registry ---------------- #
def get_video_url(url=None, video_url=None):
    video_url = url or video_url
    if video_url:
        video_url = get_corrected_url(video_url)
    return video_url
class infoRegistry(metaclass=SingletonMeta):
    """Thread-safe registry with all video assets stored under ~/videos/<video_id>/ or flat."""

    def __init__(self, video_root=None, flat_layout: bool = False, **kwargs):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.video_root = get_video_root(video_root)
            self.flat_layout = flat_layout
            self.registry_path = os.path.join(self.video_root, "registry.json")
            self._load_registry()


    def _load_registry(self):
        with _LOCK:
            self.registry = {"by_url": {}, "by_id": {}, "by_path": {}}
            if os.path.isfile(self.registry_path):
                try:
                    with open(self.registry_path, "r", encoding="utf-8") as f:
                        j = json.load(f)
                    self.registry["by_url"].update(j.get("by_url", {}))
                    self.registry["by_id"].update(j.get("by_id", {}))
                    self.registry["by_path"].update(j.get("by_path", {}))
                except Exception:
                    pass

    def _save_registry(self):
        with _LOCK:
            get_atomic_write(self.registry_path, self.registry)

    # ---------- pruning ----------

    def prune_registry(self, dry_run: bool = False):
        """Remove broken .NA / recommended / missing-path entries."""
        removed = []
        with _LOCK:
            to_delete = []
            for vid, meta in self.registry["by_id"].items():
                vpath = meta.get("video_path")
                url = meta.get("url", "")
                if not vpath or vpath.endswith(".NA") or not os.path.exists(vpath):
                    to_delete.append(vid)
                if url.endswith("/watch") and "v=" not in url:
                    to_delete.append(vid)
            for vid in set(to_delete):
                removed.append(vid)
                self.registry["by_id"].pop(vid, None)
                self.registry["by_url"] = {u: v for u, v in self.registry["by_url"].items() if v != vid}
                self.registry["by_path"] = {p: v for p, v in self.registry["by_path"].items() if v != vid}
            if not dry_run:
                self._save_registry()
        if removed:
            logger.info(f"[infoRegistry] Pruned {len(removed)} invalid entries: {removed}")
        return removed

    # ---------- cache helpers ----------


    def _read_cached_info(self, video_id: str) -> dict | None:
        cache_dir = self.video_root if self.flat_layout else os.path.join(self.video_root, video_id)
        cache = os.path.join(cache_dir, "info.json")
        if os.path.isfile(cache):
            try:
                with open(cache, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return None
        return None

    def _write_cached_info(self, video_id: str, info: dict) -> str:
        # Prefer the actual folder that already holds the video
        cache_dir = info.get("directory") or (
            self.video_root if self.flat_layout else os.path.join(self.video_root, video_id)
        )
        os.makedirs(cache_dir, exist_ok=True)
        cache = os.path.join(cache_dir, "info.json")
        get_atomic_write(cache, info)
        return cache

    def _resolve_video_id(self, url: str | None, video_path: str | None, hint_id: str | None) -> str | None:
        if hint_id:
            return hint_id
        if video_path and video_path in self.registry["by_path"]:
            return self.registry["by_path"][video_path]
        if url and url in self.registry["by_url"]:
            return self.registry["by_url"][url]
        return None

    def _link(self, video_id: str, url: str | None, video_path: str | None):
        with _LOCK:
            if url:
                self.registry["by_url"][url] = video_id
            if video_path:
                self.registry["by_path"][video_path] = video_id
            rec = self.registry["by_id"].get(video_id, {})
            if url:
                rec["url"] = url
            if video_path:
                rec["video_path"] = video_path
            rec["timestamp"] = time.time()
            self.registry["by_id"][video_id] = rec
            self._save_registry()
    def edit_info(self, data: dict, url: str | None = None,
                  video_id: str | None = None, video_path: str | None = None):
        cur = self.get_video_info(url=url, video_id=video_id, video_path=video_path, force_refresh=False)
        if not cur:
            raise RuntimeError("No existing info to edit")

        cur.update(data or {})

        # Stable ID: prefer existing values; never force a new slug unless absolutely needed
        canonical = (
            cur.get("video_id")
            | cur.get("id")
            | video_id
            | (get_sha12(url) if url else None)
        )
        if not canonical:
            canonical = generate_video_id(video_path or "video")

        cur["video_id"] = canonical

        # Use the folder that actually contains the mp4
        video_dir = (
            cur.get("directory")
            or (os.path.dirname(os.path.abspath(cur.get("file_path"))) if cur.get("file_path") else None)
            or (os.path.dirname(os.path.abspath(video_path)) if video_path else None)
        )

        if video_dir:
            # Expand schema IN PLACE (no <root>/<video_id> subdir)
            cur = ensure_standard_paths(cur, video_dir, flat_layout=True)
            cache_path = os.path.join(video_dir, "info.json")
        else:
            # Last resort
            base = self.video_root if self.flat_layout else os.path.join(self.video_root, canonical)
            os.makedirs(base, exist_ok=True)
            cur = ensure_standard_paths(cur, base, flat_layout=self.flat_layout)
            cache_path = os.path.join(base, "info.json")

        get_atomic_write(cache_path, cur)
        self._link(canonical, url, cur.get("file_path") or video_path)
        cur["info_path"] = cache_path
        return cur

    # ---------- main API ----------

    def get_video_info(self, url: str | None = None, video_id: str | None = None,
                       force_refresh: bool = False, video_path: str | None = None,
                       download=False) -> dict | None:
        # prune each call
        self.prune_registry(dry_run=False)

        # reject bare /watch
        if url and "youtube.com/watch" in url and "v=" not in url:
            logger.debug(f"[infoRegistry] Ignoring bare watch URL: {url}")
            return None

        if video_path and os.path.isfile(video_path):
            vid = video_id or generate_video_id(video_path)
            info = make_video_info(video_path)
            cache = self._write_cached_info(vid, info)
            self._link(vid, url, os.path.abspath(video_path))
            info["info_path"] = cache
            info["video_id"] = vid
            return ensure_standard_paths(info, self.video_root)

        vid = self._resolve_video_id(url, video_path, video_id)

        if vid and not force_refresh:
            cached = self._read_cached_info(vid)
            if cached:
                self._link(vid, url, cached.get("file_path"))
                cached["info_path"] = os.path.join(self.video_root, vid, "info.json")
                cached["video_id"] = vid
                return ensure_standard_paths(cached, self.video_root)

        if url:
            info = get_yt_dlp_info(url)
            if info:
                vid = info.get("id") or get_sha12(url)
                cache = self._write_cached_info(vid, info)
                self._link(vid, url, None)
                info["info_path"] = cache
                info["video_id"] = vid
                return ensure_standard_paths(info, self.video_root)

        return None

    def list_cached_videos(self):
        with _LOCK:
            return [
                {"video_id": vid, "url": meta.get("url"),
                 "video_path": meta.get("video_path"), "timestamp": meta.get("timestamp")}
                for vid, meta in self.registry["by_id"].items()
            ]


# ---------------- Downloader ---------------- #

class VideoDownloader:
    def __init__(self, url=None,download_directory=None, user_agent=None,
                 video_extention="mp4", download_video=True,
                 video_path=None,
                 output_filename=None, ydl_opts=None,
                 registry=None, force_refresh=False,
                 flat_layout: bool = False,video_url =None):

        self.video_url = get_video_url(url or video_url )
        self.video_urls = make_list(self.video_url)
        self.video_id =  generate_video_id(self.video_url)
        self.registry = registry or infoRegistry(video_root=download_directory,flat_layout=flat_layout)
        self.ydl_opts = ydl_opts or {}
        self.get_download = download_video
        self.user_agent = user_agent
        self.video_extention = video_extention
        self.download_directory = get_video_root(download_directory)
        self.output_filename = output_filename
        self.force_refresh = force_refresh
        self.flat_layout = flat_layout   # 🔑
        self.video_path=video_path
        self.info = self.registry.get_video_info(url=self.video_url,video_id=self.video_id,video_path=self.video_path, force_refresh=self.force_refresh) or {}
        self.video_path=self.info.get('video_path') or self.video_path
        
        self.monitoring = True
        self.pause_event = threading.Event()

        self._start()

    def _start(self):
        self.download_thread = threading.Thread(
            target=self._download_entrypoint, name="video-download", daemon=True
        )
        self.monitor_thread = threading.Thread(
            target=self._monitor, name="video-monitor", daemon=True
        )
        self.download_thread.start()
        self.monitor_thread.start()
        self.download_thread.join()

    def stop(self):
        self.monitoring = False
        self.pause_event.set()

    def _monitor(self, interval=30, max_minutes=15):
        start = time.time()
        while self.monitoring:
            logger.info("Monitoring...")
            if time.time() - start > max_minutes * 60:
                logger.info("Monitor: timeout reached, stopping.")
                break
            self.pause_event.wait(interval)
        logger.info("Monitor: exited.")

    def _build_ydl_opts(self, outtmpl, extractor_client=None):
        opts = {
            "quiet": True,
            "noprogress": True,
            # write under <download_directory>/<id>/<id>.<ext>
            "outtmpl": outtmpl,                      # see call-site below
            # pick best and merge; final container = mp4
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            # remux to mp4 even when streams are webm/opus
            "postprocessors": [
                {"key": "FFmpegVideoRemuxer", "preferedformat": "mp4"},
            ],
            "retries": 5,
            "fragment_retries": 5,
            "ignoreerrors": False,
            # optional: YouTube client to reduce 403s
            "extractor_args": {"youtube": {"player_client": ["android"]}},
        }
        if extractor_client:
            opts.setdefault("extractor_args", {}).setdefault("youtube", {})["player_client"] = [extractor_client]
        if self.user_agent:
            opts["http_headers"] = {"User-Agent": self.user_agent}
        opts.update(self.ydl_opts or {})
        return opts

    def _download_entrypoint(self):
        try:
            for url in self.video_urls:
                self._download_single(url)
        finally:
            self.stop()
    
    def _download_single(self, url=None,download_directory=None, user_agent=None,
                         video_extention="mp4", download_video=True,
                         video_path=None, output_filename=None, ydl_opts=None,
                         registry=None, force_refresh=False,
                         flat_layout: bool = False,video_url =None):
        video_url = get_video_url(url or video_url  or self.video_url)
        self.info = self.registry.get_video_info(url=video_url, force_refresh=self.force_refresh)
        info_video_path = self.info.get('video_path')
        if info_video_path and os.path.isfile(info_video_path) and not force_refresh:
            self.video_path = info_video_path
            self.video_id = self.info.get("id")
            self.video_url = video_url
            return self.info
        ydl_opts = ydl_opts or self.ydl_opts or {}
        user_agent = user_agent or self.user_agent
        force_refresh = force_refresh or self.force_refresh
        download_directory = download_directory or self.download_directory
        video_extention = video_extention or self.video_extention
        output_filename = output_filename or self.output_filename
        video_path = video_path or self.video_path
        if video_path:
             dirname = os.path.dirname(video_path)
             output_filename = dirname if dirname else download_directory or get_video_root(download_directory)
             basename = os.path.basename(video_path)
             filename,ext = os.path.splitext(basename)
             output_filename = filename if filename else output_filename or 'video'
             video_extention = ext if ext else video_extention or '.mp4'
        output_filename = output_filename or 'video'
        download_directory = download_directory  or get_video_root(download_directory)
        flat_layout = flat_layout or self.flat_layout
        registry = registry or self.registry or infoRegistry(
             video_root=download_directory,
             flat_layout=flat_layout
             )
        logger.info(f"[VideoDownloader] Processing: {video_url}")
        video_url = get_corrected_url(url or video_url or self.url or self.video_url) 
        if "youtube.com/watch" in video_url and "v=" not in video_url:
            logger.debug(f"[VideoDownloader] Skipping bare watch URL: {video_url}")
            return None

        info = self.registry.get_video_info(url=video_url, force_refresh=self.force_refresh)
        if not info:
            logger.error("[VideoDownloader] No info; cannot determine target directory")
            return None

        directory = info.get("directory") or os.path.join(self.download_directory, info.get("id", "video"))
        check_create_logs(f"making this directory == {directory} line 316")
        os.makedirs(directory, exist_ok=True)

        # force an actual yt-dlp field: %(ext)s (not %(video_extention)s)
        # this will become video.mp4 because merge_output_format='mp4'
        outtmpl = os.path.join(directory, "video.%(ext)s")

        with yt_dlp.YoutubeDL(self._build_ydl_opts(outtmpl)) as ydl:
            raw_info = ydl.extract_info(video_url, download=self.get_download)

        # compute final path (should already be video.mp4 with the template above)
        temp_path = ydl.prepare_filename(raw_info)
        final_path = os.path.join(directory, "video.mp4")
        if os.path.abspath(temp_path) != os.path.abspath(final_path) and os.path.isfile(temp_path):
            shutil.move(temp_path, final_path)

        # minimal info for registry
        video_id = raw_info.get("id") or generate_video_id(raw_info.get("title") or "video")
        minimal_info = {
            "id": raw_info.get("id"),
            "title": raw_info.get("title"),
            "ext": "mp4",
            "duration": raw_info.get("duration"),
            "upload_date": raw_info.get("upload_date"),
            "video_id": video_id,
            "video_path": final_path,
            "file_path": final_path,
        }
        self.registry.edit_info(minimal_info, url=video_url, video_id=video_id, video_path=final_path)


        info = self.registry.get_video_info(video_id=video_id)
        logger.info(f"[VideoDownloader] Stored in registry at {info['video_path']}")
        return info
def get_info_from_mgr(mgr):
    if hasattr(mgr, 'info'):
        return mgr.info
    video_path, video_id, video_url = None, None, None
    if hasattr(mgr, 'video_path'):
        video_path = mgr.video_path
    if hasattr(mgr, 'video_id'):
        video_id = mgr.video_id
    elif hasattr(mgr, 'id'):
        video_id = mgr.id
    if hasattr(mgr, 'video_url'):
        video_url = mgr.video_url
    video_info = get_video_info(
        url=video_id,
        video_url=video_url,
        video_path=video_path
        )
    return video_info
def get_videoDownloader(url=None,
                   download_directory=None,
                   user_agent=None,
                   video_extention=None,
                   download_video=True,
                   video_path=None,
                   output_filename=None,
                   ydl_opts=None,
                   registry=None,
                   force_refresh=False,
                   flat_layout: bool = False,
                   video_url=None):
    video_url = get_video_url(url or video_url)
    videoDownload_mgr = VideoDownloader(
        video_url=video_url,
        download_directory=download_directory,
        user_agent=user_agent,
        video_extention=video_extention,
        download_video=download_video,
        video_path=video_path,
        output_filename=output_filename,
        ydl_opts=ydl_opts,
        registry=registry,
        flat_layout=flat_layout
        )
    return videoDownload_mgr
def download_video(url=None,
                   download_directory=None,
                   user_agent=None,
                   video_extention=None,
                   download_video=True,
                   video_path=None,
                   output_filename=None,
                   ydl_opts=None,
                   registry=None,
                   force_refresh=False,
                   flat_layout: bool = False,
                   video_url=None):
        video_url = get_video_url(url or video_url)
        videoDownload_mgr = get_videoDownloader(
            video_url=video_url,
            download_directory=download_directory,
            user_agent=user_agent,
            video_extention=video_extention,
            download_video=download_video,
            video_path=video_path,
            output_filename=output_filename,
            ydl_opts=ydl_opts,
            registry=registry,
            flat_layout=flat_layout
            )
        
        return get_info_from_mgr(videoDownload_mgr)

def get_infoRegistry(video_root=None, flat_layout=None):
    return infoRegistry(video_root=video_root, flat_layout=flat_layout)

def get_registry_video_root(video_root=None, flat_layout=None):
    registry_mgr = get_infoRegistry(video_root=video_root, flat_layout=flat_layout)
    return registry_mgr.video_root

def get_registry_path(video_root=None, flat_layout=None):
    registry_mgr = get_infoRegistry(video_root=video_root, flat_layout=flat_layout)
    return registry_mgr.registry_path

def get_video_info(url=None, video_url=None, video_id=None, 
                        video_path=None, video_root=None,
                        force_refresh=False, flat_layout=None, download=False):
    registry_mgr = get_infoRegistry(video_root=video_root, flat_layout=flat_layout)
    url = get_video_url(url or video_url)
    video_info = registry_mgr.get_video_info(
        url=url,
        video_id=video_id,
        video_path=video_path,
        force_refresh=force_refresh,
    )
    if download:
        video_info = download_video(
            video_url=video_url,
            download_directory=video_root,
            download_video=download,
            video_path=video_path,
            flat_layout=flat_layout
            )
    return video_info or {}

def get_video_info_spec(url=None, video_url=None, video_id=None, 
                        video_path=None, video_root=None, key=None,
                        force_refresh=False, flat_layout=None, download=False):
    video_url = get_video_url(url or video_url)
    video_info = get_video_info(
        video_url=video_url,
        video_id=video_id,
        video_path=video_path,
        force_refresh=force_refresh,
        video_root=video_root,
        flat_layout=flat_layout,
        download=download
    )
    if not key:
        return video_info
    keys = make_list(key)
    value = None
    for key in keys:
        value = video_info.get(key)
        if not value:
            values = make_list(get_any_value(video_info, key) or None)
            value = values[0]
        if value:
            break
    return value

def get_video_id(
        url=None,
        video_url=None,
        video_id=None,
        video_path=None,
        force_refresh=False,
        download=False,
        video_root=None,
        flat_layout=None
    ):
    info_spec = get_video_info_spec(
        url=url,
        video_url=video_url,
        video_id=video_id,
        video_path=video_path,
        force_refresh=force_refresh,
        download=download,
        video_root=video_root,
        flat_layout=flat_layout,
        key=['id','video_id']
        )
    return info_spec
def get_video_title(
        url=None,
        video_url=None,
        video_id=None,
        video_path=None,
        force_refresh=False,
        download=False,
        video_root=None,
        flat_layout=None
    ):
    info_spec = get_video_info_spec(
        url=url,
        video_url=video_url,
        video_id=video_id,
        video_path=video_path,
        force_refresh=force_refresh,
        download=download,
        video_root=video_root,
        flat_layout=flat_layout,
        key=['title']
        )
    return info_spec
def get_video_filepath(
        url=None,
        video_url=None,
        video_id=None,
        video_path=None,
        force_refresh=False,
        download=False,
        video_root=None,
        flat_layout=None
    ):
    info_spec = get_video_info_spec(
        url=url,
        video_url=video_url,
        video_id=video_id,
        video_path=video_path,
        force_refresh=force_refresh,
        download=download,
        video_root=video_root,
        flat_layout=flat_layout,
        key=['filepath','file_path','video_path','videopath']
        )
    return info_spec

def get_video_info_from_mgr(video_mgr):
    try:
        info = video_mgr.info
        return info
    except Exception as e:
        print(f"{e}")
        return None

