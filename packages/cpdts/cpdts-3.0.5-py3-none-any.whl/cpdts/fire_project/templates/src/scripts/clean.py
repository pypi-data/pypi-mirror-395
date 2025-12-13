import shutil
from pathlib import Path


def clean():
    """清除 uv build 生成的 dist 文件夹"""
    dist_path = Path("dist")
    if dist_path.exists():
        shutil.rmtree(dist_path)
        print(f"已删除 {dist_path} 文件夹")
    else:
        print(f"{dist_path} 文件夹不存在，无需清理")
