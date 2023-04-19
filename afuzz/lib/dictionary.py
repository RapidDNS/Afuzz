import re
import tldextract

from afuzz.settings import CONFIG_EXTENSIONS, COMMON_EXTENSIONS, JAVA_EXTENSIONS, PHP_EXTENSIONS, ASPX_EXTENSIONS, \
    BACKUP_EXTENSIONS, OTHER_EXTENSIONS
from afuzz.utils.common import CaseInsensitiveDict, compatible_path

from afuzz.settings import DATA


class Dictionary:
    def __init__(self, **kwargs):
        self._index = 0
        self._items = self.generate(**kwargs)
        self.type = kwargs.get("list_type", None)
    @property
    def index(self):
        return self._index

    def __next__(self):
        try:
            path = self._items[self._index]
        except IndexError:
            raise StopIteration

        self._index += 1

        return path

    def __contains__(self, item):
        return item in self._items

    def __getstate__(self):
        return (self._items, self._index)

    def __setstate__(self, state):
        self._items, self._index = state

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def __add__(self, other):
        new_items = self._items + other._items
        return self.__class__(list_type="add", items=new_items)

    def items(self):
        return self._items

    def read_list(self, filename):
        result_list = []
        with open(filename, "r", encoding="utf-8") as list_file:
            for line in list_file:
                line = line.strip()
                if line and "==" in line:
                    key, value = line.split("==", 1)
                    result_list.append((key, value))
        return result_list

    def generate(self, subdomain="", files=[], extensions=[], list_type="path",items=[]):
        wordlist = []
        if list_type == "add":
            wordlist = list(set(items))
            return wordlist
        if not files and list_type == "path":
            for name in ["dict.txt"]:
                files.append(compatible_path(DATA + "/" + name))

        #files = [DATA + "/api.txt"]

        if list_type == "path":
            tld_res = tldextract.extract(subdomain)
            domain = tld_res.domain
            root_domain = domain + "." + tld_res.suffix
            sub = subdomain.rstrip(root_domain)
            subs = []

            if "." in sub:
                subnames = sub.split(".")
                for subname in subnames:
                    if "-" in subname:
                        for temp in subname.split("-"):
                            if temp not in subs:
                                subs.append(temp)
                    else:
                        subs.append(subname)
                sub_all = "".join(subs)
                sub_all_a = "-".join(subs)
                sub_all_b = "_".join(subs)
                subs.append(sub_all)
                subs.append(sub_all_a)
                subs.append(sub_all_b)
            if sub not in subs:
                subs.append(sub)

            new_wordlist = []
            for filename in files:
                with open(filename, "r", encoding="utf=8") as dict_file:
                    for line in dict_file:
                        line = line.strip()
                        temp_list = []
                        if "%subdomain%" in line and subdomain:
                            temp_list.append(line.replace("%subdomain%", subdomain))
                        elif "%domain%" in line and domain:
                            temp_list.append(line.replace("%domain%", domain))
                        elif "%rootdomain%" in line and root_domain:
                            temp_list.append(line.replace("%rootdomain%", root_domain))
                        elif "%sub%" in line and subs:
                            for subname in subs:
                                temp_list.append(line.replace("%sub%", subname))
                        else:
                            temp_list.append(line)
                        for temp in temp_list:
                            if temp not in new_wordlist:
                                new_wordlist.append(temp)

            for line in new_wordlist:
                if "%ext%" in line or "%EXT%" in line:
                    for ext in extensions:
                        dict_text = line.replace("%ext%".upper(), ext)
                        dict_text = dict_text.replace("%ext%", ext)
                        if dict_text not in wordlist:
                            wordlist.append(dict_text)
                elif line not in wordlist:
                    wordlist.append(line)

        elif list_type == "badstr":
            filepath = compatible_path(DATA + "/bad_strings.txt")
        elif list_type == "whitelist":
            filepath = compatible_path(DATA + "/whitelist.txt")
        elif list_type == "blacklist":
            filepath = compatible_path(DATA + "/blacklist.txt")
        elif list_type == "language":
            filepath = compatible_path(DATA + "/language.txt")

        if list_type != "path":
            wordlist = self.read_list(filepath)

        return wordlist

    def match(self, response, path=None):
        ret = (False, None, None)
        headers = CaseInsensitiveDict(response.headers)
        for pos, match_str in self._items:
            pos = pos.lower()
            match_str = match_str.lower()
            if self.type != "language":
                if response.page_title():
                    title = response.page_title().lower()
                else:
                    title = ""
            else:
                title = ""
            content = response.content.lower()
            if pos == "title":
                if match_str in title or match_str == title:
                    ret = (True, pos, match_str)
            elif pos == "body":
                if match_str in content:
                    ret = (True, pos, match_str)
            elif pos == "regex":
                regex = re.compile(match_str, re.I)
                match = regex.match(str(headers).lower() + content)
                if match:
                    ret = (True, pos, match_str)
            elif pos in ["400", "403", "500"]:
                if match_str == path:
                    ret = (True, pos, match_str)
            elif pos == "header":
                for _, value in headers.items():
                    if match_str.lower() in value.lower():
                        ret = (True, pos, match_str)
            elif pos == "cookie":
                if match_str in str(response.cookie).lower():
                    ret = (True, pos, match_str)
            elif pos in ["php", "aspx", "java", "python"]:
                for _, value in headers.items():
                    if match_str in value.lower():
                        ret = (True, pos, match_str)
                #if match_str in response.body:
                #    ret = (True, pos)

        return ret
