import os
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.table import Table
from rich.box import ROUNDED

def main():
    console = Console()
    
    # Load ASCII Art
    asset_path = os.path.join(os.path.dirname(__file__), 'assets', 'ascii-art.txt')
    try:
        with open(asset_path, 'r') as f:
            ascii_art = f.read()
    except FileNotFoundError:
        ascii_art = "Image not found."

    # Process ASCII Art (strip empty lines from top/bottom only)
    lines = ascii_art.split('\n')
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    
    ascii_art = '\n'.join(lines)
    
    # Define Colors
    FD_BLUE = "#1493FF"
    FD_ORANGE = "#FF9900" 
    BORDER_COLOR = FD_BLUE
    LABEL_COLOR = "bold cyan"
    VALUE_COLOR = "white"
    LINK_COLOR = "underline blue"

    # 1. ASCII Art
    art_text = Text(ascii_art, style="bold cyan", no_wrap=True, overflow='ignore')
    art_panel = Align.center(art_text)

    # 2. Name Banner (ASCII-like text using simple characters or just large bold text)
    # Since we want minimal deps, we'll use a simple text banner or just the name
    # The reference has a big ASCII name. We'll stick to a nice bold header for now.
    name_text = Text("JESSICA RUDD", style=f"bold white on {FD_BLUE}")
    
    # 3. Info Table
    grid = Table.grid(padding=(0, 2))
    grid.add_column(justify="right", style=LABEL_COLOR)
    grid.add_column(justify="left", style=VALUE_COLOR)
    
    grid.add_row("Work:", "Staff Data Engineer")
    grid.add_row("", "Analytics Engineering Team @ FanDuel")
    grid.add_row("GitHub:", Text("https://github.com/JessicaRudd", style=LINK_COLOR))
    grid.add_row("Email:", Text("jessica.rudd@fanduel.com", style=LINK_COLOR))
    grid.add_row("LinkedIn:", Text("https://www.linkedin.com/in/jmrudd/", style=LINK_COLOR))
    grid.add_row("Substack:", Text("https://funsizedatabytes.substack.com/", style=LINK_COLOR))
    
    grid.add_row() # Spacer
    grid.add_row("Card:", Text("pip install funsize-engineer", style=FD_ORANGE))

    # Assemble Content
    content = Table.grid(padding=(1, 1))
    content.add_column(justify="center")
    
    content.add_row(art_panel)
    content.add_row(Text("─" * 100, style="dim")) # Separator
    content.add_row(name_text)
    content.add_row(Text("─" * 100, style="dim")) # Separator
    content.add_row(grid)

    # Main Panel
    console.print(
        Panel(
            content,
            border_style=BORDER_COLOR,
            padding=(1, 2),
            width=108, # Width set to accommodate 100-char ASCII art + padding
            box=ROUNDED
        )
    )

if __name__ == "__main__":
    main()
