import subprocess
from pathlib import Path
import pyperclip
import toml


def public():
    """执行 uv publish 发布包到 PyPI"""
    try:
        # 检查 dist 目录
        dist_path = Path("dist")
        if not dist_path.exists():
            print("错误: dist 目录不存在，请先执行构建")
            raise FileNotFoundError("dist 目录不存在")
        
        # 列出待发布的文件
        wheel_files = list(dist_path.glob("*.whl"))
        if not wheel_files:
            print("错误: dist 目录中没有找到 wheel 文件")
            raise FileNotFoundError("没有找到 wheel 文件")
        
        print("=" * 60)
        print("开始发布包到 PyPI")
        print("=" * 60)
        print(f"发布目录: {dist_path.absolute()}")
        print("待发布文件:")
        for whl in wheel_files:
            print(f"  - {whl.name} ({whl.stat().st_size / 1024:.2f} KB)")
        print("-" * 60)
        
        # 执行发布
        result = subprocess.run(
            ["uv", "publish"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("=" * 60)
            print("✓ 发布成功!")
            print("=" * 60)
            if result.stdout:
                print(result.stdout)
            
            # 读取包名
            try:
                with open("pyproject.toml", "r", encoding="utf-8") as f:
                    config = toml.load(f)
                    package_name = config.get("project", {}).get("name", "")
                
                if package_name:
                    install_cmd = f"uv tool install {package_name} -U"
                    # 复制到剪贴板
                    pyperclip.copy(install_cmd)
                    print("\n" + "=" * 60)
                    print("📦 安装命令:")
                    print(f"   {install_cmd}")
                    print("\n✓ 命令已复制到剪贴板!")
                    print("=" * 60)
            except Exception as e:
                print(f"\n提示: {e}")
                print("   uv tool install xxx -U")
        else:
            print("=" * 60)
            print("✗ 发布失败!")
            print("=" * 60)
            if result.stderr:
                print(result.stderr)
            if result.stdout:
                print(result.stdout)
            raise RuntimeError(f"发布失败: {result.stderr}")
            
    except FileNotFoundError as e:
        if "uv" in str(e) or "找不到" in str(e):
            print("错误: 找不到 uv 命令，请确保已安装 uv")
        raise
    except Exception as e:
        print(f"发生错误: {e}")
        raise