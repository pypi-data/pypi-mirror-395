import os

SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]
POWERBI_API_BASE = "https://api.powerbi.com/v1.0/myorg"
API_URL = "https://api.fabric.microsoft.com/v1"
RESOURCE_URL = "https://api.fabric.microsoft.com"
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
WORKSPACE_ID = os.getenv("WORKSPACE_ID")
SEMANTIC_MODEL_ID = os.getenv("SEMANTIC_MODEL_ID")


def print_color(text, color="white", bold=False, bg=None):
    colors = {
        "black": 30, "red": 31, "green": 32, "yellow": 33,
        "blue": 34, "magenta": 35, "cyan": 36, "white": 37
    }

    parts = []

    if bold:
        parts.append("1")

    parts.append(str(colors.get(color.lower(), 37)))

    if bg:
        bg_num = colors.get(bg.lower(), 37) - 30 + 40
        parts.append(str(bg_num))

    ansi = ";".join(parts)

    # Safe: write start + text + reset in a **single** print
    print(f"\033[{ansi}m{text}\033[0m", end="")

    # Extra hard reset (sometimes required on Windows / VSCode / zsh)
    print("\033[0m")
