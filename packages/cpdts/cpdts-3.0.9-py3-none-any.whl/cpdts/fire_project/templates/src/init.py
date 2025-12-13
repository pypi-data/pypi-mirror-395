

import fire 



class ENTRY(object):
    def hello(self):
        print("hello")


def main() -> None:
    try:
        fire.Fire(ENTRY)
    except KeyboardInterrupt:
        print("\n操作已取消")
        exit(0)