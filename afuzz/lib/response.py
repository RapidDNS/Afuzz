import re
import hashlib
from urllib.parse import urlparse
from afuzz.utils.mimetype import MimeTypeUtils, guess_mimetype
from afuzz.settings import DEFAULT_ENCODING, UNKNOWN, MAX_RESPONSE_SIZE, ITER_CHUNK_SIZE
from afuzz.lib.dictionary import Dictionary
from afuzz.utils.common import CaseInsensitiveDict

class Response:
    def __init__(self, response):
        self.url = response.url
        self.status = response.status_code
        self.headers = CaseInsensitiveDict(response.headers)
        self.redirect = self.headers.get("location") or ""
        self.history = [res.url for res in response.history]
        self.content = ""
        self.body = response.content
        self.text = response.text
        self.title = self.page_title()

        if not MimeTypeUtils.is_binary(self.body):
            self.content = self.body.decode(
                response.encoding or DEFAULT_ENCODING, errors="ignore"
            )

        lang_dict = Dictionary(list_type="language")
        result, language, match_str = lang_dict.match(response)
        if result:
            self.language = language
        else:
            self.language = UNKNOWN

    def page_title(self):
        tt = re.search("<title.*?>(.*?)</title>", self.content, re.IGNORECASE | re.DOTALL)
        try:
            page_title = tt.group(1)
        except Exception:
            return ''
        if page_title:
            return page_title.strip()

    @property
    def raw_header(self):
        header = []
        header = ["%s: %s" % (key, value) for key, value in self.headers.items()]
        return "\n".join(header)

    @property
    def type(self):
        if "content-type" in self.headers:
            return self.headers.get("content-type").split(";")[0]
        body_type = guess_mimetype(self.body)
        if body_type != "text/plain":
            return body_type
        return UNKNOWN

    @property
    def length(self):
        try:
            print(self.headers.get("content-length"))
            print(int(self.headers.get("content-length")))
            l = int(self.headers.get("content-length"))
            #print(l)
        except TypeError:
            l = len(self.body)
            #print("typeerror")
            #print(l)

        return l

    @property
    def lines(self):
        body_line = len(self.content.split("\n"))
        if body_line < 1:
            body_line2 = len(self.content.split("\r"))
            return body_line2
        else:
            return body_line


    def md5(self, content=None):
        m = hashlib.md5()
        if content:
            m.update(content.encode())
        else:
            m.update(self.body)
        return m.hexdigest()

    @property
    def words(self):
        regex = re.compile(r"\S+", re.I+re.DOTALL)
        return len(regex.findall(self.content))


    def clean_page(self, path=None):
        patterns = [
            r"[a-f\d]{4}(?:[a-f\d]{4}-){4}[a-f\d]{12}",
            r"[0-9]{4}[-][0-9]{1,2}[-][0-9]{1,2}.\d\d:\d\d:\d\d(\.\d+)?Z?",
            r"[0-9]{4}[-][0-9]{1,2}[-][0-9]{1,2}",
            r"[0-9]{4}[/][0-9]{1,2}[/][0-9]{1,2}",
            r"<!--.+-->"
        ]
        '''
        examples
        content = "test_ e155518c-ca1b-443c-9be9-fe90fdab7345, 41E3DAF5-6E37-4BCC-9F8E-0D9521E2AA8D, 00000000-0000-0000-0000-000000000000"
        content += "2020-10-22T07:56:07.867Z,,,,asdasdasn"
        content += "2023-01-27 10:21:39Z"
        content += "33bb81a8-f625-4d38-8502-a6c192890ad2" + aabcd1llmzn"
        content += "64d56471-807d-41d8-a331-67e38c1bbd8c"
        '''

        content = self.content
        if "application/" in self.type and "application/json" not in self.type:
            return content
        for pattern in patterns:
            regex = re.compile(pattern, re.I)
            content = re.sub(regex, "", content)

        if self.type == "application/json":
            regex = re.compile(r"\d{10,13}")
            content = re.sub(regex, "", content)

        url = str(self.url)
        content = content.replace(url, "")

        path = urlparse(url).path
        if path:
            content = content.replace(path, "")

        return content
