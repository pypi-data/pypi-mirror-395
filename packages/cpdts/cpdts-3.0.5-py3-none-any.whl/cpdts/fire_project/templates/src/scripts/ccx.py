
import sys
from .build import build
from .clean import clean
from .public import public 



def ccx():
    """依次执行 clean、build 和 public 操作"""
    try:
        clean()
    except Exception as e:
        print(f"错误: clean 函数产生异常 - {e}")
        sys.exit(1)
    
    try:
        build()
    except Exception as e:
        print(f"错误: build 函数产生异常 - {e}")
        sys.exit(1)
    
    try:
        public()
    except Exception as e:
        print(f"错误: public 函数产生异常 - {e}")
        sys.exit(1)
