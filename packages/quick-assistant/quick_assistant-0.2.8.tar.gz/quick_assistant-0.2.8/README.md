## Quick Assistant

CLI tool for productivity, focused on quick daily operations.

### Installation

```bash
# Recommended (isolated environment)
pipx install quick-assistant

# Or via pip
pip install quick-assistant
```

### Windows Users

After `pipx install quick-assistant`, if `quick` is not recognized:

**Step 1: Add pipx bin to PATH**
```powershell
pipx ensurepath
```

**Step 2: Restart your terminal completely**

Close and reopen PowerShell/CMD. A new tab is NOT enough - close the entire window.

**Step 3: Verify**
```powershell
quick doctor
```

**Alternative: Run directly without PATH**

If you can't restart or modify PATH, use the full path:
```powershell
# pipx installation location
%USERPROFILE%\.local\bin\quick.exe doctor
%USERPROFILE%\.local\bin\quick.exe commit
```

### Requirements

**Option 1: Run setup (recommended)**
```bash
quick setup
```

**Option 2: Environment variable (for CI/CD)**
```bash
export GOOGLE_API_KEY="your-api-key"
```

Get your API key at: https://aistudio.google.com/apikey

### Setup

On first run, Quick Assistant will guide you through setup:

```bash
quick setup
```

**Configuration includes:**
- **Commit convention** - Choose your preferred style:
  - Conventional Commits (`feat:`, `fix:`, `refactor:`, etc.)
  - Imperative (simple verbs: `add`, `fix`, `update`)
  - Custom template (with `{diff}` placeholder)
- **API key** - Your Google Gemini API key

Configuration is saved to `~/.quick-assistant/config.json`.

### Commands

#### Setup
Configure Quick Assistant with your API key and commit style preferences.
```bash
quick setup
```

#### Commit
AI-powered git commit message generation with interactive flow.
```bash
quick commit
```

#### Doctor
Diagnose installation and PATH issues (especially helpful on Windows; it checks the `Scripts` and `pipx` paths).
```bash
quick doctor
```

### Features
- Fast AI-powered responses
- Colored and organized output
- Compatible with Windows, macOS, Linux
- Informative error messages

### Examples
- `quick setup` - Configure API key and commit style
- `quick commit` - Generate AI commit message
- `quick update` - Update to latest version
- `quick doctor` - Diagnose installation issues (Windows PATH)

### Uninstall

```bash
# If installed with pipx
pipx uninstall quick-assistant

# If installed with pip
pip uninstall quick-assistant
```
