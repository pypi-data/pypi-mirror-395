# NGROK Auto Installer & Manager

![cool booy](https://i.ibb.co/YBRz0pfh/IMG-20251206-010358.jpg)


🔰 SL Android Official ™ 🇱🇰

💻 Developer: 𝐈𝐌 𝐂𝐎𝐎𝐋 𝐁𝐎𝐎𝐘 𝓢𝓱𝓪𝓭𝓸𝔀 𝓚𝓲𝓷𝓰

[![Telegram](https://img.shields.io/badge/Telegram-Contact-blue?logo=telegram)](https://t.me/@imcoolbooy)

---
**Description:**

This Python script is designed for Termux and Linux systems to automatically install Ngrok, manage Ngrok tokens, start tunnels, and update Ngrok. The script provides a user-friendly menu with a colored CLI interface for better usability.

![Linux](https://img.shields.io/badge/Linux-compatible-orange?logo=linux)
---

---
### 🔗 How to Get Your Ngrok Token

1. Visit the official Ngrok website: (https://dashboard.ngrok.com)

2. Sign up for a free account or log in if you already have one.

3. After logging in, go to the "Auth" or "Your Authtoken" section.

4. Copy your authtoken string.

5. Paste this token into the **Enter New Ngrok Token** option in the script menu.

**Note:** The token is required to authenticate your tunnels and access free or paid Ngrok services.

---

---

## 📝 Main Menu Options & Effects

![cool booy](https://i.ibb.co/d429S7hZ/IMG-20251206-011523-375.jpg)

### 1️⃣ Install NGROK

- **Effect when selected:**

  - Detects your system OS and CPU architecture.

  - Downloads the correct Ngrok binary for your device.

  - Extracts and makes the binary executable.

  - After this, you can run Ngrok tunnels (`tcp` or `http`) from the script.

- **Outcome:** Ngrok becomes ready to use for creating tunnels without manual installation.

---

---
![cool booy](https://i.ibb.co/tp8GQYzw/IMG-20251206-010449.jpg)


### 2️⃣ Ngrok Token Manager

- **Effect when selected:**

  - Provides options to **enter, view, or delete** your Ngrok token.


#### 1) Enter New Ngrok Token


- Prompts for token input.

- Validates the token via Ngrok CLI.

- Saves the token internally for future tunnel usage.

- **Outcome:** You can now create authenticated Ngrok tunnels.


#### 2) View Saved Token


- Displays the currently saved token.

- **Outcome:** Confirms which token is active.


#### 3) Delete Saved Token


- Deletes the stored token.

- **Outcome:** Script no longer has an active token; Ngrok tunnels won't work until a new token is set.

---

---
![cool booy](https://i.ibb.co/4g5jS8wd/IMG-20251206-010530.jpg)

### 3️⃣ Ngrok Setup

- **Effect when selected:**

  - Automatically sets the `USER` environment variable in shell sessions.

- **Outcome:** Future scripts or commands using this variable run smoothly in Termux.

---

---

### 4️⃣ Check Ngrok Version

- **Effect when selected:**

  - Runs Ngrok to display its current version.

- **Outcome:** You can verify which Ngrok version is installed.

---

---

### 5️⃣ Update Ngrok

- **Effect when selected:**

  - Detects system architecture.

  - Downloads the latest Ngrok binary.

  - Replaces the existing binary with the updated version.

- **Outcome:** Always have the latest Ngrok features and fixes.

---

---

### ⚡ Important Note Before Starting a Tunnel

• Before you start a TCP or HTTP tunnel using this script:

1. **Ensure the service you want to expose is running on your local machine.**

   - For example:

     - If you want to start an HTTP tunnel on port 8080, make sure your web server is active on `localhost:8080`.

     - If you want to start a TCP tunnel on port 3306, ensure your database or service is listening on that port.

2. **Do not start a tunnel on a port that is already in use.**

   - Ngrok cannot bind to a port that is occupied by another service.

3. **Check your firewall or security settings.**

   - Make sure your firewall allows connections to the port you want to expose.

4. **Why this is important:**

   - Ngrok tunnels only forward traffic to an active host port.

   - If the port is not active or the service is not running, the tunnel will appear to work but no traffic will reach your service.

---

---

### 6️⃣ Start TCP Tunnel

- **Effect when selected:**

  - Prompts for a local TCP port.

  - Opens a public TCP tunnel to that port.

- **Outcome:** Any service on that port becomes accessible from the internet.

---

---

### 7️⃣ Start HTTP Tunnel

- **Effect when selected:**

  - Prompts for a local HTTP port.

  - Opens a public HTTP tunnel to that port.

- **Outcome:** Local web servers or applications become accessible from the internet.

---

---

### 8️⃣ Exit

- **Effect when selected:**

  - Prints a goodbye message.

  - Ends the script.

- **Outcome:** Script terminates safely and returns control to the terminal.

---

---

### 📦 Requirements

This tool uses only Python’s built-in modules:

- `os`

- `platform`

- `urllib.request`

- `zipfile`

- `sys`

- `time`

- `subprocess`

✔ **No external pip modules are required.**

✔ Works on Python **3.8+ (recommended: 3.10+)**

## ⚡ install

```
pip install IM-COOL-BOOY-NGROK
```

```
IM-COOL-BOOY-NGROK
```
---

📌 License

MIT License © 2025 𝐈𝐌 𝐂𝐎𝐎𝐋 𝐁𝐎𝐎𝐘 𝓢𝓱𝓪𝓭𝓸𝔀 𝓚𝓲𝓷𝓰

[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
