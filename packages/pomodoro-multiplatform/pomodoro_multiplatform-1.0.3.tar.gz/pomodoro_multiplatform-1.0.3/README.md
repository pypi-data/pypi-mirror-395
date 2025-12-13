# Pomodoro Timer

A simple cross-platform Pomodoro timer. Manage work and break cycles with notifications and sound alerts.

## Features

- ✅ Work/break cycles based on the Pomodoro Technique
- ✅ Desktop notifications (Windows/macOS/Linux support)
- ✅ Sound notifications
- ✅ Confirmation prompt after long breaks (continue/quit)
- ✅ Customizable time settings

## Default Settings

- Work time: 25 minutes
- Short break: 5 minutes
- Long break: 15 minutes (every 2 sessions)

## Installation

### Option 1: Install from PyPI (Recommended)

Requires Python 3.8 or higher.

```bash
pip install pomodoro-multiplatform
```

Then run:
```bash
pomodoro
```

### Option 2: Install from Source

```bash
git clone https://github.com/Rito0421/pomodoro.git
cd pomodoro
pip install -r requirements.txt
```

The timer will work without the plyer library, but notifications will be limited to console output.

## Usage

### Basic Usage

**If installed via pip:**
```bash
pomodoro
```

**If running from source (macOS/Linux):**
```bash
chmod +x pomodoro.py
./pomodoro.py
```

**If running from source (Windows):**
```bash
python pomodoro.py
```

### Customization

```bash
# Set 50 min work time and 10 min short break
pomodoro --work 50 --short 10

# Set 20 min long break every 4 sessions
pomodoro --long 20 --every 4
```

If running from source, replace `pomodoro` with `./pomodoro.py` or `python pomodoro.py`.

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--work` | 25 | Work time (minutes) |
| `--short` | 5 | Short break time (minutes) |
| `--long` | 15 | Long break time (minutes) |
| `--every` | 2 | Number of sessions before long break |

### Stopping

Press `Ctrl+C` to stop at any time.

## How It Works

1. Work timer starts (default 25 minutes)
2. Notification and sound alert when work ends
3. Short break (default 5 minutes)
4. After specified number of sessions, long break (default 15 minutes)
5. After long break, choose to continue or quit (macOS: GUI dialog, Windows/Linux: console input)
6. If continuing, return to step 1

## Platform-Specific Features

| Feature | macOS | Windows | Linux |
|---------|-------|---------|-------|
| Notifications | Notification Center (fallback without plyer) | plyer required | plyer required |
| Sound | System sound | Beep | Beep/Terminal bell |
| Confirmation | GUI dialog | Console input | Console input |

## Requirements

- Python 3.6 or higher
- (Recommended) plyer - Install with `pip install plyer`
