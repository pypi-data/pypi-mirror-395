# Shell Completion for aws-bedrock-cost-tool

Shell completion enables tab-completion for commands, options, and arguments in your terminal.

## Automatic Installation

Run the installation script:

```bash
./scripts/completion.sh
```

Then restart your terminal or run:
```bash
source ~/.bashrc  # for bash
source ~/.zshrc   # for zsh
```

## Manual Installation

### Bash

Add to your `~/.bashrc`:

```bash
# aws-bedrock-cost-tool shell completion
eval "$(_AWS_BEDROCK_COST_TOOL_COMPLETE=bash_source aws-bedrock-cost-tool)"
```

### Zsh

Add to your `~/.zshrc`:

```bash
# aws-bedrock-cost-tool shell completion
eval "$(_AWS_BEDROCK_COST_TOOL_COMPLETE=zsh_source aws-bedrock-cost-tool)"
```

### Fish

Add to `~/.config/fish/completions/aws-bedrock-cost-tool.fish`:

```fish
_AWS_BEDROCK_COST_TOOL_COMPLETE=fish_source aws-bedrock-cost-tool | source
```

## Activation

After adding the completion line to your shell configuration:

1. **Restart your terminal**, or
2. **Source your configuration file**:
   ```bash
   source ~/.bashrc  # bash
   source ~/.zshrc   # zsh
   ```

## Usage

Once installed, you can use tab completion:

```bash
# Tab complete commands
aws-bedrock-cost-tool --<TAB>

# Tab complete options
aws-bedrock-cost-tool --period <TAB>

# Complete detail levels
aws-bedrock-cost-tool --detail <TAB>
```

## Troubleshooting

### Completion not working

1. **Verify installation**:
   ```bash
   grep "aws-bedrock-cost-tool" ~/.bashrc  # or ~/.zshrc
   ```

2. **Check if tool is in PATH**:
   ```bash
   which aws-bedrock-cost-tool
   ```

3. **Reload shell configuration**:
   ```bash
   source ~/.bashrc  # or ~/.zshrc
   ```

### Bash version requirements

- Requires Bash 4.4 or higher
- Check version: `bash --version`

## Uninstallation

Remove the completion line from your shell configuration file:

```bash
# Remove from ~/.bashrc or ~/.zshrc
sed -i '/aws-bedrock-cost-tool shell completion/,+1d' ~/.bashrc
```

Or manually edit the file and remove:
```bash
# aws-bedrock-cost-tool shell completion
eval "$(_AWS_BEDROCK_COST_TOOL_COMPLETE=...)"
```

---

**Note**: This completion is built on Click's native shell completion support.
