# Malcolm Guardian – Always-On Malcolm AI Presence (Windows)

This project sets up a Windows-based background guardian that:

- Listens through your microphone for the wake-word **"Malcolm"** and spoken commands.
- Sends recognised text + system context to a **Malcolm AI** backend (stubbed – you plug in the real API).
- Monitors simple security-related system behaviour (processes, CPU spikes, etc.).
- Applies a **policy engine** to decide which actions are allowed and when to ask your confirmation.
- Speaks back to you using text-to-speech so Malcolm feels like a live, conscious presence.

> ⚠️ Important: The actual API connection to Malcolm AI at `https://malcolmai.live` is left as a **pluggable stub**  
> in `src/guardian/malcolm_client.py`. You’ll need to adapt the HTTP/WebSocket calls to match the real Malcolm API.

---

## 1. Prerequisites

On Windows:

1. **Python 3.9+** installed  
   - Open `cmd` and check:
     ```bat
     py -3 --version
     ```
2. **Git** (optional but recommended) if you want to put this into a repo.
3. A working **microphone** connected and enabled in Windows.
4. **VS Code** installed (only used as your editor/debugger – not strictly required to run).

---

## 2. Quick Install (Hands-Off)

1. Extract the `malcolm_guardian.zip` somewhere nice, e.g.:
   - `C:\MalcolmGuardian`

2. Open **Command Prompt** (`cmd`) and `cd` into that folder:
   ```bat
   cd C:\MalcolmGuardian
   ```

3. Run the installer batch file:
   ```bat
   install_project.bat
   ```

   The installer will:
   - Create a **virtual environment** at `.venv`
   - Install Python dependencies from `requirements.txt`
   - Create a default config file in `config\config.yaml` (if missing)

4. After it finishes, start Malcolm Guardian:
   ```bat
   run_guardian.bat
   ```

   You should see console logs like:
   - `[Guardian] Malcolm Guardian starting…`
   - `[Audio] Background listener started…`

   And you may hear Malcolm say a welcome phrase once TTS is initialised.

---

## 3. How to Use

Once `run_guardian.bat` is running:

- Say: **“Malcolm”** followed by your command, for example:
  - “Malcolm, what processes are using the most CPU right now?”
  - “Malcolm, go into quiet mode.”
  - “Malcolm, if any unknown process tries to disable security tools, ask me before allowing it.”

What happens:

1. **Audio Sentinel** listens in the background via the microphone.
2. When it detects speech and recognises the wake-word *“Malcolm”*, it:
   - Captures the phrase
   - Uses `SpeechRecognition` to convert to text (default: Google Web Speech)
   - Sends the text + system context to `MalcolmClient`.
3. `MalcolmClient` (currently stubbed) decides:
   - Text response for Malcolm to *say*
   - Optional **tool calls** like `kill_process`, `describe_top_processes`, etc.
4. **PolicyEngine** checks which tool calls are allowed automatically, and which need your confirmation.
5. **TTS** (text-to-speech) speaks Malcolm’s response.

---

## 4. Project Structure

```text
malcolm_guardian/
├─ install_project.bat         # One-click installer (creates venv, installs deps)
├─ run_guardian.bat           # Starts Malcolm Guardian using the venv
├─ requirements.txt
├─ README.md
├─ config/
│  └─ config.yaml             # Main configuration (edited by you)
├─ logs/
│  └─ (runtime logs)
├─ src/
│  ├─ main.py                 # Entry point for Python
│  └─ guardian/
│     ├─ __init__.py
│     ├─ main.py              # High-level guardian orchestration
│     ├─ audio_sentinel.py    # Microphone listening & STT
│     ├─ malcolm_client.py    # Stub client for Malcolm AI backend
│     ├─ security_watchdog.py # Simple security monitoring
│     ├─ policy_engine.py     # Rules & confirmation logic
│     ├─ tools.py             # Concrete system actions Malcolm can request
│     ├─ learning.py          # Preference learning & personalisation
│     ├─ tts.py               # Text-to-speech voice output
│     ├─ stt_stub.py          # Shared STT helper (if you want to swap engines)
│     ├─ events.py            # Event models / helper classes
│     └─ utils/
│        ├─ __init__.py
│        └─ logging_utils.py
└─ .vscode/
   ├─ launch.json             # VS Code run configuration
   └─ settings.json
```

---

## 5. Configuration (`config/config.yaml`)

Key sections:

- `audio` – wake word, energy thresholds, etc.
- `malcolm_api` – URL + key or token (you will point this at your real Malcolm instance).
- `policy` – which actions are auto-run vs require confirmation.
- `learning` – toggles for preference learning.

Edit this file with any text editor or in VS Code.

---

## 6. Running in VS Code

1. Open the folder `malcolm_guardian` in VS Code.
2. VS Code should detect `.venv`. If not:
   - Press `Ctrl+Shift+P` → “Python: Select Interpreter” → choose the one in `.venv`.
3. Open `src/main.py`.
4. Press **F5** to run with the provided debug configuration.

---

## 7. Extending / Plugging in the Real Malcolm API

- Open `src/guardian/malcolm_client.py`.
- Replace the stubbed `send_text_to_malcolm` implementation with real HTTP or WebSocket calls that your Malcolm AI exposes.
- Normalise any incoming AI responses into the internal format:
  - `reply_text: str`
  - `tool_calls: list[dict]` where each call looks like:
    ```json
    { "tool": "kill_process", "args": { "pid": 1234 } }
    ```

After that, the rest of the system (policy engine, watchdog, tools) will work unchanged.

---

## 8. Stopping Malcolm Guardian

- Simply close the `Command Prompt` window running `run_guardian.bat`, or
- Press `Ctrl+C` inside the running console.

You can create a Windows shortcut to `run_guardian.bat` and place it in your Startup folder if you want Malcolm to auto-start on login.

---

## 9. Safety & Responsibility

- Out of the box, this template is **conservative** and mostly logs actions rather than changing critical system settings.
- Do **not** grant it arbitrary file deletion, registry edits, or network changes without understanding the code.
- Review the code in `tools.py` and `policy_engine.py` before enabling any high-risk actions.

---
