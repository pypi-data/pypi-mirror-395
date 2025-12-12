import os

def _jupyter_labextension_paths():
    """返回 labextension 的路径"""
    return [{
        "src": "jupyterlab_chat/labextension",
        "dest": "jupyterlab-chat"  # 这应该与 package.json 中的 name 匹配
    }]