
from __future__ import annotations
import time,json,hashlib,threading,re,yt_dlp,urllib.request,m3u8_To_MP4,subprocess,re, time,yt_dlp
import os,unicodedata, threading,requests,shutil,tempfile, shutil, threading, hashlib, unicodedata,re
import json,unicodedata,hashlib,re,math,pytesseract,cv2,PyPDF2,argparse,sys,json,logging,glob,importlib
from m3u8 import M3U8  # Install: pip install m3u8
from typing import *
from pathlib import Path
from PIL import Image
import numpy as np
import moviepy.editor as mp
from datetime import datetime, timedelta 
from urllib.parse import urljoin,quote
from moviepy.editor import VideoFileClip
from urllib.parse import quote
from collections import Counter
from pdf2image import convert_from_path
from yt_dlp.postprocessor.ffmpeg import FFmpegFixupPostProcessor
import speech_recognition as sr
from pydub.silence import detect_nonsilent,split_on_silence
from pydub import AudioSegment

from abstract_utilities import *
from abstract_security import get_env_value
from abstract_webtools.managers.urlManager import *
from abstract_webtools.managers.soupManager import *
from abstract_math import divide_it,add_it,multiply_it,subtract_it
from abstract_ai.gpt_classes.prompt_selection.PromptBuilder import recursive_chunk

logger = get_logFile('video_bp')
def bool_or_default(obj,default=True):
    if obj == None:
        obj =  default
    return obj

def get_video_url(url=None, video_url=None):
    video_url = url or video_url
    if video_url:
        video_url = get_corrected_url(video_url)
    return video_url










##from abstract_utilities import (timestamp_to_milliseconds,
##                                format_timestamp,
##                                get_time_now_iso,
##                                parse_timestamp,
##                                get_logFile,
##                                url_join,
##                                make_dirs,
##                                safe_dump_to_file,
##                                safe_read_from_json,
##                                read_from_file,
##                                write_to_file,
##                                path_join,
##                                confirm_type,
##                                get_media_types,
##                                get_all_file_types,
##                                eatInner,
##                                eatOuter,
##                                eatAll,
##                                get_all_file_types,
##                                is_media_type,
##                                safe_load_from_json,
##                                get_any_value)

