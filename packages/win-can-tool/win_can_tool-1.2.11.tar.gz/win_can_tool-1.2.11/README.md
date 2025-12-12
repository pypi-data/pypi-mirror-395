# win_can_tool

A lightweight, Windows‑focused CAN message generator and simulation tool.

This project provides a simple GUI for sending repeating CAN messages using selectable profiles.  
It is designed primarily for agricultural CANbus development, CDL gateway testing, bench simulations, and rapid prototyping.

---

## ⭐ Features
- Clean Windows GUI (PyQt6)
- Select CAN interface:
  - **Virtual CAN (python-can built‑in virtual bus)**
  - **ValueCAN4** (verified)
- Load prebuilt CAN message profiles
- Live message editing (ID, DLC, hex bytes)
- Adjustable send frequency
- Console log for events and message prints
- Light/Dark theme assets included

---

## 🖥️ Running the Application

### **Option 1 — Use the EXE (Recommended)**
Download the latest release from GitHub:

```
win_can_tool.exe
```

Run it directly — no Python install required.

---

### **Option 2 — Run From Source**
```bash
pip install -r requirements.txt
python -m win_can_tool.gui
```

---

## 🧩 Project Layout
```
win_can_tool/
  bus.py
  cli.py
  engine.py
  gui.py
  profiles.py
  version.py
assets/
  gui_dark.png
  gui_light.png
win_can_tool.ico
```

---

## 📦 Releases
Every tagged version automatically builds:
- PyPI package
- Windows EXE
- CHANGELOG
- GitHub Release with artifacts

Tag format:
```
v1.2.8
```

---

## 🤝 Contributing
See **CONTRIBUTING.md** for full guidelines.

## 🛠 Development Details
See **DEVELOPMENT.md** for deep-dive architecture and internals.
