from setuptools import setup
import os
import json

# 读取 package.json 获取版本信息
with open('package.json') as f:
    package_json = json.load(f)

version = package_json['version']
name = package_json['name'].replace('@', '').replace('/', '-')

# 获取所有需要包含的文件
data_files = []

# 包含 labextension 文件
labextension_path = "jupyterlab_chat/labextension"
if os.path.exists(labextension_path):
    for root, dirs, files in os.walk(labextension_path):
        for file in files:
            file_path = os.path.join(root, file)
            # 相对于项目根目录的路径
            rel_dir = os.path.relpath(root, labextension_path)
            if rel_dir == '.':
                target_dir = f"share/jupyter/labextensions/{name}"
            else:
                target_dir = f"share/jupyter/labextensions/{name}/{rel_dir}"
            
            data_files.append((target_dir, [file_path]))

# 包含 schema 文件
schema_path = "schema"
if os.path.exists(schema_path):
    for root, dirs, files in os.walk(schema_path):
        for file in files:
            file_path = os.path.join(root, file)
            rel_dir = os.path.relpath(root, schema_path)
            if rel_dir == '.':
                target_dir = f"share/jupyter/labextensions/{name}/schema"
            else:
                target_dir = f"share/jupyter/labextensions/{name}/schema/{rel_dir}"
            
            data_files.append((target_dir, [file_path]))

setup(
    name=name,
    version=version,
    description=package_json.get('description', 'JupyterLab Chat Extension'),
    author='ChandlerFan',
    author_email='411342747@qq.com',
    packages=[],  # 没有 Python 包
    include_package_data=True,
    data_files=data_files,
    install_requires=[
        'jupyterlab>=3.2.9,<4',
    ],
    zip_safe=False,
    classifiers=[
        'Framework :: Jupyter',
        'Framework :: Jupyter :: JupyterLab',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: BSD License',
    ],
    python_requires='>=3.6',
    keywords=['jupyter', 'jupyterlab', 'jupyterlab-extension', 'chat'],
)