import re
import os
from urllib.parse import urlparse
import asyncio
import httpx
import time

from afuzz.utils.common import CaseInsensitiveDict, is_ip
from afuzz.settings import DEFAULT_HEADERS
from afuzz.lib.dictionary import Dictionary
from afuzz.settings import PHP_EXTENSIONS, ASPX_EXTENSIONS, JAVA_EXTENSIONS, COMMON_EXTENSIONS, MEDIA_EXTENSIONS, \
    BACKUP_EXTENSIONS, CONFIG_EXTENSIONS, PYTHON_EXTENSIONS, OTHER_EXTENSIONS, WS_EXTENSIONS, UNKNOWN, DATA
from afuzz.lib.response import Response
from afuzz.settings import DOT_404, DEFAULT_404, FOLDER_404, WAF_404
from afuzz.lib.result import FuzzResult
from afuzz.utils.common import compatible_path


class Fuzzer:

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self._target = options.get("target", "")
        self.depth = options.get("depth", 0)
        self.headers = CaseInsensitiveDict(DEFAULT_HEADERS)
        self.session = httpx.AsyncClient(headers=self.headers, verify=False, follow_redirects=False, timeout=60,
                                         http2=True)
        self.dict = []
        self.baddict = Dictionary(list_type="badstr")
        self.blacklist = Dictionary(list_type="blacklist")
        self.whithlist = Dictionary(list_type="whitelist")
        self.page_404 = None
        self.folder_404 = None
        self.dot_404 = None
        self.page_index = None
        self.url_parse = urlparse(self._target)
        self.targets_queue = asyncio.Queue()
        self.result_queue = asyncio.Queue()
        self.stop_flag = False
        self.result = FuzzResult(self._target, options.get("output", "result/"))
        self.waf_404 = None
        self.scanner_queue = []
        self.stop_count = 0

    async def send_msg(self, msg_type, msg_content):
        await self.result_queue.put({"type": msg_type, "content": msg_content})

    async def check_vuln(self, response, url, path, depth, target=None):
        wl_match_result, wl_match_pos, wl_match_str = self.whithlist.match(response)
        bl_match_result, bl_match_pos, bl_match_str = self.blacklist.match(response, path)
        reresult_404 = self.check_404_re(response)
        result_404 = self.check_404_page(response)

        if response.status == 400:
            return False

        if response.status == 429:
            print("The request is too fast, please reduce the number of threads.")
            return False
        # print(resp.status)
        redirect = response.redirect.strip()
        # Exclude if it jumps to the homepage of the website
        if not target:
            target = self._target

        index_url = target.replace(":443/", "/").replace(":80/", "/")
        if index_url.startswith("https://"):
            index_url_protocol = index_url.replace("https://", "http://")
        else:
            index_url_protocol = index_url.replace("http://", "https://")

        if redirect == index_url or redirect == index_url_protocol or redirect == "/":
            return False

        # If it hits the whitelist, return
        if wl_match_result:
            find_type = "whitelist"
            mark = wl_match_str
            await self.send_msg("vuln", (find_type, url, path, response, mark, depth, target))
            return True
        # Skip if hit blacklist
        # print(self.baddict.match(resp)[0])
        if self.baddict.match(response)[0] == True:
            return False

        # Determine folder path
        new_url = url.replace(":443/", "/").replace(":80/", "/")
        if new_url.startswith("https://"):
            new_url_protocol = new_url.replace("https://", "http://")
        else:
            new_url_protocol = new_url.replace("http://", "https://")

        if (not new_url.endswith("/") and (redirect == new_url + "/" or redirect == new_url_protocol + "/")) \
                or redirect == "/" + path + "/":
            print("%s 30x" % url)
            find_type = "folder"
            mark = "30x"
            await self.send_msg("vuln", (find_type, url, path, response, mark, depth, target))
            return True

        # Check blacklist content
        if bl_match_result or result_404 or reresult_404:
            return False

        if new_url[:-1] == redirect and new_url.endswith("/") and response.status != 403:
            return False

        if new_url.endswith("/") and response.status == 403 and self.folder_404.status != 403:
            print("%s 403" % url)
            find_type = "folder"
            mark = "403"
            await self.send_msg("vuln", (find_type, url, path, response, mark, depth, target))
            return True

        # all checks passed
        find_type = "check"
        mark = ""
        await self.send_msg("vuln", (find_type, url, path, response, mark, depth, target))
        return True

    async def save_result(self):
        # scan_result = FuzzResult(self._target)
        while not self.stop_flag or self.result_queue.qsize() > 0:
            if self.result_queue.qsize() == 0:
                await asyncio.sleep(0.1)
                continue

            while self.result_queue.qsize() > 0:
                msg = await self.result_queue.get()

                if msg["type"] == "msg":
                    print(msg["content"])
                else:
                    find_type, url, path, resp, mark, depth, target = msg["content"]
                    # check depth

                    if self.depth > depth + 1 and find_type == "folder":
                        print("%s (Add queue)" % url)
                        await self.produce(url, depth=depth + 1)
                        # await self.scanner_queue.put((url, depth + 1))
                    self.result.add(resp, path, find_type, mark, target=target, depth=depth)
        # print(scan_result.output())

    async def produce(self, target=None, depth=0):
        if not target:
            target = self._target

        if not target.endswith("/"):
            target = target + "/"

        if target not in self.scanner_queue:
            self.scanner_queue.append(target)
        else:
            return True

        if depth > 0:
            print(target)
        for path in self.dict:
            await self.targets_queue.put({"target": target, "path": path, "depth": depth})
        '''
        for i in range(self.options["threads"]):
            await self.targets_queue.put({"target": "stop", "path": "", "depth": depth})
        '''
        for _ in range(self.options["threads"]):
            await self.targets_queue.put({"target": "end", "path": "", "depth": depth})

    async def consume(self):
        status_50x = 0
        timeout_count = 0
        while self.targets_queue.qsize() > 0:
            target = await self.targets_queue.get()

            if target["target"] == "end" and self.depth == 0:
                # wait for task to complete
                for _ in range(2):
                    await asyncio.sleep(1)

            if status_50x > 5:
                await asyncio.sleep(0.1)
                break

            path = target["path"]
            url = target["target"] + path
            depth = target["depth"]

            if timeout_count >= 10:
                break
            for _ in range(3):
                try:
                    # read timeout

                    resp = Response(await self.session.get(url))
                    # self.processbar.update(self.process)

                    break
                except TimeoutError:
                    timeout_count += 1
                    asyncio.sleep(2)
                    continue
                except Exception as e:
                    timeout_count += 1
                    self.session = httpx.AsyncClient(headers=self.headers, verify=False, follow_redirects=False,
                                                     timeout=60, http2=True)
                    resp = None
                    continue

            if not resp:
                continue

            if resp and resp.status > 501:  # 502 and above problems are more than 5 times, then end
                status_50x += 1
                continue

            await self.check_vuln(resp, url, path, depth, target=target["target"])

    def get_exts(self, custom=None):
        if custom:
            exts = custom
        else:

            language = self.page_index.language
            if language == "aspx":
                ext = ASPX_EXTENSIONS
            elif language == "php":
                ext = PHP_EXTENSIONS
            elif language == "java":
                ext = JAVA_EXTENSIONS
            elif language == "python":
                ext = PYTHON_EXTENSIONS
            elif language == UNKNOWN:
                ext = ASPX_EXTENSIONS + PHP_EXTENSIONS + JAVA_EXTENSIONS + PYTHON_EXTENSIONS
            exts = ext + COMMON_EXTENSIONS + CONFIG_EXTENSIONS + OTHER_EXTENSIONS + WS_EXTENSIONS
        return exts

    async def start(self):
        # 1. Determine the language selection dictionary
        # 2. Get 404 page content
        # 3. Create a scanning coroutine
        # 4. Create a result display and save coroutine.
        await self.get_index()
        ext = []
        if not self.page_index:
            print("Failed to access url!")
            return True
        # result_file = open("./result/" + self.result_filename, "w", encoding='utf-8')
        language = self.page_index.language
        await self.send_msg("msg", "language: %s " % language)

        exts = self.get_exts(self.options["exts"])
        if self.url_parse.netloc:
            subdomain = self.url_parse.netloc.split(":", 1)[0]
            if is_ip(subdomain):
                subdomain = ""
        else:
            subdomain = ""

        print("Generating dictionary...")
        self.dict = Dictionary(subdomain=subdomain, extensions=exts)
        if not self.options["exts"]:
            back_dict = Dictionary(subdomain=subdomain, files=[compatible_path(DATA + "/backup.txt")],
                                   extensions=BACKUP_EXTENSIONS)
            self.dict = list(set(self.dict.items() + back_dict.items()))

        self.total = len(self.dict)
        # self.processbar = tqdm.tqdm(self.total)

        print("A total of %d entries in the dictionary" % self.total)

        print("Start getting 404 error pages")
        await self.get_404_page("file")
        await self.get_404_page("folder")
        await self.get_404_page("dot")
        await self.get_404_page("waf")

        print("Get 404 page complete")

        print("Create scan tasks")
        asyncio.create_task(self.save_result())

        try:
            asyncio.create_task(self.produce())
            all_process = [self.consume() for _ in range(self.options["threads"])]
            await asyncio.gather(*all_process)

        except KeyboardInterrupt as e:
            self.stop_flag = True
            await self.send_msg("msg", "Scan aborted by user")
            exit(-1)
        except Exception as e:
            import traceback
            traceback.print_exc()
            await self.send_msg("msg", "[__main__.exception] %s %s" % (type(e), str(e)))

        # Analyze scanned results, display and write final results after processing
        self.result.analysis()

        print(self.result.table)

        # self.result.save_table()
        self.result.save()

        self.stop_flag = True

    async def get_404_page(self, notfound_type="file"):
        # DOT_404, DEFAULT_404, FOLDER_404
        if notfound_type == "file":
            path = DEFAULT_404
        elif notfound_type == "folder":
            path = FOLDER_404
        elif notfound_type == "dot":
            path = DOT_404
        elif notfound_type == "waf":
            path = WAF_404

        try:
            page404_resp = Response(await self.session.get(self._target + path))
        except:
            page404_resp = None

        if notfound_type == "file":
            self.page_404 = page404_resp
        elif notfound_type == "folder":
            self.folder_404 = page404_resp
        elif notfound_type == "dot":
            self.dot_404 = page404_resp
        elif notfound_type == "waf":
            self.waf_404 = page404_resp

        return page404_resp

    async def get_index(self):
        try:
            index_resp = await self.session.get(self._target)
            self.page_index = Response(index_resp)
            print(self.page_index.title)
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.page_index = None
        return self.page_index
        # self.page_index = Response(await self.session.get(self._target))

    def check_404_re(self, response):
        regex = "404 (Page )*[nN]ot [fF]ound|[Ss]erver error|<title>404</title>"
        if re.findall(regex, response.content, re.I):
            return True
        else:
            return False

    def check_404_page(self, response):
        if response.status == 404:
            return True

        temp_404 = self.clean_page(self.page_404, DEFAULT_404)
        temp_page = self.clean_page(response)
        temp2_404 = self.clean_page(self.dot_404, DOT_404)
        folder_404 = self.clean_page(self.folder_404, FOLDER_404)

        if self.page_404.status == response.status and self.page_404.md5(temp_404) == response.md5(temp_page):
            return True
        elif self.dot_404.status == response.status and self.dot_404.md5(temp2_404) == response.md5(temp_page):
            return True
        elif self.folder_404.status == response.status and self.folder_404.md5(folder_404) == response.md5(temp_page):
            return True
        elif self.page_404.status == response.status and \
                self.page_404.lines == response.lines and self.page_404.title == response.title:
            return True
        elif self.folder_404.status == response.status and \
                self.folder_404.lines == response.lines and self.folder_404.title == response.title:
            return True
        elif self.dot_404.status == response.status and \
                self.dot_404.lines == response.lines and self.dot_404.title == response.title:
            return True
        elif self.waf_404.status == response.status and \
                self.waf_404.lines == response.lines and self.waf_404.title == response.title:
            return True
        elif self.page_index.status == response.status and \
                self.page_index.lines == response.lines and self.page_index.title == response.title:
            return True
        else:
            return False

    def clean_page(self, response, path=None):
        patterns = [
            r"[a-f\d]{4}(?:[a-f\d]{4}-){4}[a-f\d]{12}",
            r"[0-9]{4}[-][0-9]{1,2}[-][0-9]{1,2}.\d\d:\d\d:\d\d(\.\d+)?Z?",
            r"[0-9]{4}[-][0-9]{1,2}[-][0-9]{1,2}",
            r"[0-9]{4}[/][0-9]{1,2}[/][0-9]{1,2}",
            r"<!--.+-->"
        ]
        '''
        匹配的例子
        content = "test_ e155518c-ca1b-443c-9be9-fe90fdab7345, 41E3DAF5-6E37-4BCC-9F8E-0D9521E2AA8D, 00000000-0000-0000-0000-000000000000"
        content += "2020-10-22T07:56:07.867Z,,,,asdasdasn"
        content += "2023-01-27 10:21:39Z"
        content += "33bb81a8-f625-4d38-8502-a6c192890ad2" + aabcd1llmzn"
        content += "64d56471-807d-41d8-a331-67e38c1bbd8c"
        '''
        if response:
            content = response.content
            for pattern in patterns:
                regex = re.compile(pattern, re.I)
                content = re.sub(regex, "", content)

            if response.type == "application/json":
                regex = re.compile(r"\d{10,13}")
                content = re.sub(regex, "", content)
            url = str(response.url)
            content = content.replace(url, "")
            content = content.replace(self._target, "")

            path = urlparse(url).path
            # print(path)
            if path:
                content = content.replace(path, "")

            return content
        return ""
