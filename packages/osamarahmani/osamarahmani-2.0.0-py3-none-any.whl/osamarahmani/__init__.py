import os
import sys
import time
import random

# ================== DATA ==================
profile = {
    "name": "Osama Rahmani",
    "role": "Full-Stack Developer",
    "gmails": ["osamrahmani.tech@gmail.com", "armanmallik168@gmail.com"],
    "website": "https://osamrahmani.tech",
    # ADDED YOUR NEW LINKS HERE
    "linkedin": "https://www.linkedin.com/in/osamarahmani/",
    "github": "https://github.com/osamarahmani",
    "tech": ["Python", "JavaScript", "Node.js", "MongoDB", "TailwindCSS", "ShadCN"],
    "focus": ["Full-Stack Apps", "Clean UI", "Secure Backend"]
}

# ================== COLORS ==================
def theme(text): return f"\033[38;2;218;142;118m{text}\033[0m"
def bg_theme(text): return f"\033[48;2;218;142;118m\033[38;5;232m {text} \033[0m"
def color(code, text): return f"\033[38;5;{code}m{text}\033[0m"
def bold(text): return f"\033[1m{text}\033[0m"

CYAN, BLUE, GRAY, WHITE = 45, 33, 240, 15

# ================== ANIMATION LOGIC ==================
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def typewriter(text, speed=0.005, end="\n"):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed + random.uniform(0, 0.005))
    sys.stdout.write(end)

def loading_bar():
    print("\n")
    total = 40
    prefix = theme("  INITIALIZING: ")
    for i in range(total + 1):
        percent = int((i / total) * 100)
        filled = "█" * i
        empty = "░" * (total - i)
        sys.stdout.write(f"\r{prefix} {theme(f'|{filled}{empty}|')} {percent}%")
        sys.stdout.flush()
        time.sleep(0.01)
    print("\n")

def get_banner_art():
    return f"""
    {theme('╔══════════════════════════════════════════════════════════════════════════╗')}
    {theme('  ██████╗ ███████╗ █████╗ ███╗   ███╗ █████╗     ')}
    {theme(' ██╔═══██╗██╔════╝██╔══██╗████╗ ████║██╔══██╗    ')}
    {theme(' ██║   ██║███████╗███████║██╔████╔██║███████║    ')}
    {theme(' ██║   ██║╚════██║██╔══██║██║╚██╔╝██║██╔══██║    ')}
    {theme(' ╚██████╔╝███████║██║  ██║██║ ╚═╝ ██║██║  ██║     ')}
    {theme('  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝     ')}
    {theme('╚══════════════════════════════════════════════════════════════════════════╝')}"""

def get_columns():
    # Icons added here
    c1 = [
        f"{bold(theme('➜ IDENTITY'))}",
        f"  {color(CYAN, 'User:')} {profile['name'].upper()}",
        f"  {color(CYAN, 'Loc: ')} India (UTC +5:30)",
        "",
        f"{bold(theme('➜ CONNECT'))}",
        f"  {color(CYAN, '📧 Mail:')} {profile['gmails'][0]}",
        f"  {color(CYAN, '🌐 Web :')} {profile['website']}",
        # NEW GITHUB AND LINKEDIN LINES
        f"  {color(CYAN, '🐙 Git :')} {profile['github']}",
        f"  {color(CYAN, '💼 Link:')} {profile['linkedin']}", 
    ]
    c2 = [
        f"{bold(theme('⚡ TECH STACK'))}",
        f"  {theme('•')} {', '.join(profile['tech'][:3])}",
        f"  {theme('•')} {', '.join(profile['tech'][3:])}",
        "",
        f"{bold(theme('⚡ SPECIALTY'))}",
        f"  {theme('•')} {profile['focus'][0]}",
        f"  {theme('•')} {profile['focus'][1]}",
        f"  {theme('•')} {profile['focus'][2]}",
        "",
        f"  {color(GRAY, '(Full list on GitHub)')}"
    ]
    return c1, c2

# ================== EXPORTED VARIABLES ==================
# You can now access these directly
name = profile["name"]
role = profile["role"]
website = profile["website"]
gmail = profile["gmails"]
github = profile["github"]      # <--- NEW
linkedin = profile["linkedin"]  # <--- NEW

# ================== STATIC PORTFOLIO ==================
def create_static_portfolio():
    os.system('color')
    lines = [get_banner_art()]
    lines.append(f"          {bg_theme(profile['role'].upper())}   {color(WHITE, '❖ ' + profile['website'])}")
    lines.append("\n" + color(GRAY, "─" * 80))
    c1, c2 = get_columns()
    
    # Logic to handle uneven lists (since c1 is now longer with new links)
    max_len = max(len(c1), len(c2))
    for i in range(max_len):
        col1_txt = c1[i] if i < len(c1) else ""
        col2_txt = c2[i] if i < len(c2) else ""
        lines.append(f"  {col1_txt:<50} {col2_txt}") # Increased spacing to 50 for long URLs

    lines.append("\n" + color(GRAY, "─" * 80))
    arrow = theme('→')
    lines.append(f"  {bg_theme(' WORK PROCESS ')}  Brief {arrow} Design {arrow} Build {arrow} Launch")
    lines.append("\n" + bold(theme("  LET'S BUILD THE FUTURE TOGETHER.")) + " Available for projects.")
    lines.append(theme("═" * 80))
    lines.append(f"{color(242, ' © 2025 Osama Rahmani | Full-Stack Developer ').center(88)}")
    return "\n".join(lines)

portfolio = create_static_portfolio()

# ================== ANIMATION FUNCTION ==================
def run():
    """Run the CLI Animation."""
    os.system('color') 
    clear()
    loading_bar()
    print(get_banner_art()) 
    time.sleep(0.2)
    print(f"          {bg_theme(profile['role'].upper())}   {color(WHITE, '❖ ' + profile['website'])}")
    typewriter(color(GRAY, "─" * 80), speed=0.001)
    
    c1, c2 = get_columns()
    max_len = max(len(c1), len(c2))
    
    for i in range(max_len):
        col1_txt = c1[i] if i < len(c1) else ""
        col2_txt = c2[i] if i < len(c2) else ""
        
        row = f"  {col1_txt:<50} {col2_txt}"
        
        if "➜" in row or "⚡" in row:
            print(row)
            time.sleep(0.1)
        else:
            typewriter(row, speed=0.002)
            
    typewriter(color(GRAY, "─" * 80), speed=0.001)
    arrow = theme('→')
    print(f"  {bg_theme(' WORK PROCESS ')}  Brief {arrow} Design {arrow} Build {arrow} Launch")
    time.sleep(0.3)
    print("\n" + bold(theme("  LET'S BUILD THE FUTURE TOGETHER.")) + " Available for projects.")
    print(theme("═" * 80))
    print(f"{color(242, ' © 2025 Osama Rahmani | Full-Stack Developer ').center(88)}\n")

if __name__ == "__main__":
    run()