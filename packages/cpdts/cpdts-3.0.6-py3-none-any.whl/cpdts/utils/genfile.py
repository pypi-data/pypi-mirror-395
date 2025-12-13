from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Template, TemplateError


def create_file_with_path(
    relative_path: str,
    template_path: str,
    data: Optional[Dict[str, Any]] = None
) -> Path:
    """
    根据模板创建文件，自动创建所需的目录结构
    
    Args:
        relative_path: 目标文件的相对路径
        template_path: Jinja2 模板文件路径
        data: 传递给模板的数据字典
        
    Returns:
        Path: 创建的文件路径对象
        
    Raises:
        FileNotFoundError: 模板文件不存在
        TemplateError: 模板渲染失败
        IOError: 文件写入失败
    """
    if data is None:
        data = {}
    
    # 使用 Path 对象处理路径
    target_path = Path(relative_path)
    template_file = Path(template_path)
    
    # 验证模板文件存在
    if not template_file.exists():
        raise FileNotFoundError(f"模板文件不存在: {template_path}")
    
    # 创建目标目录
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 读取并渲染模板
    try:
        template_content = template_file.read_text(encoding='utf-8')
        template = Template(template_content)
        rendered_content = template.render(data)
    except TemplateError as e:
        raise TemplateError(f"模板渲染失败: {e}")
    
    # 写入文件
    target_path.write_text(rendered_content, encoding='utf-8')
    
    return target_path
    


# print(os.path.split("/test/test/1.txt"))
# print(os.path.split("/test/testdir/"))