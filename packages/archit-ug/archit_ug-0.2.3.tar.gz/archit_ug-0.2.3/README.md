# Errol 4 Sonic – 120B Formal Interactive AI Library

`archit_ug` is a lightweight Python library that provides an interactive chat interface powered by the Errol 4 Sonic 120B LLM.  
It includes built-in streaming, colored terminal output, automatic API key loading, and a clean developer-friendly workflow.

## Features
- 🔥 Streaming chat completions  
- 🎨 Colored terminal output  
- 🔑 Auto-load Cerebras API key  
- 🧠 Lightweight wrapper around Cerebras SDK  
- 📝 Easy to extend for custom AI agents  

# Changelog

## 0.2.3
- Fixed README.md bug
- Fixed Project description bug

## 0.2.2
- Added README.md
- Added project description

## 0.2.1
- Put CHANGES.md into MANIFEST.in
- Fixed major CHANGES.md bug

## 0.2.0
- Added CHANGES.md support
- Changes and refreshed pyproject file
- Fixed minor bugs
- First use of release.sh

## 0.1.9
- Fixed missing color output (Fore.RED not showing in Jupyter)
- Fixed file path for API key loader
- Improved library detection logic

## 0.1.8
- Added cerebras_key.txt support inside package
- Improved packaging with MANIFEST.in

## 0.1.7
- Improved core.chat behavior and fixed minor bugs

## 0.1.6
- Published initial working version of library

# Installation
```python
from archit_ug import start_chat
start_chat()