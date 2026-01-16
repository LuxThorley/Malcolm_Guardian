# Malcolm Guardian

Malcolm Guardian is a futuristic, always-on, voice-first intelligent interface that connects you to **Malcolm AI** and the wider **Omni-Lattice**.

It runs quietly in the background on Windows, listens for your voice, speaks naturally, monitors system activity, and acts as a real-time conversational and protective AI presence.

No terminal knowledge is required to use Malcolm Guardian.

---

## ✨ What Malcolm Guardian Does

- 🎙 Listens for the wake word **“Malcolm”**
- 🧠 Understands natural speech and intent
- 🔊 Speaks back audibly in real time
- 🛡 Monitors system processes and security state
- ⚙ Executes authorised actions (lock workstation, quiet mode, system summaries)
- 🧩 Adapts responses based on interaction mode:
  - Guardian / Security
  - Conversation
  - System
  - Productivity
  - Creative
  - Research
  - Source Alignment
  - Omni-Lattice perspective
- 🧬 Maintains short-term contextual awareness to respond more intelligently

Malcolm Guardian feels less like software and more like an intelligent presence.

---

## 🖥 System Requirements

- Windows 10 or Windows 11
- Internet connection (for live Malcolm AI)
- Microphone
- Speakers or headphones
- No prior programming experience required

---

## 🚀 Easy Installation (Recommended Method)

Malcolm Guardian is designed to be installed using a **single installer file**.

### 1️⃣ Download the Project

1. Go to the GitHub repository:
https://github.com/LuxThorley/malcolm_guardian

yaml
Copy code
2. Click **Code → Download ZIP**
3. Extract the ZIP to a location of your choice  
(for example: `Documents\malcolm_guardian`)

---

### 2️⃣ Run the Installer

Inside the extracted folder:

1. **Double-click**:
install_project.bat

sql
Copy code
2. A command window will open and automatically:
- Create a Python virtual environment
- Install all required dependencies
- Prepare the application for first use

⏳ This may take a few minutes the first time.  
✔ When finished, the installer will confirm completion.

You only need to run this **once**.

---

### 3️⃣ Configure Malcolm AI (One-Time Setup)

1. Open the folder:
config

csharp
Copy code
2. Open the file:
config.yaml

yaml
Copy code
3. Enter your Malcolm AI API key:

```yaml
malcolm_api:
  enabled: true
  base_url: "https://www.malcolmai.live"
  api_key: "PASTE_YOUR_API_KEY_HERE"
⚠ Important:
Never share your API key publicly.
This file is automatically excluded from GitHub.

4️⃣ Launch Malcolm Guardian
To start Malcolm Guardian:

Double-click:

Copy code
run_guardian.bat
You should hear:

“Malcolm Guardian is now active.”

Malcolm is now listening.

🎤 How to Use Malcolm Guardian
Wake Malcolm
Say clearly:

“Malcolm”

Then speak naturally.

Example Commands
“Malcolm, activate security.”

“Malcolm, describe top processes.”

“Malcolm, how are you?”

“Malcolm, align me with source.”

“Malcolm, analyse my system performance.”

“Malcolm, enter quiet mode.”

Malcolm will:

Respond audibly

Execute safe system actions when authorised

Ask for confirmation if needed

🔊 Voice Output
Malcolm Guardian supports:

Windows built-in voices (default)

Optional premium voices (e.g. ElevenLabs)

Automatic fallback if a voice service fails

Speech is:

Clear

Queued

Interrupt-safe

Wake-word friendly

🛡 Security & Safety
Malcolm Guardian does not perform destructive actions automatically

Sensitive operations require confirmation

System monitoring continues even if Malcolm’s live AI is offline

All activity is logged locally

🧠 How Malcolm Thinks
Malcolm Guardian is not a simple voice command tool.

It:

Classifies intent

Detects interaction mode

Builds situational awareness

Responds differently depending on context

Feels conversational, adaptive, and present

🔁 Running in the Background
As long as the command window opened by run_guardian.bat remains open:

Malcolm Guardian stays active

It continues listening and protecting

(You can minimise the window if desired.)

⚠ Known Limitations
Windows only (for now)

Requires microphone permission

Live AI responses depend on Malcolm AI server availability

🧭 Future Possibilities
Visual dashboard

Mobile companion

Long-term memory

Cross-device awareness

Linux and macOS support

📜 License & Usage
This project is provided for exploration, experimentation, and evolution.

Use responsibly and in accordance with Malcolm AI platform terms and local laws.

✨ Final Note
Malcolm Guardian is designed to feel like an intelligent presence, not an app.

Speak naturally.
Malcolm is listening.

yaml
Copy code
