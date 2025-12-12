# LLM File Organizer

**Stop manually organizing files. Let AI do it.**

LLM File Organizer uses LLMs to intelligently categorize and organize your cluttered directories. Point it at your Downloads folder, answer a few questions, and watch years of digital chaos transform into tidy, labeled folders.

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

```
    ╦  ╦  ╔╦╗  ╔═╗┬┬  ┌─┐  ╔═╗┬─┐┌─┐┌─┐┌┐┌┬┌─┐┌─┐┬─┐
    ║  ║  ║║║  ╠╣ ││  ├┤   ║ ║├┬┘│ ┬├─┤││││┌─┘├┤ ├┬┘
    ╩═╝╩═╝╩ ╩  ╚  ┴┴─┘└─┘  ╚═╝┴└─└─┘┴ ┴┘└┘┴└─┘└─┘┴└─

    AI-Powered Filesystem Organizer
```

## 30-Second Quick Start

```bash
# Install
pip install "llm-file-organizer[openai]"

# Set your API key
export OPENAI_API_KEY="sk-..."

# Run it
lfo ~/Downloads
```

That's it. The interactive wizard handles the rest.

---

## Why LLM File Organizer?

| The Problem | The Solution |
|-------------|--------------|
| Downloads folder with 847 files | Organized into logical categories |
| "I'll sort these later" (you won't) | AI sorts them now |
| Random screenshots everywhere | Automatically grouped |
| Project folders mixed with random ZIPs | Projects detected and kept intact |

---

## Installation

```bash
# Pick your AI provider
pip install "llm-file-organizer[openai]"      # gpt-5-mini (default)
pip install "llm-file-organizer[anthropic]"   # Claude
pip install "llm-file-organizer[ollama]"      # Local models (free!)
pip install "llm-file-organizer[all]"         # All of the above
```

### From Source

```bash
git clone https://github.com/moop6535/llm-file-organizer.git
cd llm-file-organizer
pip install -e ".[all,dev]"
```

---

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  Your Downloads Folder                                       │
│  ├── IMG_4521.jpg                                           │
│  ├── quarterly-report-final-v2-FINAL.xlsx                   │
│  ├── react-todo-app/                                        │
│  ├── screenshot 2024-01-15 at 3.42.12 PM.png               │
│  ├── invoice_march.pdf                                      │
│  ├── node_modules.zip  (we've all been there)              │
│  └── ... 200 more files                                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   LLM File Organizer  │
                    │   (AI Magic)  │
                    └───────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  _Organized/                                                 │
│  ├── Files/                                                  │
│  │   ├── Images/                                            │
│  │   │   ├── IMG_4521.jpg                                   │
│  │   │   └── screenshot 2024-01-15 at 3.42.12 PM.png       │
│  │   ├── Documents/                                         │
│  │   │   ├── quarterly-report-final-v2-FINAL.xlsx          │
│  │   │   └── invoice_march.pdf                              │
│  │   └── Archives/                                          │
│  │       └── node_modules.zip                               │
│  └── Folders/                                               │
│      └── Projects/                                          │
│          └── react-todo-app/  (kept intact!)               │
└─────────────────────────────────────────────────────────────┘
```

### What Gets Sent to AI?

**Only filenames and folder names.** Never file contents.

The AI sees: `"quarterly-report-final-v2-FINAL.xlsx"`
The AI categorizes it as: `Documents`

Your data stays on your machine. The AI just reads the labels on the boxes.

---

## Interactive Mode

Run `lfo` with no arguments for the full guided experience:

```
❯ lfo

    ╔═╗╔═╗  ╔═╗┬  ┌─┐┌─┐┌┐┌┌─┐┬─┐
    ╠╣ ╚═╗  ║  │  ├┤ ├─┤│││├┤ ├┬┘
    ╚  ╚═╝  ╚═╝┴─┘└─┘┴ ┴┘└┘└─┘┴└─

    AI-Powered Filesystem Organizer  v0.1.0

┌─────────────────────────────────────────┐
│ Your Organization Plans                  │
├─────────────────────────────────────────┤
│ Directory          Pending  Undoable    │
│ ~/Downloads        1        -           │
│ ~/Desktop          -        1           │
└─────────────────────────────────────────┘

? What would you like to do?
❯ Execute pending plan: ~/Downloads (47 moves)
  Undo last execution: ~/Desktop (23 items)
  View/manage all plans
  ─────────
  Organize a new directory
  Exit
```

### Features of Interactive Mode

- **Status Dashboard** - See all your pending and undoable plans at a glance
- **Tab Completion** - Custom paths support tab completion (finally!)
- **Smart Defaults** - Detects which API keys you have configured
- **Step-by-Step** - Never get lost in a maze of CLI flags

---

## CLI Reference

```
lfo [TARGET] [OPTIONS]

Arguments:
  TARGET                   Directory to organize (default: interactive)

Actions (mutually exclusive):
  -i, --interactive        Interactive mode (default if no target)
  --execute                Classify and move immediately
  --from-plan              Execute saved plan without re-classifying
  --undo                   Undo the last organization

Scan Options:
  -d, --depth N            How deep to scan (0=top, -1=unlimited)
  --no-dirs                Only organize files, not directories
  --flatten                Extract files from subdirs (projects stay intact)
  -f, --filter PRESET      Use a preset filter (see below)
  --ext EXTENSIONS         Only these extensions (comma-separated)
  --min-size SIZE          Minimum file size (e.g., "10MB")
  --max-size SIZE          Maximum file size (e.g., "1GB")

AI Options:
  -p, --provider NAME      openai, anthropic, or ollama
  -m, --model NAME         Specific model (e.g., "gpt-4o", "claude-sonnet-4-20250514")
  --batch-size N           Files per API request (default: 50)

Output:
  -v, --verbose            Show detailed progress
  -q, --quiet              Minimal output
  --version                Show version
```

---

## Examples

### The Basics

```bash
# Interactive mode - the recommended way
lfo

# Organize a specific directory
lfo ~/Downloads

# Execute immediately (skip the review step)
lfo ~/Downloads --execute
```

### Filtering

```bash
# Only images
lfo ~/Pictures --filter images

# Only large files (100MB+)
lfo --filter large_files

# Only files older than a year (digital archaeology)
lfo --filter old_files

# Only specific extensions
lfo --ext "pdf,docx,xlsx"

# Combine size filters
lfo --min-size 10MB --max-size 500MB
```

### Deep Scans

```bash
# Scan 2 levels deep
lfo ~/Projects --depth 2

# Scan everything (brave mode)
lfo ~/Projects --depth -1

# Flatten mode: pull files out of subdirectories
# (Projects like git repos are detected and kept intact)
lfo ~/Projects --depth 2 --flatten
```

### Different AI Providers

```bash
# Use Claude instead of GPT
export ANTHROPIC_API_KEY="sk-ant-..."
lfo --provider anthropic

# Use local Ollama (free, private)
lfo --provider ollama --model llama3.2

# Use a specific model
lfo --provider openai --model gpt-4o
```

### The Two-Step Workflow

```bash
# Step 1: Classify and create a plan (no files move yet)
lfo ~/Downloads

# Step 2: Review the plan
cat ~/.lfo/plans/Users_you_Downloads/plan_*.json

# Step 3: Execute when ready
lfo ~/Downloads --from-plan

# Oops? Undo everything
lfo ~/Downloads --undo
```

---

## Filter Presets

| Preset | What It Matches |
|--------|-----------------|
| `images` | jpg, png, gif, svg, webp, heic, and friends |
| `documents` | pdf, doc, docx, txt, md, rtf, odt |
| `code` | py, js, ts, java, c, cpp, go, rs, rb, php |
| `media` | mp3, mp4, avi, mov, mkv, wav, flac |
| `archives` | zip, tar, gz, rar, 7z, bz2 |
| `large_files` | Anything over 100MB |
| `old_files` | Not modified in over a year |
| `recent_files` | Modified in the last 30 days |

---

## Smart Features

### Project Detection

LLM File Organizer automatically detects project directories and keeps them intact. It looks for:

- Version control: `.git`, `.svn`, `.hg`
- Python: `pyproject.toml`, `setup.py`, `requirements.txt`
- Node.js: `package.json`, `yarn.lock`, `pnpm-lock.yaml`
- Rust: `Cargo.toml`
- Go: `go.mod`
- And many more...

Your `react-app/` folder won't get its files scattered across 15 different categories. It moves as a unit into `Projects/` or `Development/`.

### Smart Classification Mode

By default, LLM File Organizer uses **Smart Mode**:

1. Files with known extensions (`.jpg`, `.pdf`, `.py`, etc.) are auto-classified locally
2. Only unknown/ambiguous files get sent to the AI
3. Saves API costs and speeds things up

Want the AI to classify everything for smarter grouping? Use **Full LLM Mode** in interactive mode.

### Category Consolidation

If the AI gets too creative with categories (looking at you, "Miscellaneous_Data_Files_Various"), LLM File Organizer automatically consolidates similar categories into broader groups.

---

## Configuration

### Environment Variables

| Variable | Required For | Example |
|----------|--------------|---------|
| `OPENAI_API_KEY` | OpenAI | `sk-proj-...` |
| `ANTHROPIC_API_KEY` | Anthropic | `sk-ant-...` |
| `OLLAMA_HOST` | Remote Ollama | `http://192.168.1.100:11434` |

### Using a .env File

Create `.env` in your working directory or home folder:

```bash
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
```

LLM File Organizer loads it automatically.

---

## Safety First

We know you're trusting us with your files. Here's how we keep them safe:

| Feature | What It Does |
|---------|--------------|
| **Dry-run by default** | Running `lfo ~/Downloads` creates a plan but moves nothing |
| **Explicit confirmation** | You must type `yes` before any files move |
| **Undo log first** | The undo log is saved *before* any move happens |
| **No overwrites** | Existing files at destination are skipped |
| **Full undo** | `--undo` restores everything to original locations |
| **Plan history** | All plans are saved with timestamps for your records |

---

## FAQ

### Is my data sent to the cloud?

Only **filenames**. Never file contents. If your file is called `secret_passwords.txt`, the AI will see that name (and probably put it in `Documents/`—you might want to reconsider that filename).

### What if I don't have an API key?

Use Ollama! It runs locally on your machine:

```bash
# Install Ollama (https://ollama.com)
ollama pull llama3.2

# Run LLM File Organizer with Ollama
lfo --provider ollama
```

### Can I customize the categories?

Not yet, but it's on the roadmap. For now, the AI picks categories based on your files, guided by a set of standard categories like `Documents`, `Images`, `Projects`, etc.

### What happens to empty folders after undo?

LLM File Organizer offers to clean them up. You'll be prompted after the undo completes.

---

## Development

```bash
git clone https://github.com/moop6535/llm-file-organizer.git
cd llm-file-organizer

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install with dev dependencies
pip install -e ".[all,dev]"

# Run tests
pytest

# Run linter
ruff check src/
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Contributing

Found a bug? Have an idea? PRs welcome.

Just please don't submit a PR that reorganizes the codebase into 47 micro-modules. We have an AI for that now.
