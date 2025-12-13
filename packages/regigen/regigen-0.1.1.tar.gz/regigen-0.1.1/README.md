rotation_utils_package/
├── rotation_utils/        # 实际的 Python 模块
│   ├── __init__.py        # 导入类和函数
│   └── geometry.py        # 包含核心代码的模块
├── pyproject.toml         # 配置项目元数据和构建系统
├── README.md              # 项目描述文件
└── LICENSE                # 许可证文件



在pyproject.toml同级执行
pip install build
python -m build  # build失败，使用下面指定源后再pip
# 确保在运行构建命令的同一行或之前设置了环境变量
PIP_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple" python -m build



# 如果是本地文件，使用本地路径
pip install dist/rotation_utils_geometry-0.1.0-py3-none-any.whl