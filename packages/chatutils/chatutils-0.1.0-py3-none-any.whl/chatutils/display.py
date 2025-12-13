from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()


def print_panel(content, title=None, border_style="blue", title_align="center"):
    panel = Panel(
        Markdown(content, code_theme="github-dark"),
        title=title,
        border_style=border_style,
        title_align=title_align,
    )
    console.print(panel)


def print_markdown(content, border=False):
    md_content = content + "\n\n---" if border else content
    console.print(Markdown(md_content, code_theme="github-dark"))


def print_code(code, extension=""):
    print_markdown(f"```{extension}\n{code}\n```")


def print_chat_messages(messages):
    md_content = markdown(messages)
    print_panel(md_content)


# utility
def markdown(prompt):
    out = []
    for m in prompt:
        out.append(f"\n## [{m['role']}]\n")
        for line in m["content"].split("\n"):
            out.append(f"> {line}" if m["role"] == "user" else line)
    return "\n".join(out).strip()
