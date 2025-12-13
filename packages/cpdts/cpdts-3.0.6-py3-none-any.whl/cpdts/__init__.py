

import fire 
from .fire_project import fire_create 



class ENTRY(object):
    
    def fire(self) -> None:
        """快速 创建 fire项目"""
        fire_create()
    
def main() -> None:
    try:
        fire.Fire(ENTRY)
    except KeyboardInterrupt:
        print("\n操作已取消")
        exit(0)

