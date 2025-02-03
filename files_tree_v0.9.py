import os
from tkinter import Tk, filedialog
from colorama import Fore, init

# 初始化colorama（用于跨平台颜色支持）
init(autoreset=True)

def select_directory():
    """通过对话框选择目录"""
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    directory = filedialog.askdirectory(title="请选择目录")
    return directory

def generate_tree(directory, prefix=""):
    """递归生成目录树结构"""
    try:
        entries = os.listdir(directory)
    except PermissionError:
        return [f"{prefix}└── {Fore.RED}[权限被拒绝]"]
    except UnicodeDecodeError:
        return [f"{prefix}└── {Fore.YELLOW}[文件名解码失败]"]
    except Exception as e:
        return [f"{prefix}└── {Fore.RED}[错误: {e}]"]

    tree = []
    entries = sorted(entries)  # 按名称排序（可选）
    for index, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        is_last = index == len(entries) - 1
        connector = "└── " if is_last else "├── "

        # 处理符号链接
        if os.path.islink(path):
            link_target = os.readlink(path)
            tree.append(f"{prefix}{connector}{Fore.CYAN}{entry} -> {link_target}")
            continue

        # 颜色和目录标识
        display_name = entry
        if os.path.isdir(path):
            display_name = f"{Fore.BLUE}{display_name}/"  # 目录加斜杠和颜色
        else:
            display_name = f"{Fore.GREEN}{display_name}"  # 文件颜色

        tree.append(f"{prefix}{connector}{display_name}")

        if os.path.isdir(path) and not os.path.islink(path):  # 避免递归链接
            extension = "    " if is_last else "│   "
            subtree = generate_tree(path, prefix + extension)
            tree.extend(subtree)
    
    return tree

def main():
    print("=== 文件树生成器 ===")
    directory = select_directory()
    if not directory:
        print("未选择目录，程序退出。")
        return

    print(f"\n生成目录树：{directory}")
    print("\n".join(generate_tree(directory)))

if __name__ == "__main__":
    main()