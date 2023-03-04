import sys
sys.dont_write_bytecode = True

from afuzz import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
