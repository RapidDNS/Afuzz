import os
from pathlib import Path
import platform
from afuzz.utils.common import compatible_path
import afuzz.lib.config as mem

#VERSION = "0.1.6"

DEFAULT_HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "accept": "*/*",
    "accept-encoding": "*",
    "keep-alive": "timeout=15, max=1000",
    "cache-control": "max-age=0",
    #"Range": "bytes=0-1024000"
}

current_dir = Path(__file__).resolve().parent.parent.parent

afuzz_dir = compatible_path(mem.__file__.replace(compatible_path('/lib/config.py'), ''))

#DATA = str(Path(__file__).parent.resolve() / "db")
DATA = str(Path(__file__).parent.resolve() / "db")

PLATFORM_SYSTEM = platform.system()

NEW_LINE = os.linesep

DEFAULT_ENCODING = "utf-8"

COMMON_EXTENSIONS = ["html", "htm", "js"]

BACKUP_EXTENSIONS = ["zip", "rar", "tar", "tar.gz", "war", "jar", "tar.bz2", "sql", "bak"]

CONFIG_EXTENSIONS = ["conf", "config", "log", "properties", "ini", "json", "txt", "xml", "yaml", "yml"]

ASPX_EXTENSIONS = ["aspx", "ashx", "asmx", "dll"]

PHP_EXTENSIONS = ["php", "php5", "php7", "inc"]

JAVA_EXTENSIONS = ["do", "action", "jsp", "java", "jspx"]

OTHER_EXTENSIONS = ["sh", "bat", "cgi"]

WS_EXTENSIONS = ["wsdl", "asmx", "asdl", "jws"]

PYTHON_EXTENSIONS = ["py"]

MEDIA_EXTENSIONS = [
    "webm", "mkv", "avi", "ts", "mov", "qt", "amv", "mp4", "m4p", "m4v", "mp3", "swf", "mpg", "mpeg", "jpg", "jpeg",
    "pjpeg", "png", "woff", "woff2", "svg", "webp", "bmp", "pdf", "wav", "vtt"]

# EXCLUDE_OVERWRITE_EXTENSIONS = MEDIA_EXTENSIONS + ("axd", "cache", "coffee", "conf", "config", "css", "dll", "lock", "log", "key", "pub", "properties", "ini", "jar", "js", "json", "toml", "txt", "xml", "yaml", "yml")

CRAWL_ATTRIBUTES = ["action", "cite", "data", "formaction", "href", "longdesc", "poster", "src", "srcset", "xmlns"]

CRAWL_TAGS = [
    "a", "area", "base", "blockquote", "button", "embed", "form", "frame", "frameset", "html", "iframe", "input", "ins",
    "noframes", "object", "q", "script", "source"]

AUTHENTICATION_TYPES = ["basic", "digest", "bearer", "ntlm", "jwt"]

ROBOTS_TXT_REGEX = r"(?:Allow|Disallow): /(.*)"

ITER_CHUNK_SIZE = 1024 * 1024

MAX_RESPONSE_SIZE = 1000 * 1024 * 1024

UNKNOWN = "unknown"

TEXT_CHARS = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7F})

DEFAULT_404 = "gltetAc0012adddalmz/19lsjfo.html"

FOLDER_404 = "nt4ffaoxewps/ablzqqqo/eelsqqwlz"

DOT_404 = ".ADMINDDDD"

WAF_404 = '?tag="><script>alert(/test/);</script>'