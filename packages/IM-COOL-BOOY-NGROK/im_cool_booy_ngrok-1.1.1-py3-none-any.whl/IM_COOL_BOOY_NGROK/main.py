# IM_COOL_BOOY_NGROK/main.py
#!/usr/bin/env python3
import os
import platform
import urllib.request
import zipfile
import sys
import time
import subprocess

def main_function():
    print("This is the main_function.")

# ---------------- COLORS ----------------
R = "\033[31m"
G = "\033[32m"
Y = "\033[33m"
B = "\033[34m"
C = "\033[36m"
M = "\033[35m"
W = "\033[0m"

# ---------------- PATHS ----------------
NGROK_YML_PATH = os.path.expanduser("~/.ngrok2/ngrok.yml")

# ---------------- FRAME MAKER ----------------
def box(text):
    line = "═" * (len(text) + 4)
    return f"{B}╔{line}╗\n║  {text}  ║\n╚{line}╝{W}"

# ---------------- BANNER ----------------
def banner():
    os.system("clear")
    print(box("NNGROK AUTO INSTALLER & MANAGER"))
    print()

# -------- System Detection --------
def detect_system():
    system = platform.system().lower()
    machine = platform.machine().lower()
    if system.startswith("linux") and "android" in platform.release().lower():
        system = "android"
    return system, machine

# -------- Create Download URL --------
def ngrok_url(system, machine):
    arch_map = {
        "x86_64": "amd64",
        "aarch64": "arm64",
        "armv7l": "arm",
        "armv8": "arm64",
        "i686": "386",
        "x86": "386",
    }
    arch = arch_map.get(machine, machine)
    return f"https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-stable-{system}-{arch}.zip"

# -------- Download with progress bar --------
def download(url, filename):
    print(f"{Y}[+] Downloading ngrok...{W}")
    def show_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent = min(downloaded * 100 / total_size, 100)
        bar_len = 40
        fill = int(bar_len * percent / 100)
        bar = f"{G}{'█' * fill}{Y}{'-' * (bar_len - fill)}{W}"
        sys.stdout.write(f"\r[{bar}] {percent:.2f}%")
        sys.stdout.flush()
    urllib.request.urlretrieve(url, filename, reporthook=show_progress)
    print(f"\n{G}[✔] Download complete.!{W}")

# -------- Extract ZIP --------
def extract(zip_file, folder):
    with zipfile.ZipFile(zip_file, "r") as z:
        z.extractall(folder)
    print(f"{G}[✔] Extracted successfully.!{W}")

# -------- Install NGROK --------
def install_ngrok():
    banner()
    print(box("DETECTING DEVICE"))
    print()
    system, machine = detect_system()
    print(f"{G}[✔] System OS: {system}{W}")
    print(f"{G}[✔] Architecture: {machine}{W}")

    url = ngrok_url(system, machine)
    filename = "ngrok.zip"
    install_dir = os.path.join(os.getcwd(), "ngrok")
    if not os.path.exists(install_dir):
        os.makedirs(install_dir)

    download(url, filename)
    extract(filename, install_dir)

    ngrok_path = os.path.join(install_dir, "ngrok")
    os.chmod(ngrok_path, 0o755)

    print(f"\n{G}[✔] NGROK INSTALLED SUCCESSFULLY.!{W}")
    print(f"{C}Path: {ngrok_path}{W}")
    input("\nPress ENTER to return to menu...")

# ============================================================
#                 NGROK TOKEN MANAGER
# ============================================================
def token_banner():
    os.system("clear")
    print(box("NGROK TOKEN MANAGER"))
    print(f"{Y}Token Save Path:{W} {NGROK_YML_PATH}\n")

def token_menu():
    while True:
        token_banner()
        print(f"""
{B}╔══════════════════════════════════╗
║ {G}[1]{W} Enter New Ngrok Token        {B}║
║ {G}[2]{W} View Saved Token             {B}║
║ {G}[3]{W} Delete Saved Token           {B}║
║ {R}[0]{W} Back to Main Menu            {B}║
╚══════════════════════════════════╝{W}
""")
        choice = input(f"{C}💻 Select an option: → {W}")
        if choice == "1":
            set_token()
        elif choice == "2":
            view_token()
        elif choice == "3":
            delete_token()
        elif choice == "0":
            break
        else:
            print(f"{R}[!] Invalid Option.!{W}")
            time.sleep(1)

