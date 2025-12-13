

import os
from pathlib import Path
from cookiecutter.main import cookiecutter
import fire


def create(output_dir: str = "."):
    """
    使用 cookiecutter 生成 Django 项目
    
    参数:
        output_dir: 项目输出目录,默认为当前目录
    """
    # 获取模板路径(相对于当前文件)
    template_path = Path(__file__).parent / "cookiecutter-django-main"
    
    # 确保模板路径存在
    if not template_path.exists():
        print(f"错误: 模板路径不存在 {template_path}")
        return
    
    # 转换为绝对路径
    template_path = template_path.resolve()
    output_dir = Path(output_dir).resolve()
    
    print(f"正在使用模板: {template_path}")
    print(f"输出目录: {output_dir}")
    
    try:
        # 调用 cookiecutter 生成项目
        project_path = cookiecutter(
            str(template_path),
            output_dir=str(output_dir)
        )
        print(f"\n✓ 项目创建成功: {project_path}")
    except Exception as e:
        print(f"\n✗ 项目创建失败: {e}")

def main() -> None:
    try:
        fire.Fire(create)
    except KeyboardInterrupt:
        print("\n操作已取消")
        exit(0)