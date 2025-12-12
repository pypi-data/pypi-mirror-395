import os
import tempfile
import subprocess
import shutil
from rich.syntax import Syntax
from rich.console import Console

console = Console()

ALLOWED_EDITORS = ["vim", "vi", "nano", "emacs", "code", "subl"]

def beautify_diff(diff_output: str) -> None:
    syntax = Syntax(
        diff_output,
        "diff",
        line_numbers=True,
        word_wrap=True,
        indent_guides=False,
        theme="monokai",
    )
    console.print(syntax)


def edit_commit_message(initial_message: str) -> str:
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".tmp", delete=False) as tf:
        tf.write(initial_message)
        tf.flush()
        tf_name = tf.name

    editor_from_env = os.environ.get("EDITOR")
    editor_to_use = None

    if editor_from_env:
        # 提取命令的基本名称 (例如 /usr/bin/vim -> vim)
        editor_basename = os.path.basename(editor_from_env)
        # 检查基本名称是否在允许列表中，并且该命令确实存在于 PATH 中
        if editor_basename in ALLOWED_EDITORS and shutil.which(editor_from_env):
            editor_to_use = editor_from_env
        else:
            console.print(f"[yellow]Warning:[/yellow] EDITOR environment variable ('{editor_from_env}') is not in the allowed list ({ALLOWED_EDITORS}) or not found. Falling back to 'vim'.")
            # Fallback to default if validation fails

    # 如果环境变量未设置或验证失败，则尝试默认的 'vim'
    if editor_to_use is None:
        if shutil.which("vim"):
            editor_to_use = "vim"
        else:
            # 如果连 vim 都没有，则需要处理错误情况
            console.print("[red]Error:[/red] Default editor 'vim' not found. Please install it or set a valid EDITOR environment variable from the allowed list.")
            os.unlink(tf_name) # 清理临时文件
            # 根据你的应用逻辑，这里可以抛出异常或返回原始消息
            # raise RuntimeError("No valid editor found.")
            return initial_message # 或者简单返回未编辑的消息

    try:
        # 推荐使用 subprocess.run 替代 subprocess.call
        # check=True 会在命令返回非零退出码时抛出 CalledProcessError 异常
        subprocess.run([editor_to_use, tf_name], check=True)
    except FileNotFoundError:
        console.print(f"[red]Error:[/red] Editor command '{editor_to_use}' not found. Please check your installation and PATH.")
        os.unlink(tf_name)
        return initial_message # 返回未编辑的消息
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error:[/red] Editor '{editor_to_use}' exited with status {e.returncode}.")
        # 即使编辑器出错，文件可能已被部分修改，但我们通常认为编辑失败
        os.unlink(tf_name)
        return initial_message # 返回未编辑的消息
    except Exception as e:
        console.print(f"[red]An unexpected error occurred while running the editor:[/red] {e}")
        os.unlink(tf_name)
        return initial_message # 返回未编辑的消息


    # 确保文件最终被读取和删除
    edited_message = initial_message # 默认值以防文件读取失败
    if os.path.exists(tf_name):
        try:
            with open(tf_name, "r") as tf:
                edited_message = tf.read().strip()
        except Exception as e:
            console.print(f"[red]Error reading temporary file {tf_name}:[/red] {e}")
            # 保留原始消息
        finally:
            os.unlink(tf_name) # 确保在任何情况下都尝试删除
    else:
        console.print(f"[yellow]Warning:[/yellow] Temporary file {tf_name} seems to have been deleted by the editor.")
        # 在这种情况下，我们无法获取编辑后的消息，返回原始消息
        edited_message = initial_message


    return edited_message