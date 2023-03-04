Afuzz - An automated web path fuzzing tool
=======

Afuzz is an automated web path fuzzing tool for the Bug Bounty projects.

![Build](https://img.shields.io/badge/Built%20with-Python-Blue)
![Release](https://img.shields.io/github/release/rapiddns/afuzz.svg)
![Stars](https://img.shields.io/github/stars/rapiddns/afuzz.svg)
<a href="https://twitter.com/intent/tweet?text=afuzz-Afuzz is an automated web path fuzzing tool for the Bug Bounty projects.%20by%20@Rapiddns%0A%0Ahttps://github.com/rapiddns/afuzz">
    ![Tweet](https://img.shields.io/twitter/url?url=https%3A%2F%2Fgithub.com%2Frapiddns%2Fafuzz)
</a>

**Afuzz** is being actively developed by [@rapiddns](https://twitter.com/rapiddns)

## Features
- Afuzz automatically detects the development language used by the website, and generates extensions according to the language
- Uses blacklist to filter invalid pages
- Uses whitelist to find content that bug bounty hunters are interested in in the page
- filters random content in the page
- judges 404 error pages in multiple ways
- perform statistical analysis on the results after scanning to obtain the final result.

Installation
------------
```
git clone https://github.com/rapiddns/Afuzz.git
cd Afuzz
python setup.py install
```

OR 
```
pip install afuzz
```

Run
------------

```
afuzz -u http://testphp.vulnweb.com -t 30
```

Result
------------

Table
```
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                                                                                    http://testphp.vulnweb.com/                                                                                    |
+-----------------------------+---------------------+--------+-----------------------------------+-----------------------+--------+--------------------------+-------+-------+-----------+----------+
|            target           |         path        | status |              redirect             |         title         | length |       content-type       | lines | words |    type   |   mark   |
+-----------------------------+---------------------+--------+-----------------------------------+-----------------------+--------+--------------------------+-------+-------+-----------+----------+
| http://testphp.vulnweb.com/ | .idea/workspace.xml |  200   |                                   |                       | 12437  |         text/xml         |  217  |  774  |   check   |          |
| http://testphp.vulnweb.com/ |        admin        |  301   | http://testphp.vulnweb.com/admin/ | 301 Moved Permanently |  169   |        text/html         |   8   |   11  |   folder  |   30x    |
| http://testphp.vulnweb.com/ |      login.php      |  200   |                                   |       login page      |  5009  |        text/html         |  120  |  432  |   check   |          |
| http://testphp.vulnweb.com/ |     .idea/.name     |  200   |                                   |                       |   6    | application/octet-stream |   1   |   1   |   check   |          |
| http://testphp.vulnweb.com/ |    .idea/vcs.xml    |  200   |                                   |                       |  173   |         text/xml         |   8   |   13  |   check   |          |
| http://testphp.vulnweb.com/ |        .idea/       |  200   |                                   |    Index of /.idea/   |  937   |        text/html         |   14  |   46  | whitelist | index of |
| http://testphp.vulnweb.com/ |       cgi-bin/      |  403   |                                   |     403 Forbidden     |  276   |        text/html         |   10  |   28  |   folder  |   403    |
| http://testphp.vulnweb.com/ | .idea/encodings.xml |  200   |                                   |                       |  171   |         text/xml         |   6   |   11  |   check   |          |
| http://testphp.vulnweb.com/ |      search.php     |  200   |                                   |         search        |  4218  |        text/html         |  104  |  364  |   check   |          |
| http://testphp.vulnweb.com/ |     product.php     |  200   |                                   |    picture details    |  4576  |        text/html         |  111  |  377  |   check   |          |
| http://testphp.vulnweb.com/ |        admin/       |  200   |                                   |    Index of /admin/   |  248   |        text/html         |   8   |   16  | whitelist | index of |
| http://testphp.vulnweb.com/ |        .idea        |  301   | http://testphp.vulnweb.com/.idea/ | 301 Moved Permanently |  169   |        text/html         |   8   |   11  |   folder  |   30x    |
+-----------------------------+---------------------+--------+-----------------------------------+-----------------------+--------+--------------------------+-------+-------+-----------+----------+```
```

Json
```Json
{
    "result": [
        {
            "target": "http://testphp.vulnweb.com/",
            "path": ".idea/workspace.xml",
            "status": 200,
            "redirect": "",
            "title": "",
            "length": 12437,
            "content_type": "text/xml",
            "lines": 217,
            "words": 774,
            "type": "check",
            "mark": "",
            "subdomain": "testphp.vulnweb.com",
            "depth": 0,
            "url": "http://testphp.vulnweb.com/.idea/workspace.xml"
        },
        {
            "target": "http://testphp.vulnweb.com/",
            "path": "admin",
            "status": 301,
            "redirect": "http://testphp.vulnweb.com/admin/",
            "title": "301 Moved Permanently",
            "length": 169,
            "content_type": "text/html",
            "lines": 8,
            "words": 11,
            "type": "folder",
            "mark": "30x",
            "subdomain": "testphp.vulnweb.com",
            "depth": 0,
            "url": "http://testphp.vulnweb.com/admin"
        },
        {
            "target": "http://testphp.vulnweb.com/",
            "path": "login.php",
            "status": 200,
            "redirect": "",
            "title": "login page",
            "length": 5009,
            "content_type": "text/html",
            "lines": 120,
            "words": 432,
            "type": "check",
            "mark": "",
            "subdomain": "testphp.vulnweb.com",
            "depth": 0,
            "url": "http://testphp.vulnweb.com/login.php"
        },
        {
            "target": "http://testphp.vulnweb.com/",
            "path": ".idea/.name",
            "status": 200,
            "redirect": "",
            "title": "",
            "length": 6,
            "content_type": "application/octet-stream",
            "lines": 1,
            "words": 1,
            "type": "check",
            "mark": "",
            "subdomain": "testphp.vulnweb.com",
            "depth": 0,
            "url": "http://testphp.vulnweb.com/.idea/.name"
        },
        {
            "target": "http://testphp.vulnweb.com/",
            "path": ".idea/vcs.xml",
            "status": 200,
            "redirect": "",
            "title": "",
            "length": 173,
            "content_type": "text/xml",
            "lines": 8,
            "words": 13,
            "type": "check",
            "mark": "",
            "subdomain": "testphp.vulnweb.com",
            "depth": 0,
            "url": "http://testphp.vulnweb.com/.idea/vcs.xml"
        },
        {
            "target": "http://testphp.vulnweb.com/",
            "path": ".idea/",
            "status": 200,
            "redirect": "",
            "title": "Index of /.idea/",
            "length": 937,
            "content_type": "text/html",
            "lines": 14,
            "words": 46,
            "type": "whitelist",
            "mark": "index of",
            "subdomain": "testphp.vulnweb.com",
            "depth": 0,
            "url": "http://testphp.vulnweb.com/.idea/"
        },
        {
            "target": "http://testphp.vulnweb.com/",
            "path": "cgi-bin/",
            "status": 403,
            "redirect": "",
            "title": "403 Forbidden",
            "length": 276,
            "content_type": "text/html",
            "lines": 10,
            "words": 28,
            "type": "folder",
            "mark": "403",
            "subdomain": "testphp.vulnweb.com",
            "depth": 0,
            "url": "http://testphp.vulnweb.com/cgi-bin/"
        },
        {
            "target": "http://testphp.vulnweb.com/",
            "path": ".idea/encodings.xml",
            "status": 200,
            "redirect": "",
            "title": "",
            "length": 171,
            "content_type": "text/xml",
            "lines": 6,
            "words": 11,
            "type": "check",
            "mark": "",
            "subdomain": "testphp.vulnweb.com",
            "depth": 0,
            "url": "http://testphp.vulnweb.com/.idea/encodings.xml"
        },
        {
            "target": "http://testphp.vulnweb.com/",
            "path": "search.php",
            "status": 200,
            "redirect": "",
            "title": "search",
            "length": 4218,
            "content_type": "text/html",
            "lines": 104,
            "words": 364,
            "type": "check",
            "mark": "",
            "subdomain": "testphp.vulnweb.com",
            "depth": 0,
            "url": "http://testphp.vulnweb.com/search.php"
        },
        {
            "target": "http://testphp.vulnweb.com/",
            "path": "product.php",
            "status": 200,
            "redirect": "",
            "title": "picture details",
            "length": 4576,
            "content_type": "text/html",
            "lines": 111,
            "words": 377,
            "type": "check",
            "mark": "",
            "subdomain": "testphp.vulnweb.com",
            "depth": 0,
            "url": "http://testphp.vulnweb.com/product.php"
        },
        {
            "target": "http://testphp.vulnweb.com/",
            "path": "admin/",
            "status": 200,
            "redirect": "",
            "title": "Index of /admin/",
            "length": 248,
            "content_type": "text/html",
            "lines": 8,
            "words": 16,
            "type": "whitelist",
            "mark": "index of",
            "subdomain": "testphp.vulnweb.com",
            "depth": 0,
            "url": "http://testphp.vulnweb.com/admin/"
        },
        {
            "target": "http://testphp.vulnweb.com/",
            "path": ".idea",
            "status": 301,
            "redirect": "http://testphp.vulnweb.com/.idea/",
            "title": "301 Moved Permanently",
            "length": 169,
            "content_type": "text/html",
            "lines": 8,
            "words": 11,
            "type": "folder",
            "mark": "30x",
            "subdomain": "testphp.vulnweb.com",
            "depth": 0,
            "url": "http://testphp.vulnweb.com/.idea"
        }
    ],
    "total": 12,
    "target": "http://testphp.vulnweb.com/"
}
```

Wordlists (IMPORTANT)
---------------
**Summary:**
  - Wordlist is a text file, each line is a path.
  - About extensions, Afuzz replaces the `%EXT%` keyword with extensions from **-e** flag.If no flag -e, the default is used.
  - Generate a dictionary based on domain names. Afuzz replaces %subdomain% with host, %rootdomain% with root domain, %sub% with subdomain, and %domain% with domain. And generated according to %ext%
 
**Examples:**

- Normal extensions
```
index.%EXT%
```

Passing **asp** and **aspx** extensions will generate the following dictionary:

```
index
index.asp
index.aspx
```

- host

```
%subdomain%.%ext%
%sub%.bak
%domain%.zip
%rootdomain%.zip
```

Passing **https://test-www.hackerone.com** and **php** extension will genrate the following dictionary:

```
test-www.hackerone.com.php
test-www.zip
test.zip
www.zip
testwww.zip
hackerone.zip
hackerone.com.zip
```

Options
-------

```
  ##   ##### ##  # #### ####
 # ##   ##   ##  #   ##   ##
 ####   #### ##  #  ##   ##
 # ##   ##   ##  # ##   ##
## ### ####   ###  #### ####

usage: afuzz [options]

An Automated Web Path Fuzzing Tool.
By RapidDNS (https://rapiddns.io)

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Target URL
  -o OUTPUT, --output OUTPUT
                        Output file
  -e EXTENSIONS, --extensions EXTENSIONS
                        Extension list separated by commas (Example: php,aspx,jsp)
  -t THREAD, --thread THREAD
                        Number of threads
  -d DEPTH, --depth DEPTH
                        Maximum recursion depth
```

How to use
---------------

Some examples for how to use dirsearch - those are the most common arguments. If you need all, just use the **-h** argument.

### Simple usage
```
afuzz -u https://target
```

```
afuzz -e php,html,js,json -u https://target
```

```
afuzz -e php,html,js -u https://target -d 3
```

### Threads
The thread number (**-t | --threads**) reflects the number of separated brute force processes. And so the bigger the thread number is, the faster afuzz runs. By default, the number of threads is 10, but you can increase it if you want to speed up the progress.

In spite of that, the speed still depends a lot on the response time of the server. And as a warning, we advise you to keep the threads number not too big because it can cause DoS.

```
afuzz -e aspx,jsp,php,htm,js,bak,zip,txt,xml -u https://target -t 50
```

----
### Blacklist
The **blacklist.txt** and **bad_string.txt** files in the /db directory are blacklists, which can filter some pages

The **blacklist.txt** file is the same as dirsearch. 

The **bad_stirng.txt** file is a text file, one per line. The format is position==content. With == as the separator, position has the following options: header, body, regex, title

----
### Language detection

The **language.txt** is the detection language rule, the format is consistent with **bad_string.txt**. Development language detection for website usage.


References
---------------
Thanks to open source projects for inspiration

- [Dirsearch](ttps://github.com/maurosoria/dirsearch) by by Shubham Sharma
- [wfuzz](https://github.com/xmendez/wfuzz) by Xavi Mendez
- [arjun](https://github.com/s0md3v/Arjun) by Somdev Sangwan
