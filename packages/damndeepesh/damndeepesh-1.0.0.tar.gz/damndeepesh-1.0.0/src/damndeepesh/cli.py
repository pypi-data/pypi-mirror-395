import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.layout import Layout
from rich.text import Text
from rich.theme import Theme

# Define a custom theme
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "danger": "bold red",
    "title": "bold magenta",
    "header": "bold green",
    "link": "underline blue"
})

console = Console(theme=custom_theme)

def fetch_portfolio_data():
    """
    Fetches the portfolio website content.
    Since scraping dynamic Next.js sites can be brittle with just BS4 if not careful with classes,
    we will try to extract text based on known headers or structure.
    
    For a more robust solution in a real-world scenario, we might want to check for 
    specific meta tags or JSON-LD, but here we will do a best-effort text extraction
    simulating the 'browsing' experience.
    """
    url = "https://www.deepeshgupta.dev"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        console.print(f"[danger]Error fetching portfolio: {e}[/danger]")
        return None




import re
import sys
import time
import random
from rich.prompt import Prompt
from rich.live import Live
from rich.table import Table
from rich.align import Align

def parse_portfolio_data(html_content):
    """
    Parses the HTML and returns a structured dictionary of data.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    data = {}
    
    # helper
    def get_section_content(header_pattern):
        header = soup.find(string=re.compile(header_pattern, re.IGNORECASE))
        if not header: return None
        parent = header.parent
        while parent and parent.name not in ['h1', 'h2', 'h3', 'h4', 'div', 'section']:
            parent = parent.parent
        if not parent: return None
        content = []
        curr = parent.find_next_sibling()
        steps = 0
        while curr and steps < 50: 
            if curr.name in ['h1', 'h2', 'h3', 'h4', 'header', 'footer']: break
            text = curr.get_text(strip=True, separator=" ")
            if text: content.append(text)
            curr = curr.find_next_sibling()
            steps += 1
        return "\n".join(content)

    data['mission'] = get_section_content(r"The Mission")
    data['arsenal'] = get_section_content(r"Arsenal")

    # Projects
    projects = []
    candidates = soup.find_all(['h3', 'h4'])
    ignored_headers = [
        "The Mission", "Arsenal", "Core Focus", "Experience", "Connect", 
        "System Online", "Andovar India (Remote)", "Localization Engineering Intern"
    ]
    for h in candidates:
        text = h.get_text(strip=True)
        if not text or any(ignored in text for ignored in ignored_headers): continue
        if text in ["Languages", "Frameworks"]: continue
        
        title = text
        desc_lines = []
        link = ""
        curr = h.find_next_sibling()
        steps = 0
        while curr and steps < 10:
            if curr.name in ['h1', 'h2', 'h3', 'h4', 'header', 'footer']: break
            t = curr.get_text(strip=True, separator=" ")
            if t: desc_lines.append(t)
            if not link:
                l = curr.find('a', href=True)
                if l: link = l['href']
            curr = curr.find_next_sibling()
            steps += 1
        if not link:
            l = h.find('a', href=True)
            if l: link = l['href']
            
        if desc_lines or link:
            projects.append({'title': title, 'desc': "\n".join(desc_lines), 'link': link})
    data['projects'] = projects

    # Experience
    experience = []
    role_header = soup.find(string=re.compile("Localization Engineering Intern"))
    if role_header:
         role_elem = role_header.parent
         while role_elem and role_elem.name not in ['h3', 'h4', 'div']: role_elem = role_elem.parent
         if role_elem:
             content_lines = ["[bold]Andovar India (Remote)[/bold]", f"\n[bold cyan]{role_header}[/bold cyan]"]
             curr = role_elem.find_next_sibling()
             steps = 0
             while curr and steps < 10:
                 if curr.name in ['h1', 'h2', 'h3', 'h4', 'footer']: break
                 text = curr.get_text(strip=True, separator=" ")
                 if "What's Next" in text: break
                 if text: content_lines.append(text)
                 curr = curr.find_next_sibling()
                 steps += 1
             experience.append("\n".join(content_lines))
    data['experience'] = experience
    
    # Socials
    links = soup.find_all('a', href=True)
    socials = []
    seen = set()
    for l in links:
        href = l['href']
        if "github.com" in href or "linkedin.com" in href or "x.com" in href or "t.me" in href:
             if href not in seen:
                 socials.append(href)
                 seen.add(href)
    data['socials'] = socials

    return data


def binary_matrix_effect():
    """Easter egg: Binary Matrix rain effect (0101)"""
    matrix_chars = ["0", "1"]
    console.clear()
    with Live(console=console, refresh_per_second=15) as live:
        for _ in range(100):
            lines = []
            for _ in range(console.height - 1):
                # Binary density
                line = "".join(random.choice(matrix_chars + [" "]*15) for _ in range(console.width))
                lines.append(f"[bold green]{line}[/bold green]")
            live.update(Align.center("\n".join(lines)))
            time.sleep(0.05)
    console.clear()
    console.print("[bold green]The system is binary. But the world is not.[/bold green]\n")

def god_mode():
    """Easter egg: Konami Code"""
    console.print("\n[bold red]GOD MODE ENABLED[/bold red]")
    time.sleep(1)
    console.print("[italic cyan]root@deepesh-mainframe:~# [/italic cyan]", end="")
    time.sleep(1)
    console.print("sudo make-me-a-sandwich")
    time.sleep(1)
    console.print("[dim]Access Denied. Even God needs sudo privileges.[/dim]\n")

def coffee_break():
    """Easter egg: Coffee"""
    art = """
      )  (
     (   ) )
      ) ( (
    _______)_
 .-'---------|  
( C|/////////|
 '-._________|
  '─────────'
    """
    console.print(Panel(art, title="[bold yellow]Coffee Break[/bold yellow]", border_style="yellow", expand=False))
    console.print("Fueling up for more coding...\n")


from .data import JOKES, FORTUNES

def fake_ls():
    """Easter egg: Fake file system"""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Permissions", style="dim")
    table.add_column("Size", justify="right")
    table.add_column("User", style="cyan")
    table.add_column("Date")
    table.add_column("Name", style="bold green")

    files = [
        ("-rw-r--r--", "1.2M", "deepesh", "Dec 06", "portfolio_v1.py"),
        ("drwxr-xr-x", "4.0K", "root", "Dec 05", "secret_plans/"),
        ("-rw-r--r--", "42B", "deepesh", "May 04", "meaning_of_life.txt"),
        ("-rw-------", "8.0K", "root", "Jan 01", ".bash_history"),
        ("-rwxr-xr-x", "999K", "admin", "Nov 11", "world_domination_script.sh"),
    ]
    
    for row in files:
        table.add_row(*row)
    
    console.print(table)
    console.print("\n")

def tell_joke():
    """Easter egg: Random jokes"""
    console.print(Panel(random.choice(JOKES), title="[bold yellow]Dad Joke[/bold yellow]", border_style="yellow"))
    console.print("\n")

def fortune_cookie():
    """Easter egg: Tech quotes"""
    console.print(Panel(random.choice(FORTUNES), title="[bold purple]Fortune[/bold purple]", border_style="purple"))
    console.print("\n")

def secret_help():
    """Easter egg: Help menu"""
    table = Table(title="[bold red]SECRET COMMAND LIST[/bold red]", show_header=True, header_style="bold red")
    table.add_column("Command", style="cyan")
    table.add_column("Effect", style="green")
    
    commands = [
        ("ls / dir", "Browse the (fake) system"),
        ("joke", "Receive a terrible programming joke"),
        ("fortune", "Receive ancient tech wisdom"),
        ("coffee", "Take a well-deserved break"),
        ("0101", "Enter the Matrix"),
        ("konami", "Enable God Mode"),
        ("hack", "Feel like a 90s movie hacker"),
        ("42", "The Answer"),
    ]
    
    for cmd in commands:
        table.add_row(*cmd)
        
    console.print(table)
    console.print("\n")

from rich.columns import Columns
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
import time
import random

def simulate_boot():
    """Simulate a cool cyberpunk boot sequence."""
    console.clear()
    
    # Phase 1: System Check
    with Progress(
        SpinnerColumn(spinner_name="dots"),
        TextColumn("[bold green]{task.description}"),
        BarColumn(bar_width=None, style="green", complete_style="bold green"),
        console=console,
        transient=True
    ) as progress:
        task1 = progress.add_task("[green]Initializing secure connection...", total=100)
        task2 = progress.add_task("[green]Verifying encryption keys...", total=100)
        task3 = progress.add_task("[green]Downloading portfolio data...", total=100)

        while not progress.finished:
            progress.update(task1, advance=random.randint(1, 5))
            if progress.tasks[0].completed > 50:
                progress.update(task2, advance=random.randint(1, 8))
            if progress.tasks[1].completed > 60:
                progress.update(task3, advance=random.randint(1, 10))
            time.sleep(0.05)
    
    console.print("[bold green]ACCESS GRANTED.[/bold green]\n", justify="center")
    time.sleep(0.5)

def print_banner():
    """Print ASCII Banner."""
    banner = """
[bold cyan]
  ____  _____ _____ ____  _____ ____  _   _ 
 |  _ \| ____| ____|  _ \| ____/ ___|| | | |
 | | | |  _| |  _| | |_) |  _| \___ \| |_| |
 | |_| | |___| |___|  __/| |___ ___) |  _  |
 |____/|_____|_____|_|   |_____|____/|_| |_|
