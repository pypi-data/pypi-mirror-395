

import fire
from pathlib import Path
from cookiecutter.main import cookiecutter


def create():
    """调用 cookiecutter 模板创建 Django 项目"""
    # 获取模板路径(相对于当前文件的位置)
    template_path = Path(__file__).parent / "cookiecutter-django-main"
    
    # 确保模板路径存在
    if not template_path.exists():
        print(f"错误: 模板路径不存在: {template_path}")
        return
    
    # 调用 cookiecutter 生成项目
    try:
        cookiecutter(str(template_path))
        print("项目创建成功!")
    except Exception as e:
        print(f"创建项目时出错: {e}")

def main() -> None:
    try:
        fire.Fire(create)
    except KeyboardInterrupt:
        print("\n操作已取消")
        exit(0)