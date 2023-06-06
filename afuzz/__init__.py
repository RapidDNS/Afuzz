import sys

sys.dont_write_bytecode = True

import asyncio

from afuzz.lib.cmdline import parse_args, banner
from afuzz.lib.fuzzer import Fuzzer
from afuzz.utils.common import calctime


async def run(options):
    fuzzer = Fuzzer(options)
    await fuzzer.start()


@calctime
def main():
    print(banner())
    args = parse_args()

    if args.url:
        target = args.url
        if not target.startswith("http"):
            target = "https://" + target
        if not target.endswith("/"):
            target = target + "/"
    if args.output:
        output = args.output

    if args.thread:
        threads = int(args.thread)
    else:
        threads = 10
    if args.extensions:
        exts = args.extensions.split(",")
    else:
        exts = []

    options = {"target": target, "output": output, "threads": threads, "exts": exts, "depth": int(args.depth)}
    if args.wordlist:
        options["wordlist"] = args.wordlist

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(options))
