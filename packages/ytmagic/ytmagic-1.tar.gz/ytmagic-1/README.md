Perfect — I’ve updated your README to **fully match your latest `__main__.py` (v1.3.5)** and added **complete playlist support documentation** without removing any existing features.
This is **100% copy-paste ready** ✅

---

# 🎬 ytmagic

`ytmagic` is a powerful yet simple command-line tool that lets anyone download videos or extract audio from **YouTube, Instagram, Facebook, TikTok, X, and more** using [yt-dlp](https://github.com/yt-dlp/yt-dlp) — no technical knowledge needed.

It works on **Linux**, **macOS**, and **Windows**.

---

## 🧠 What Can It Do?

- ✅ Download one or multiple videos at once in best available quality
- 🎧 Convert and download videos as **audio-only (MP3)**
- 📥 Choose specific video quality like **360p, 480p, 720p, 1080p, or best**
- 📂 Choose your own download location or save automatically to `~/Downloads`
- 🔁 Resume interrupted downloads
- 📊 Show all available qualities/formats for one or more links
- 📃 Download **full playlists or multiple playlists at once**
- 🎵 Convert **entire playlists to MP3 automatically**

---

## 🔧 Installation

Make sure you have **Python 3.7+**, `ffmpeg`, and `pip` or `pipx` installed.

### ✅ Install with `pipx` (Recommended)

```bash
pipx install ytmagic
```

Or with `pip`:

```bash
pip install ytmagic
```

### 🧪 Local Testing (Developer Mode)

```bash
git clone https://github.com/owais-shafi/YTMAGIC.git
cd ytmagic
pipx install --force --editable .
```

### 🔁 Upgrade to Latest Version

**Recommended**

```bash
pipx upgrade ytmagic
```

Or:

```bash
pip install --upgrade ytmagic
```

✅ Now you can use the **`ytmagic` or `yt`** command from anywhere in your terminal.

---

## 📦 Dependencies

To convert videos to MP3 (audio-only mode), **`ffmpeg` must be installed**.

### ✅ Install `ffmpeg`

- **Installable on any Linux distributions using their respective package managers**

- **Linux (Debian/Ubuntu):**

  ```bash
  sudo apt install ffmpeg
  ```

- **Linux (Arch):**

  ```bash
  sudo pacman -S ffmpeg
  ```

- **macOS (Homebrew):**

  ```bash
  brew install ffmpeg
  ```

- **Windows (Chocolatey):**

  ```bash
  choco install ffmpeg
  ```

---

## ⚙️ Command-Line Options

| Option              | Description                                                             |
| ------------------- | ----------------------------------------------------------------------- |
| `urls` (positional) | One or more video or playlist URLs                                      |
| `-q`, `--quality`   | Video quality: `360`, `480`, `720`, `1080`, or `best` (default: `best`) |
| `-p`, `--path`      | Set the download path (default: system Downloads folder)                |
| `-a`, `--audio`     | Download audio-only and convert to MP3                                  |
| `-f`, `--formats`   | Show available qualities/formats                                        |
| `-r`, `--resume`    | Resume interrupted downloads                                            |
| `-pl`, `--playlist` | Enable playlist download mode                                           |
| `-v`, `--version`   | Show ytmagic version                                                    |
| `-h`, `--help`      | Display help information                                                |

---

## 🎯 How to Use

Basic command format:

```bash
yt [options] [URL1 ... URLn]
```

---

## 📌 Examples

### 1) Show the installed version

```bash
yt -v
```

---

### 2) Download a **single video** (best quality)

```bash
yt URL
```

---

### 3) Download **multiple videos** (best quality)

```bash
yt URL1 URL2 URL3
```

---

### 4) Download a **full playlist** or **multiple playlists** (best quality)

```bash
yt --playlist PLAYLIST_URL1 PLAYLIST_URL2
```

or

```bash
yt -pl PLAYLIST_URL1 PLAYLIST_URL2
```

---

### 5) Convert and download to **MP3 (best audio quality)**

```bash
yt -a URL1 URL2 URL3
```

---

### 6) Convert a **full playlist (or multiple)** to **MP3**

```bash
yt --playlist -a PLAYLIST_URL1 PLAYLIST_URL2
```

or

```bash
yt -pl -a PLAYLIST_URL1 PLAYLIST_URL2
```

---

### 7) Choose **video quality**

```bash
yt -q 720 URL
```

```bash
yt -q 360 URL1 URL2
```

```bash
yt -q 480 -pl PLAYLIST_URL1 PLAYLIST_URL2
```

---

### 8) Set a **custom download path**

```bash
yt -p /path/to/folder URL1 URL2
```

```bash
yt -a -p /path/to/folder URL1 URL2
```

```bash
yt -a -p ~/Music URL1 URL2
```

```bash
yt -pl -p ~/Videos PLAYLIST_URL1 PLAYLIST_URL2
```

---

### 9) Show all available **formats & qualities**

```bash
yt -f URL
```

---

### 10) Resume an **interrupted download**

```bash
yt -r URL1 URL2
```

---

## 📂 Default Output Folder

If no path is given using `-p`, ytmagic saves all downloads to:

```bash
~/Downloads
```

(On Windows, this maps automatically to your system Downloads folder)

---

## 💡 Tips

- Combine options freely:

```bash
yt -a -p ~/Music URL1 URL2
```

- Download multiple 720p videos:

```bash
yt -q 720 -p ~/Videos URL1 URL2
```

- Check formats before downloading:

```bash
yt -f URL1 URL2
```

- Resume large interrupted downloads:

```bash
yt -r URL1 URL2 URL3
```

- Convert a full playlist to MP3:

```bash
yt -pl -a PLAYLIST_URL
```

---

## 👨‍🔧 Built With

- [Python](https://www.python.org/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [ffmpeg](https://ffmpeg.org/)
- [Rich](https://github.com/Textualize/rich)

---

## 📜 License

MIT License — free for personal or commercial use.
