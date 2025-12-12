from setuptools import setup, find_packages

setup(
    name='tsjson',  # 包名，必须唯一（检查 PyPI 是否已存在）
    version='1.0.0',    # 版本号，格式如 x.y.z
    packages=find_packages(),  # 自动发现包
    description='A simple example package',
    # long_description=open('README.md').read(),  # 从 README.md 读取
    long_description_content_type='text/markdown',
    author='Gavin',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/my_package',  # 项目主页（可选）
    classifiers=[  # 分类标签，帮助搜索
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # 支持的 Python 版本
)
