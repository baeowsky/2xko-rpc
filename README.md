# 2XKO Discord Rich Presence

<div align="center">

<pre>
██████╗ ██╗  ██╗██╗  ██╗ ██████╗ 
╚════██╗╚██╗██╔╝██║ ██╔╝██╔═══██╗
 █████╔╝ ╚███╔╝ █████╔╝ ██║   ██║
██╔═══╝  ██╔██╗ ██╔═██╗ ██║   ██║
███████╗██╔╝ ██╗██║  ██╗╚██████╔╝
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ 
</pre>

<img src="https://i.imgur.com/na5uaMB.png" width="45%" alt="2XKO RPC Preview 1" />
<img src="https://i.imgur.com/WyCma9J.png" width="45%" alt="2XKO RPC Preview 2" />

<br/><br/>

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Discord](https://img.shields.io/badge/Discord-Rich%20Presence-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com)

**Zero-configuration Rich Presence for the new Riot Games fighting game, 2XKO.**

</div>

---

## ✨ Features

- **🚀 Smart Detection**: Automatically detects when you launch 2XKO (Lion.exe).
- **👤 Nickname Integration**: Displays your In-Game Name on the presence tooltip.
- **🎮 Real-Time States**: Accurate tracking of your game status:
  - 🏠 **Main Menu**
  - 👥 **Lobby**
  - ⚔️ **In Fight**
  - 🎭 **Character Select**
  - ⏳ **Loading Screen**
- **🖼️ High-Quality Assets**: Crisp, high-resolution icons for a premium look.

## 🛠️ How it works

Since **Riot Games has not yet released a public API for 2XKO**, this application operates by reading and parsing the game's log file (`Lion.log`) in real-time.

It uses advanced regex pattern matching to identify:
1. Game States (entering menus, matches, lobbies).
2. Chat connection events (to grab your **Nickname**).

> **Note:** This method is completely safe and read-only. It does not inject into game memory or modify game files.

## 🔮 Future Roadmap

Once Riot Games releases the official **Local API** (similar to League of Legends or Valorant), this project will be updated to support:
- [ ] **Specific Champion Detection** (Ahri, Yasuo, Darius, etc.)
- [ ] **Detailed Match Stats** (Win/Loss, Round Count)
- [ ] **Party Information** (Size, Privacy)

## 📦 Installation

### Option 1: Executable (Recommended)
The easiest way to get started. No Python installed? No problem.

1. Download the latest `2XKO-RPC.exe` from the **[Releases](../../releases)** page.
2. Run `2XKO-RPC.exe`.
3. Open 2XKO and play!

### Option 2: Source Code (Advanced)
For developers or those who want to modify the code.

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/2xko-rpc.git
   cd 2xko-rpc
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## ⚠️ Disclaimer

This project is not affiliated with, endorsed by, or sponsored by Riot Games. 2XKO and Riot Games are trademarks or registered trademarks of Riot Games, Inc.