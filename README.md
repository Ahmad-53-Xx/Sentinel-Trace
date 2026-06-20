<div align="center">
  <img src="assets/53_logo.png" alt="53 Signature Logo" width="600" style="border-radius: 10px;"/>
  <h1>👁️ Sentinel-Trace</h1>
  <p><b>Advanced Digital Footprint Auditor & OSINT Engine</b></p>

  ![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
  ![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
  ![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
</div>

---

## 📖 Executive Summary
**Sentinel-Trace** is a high-performance, asynchronous OSINT (Open Source Intelligence) tool designed to map the digital footprint of a target username across the web. Built with a modern, dark-mode graphical interface, it translates raw reconnaissance data into an actionable "Privacy Health Score" for the end-user.

## ⚡ Features
* **Asynchronous OSINT Engine:** Utilizes `aiohttp` to poll 15+ target databases and platforms concurrently, reducing scan times from minutes to seconds.
* **Modern GUI:** Built with `CustomTkinter` to provide a sleek, responsive, and standalone desktop experience without freezing during heavy network requests.
* **Privacy Health Algorithm:** Automatically calculates a risk score based on the surface area of exposed profiles.
* **Automated PDF Reporting:** Generates formatted, professional intelligence reports (via `fpdf2`) for offline auditing and remediation tracking.

## 🛠️ Architecture
Sentinel-Trace separates its core logic from its interface:
* `core/username_checker.py` : The multithreaded networking backend.
* `core/report_generator.py` : The dynamic PDF constructor.
* `main.py` : The CustomTkinter frontend and threading coordinator.

## 🚀 Installation & Usage

### Prerequisites
* Python 3.8 or higher.
* Git installed on your system.

### Setup Instructions

**1. Clone the repository:**
```bash
git clone [https://github.com/Ahmad-53-Xx/Sentinel-Trace.git](https://github.com/Ahmad-53-Xx/Sentinel-Trace.git)
cd Sentinel-Trace
```

**2. Install the required dependencies:**
It is recommended to use a virtual environment, but you can install the requirements directly:
```bash
pip install -r requirements.txt
```

**3. Launch the application:**
```bash
python main.py
```
*(Note: Use `python3 main.py` on Linux/macOS environments).*

---

## 🛡️ Security Warning
**Please be aware:** This tool interacts with live public endpoints and APIs. Scanning a high volume of targets rapidly may trigger Web Application Firewalls (WAF) or result in temporary IP bans from the queried platforms. It is highly recommended to use a VPN or proxy network when conducting extensive OSINT research to protect your local IP address.

## ⚖️ Disclaimer & Ethical Use
**Sentinel-Trace** is developed strictly for **defensive auditing, personal privacy management, and academic cybersecurity research**. 

The author assumes absolutely no liability and is not responsible for any misuse, damage, or legal consequences caused by this program. Do not deploy this tool to track, harass, or gather intelligence on individuals without their explicit, documented consent. Users are solely responsible for ensuring their actions comply with all applicable local, state, and federal laws.

---
*Architected and Developed by **Ahmad Abu Zayed***
