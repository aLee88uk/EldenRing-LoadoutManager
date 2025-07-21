![Banner](https://i.imgur.com/Fw0TUwe.png)
# Elden Ring Loadout Manager

**Offline Loadout Swapper + Mimic Gear Handler**

Quickly switch between gear sets — and auto-gear your Mimic Tear with a dedicated loadout!  
This standalone Python-based tool provides fast and flexible equipment presets for Elden Ring (v1.16), without modifying game files.

---

## ⚠️ Important Notes

- This tool only works with **Elden Ring version 1.16**
- **Offline use only.** Do **not** use this tool online or in Seamless Co-op.
- Some equipped gear may **not appear visually** in the in-game menu, but **they are applied and working correctly.**

---

## ✅ Features

- Save and load up to **4 gear presets** (armor, weapons, talismans)
- Automatically equip a unique **Mimic Tear preset** during summons
- Fully customizable **keyboard** and **controller hotkeys**
- Toggle which gear slots are saved/loaded (e.g., skip armor)
- Support for unlimited **profiles**, each with its own presets/settings
- Rename, delete, and switch profiles via settings menu
- Remembers the **last used profile** between sessions
- Clean separation of user data in the `Profiles/` directory

---

## 🎮 Default Hotkeys

### Keyboard

| Action              | Key Combination     |
|---------------------|---------------------|
| Save Preset 1–4     | Shift + 1–4         |
| Load Preset 1–4     | Ctrl + 1–4          |
| Save Mimic Preset   | Shift + 0           |

### Controller

| Action              | Button Combo                        |
|---------------------|--------------------------------------|
| Save Preset 1–4     | LT + RT + D-Pad (Up, Right, Down, Left) |
| Load Preset 1–4     | RT + D-Pad (Up, Right, Down, Left)       |
| Save Mimic Preset   | LT + RT + Left Stick Press (LS)          |

> 💡 **Reminder**: To use the Mimic preset swapper, you **must save a preset** using Shift + 0 (keyboard) or RT + LT + LS (controller).  
> The preset will only trigger if **Mimic Tear is in the bottom pouch slot.**

![Mimic Pouch Placement](https://i.imgur.com/cIrcPbZ.png)

---

## 🧪 VirusTotal & False Positives

Some antivirus programs may flag this tool due to the way it's packaged (via PyInstaller).  
This is a known **false positive** — the program does **not** contain any malicious code.

VirusTotal report:  
https://www.virustotal.com/gui/file/1bf6921dd466ad3be7c4f5e5fe5e962dbc52bdda6b59b44cc60dcc909a97f9e7

### Why does this happen?

Many antivirus engines flag **PyInstaller-packed EXEs** due to their dynamic loading behavior, even if the actual script is harmless.

---

## 🔧 Installation

### Option 1: Use the Precompiled EXE

1. Download the latest release from the [Releases](https://github.com/aLee88uk/EldenRing-LoadoutManager/releases) page.
2. Extract and run `EldenRingLoadoutManager.exe`
3. Right-click the tray icon to access settings.


---

### Option 2: Run from Source (Python)

If you're cautious or want to inspect the code:

1. Install [Python 3.11+](https://www.python.org/downloads/)
2. Clone or download this repository
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
