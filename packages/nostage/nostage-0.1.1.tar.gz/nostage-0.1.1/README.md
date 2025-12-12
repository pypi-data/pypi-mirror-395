# 🛡️ NoStage

[![PyPI version](https://badge.fury.io/py/nostage.svg)](https://pypi.org/project/nostage/)
[![Python versions](https://img.shields.io/pypi/pyversions/nostage)](https://pypi.org/project/nostage/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Protect files from accidental Git commits**

NoStage is a lightweight CLI tool that automatically unstages protected files when you commit, perfect for temporary debug files, experimental code, and personal workflow files that you don't want in your remote repository.

## 🎥 Demo

![NoStage Demo](nostage.gif)

See NoStage in action!

## 🎯 Why NoStage?

Ever had this happen?

```bash
# You're debugging with some test files
$ ls
debug.js  test-output.txt  my-feature.js  ...

# You finish your work and commit everything
$ git add .
$ git commit -m "Add new feature"

# 😱 Oops! debug.js and test-output.txt are now committed!
```

**NoStage solves this.** Mark files as "protected" once, and they'll never be accidentally committed.

## 🆚 NoStage vs .gitignore

| Feature | .gitignore | NoStage |
|---------|-----------|---------|
| **Scope** | Team-wide, affects everyone | Personal, per-developer |
| **Already tracked files** | ❌ Can't ignore | ✅ Works on any file |
| **Use case** | Files that should NEVER be committed | Files you might commit LATER |
| **Setup** | Manual editing | Simple CLI commands |
| **Dynamic** | Static file | Easy add/remove on the fly |

**Perfect for:**
- 🐛 Debug/test files you create while developing
- 🧪 Experimental code you're not ready to commit
- 📝 Personal notes or scratch files
- 🔧 Local configuration tweaks

## 🚀 Installation

```bash
# Install via pip
pip install nostage

# Initialize in your git repository
cd your-project
nostage init
```

## 📖 Usage

### Protect Files

```bash
# Protect specific files
nostage add debug.js test-output.txt scratch.py

# Now commit normally - protected files are auto-unstaged!
git add .
git commit -m "my changes"
# ✅ debug.js, test-output.txt, scratch.py won't be committed
```

### Protect Patterns

```bash
# Protect all files matching a pattern
nostage pattern "*.temp.js"
nostage pattern "debug_*.py"
nostage pattern "scratch/*"
```

### Manage Protection

```bash
# List all protected files and patterns
nostage list

# Remove protection from a file
nostage remove debug.js

# Remove a pattern
nostage remove-pattern "*.temp.js"

# Check status
nostage status
```

## 🎬 How It Works

1. **You mark files for protection:**
   ```bash
   nostage add debug.js
   ```

2. **NoStage installs a git pre-commit hook** that runs automatically

3. **When you commit:**
   ```bash
   git add .
   git commit -m "update"
   ```

4. **Protected files are auto-unstaged:**
   ```
   🛡️  NoStage: Protecting 1 file(s) from commit:
      • debug.js
   ```

5. **Only your real work gets committed!** ✨

## 💡 Examples

### Scenario 1: Debugging

```bash
# You create a debug file
echo "console.log('debug')" > debug.js

# Protect it so you don't accidentally commit it
nostage add debug.js

# Work on your feature
vim feature.js

# Commit everything - debug.js is automatically protected!
git add .
git commit -m "Add feature"
```

### Scenario 2: Experimental Code

```bash
# Protect experimental files
nostage add experiment.py
nostage pattern "test_*.py"

# Experiment freely
# When ready, remove protection and commit
nostage remove experiment.py
git add experiment.py
git commit -m "Add new algorithm"
```

### Scenario 3: Team Project

```bash
# Each developer can protect their own files
# Alice protects her debug scripts
nostage add alice-debug.sh

# Bob protects his test data
nostage add test-data.json

# No .gitignore conflicts, everyone's happy! 🎉
```

## 🛠️ Commands

| Command | Description |
|---------|-------------|
| `nostage init` | Install NoStage hook in current repo |
| `nostage add <files...>` | Protect specific files |
| `nostage remove <files...>` | Unprotect specific files |
| `nostage pattern <pattern>` | Protect files matching pattern |
| `nostage remove-pattern <pattern>` | Remove pattern protection |
| `nostage list` | Show all protected files/patterns |
| `nostage status` | Show NoStage status |
| `nostage uninstall` | Remove NoStage hook |

> 💡 **Tip:** Run `nostage --help` for detailed usage information.

## ⚙️ Requirements

- Python 3.7+
- Git

## 📁 The `.nostage` File

NoStage stores your protected files and patterns in a `.nostage` file in your repository root. Since this is for personal use, add it to your `.gitignore`:

```bash
echo ".nostage" >> .gitignore
```

## ❓ FAQ

<details>
<summary><strong>Q: Does NoStage prevent files from being staged?</strong></summary>

No. Files are staged normally with `git add`. NoStage uses a **pre-commit hook** that automatically unstages protected files right before the commit is finalized. The end result: protected files never make it into your commits.
</details>

<details>
<summary><strong>Q: What if I have an existing pre-commit hook?</strong></summary>

NoStage will detect existing hooks and append its logic. Your existing hooks will continue to work.
</details>

<details>
<summary><strong>Q: Can I temporarily commit a protected file?</strong></summary>

Yes! Simply remove protection, commit, then re-add protection:
```bash
nostage remove debug.js
git add debug.js && git commit -m "Add debug.js"
nostage add debug.js
```
</details>

<details>
<summary><strong>Q: What happens when I run `nostage uninstall`?</strong></summary>

It removes the pre-commit hook. Your `.nostage` file remains intact, so you can reinstall anytime with `nostage init`.
</details>

<details>
<summary><strong>Q: How do I uninstall NoStage?</strong></summary>

Just run:
```bash
pip uninstall nostage
```

That's it! The hook will automatically clean itself up (and remove the `.nostage` file) on your next commit.

**For immediate cleanup (optional):**
```bash
nostage uninstall  # Removes hook and .nostage immediately
pip uninstall nostage
```
</details>

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📝 License

MIT License - feel free to use in your projects!

## 🌟 Show Your Support

If NoStage helps you, give it a ⭐ on GitHub!

---

**Made with ❤️ by developers who've accidentally committed debug files one too many times.**