[/bold cyan]
[dim]         PORTFOLIO TERMINAL INTERFACE v1.0         [/dim]
    """
    console.print(Align.center(banner))

def create_skills_panel(skills_text):
    """Create a grid layout for skills."""
    if not skills_text: return None
    
    # Basic parsing: split by obvious delimiters or known keywords
    # Since scraping gives us a block of text, let's try to identify common keywords
    # or just split by spaces if it's clean list from site
    
    # Refined scraping usually gives "Languages Python Java..."
    # Let's try to just dump words into badges for now
    words = skills_text.replace("Languages", "").replace("Frameworks", "").split()
    
    skill_badges = []
    colors = ["red", "green", "blue", "magenta", "cyan", "yellow"]
    
    for word in words:
        if len(word) < 2: continue
        color = random.choice(colors)
        skill_badges.append(
            Panel(
                f"[bold {color}]{word}[/bold {color}]",
                expand=False,
                border_style="dim"
            )
        )
            
    return Panel(
        Columns(skill_badges, align="center", expand=True),
        title="[bold yellow]WAR CHEST (ARSENAL)[/bold yellow]",
        border_style="yellow",
        padding=(1, 2)
    )

def display_full_portfolio(data):
    """Render all sections sequentially."""
    console.clear()
    
    print_banner()
    console.print("\n")
    
    # Mission
    if data.get('mission'):
        mission_panel = Panel(
            Text(data['mission'], justify="center", style="white"),
            title="[bold blue]CURRENT MISSION[/bold blue]",
            border_style="blue",
            padding=(1, 2)
        )
        console.print(mission_panel)
        console.print("\n")
    
    # Skills
    if data.get('arsenal'):
        console.print(create_skills_panel(data['arsenal']))
        console.print("\n")

    # Projects
    if data.get('projects'):
        console.print(Align.center("[bold cyan]--- CORE PROTOCOLS (PROJECTS) ---[/bold cyan]"))
        console.print("\n")
        
        for p in data['projects']:
            desc = p.get('desc', '')
            if "View Project" in desc: desc = desc.replace("View Project", "")
            
            title = p.get('title', 'Project')
            link = p.get('link', '')
            
            # Format description for better readability
            content = f"{desc}"
            if link:
                content += f"\n\n[bold]LINK :: [/bold][link={link}]{link}[/link]"
                
            console.print(Panel(
                content,
                title=f"[bold green]{title}[/bold green]",
                border_style="green",
                padding=(1, 2)
            ))
        console.print("\n")

    # Experience
    if data.get('experience'):
            console.print(Align.center("[bold magenta]--- PREVIOUS ENGAGEMENTS ---[/bold magenta]"))
            console.print("\n")
            for exp in data['experience']:
                console.print(Panel(exp, border_style="magenta", padding=(1, 2)))
            console.print("\n")

    # Connect
    console.print(Align.center("[bold]--- SECURE CHANNELS ---[/bold]"))
    console.print("\n")
    console.print("Website: [link=https://www.deepeshgupta.dev]https://www.deepeshgupta.dev[/link]", justify="center")
    
    social_links = []
    for s in data.get('socials', []):
        name = "Link"
        if "github" in s: name = "GitHub"
        elif "linkedin" in s: name = "LinkedIn"
        elif "x.com" in s: name = "X (Twitter)"
        elif "t.me" in s: name = "Telegram"
        
        social_links.append(f"[{name}]({s})")
    
    console.print(Align.center(" • ".join([f"[link={s}]{s}[/link]" for s in data.get('socials', [])])))
    console.print("\n")


def hidden_listener():
    """Hidden input listener for easter eggs."""
    console.print("[dim]Session Active. Press Enter to disconnect...[/dim]", justify="center")
    
    while True:
        # We use password=True to make it feel hidden (no echo)
        # But we need to handle simple Enter (empty string) to exit
        # Added a distinctive prompt character to hint interactivity
        code = Prompt.ask(" [dim]>[/dim] ", password=True, show_default=False)
        code = code.strip().lower() # Normalize input
        
        if not code:
            console.print("[bold red]Terminating connection... Goodbye![/bold red]")
            break

        if code in ["ls", "dir"]:
            fake_ls()
            console.print("[dim]Press Enter to disconnect...[/dim]", justify="center")
            
        elif code in ["joke", "jokes"]:
            tell_joke()
            console.print("[dim]Press Enter to disconnect...[/dim]", justify="center")
            
        elif code in ["fortune", "quote"]:
            fortune_cookie()
            console.print("[dim]Press Enter to disconnect...[/dim]", justify="center")
            
        elif code in ["help", "?", "man"]:
            secret_help()
            console.print("[dim]Press Enter to disconnect...[/dim]", justify="center")
            
        elif code == "0101":
            binary_matrix_effect()
            console.print("[dim]Press Enter to disconnect...[/dim]", justify="center")
        
        elif code == "coffee":
            coffee_break()
            console.print("[dim]Press Enter to disconnect...[/dim]", justify="center")
            
        elif code == "hack":
            # Using dots spinner as fixed previously
            with console.status("[bold green]Hacking mainframe...[/bold green]", spinner="dots"): 
                time.sleep(2)
            console.print("[bold green]Access Granted. Just kidding, this is a portfolio.[/bold green]")
            console.print("[dim]Press Enter to disconnect...[/dim]", justify="center")
            
        elif "upupdowndown" in code or code == "konami": # Loose matching + explicit text
             god_mode()
             console.print("[dim]Press Enter to disconnect...[/dim]", justify="center")
             
        elif code == "42":
             console.print("[bold blue]The Answer to the Ultimate Question of Life, the Universe, and Everything is... Portfolio.[/bold blue]")
             console.print("[dim]Press Enter to disconnect...[/dim]", justify="center")



def main():
    simulate_boot()
    html = fetch_portfolio_data() # Moving fetch after generic boot seq to feel smoother
    
    if html:
        data = parse_portfolio_data(html)
        display_full_portfolio(data)
        hidden_listener()



if __name__ == "__main__":
    main()
