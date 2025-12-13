
from pathlib import Path
from ..utils import create_file_with_path
import re
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyCompleter, WordCompleter
from prompt_toolkit.validation import Validator, ValidationError


class ProjectNameValidator(Validator):
    """验证Python项目名称是否合法"""
    def validate(self, document):
        text = document.text.strip()
        if not text:
            raise ValidationError(
                message='项目名称不能为空',
                cursor_position=len(document.text)
            )
        # 检查是否符合Python包命名规范（PEP 8）：只能包含小写字母、数字和下划线，且不能以数字开头
        if not re.match(r'^[a-z_][a-z0-9_]*$', text):
            raise ValidationError(
                message='项目名称只能包含小写字母、数字和下划线，且不能以数字开头',
                cursor_position=len(document.text)
            )


class YesNoValidator(Validator):
    """验证输入是否为 yes/no 或 y/n"""
    def validate(self, document):
        text = document.text.lower().strip()
        if text not in ['yes', 'no', 'y', 'n']:
            raise ValidationError(
                message='请输入 yes/no 或 y/n',
                cursor_position=len(document.text)
            )


class PythonVersionValidator(Validator):
    """验证Python版本是否在支持的版本列表中"""
    def __init__(self, valid_versions):
        self.valid_versions = valid_versions
    
    def validate(self, document):
        text = document.text.strip()
        if not text:
            raise ValidationError(
                message='Python版本不能为空',
                cursor_position=len(document.text)
            )
        if text not in self.valid_versions:
            raise ValidationError(
                message=f'请选择有效的Python版本: {", ".join(self.valid_versions)}',
                cursor_position=len(document.text)
            )


def fire_create():
    # 获取当前模块文件的目录

    project_name = prompt(
        "请输入Python项目名称: ",
        validator=ProjectNameValidator(),
        validate_while_typing=False
    ).strip()

    # 使用 FuzzyCompleter 让用户选择 Python版本
    python_versions = ['3.8', '3.9', '3.10', '3.11', '3.12', '3.13', '3.14', '3.14t']
    python_version_completer = FuzzyCompleter(
        WordCompleter(python_versions, ignore_case=True)
    )
    python_version = prompt(
        "请选择Python版本 (支持模糊搜索TAB补全): ",
        completer=python_version_completer,
        validator=PythonVersionValidator(python_versions),
        validate_while_typing=False,
        default='3.13'
    ).strip()
    
    # 使用 prompt_toolkit 的 FuzzyCompleter 询问 yes/no
    yes_no_completer = FuzzyCompleter(
        WordCompleter(['yes', 'no'], ignore_case=True)
    )
    
    pypi_check_answer = prompt(
        "是否进行PYPI项目名称检查 (yes/no): ",
        completer=yes_no_completer,
        validator=YesNoValidator(),
        validate_while_typing=False
    ).lower().strip()
    
    pypi_name_check = pypi_check_answer in ['yes', 'y']
    # 如果用户同意检查项目名字冲突 则执行检查操作 直到通过为止 
    
    if pypi_name_check:
        try:
            while True: 
                if not check_pypi_package_name(project_name):
                    break 
                else:
                    print("包名已存在，请重新输入")
                    project_name = prompt(
                        "请输入项目名称: ",
                        validator=ProjectNameValidator(),
                        validate_while_typing=False
                    ).strip()
                    continue
        except :
            return
    
    creat_process(project_name,python_version)

def check_pypi_package_name(package_name):
    # 检查当前 package_name 是否已经存在于 PyPI 上
    import requests
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=10)
        if response.status_code == 200:
            print("包名已存在，不可以使用")
            return True  # 包名已存在
        elif response.status_code == 404:
            print("包名不存在，可以正常使用")
            # print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            # 虽然能够检查到 包名是不是已经存在了 但是仍然无法判断这个包名能不能用 真的头痛

            return False  # 包名不存在，可以使用
        else:
            print(f"检查包名时出现异常状态码: {response.status_code}")
            return None  # 检查失败
    except requests.exceptions.RequestException as e:
        print(f"检查包名时网络请求失败: {e}")
        return None  # 检查失败



def creat_process(project_name,python_version):
    current_dir = Path(__file__).parent

    items = {
        ".vscode/settings.json":{
            "template": "templates/vscode/settings.json",
        },
        ".vscode/extensions.json":{
            "template": "templates/vscode/extensions.json",
        },
        ".kiro/hooks/auto-init-imports.kiro.hook":{
            "template": "templates/kiro/auto-init-imports.kiro.hook",
        },
        ".kiro/hooks/optimize-docstring-format.kiro.hook":{
            "template": "templates/kiro/optimize-docstring-format.kiro.hook",
        },
        ".kiro/hooks/generate-code-from-comments.kiro.hook":{
            "template": "templates\\kiro\\generate-code-from-comments.kiro.hook",
        },
        ".kiro/steering/main.md":{
            "template": "templates/kiro/main.md",
        },
        f"src/{project_name}/__init__.py":{
            "template": "templates/src/init.py",
        },
        f"src/{project_name}/decorators/singleton.py":{
            "template": "templates/src/decorators/singleton.py",
        },
        f"src/scripts/clean.py":{
            "template":"templates/src/scripts/clean.py"
        },
        f"src/scripts/build.py":{
            "template":"templates/src/scripts/build.py"
        },
        f"src/scripts/public.py":{
            "template":"templates/src/scripts/public.py"
        },
        f"src/scripts/ccx.py":{
            "template":"templates/src/scripts/ccx.py"
        },

        # f"scripts/build_and_publish.py":{
        #     "template": "templates/scripts/build_and_publish.py",
        # },
        "pyproject.toml":{
            "template": "templates/pyproject.toml.j2",
            "data": {
                "project_name": project_name,
                "python_version": python_version
            }
        },
        ".gitignore":{
            "template": "templates/.gitignore",
        },
        "README.md":{
            "template": "templates/README.md",
        }
    }


    for item in items:
        template = items[item]["template"]
        data = items[item].get("data", {})
        create_file_with_path(f'{project_name}/{item}', f"{current_dir}/{template}", data)

    pass