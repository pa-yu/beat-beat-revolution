# Beat Beat Revolution

> A rhythm-based music game built with Python  
> Created by Paige Yu for class 15-112 at Carnegie Mellon University

---

## Overview

**Beat Beat Revolution** is a music rhythm game where players tap arrow keys in sync with the beat of popular songs.  
Built using Python, the game leverages **audio signal processing**, **real-time input handling**, and **dynamic visuals** to create an interactive and fun gameplay experience.

---

## Features

- **Dynamic beat detection** using `aubio` (real-time onset tracking)
- **Arrow-based gameplay** synced to music tempo
- **Scoring system**: Perfect, Great, Good, Miss, Combo Multipliers
- **Custom visuals and animated UI** with `cmu_112_graphics` and `Pillow`
- **High score saving** and player name input
- Song picker, player selection, pause/resume, and game state handling
- **Upload your own `.mp3` songs** to play with your own music!

---

## Tech Stack

- **Language**: Python 3  
- **Libraries**: `pygame`, `aubio`, `Pillow`, `cmu_112_graphics`  
- **Tools**: Audio analysis, real-time event handling, image processing

---

## Demo

📺 [Watch the gameplay demo on YouTube](https://www.youtube.com/watch?v=h2g2-FHkbgg)

---

## Installation

Follow the steps below to set up and run **Beat Beat Revolution** on your local machine.

---

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/beat-beat-revolution.git
cd beat-beat-revolution
```

> Replace `yourusername` with your actual GitHub username.

---

### 2. Install All Required Python Packages

Use the `requirements.txt` file to install all dependencies:

```bash
pip install -r requirements.txt
```
> If you are using a Mac, you may have to use `pip3` instead.

This installs:
- `aubio` – for beat/onset detection  
- `pygame` – for audio playback  
- `Pillow` – for image processing

---

#### MacOS Users – Having Trouble Installing `pygame`

If you see an error like:

```
/bin/sh: sdl2-config: command not found
```

You need to install SDL2, which `pygame` depends on. Here's how:

1. **Install Homebrew** (if you don’t already have it):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. **Install SDL2 libraries**:
```bash
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
```

3. **Install `pygame` as a binary (not from source)**:
```bash
pip install pygame --only-binary :all:
```
> This may take a while to install

4. **Then install the rest of the requirements**:
```bash
pip install -r requirements.txt --no-deps
```

---

### 3. (Optional) Add Your Own Songs

Upload any `.mp3` file of your choice.  
The file **must be in the song directory** to be recognized during song import.
