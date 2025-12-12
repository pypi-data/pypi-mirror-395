# 🚌 WIN CAN TOOL
### Windows CAN-Bus Simulator & Testing Tool
**GUI + CLI • J1939-style messages • Real hardware output • Windows EXE auto-builds**

![License](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![PyPI](https://img.shields.io/pypi/v/win-can-tool.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-purple.svg)

---

## 🚀 Overview
**WIN CAN TOOL** is a CAN-Bus simulator with both a **GUI** and **CLI** interface.
It allows you to:

- simulate engine, GNSS, and vehicle messages
- output CAN traffic to real hardware (ValueCAN, Kvaser, Peak, virtual, ICS, etc.)
- test dashboards, gateways, CDL devices, or software decoders
- run dynamic simulation profiles
- build custom message streams with Python

Every version tag automatically produces a **Windows EXE release**.

---

## 📥 Download the Windows EXE
Latest release:
👉 https://github.com/kfafard/win_can_tool/releases/latest

Download `win_can_tool.zip`, unzip, and run **win_can_tool.exe**.

---

## 📦 Install via PyPI
Prefer the Python version?

```bash
pip install win-can-tool
````

Run GUI:

```bash
win-can-gui
```

Run CLI:

```bash
win-can-cli --interface virtual --channel 0
```

---

## 🖥 GUI Features

* Live GNSS position manipulation
* Real-time engine RPM, hours, speed, load, fuel, temps
* Clean PyQt6 interface
* Status bar + event log
* Auto-generated CAN frames at realistic frequencies
* Selectable python-can backend interface

## 🖥 GUI Preview

### 🌙 Dark Mode
![Dark Mode](assets/gui_dark.png)

### ☀️ Light Mode
![Light Mode](assets/gui_light.png)


---

## 🛠 CLI Usage Example

Send simulated CAN frames over a selected hardware interface:

```bash
win-can-cli --interface neovi --channel 1
```

Run the virtual interface:

```bash
win-can-cli --interface virtual --channel 0
```

---

## 📁 Project Structure

```
win_can_tool/
 ├── bus.py              # CAN interface layer (python-can)
 ├── engine.py           # Engine + GNSS simulation models
 ├── gui.py              # PyQt6 GUI application
 ├── cli.py              # CLI interface
 ├── profiles.py         # Simulation profiles
 ├── can_gui_launcher.py # PyInstaller entrypoint for EXE builds
```

---

## ⚙ Simulation Profiles

Profiles define preset simulation states. Example:

```python
{
    "engine": {"rpm": 1500, "speed_kph": 12.4},
    "gnss":   {"lat": 51.23456, "lon": -102.34567}
}
```

---

## 🔧 Development

Clone the repo:

```bash
git clone https://github.com/kfafard/win_can_tool
cd win_can_tool
```

Install in editable mode:

```bash
pip install -e .
```

Run GUI manually:

```bash
python -m win_can_tool.gui
```

---

## 🏗 Auto-Build Pipeline

GitHub Actions automatically:

1. Builds the EXE using PyInstaller
2. Zips the executable
3. Creates a GitHub Release
4. Uploads the binary

Triggered by pushing a version tag:

```bash
git tag v1.0.9
git push origin v1.0.9
```

---

## 🤝 Contributing

Pull requests and issues are welcome.

---

## 📜 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 📝 Changelog

All notable changes are documented in the [CHANGELOG.md](CHANGELOG.md).

Latest release: **v1.1.0**

---

## ⚡ Credits

Developed by **Kurtis Fafard**
Built for real-world CAN-Bus testing, simulation, and rapid development.
