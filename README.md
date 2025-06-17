# 🛡Real-Time Threat Intelligence Aggregator (TUI Edition)

A sleek, terminal-based **Real-Time Threat Intelligence Aggregator (RTIA)** built using **Python** and a **TUI (Text-based User Interface)** framework. This tool provides an interactive interface to fetch and monitor IP threat data using the **AbuseIPDB API** — ideal for cybersecurity hobbyists, analysts, or students learning asynchronous Python and terminal UIs.

>  This project emphasizes **TUI experience** over traditional CLI. It is clean, structured, and interactive.

---

##  Features

-  Real-time IP lookup via **AbuseIPDB API**
-  Fully interactive TUI using [`Rich`](https://github.com/Textualize/rich) and [`Typer`](https://github.com/tiangolo/typer)
-  Asynchronous requests with `httpx` and `asyncio`
-  Threat data displayed in rich tables with abuse scores and geolocation
-  Real-time logs and optional data export
-  Modular structure for extensibility

---

##  Screenshot

![image](https://github.com/user-attachments/assets/81bf4969-326e-40c1-a198-fe6b7794473e)

---

## 🔧 Installation

```bash
git clone https://github.com/yourusername/rtia-tui.git
cd rtia-tui
pip install -r requirements.txt
