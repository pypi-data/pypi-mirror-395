import os
import sys
import shutil
import py7zr
from pyscreeps_arena.core import const, config
def CMD_NewProject():
    """
    cmd:
        pyscreeps-arena  [project_path]
        arena [project_path]

    * 复制"src" "game" "build.py" 到指定目录

    Returns:

    """
    if len(sys.argv) < 2:
        print("Usage: pyarena new [project_path]\n# or\narena new [project_path]")
        return
    project_path = sys.argv[1]
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    this_path = os.path.dirname(os.path.abspath(__file__))
    extract_7z(os.path.join(this_path, 'project.7z'), project_path)
    print("Project created at", project_path)

def CMD_OpenUI():
    """
    cmd:
        psaui

    * 打开UI界面

    Returns:

    """
    try:
        from pyscreeps_arena.ui.project_ui import run_project_creator
        run_project_creator()
    except ImportError as e:
        print(f"错误: 无法导入UI模块 - {e}")
        print("请确保已安装PyQt6: pip install PyQt6")
    except Exception as e:
        print(f"错误: 打开UI界面失败 - {e}")

def extract_7z(file_path, output_dir):
    with py7zr.SevenZipFile(file_path, mode='r') as archive:
        archive.extractall(path=output_dir)

if __name__ == '__main__':
    CMD_OpenUI()
