import os
import sys
import argparse
from asciistuff import Banner


def banner():
    return Banner("AFUZZ")


def parse_args():
    parser = argparse.ArgumentParser(prog='Afuzz',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description='An Automated Web Path Fuzzing Tool.\nBy RapidDNS (https://rapiddns.io)',
                                     usage='afuzz [options]')

    parser.add_argument('-u', '--url', help="Target URL", default="", required=True)
    parser.add_argument('-o', '--output', help='Output file', default="result/result", required=False)
    parser.add_argument('-e', '--extensions', help="Extension list separated by commas (Example: php,aspx,jsp)",
                        default=False, required=False)
    parser.add_argument('-t', '--thread', help='Number of threads', default=10)
    parser.add_argument('-d', '--depth', help='Maximum recursion depth', default=0)
    parser.add_argument('-w', '--wordlist', help='wordlist', required=False, default=None)
    parser.add_argument('-f', '--fullpath', help='fullpath', action='store_true')
    parser.add_argument('-p', '--proxy', help='proxy, (ex:http://127.0.0.1:8080)', required=False, default=None)

    if len(sys.argv) == 1:
        sys.argv.append('-h')

    args = parser.parse_args()

    return args
