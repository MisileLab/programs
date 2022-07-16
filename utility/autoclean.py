import os
import click
from shutil import rmtree
from simple_term_menu import TerminalMenu
from tqdm import tqdm
from pygments import formatters, highlight, lexers
from pygments.util import ClassNotFound

a = []

def highlight_file(filepath):
    if os.path.isfile(filepath):
        try:
            with open(filepath, "r") as f:
                file_content = f.read()
        except UnicodeDecodeError:
            return "This file is exec file or has invaild characters."
        try:
            lexer = lexers.get_lexer_for_filename(filepath, stripnl=False, stripall=False)
        except ClassNotFound:
            lexer = lexers.get_lexer_by_name("text", stripnl=False, stripall=False)
        formatter = formatters.TerminalFormatter(bg="dark")
        highlighted_file_content = highlight(file_content, lexer, formatter)
        return highlighted_file_content
    elif os.path.isdir(filepath):
        return '\n'.join(os.listdir(filepath))

@click.command("CleanUtility")
@click.option("--size", help="file that equal or bigger than this size will be remove, support suffix kb/mb/gb", required=True)
@click.option("--path", help="path that will be cleaned", required=False, default=os.getcwd())
def main(size, path):
    if size.endswith("kb"):
        size = int(size.removesuffix("kb")) * 1024
    elif size.endswith("mb"):
        size = int(size.removesuffix("mb")) * 1024 * 1024
    elif size.endswith("gb"):
        size = int(size.removesuffix("gb")) * 1024 * 1024 * 1024
    else:
        filter(str.isdigit, size)
        size = int(size)

    os.chdir(path)

    for i in tqdm(os.listdir()):
        if os.path.getsize(i) >= size:
            a.append(i)

    if a.__len__() == 0:
        print("No files found")
        return

    menu = TerminalMenu(
        a,
        title="Checked file won't remove.",
        multi_select=True,
        show_multi_select_hint=True,
        preview_command=highlight_file
    )

    menu.show()

    for i in tqdm([c for c in a if c not in menu.chosen_menu_entries]):
        if os.path.isfile(i):
            os.remove(i)
        elif os.path.isdir(i):
            rmtree(i)

main()
