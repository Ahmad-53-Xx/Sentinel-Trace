# 👁️ Sentinel-Trace: Digital Footprint Auditor

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

**Sentinel-Trace** is a high-performance, asynchronous OSINT (Open Source Intelligence) tool designed to map the digital footprint of a target username across the web. Built with a modern, dark-mode graphical interface, it translates raw reconnaissance data into an actionable "Privacy Health Score" for the end-user.

---

## ⚡ Features

* **Asynchronous OSINT Engine:** Utilizes `aiohttp` to poll 15+ target databases and platforms concurrently, reducing scan times from minutes to seconds.
* **Modern GUI:** Built with `CustomTkinter` to provide a sleek, responsive, and standalone desktop experience without freezing during heavy network requests.
* **Privacy Health Algorithm:** Automatically calculates a risk score based on the surface area of exposed profiles.
* **Automated PDF Reporting:** Generates formatted, professional intelligence reports (via `fpdf2`) for offline auditing and remediation tracking.

## 🛠️ Architecture

Sentinel-Trace separates its core logic from its interface:
* `core/username_checker.py`: The multithreaded networking backend.
* `core/report_generator.py`: The dynamic PDF constructor.
* `main.py`: The CustomTkinter frontend and threading coordinator.

## 🚀 Installation & Usage

### Prerequisites
* Python 3.8 or higher.

### Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/Ahmad-53-Xx/Sentinel-Trace.git](https://github.com/Ahmad-53-Xx/Sentinel-Trace.git)
   cd Sentinel-Trace
