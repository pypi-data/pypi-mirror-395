# coding=utf-8
import setuptools  # 导入setuptools打包工具
from pathlib import Path

def parse_requirements(filename):
    """使用 packaging 包安全地解析 requirements.txt"""
    try:
        from packaging.requirements import Requirement
    except ImportError:
        # 回退方案：如果packaging不可用，尝试简单处理
        return simple_parse_requirements(filename)

    requirements = []
    file_path = Path(filename)

    if not file_path.exists():
        return requirements

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 跳过空行和注释
            if not line or line.startswith('#'):
                continue
            try:
                # 使用packaging验证并规范化需求字符串
                req = Requirement(line)
                requirements.append(str(req))
            except Exception:
                # 如果解析失败，回退到原始行
                requirements.append(line)

    return requirements


def simple_parse_requirements(filename):
    """简化的解析器，作为回退方案"""
    file_path = Path(filename)
    if not file_path.exists():
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        return [
            line.strip() for line in f
            if line.strip() and not line.startswith('#')
        ]


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easy_use_tools",  # Your tool name
    version="1.0.6",  # tool version, you need confirm the every release version is unique
    author="yuanyang.li",  # author name
    author_email="yuanyang.edison.li@gmail.com",  # author email
    description="An easy use tools package",  # tool description
    long_description=long_description,  # the README.md
    long_description_content_type="text/markdown",
    url="https://github.com/XXX",  # github url
    license_files=['LICENSE'],
    packages=setuptools.find_packages(),
    # 依赖管理
    install_requires=parse_requirements('requirements'),
    # install_requires=[
    #     "requests >= 2.25.1",  # set target version
    #     "shortuuid",  # not version  require
    #     "PyYAML >= 5.4.1",
    # ],

    entry_points={
        "console_scripts" : ['show_info = easy_use_tools.manage:run']
    }, # after installation,type 'show_info' in cmd line,will call run function in 'easy_use_tools.manage.py',format:'cmd=package.module:function'
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',  # python version requirement
)