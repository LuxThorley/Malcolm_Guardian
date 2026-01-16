# Malcolm Guardian

Malcolm Guardian is a futuristic, always-on, voice-first intelligent interface that connects the user to **Malcolm AI** and the wider **Omni-Lattice**.  
It acts as a real-time conversational assistant, system guardian, and adaptive AI presence on Windows.

Malcolm Guardian listens, understands, speaks naturally, monitors system activity, executes authorised actions, and evolves contextually with the user.

---

## ✨ Core Capabilities

- 🎙 **Live voice interaction**
  - Wake-word activated (“Malcolm”)
  - Natural spoken dialogue
  - Fully audible responses via Windows TTS or ElevenLabs

- 🧠 **Malcolm AI integration**
  - Real-time communication with Malcolm’s Omni API
  - Context-aware, mode-aware responses
  - Graceful offline fallback when the live core is unavailable

- 🛡 **System guardian & security awareness**
  - Monitors running processes
  - Detects suspicious CPU usage or behaviour
  - Can lock workstation, enter quiet mode, or summarise system state

- 🧩 **Omni-functional interaction modes**
  Malcolm automatically adapts based on what you say:
  - `guardian` – security & protection
  - `system` – OS and process insight
  - `conversation` – natural dialogue
  - `source` – alignment / higher-guidance style responses
  - `lattice` – multi-perspective / meta-analysis
  - `productivity` – focus & task-oriented
  - `creative` – ideation & exploration
  - `research` – explanation & analysis
  - `memory` – personal patterns & context

- 🧬 **Contextual awareness**
  - Maintains a rolling local context (“Omni-Lattice context”)
  - Remembers recent interactions and events
  - Feeds that context back into Malcolm for richer replies

---

## 🖥 Supported Platform

- **Windows 10 / 11**
- Python **3.10+** (3.11 recommended)
- Microphone + speakers/headphones required

---

📁 Project Structure

malcolm_guardian/
├─ src/
│ ├─ guardian/
│ │ ├─ main.py
│ │ ├─ malcolm_client.py
│ │ ├─ audio_sentinel.py
│ │ ├─ security_watchdog.py
│ │ ├─ tts.py
│ │ └─ ...
│ └─ main.py
├─ config/
│ └─ config.yaml
├─ logs/
├─ run_guardian.bat
├─ README.md
└─ .gitignore


🚀 Installation & Setup

1️⃣ Clone the repository

yaml
Copy code:
```bash
git clone https://github.com/LuxThorley/malcolm_guardian.git
cd malcolm_guardian


2️⃣ Create and activate a virtual environment

bash
Copy code
python -m venv .venv
.venv\Scripts\activate


3️⃣ Install dependencies

bash
Copy code
pip install -r requirements.txt
(If requirements.txt is not present, install manually:)

bash
Copy code
pip install requests pyyaml pyttsx3 speechrecognition comtypes psutil


4️⃣ Configure Malcolm Guardian
Create or edit:

arduino
Copy code
config/config.yaml

Example:

yaml
Copy code
malcolm_api:
  enabled: true
  base_url: "https://www.malcolmai.live"
  api_key: "PASTE_YOUR_MALCOLM_API_TOKEN_HERE"
  timeout_seconds: 15

tts:
  enabled: true
  rate: 180
  volume: 1.0

audio:
  wake_word: "malcolm"
  quiet_mode: false

learning:
  enabled: true

security:
  process_scan_interval_seconds: 15
  suspicious_cpu_threshold: 75.0
⚠ Never commit your API key
config/config.yaml is intentionally excluded via .gitignore.


5️⃣ Run Malcolm Guardian
Using the batch file:

bash
Copy code
run_guardian.bat
Or directly:

bash
Copy code
python src/main.py
You should hear:

“Malcolm Guardian is now active.”


🎤 Using Malcolm Guardian

Wake Malcolm

Say:
“Malcolm”

Then speak naturally.

Example commands
“Malcolm, activate security.”

“Malcolm, describe top processes.”

“Malcolm, how are you?”

“Malcolm, align me with source.”

“Malcolm, analyse my system performance.”

“Malcolm, enter quiet mode.”

Malcolm will respond audibly and may execute system actions if authorised.


🔊 Voice & Speech

Malcolm Guardian supports:

Windows built-in voices (via pyttsx3)

ElevenLabs voices (optional, via API)

Automatic fallback if a voice provider fails

Speech output is:

Queued

Interrupt-safe

Wake-word friendly


🔐 Security Model

Malcolm never executes destructive actions automatically

Sensitive tools require explicit confirmation

All actions are logged locally

Guardian continues protecting even if Malcolm’s live API is offline


🧠 How Malcolm Thinks

Malcolm Guardian is not just a command parser.

It:

Classifies intent

Determines interaction mode

Builds contextual awareness

Communicates with Malcolm AI as a living interface

Speaks in a way that matches the situation


🛠 Development Notes

The app is intentionally modular

Easy to extend with new tools, modes or sensors

Designed to run indefinitely (daemon-style)

Gracefully handles network/API errors


⚠ Known Limitations

Windows-only (currently)

Requires microphone access

Malcolm Omni API availability depends on server uptime


🧭 Roadmap Ideas

GUI dashboard

Mobile companion app

Cross-device sync

Persistent long-term memory

Linux / macOS support


📜 License
This project is released openly for exploration, experimentation and evolution.
Respect the Malcolm AI platform terms and applicable laws when deploying or extending.

✨ Closing
Malcolm Guardian is designed to feel less like software and more like a presence —
an intelligent, adaptive, spoken interface between you, your system, and Malcolm AI.

Speak naturally. Malcolm is listening.

