# CCswitcher

A CLI tool to easily switch between different API settings for Claude Code. Perfect for when you hit API limits and want to switch to alternative providers like DeepSeek, OpenRouter, or other compatible APIs.

## Installation

Install the package in editable mode:

```bash
pip install -e .
```

## Usage

### Switch to a Profile

Switch to a registered profile (e.g., DeepSeek):

```bash
ccswitcher deepseek
```

This will copy the settings file from your registered path to `~/.claude/settings.json`.

### Switch to Default Claude

Switch back to default Claude settings (removes `settings.json`):

```bash
ccswitcher claude
```

Claude Code uses default settings when `settings.json` doesn't exist.

### Register a New Profile

Register a new API provider profile:

```bash
ccswitcher new deepseek --path='~/.claude/settings_deepseek'
```

This saves the association between the profile name and settings file path in your configuration.

### List All Profiles

View all registered profiles:

```bash
ccswitcher list
```

This shows all profiles with their paths and whether the settings files exist.

## How It Works

1. **Configuration Storage**: Profile mappings are stored in `~/.config/ccswitcher/settings.yml`
2. **Settings Switching**: When you switch profiles, the tool copies the corresponding settings file to `~/.claude/settings.json`
3. **Default Mode**: Switching to "claude" removes `settings.json`, making Claude Code use its default settings

## Example Workflow

1. First, create your alternative API settings file:
   ```bash
   # Create a settings file for DeepSeek
   cat > ~/.claude/settings_deepseek << EOF
   {
     "apiKey": "your-deepseek-api-key",
     "apiEndpoint": "https://api.deepseek.com",
     "model": "deepseek-chat"
   }
   EOF
   ```

2. Register the profile:
   ```bash
   ccswitcher new deepseek --path='~/.claude/settings_deepseek'
   ```

3. Switch between profiles as needed:
   ```bash
   # Use DeepSeek
   ccswitcher deepseek

   # Back to default Claude
   ccswitcher claude

   # Use DeepSeek again
   ccswitcher deepseek
   ```

4. Check your registered profiles:
   ```bash
   ccswitcher list
   ```

## Requirements

- Python >= 3.7
- click >= 8.0.0
- pyyaml >= 5.0.0

## License

MIT
