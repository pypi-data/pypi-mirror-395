from imports.src.abstract_webtools.managers.videoDownloader import *
from urllib.parse import urlparse, parse_qs
import os
import mimetypes
import yt_dlp
import os
calls  = {'download': {'key': 'download', 'subkey': None},
 'audio': {'key': 'audio', 'subkey': None},
 'whisper': {'key': 'whisper', 'subkey': None},
 'whisper_text': {'key': 'whisper', 'subkey': 'text'},
 'whisper_segments': {'key': 'whisper', 'subkey': 'segments'},
 'metadata': {'key': 'metadata', 'subkey': None},
 'title': {'key': 'title', 'subkey': None},
 'summary': {'key': 'summary', 'subkey': None},
 'keywords': {'key': 'keywords', 'subkey': None},
 'thumbnails': {'key': 'thumbnails', 'subkey': None},
 'seodata': {'key': 'seodata', 'subkey': None},  
 'get_captions': {'key': 'captions', 'subkey': None},
 'thumbnails_dict': {'key': 'thumbnails', 'subkey': None},
 'thumbnails': {'key': 'thumbnails', 'subkey': ['thumbnails','thumbnails']},
 'thumbnail_dir': {'key': 'info', 'subkey': 'thumbnail_directory'},
 'thumbnail_paths': {'key': 'thumbnails', 'subkey': ['thumbnails','paths']},
 'info': {'key': 'info', 'subkey': None},
 'get_video_directory': {'key': 'info', 'subkey': 'directory'},
 'get_video_path': {'key': 'info', 'subkey': 'video_path'},
 'get_audio_path': {'key': 'info', 'subkey': 'audio_path'},

 'aggregated': {'key': 'aggregated', 'subkey': None},
 'all': {'key': 'all', 'subkey': None}}

video_url = "https://www.instagram.com/reel/DRS6A9yEnA_"
def get_all_from_source(video_url):
    call_keys = ["info","download","whisper","video_path","all"]
    data={"url":video_url}
    for endpoint,call_values in calls.items():
        sub_endpoint = "hugpy"
        url = f"https://typicallyoutliers.com/{sub_endpoint}"
        print(endpoint)
        result = postRequest(url,endpoint=endpoint,data=data)

        input(result)
get_all_from_source(video_url)