# -------- Validate and Save Ngrok Token with Version --------
def set_token():
    token_banner()
    token = input(f"{Y}💻 Enter Your Ngrok Token: → {W} ").strip()
    if token == "":
        print(f"{R}Token cannot be empty.!{W}")
        time.sleep(1)
        return

    os.makedirs(os.path.dirname(NGROK_YML_PATH), exist_ok=True)

    # Validate token using ngrok CLI
    result = os.system(f"./ngrok/ngrok authtoken {token} > /dev/null 2>&1")
    if result != 0:
        print(f"{R}❌ Invalid Ngrok Token.! Enter a valid token.{W}")
        time.sleep(2)
        return

    # Get current ngrok version
    try:
        version_output = subprocess.check_output(["./ngrok/ngrok", "version"]).decode().strip()
        version_number = version_output.split()[-1] if len(version_output.split()) >= 3 else "2"
    except:
        version_number = "2"

    # Save valid token with version
    with open(NGROK_YML_PATH, "w") as f:
        f.write(f"version: \"{version_number}\"\nauthtoken: '{token}'\n")
    print(f"\n{G}✔ Token Saved Successfully with Ngrok Version {version_number}!{W}")
    input("\nPress ENTER to return...")

def view_token():
    token_banner()
    if not os.path.exists(NGROK_YML_PATH):
        print(f"{R}❌ No token found!{W}")
    else:
        token = open(NGROK_YML_PATH).read().strip()
        print(f"{G}💻 Saved Token: → {W}\n{token}")
    input("\nPress ENTER to return...")

def delete_token():
    token_banner()
    if os.path.exists(NGROK_YML_PATH):
        os.remove(NGROK_YML_PATH)
        print(f"{G}✔ Token deleted.!{W}")
    else:
        print(f"{R}No token to delete.!{W}")
    input("\nPress ENTER to return...")

# -------- NGROK SETUP (Auto export USER) --------
def ngrok_setup():
    banner()
    print(box("NGROK SETUP"))
    zsh_path = os.path.expanduser("~/.zshrc")
    bash_path = os.path.expanduser("~/.bashrc")
    with open(zsh_path, "a") as f:
        f.write("\nexport USER=termux\n")
    with open(bash_path, "a") as f:
        f.write("\nexport USER=termux\n")
    print(f"{G}✔ USER environment variable set in {zsh_path} and {bash_path}{W}")
    input("\nPress ENTER to return to menu...")

# -------- Update NGROK --------
def update_ngrok():
    banner()
    print(box("NGROK UPDATE"))
    system, machine = detect_system()
    url = ngrok_url(system, machine)
    filename = "ngrok.zip"
    install_dir = os.path.join(os.getcwd(), "ngrok")

    download(url, filename)
    extract(filename, install_dir)

    ngrok_path = os.path.join(install_dir, "ngrok")
    os.chmod(ngrok_path, 0o755)
    print(f"\n{G}✔ NGROK Updated Successfully.!{W}")
    input("\nPress ENTER to return to menu...")

# -------- Start TCP Tunnel --------
def start_tcp():
    banner()
    port = input(f"{C}🌍 Enter Local Port: → {W}")
    os.system(f"./ngrok/ngrok tcp {port}")

# -------- Start HTTP Tunnel --------
def start_http():
    banner()
    port = input(f"{C}🌍 Enter HTTP Port: → {W}")
    os.system(f"./ngrok/ngrok http {port}")

# -------- MENU --------
def menu():
    while True:
        banner()
        print(f"""
{B}╔══════════════════════════════════╗
║ {G}[1]{W} Install NGROK                {B}║
║ {G}[2]{W} Ngrok Token Manager          {B}║
║ {G}[3]{W} Ngrok Setup                  {B}║
║ {G}[4]{W} Check ngrok Version          {B}║
║ {G}[5]{W} Update Ngrok                 {B}║
║ {G}[6]{W} Start TCP Tunnel             {B}║
║ {G}[7]{W} Start HTTP Tunnel            {B}║
║ {G}[8]{W} Exit                         {B}║
╚══════════════════════════════════╝{W}
""")
        choice = input(f"{C}💻 Select Option: → {W}")
        if choice == "1":
            install_ngrok()
        elif choice == "2":
            token_menu()
        elif choice == "3":
            ngrok_setup()
        elif choice == "4":
            os.system("./ngrok/ngrok version")
            input("\nPress ENTER to return...")
        elif choice == "5":
            update_ngrok()
        elif choice == "6":
            start_tcp()
        elif choice == "7":
            start_http()
        elif choice == "8":
            print(f"{G}🔰 SL Android Official ™{W}")
            print(f"{G}💻 Developer: 𝐈𝐌 𝐂𝐎𝐎𝐋 𝐁𝐎𝐎𝐘 𝓢𝓱𝓪𝓭𝓸𝔀 𝓚𝓲𝓷𝓰{W}")
            exit()
        else:
            print(f"{R}[!] Invalid choice.!{W}")
            time.sleep(1)

menu()
