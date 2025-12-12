![GitHub forks](https://img.shields.io/github/forks/2kDarki/Habitrax?style=social)
![GitHub stars](https://img.shields.io/github/stars/2kDarki/Habitrax?style=social)

# Habitrax

A terminal-based personal development tracker combining habit building, productivity, and introspection into one unified system.

--- 

## What is Habitrax? 

Habitrax is a CLI app designed to help you:

- Track your tasks, productivity, and self-discipline
- Reflect daily with randomized deep questions 
- Monitor progress using gamified stats and leveling 
- Build powerful habits using philosophies from: 
  - Deep Work
  - Atomic Habits
  - Slight Edge
  - Think & Grow Rich
  - Shadow Work Journal 

> You don't just live life — you *level through it*. 

--- 

## Quickstart

```bash
git clone https://github.com/2kDarki/Habitrax.git 
cd Habitrax 
python run.py
```

or through pip:
```bash
pip install habitrax
Habitrax # or python -m hbx
```

> Requires Python 3.10+ installed. 

That's it — Habitrax runs out-of-the-box.

---

## Philosophy

Most productivity apps force structure on you.  
Habitrax does the opposite — it's a *sandbox for your goals, actions, and reflections.*

- Every decision is a vote toward your future self  
- Every session is data, analyzed and visualized for self-awareness  
- You define your purpose, rules, and trajectory  

---

## Core Modules

- Session Logging – Track tasks, time, focus, and productivity quality
- Debrief – Daily introspection with randomized deep questions
- Soul Work – Gratitude, philosophy, and "Slight Edge" voting
- Status Window – Gamified dashboard for categories and missions
- Notebook – Store insights, mantras, or journal entries
- Statistics – Filter and visualize productivity trends
- Missions – Self-defined goals with tracked completion
- Coffer – Manually track your finances
- Almanack – Define your chief aim and personal commandments

---

## Why Terminal?

- Built entirely on a smartphone as a *learning project*
- No external dependencies or frameworks
- Made for speed, clarity, and minimalism
- Focus is on function, not flash — every feature serves personal growth

---

## Tech Stack

- Language: Python  
- Libraries: tuikit
- Storage: JSON 
- Interface: Terminal-based, menu-driven  

---

## Folder Structure

```
Habitrax/
        ├── sreenshots/      ← Example screenshots
        ├── src/ 
            ├── Habitrax/    ← Shim
            └── hbx/         ← App source code
        ├── data/            ← Stored user data (JSON) 
        ├── pyproject.toml   ← Packaging configuration 
        ├── requirements.txt ← Empty (0 dependencies) 
        ├── run.py           ← Entry point 
        ├── README.md        ← You are here
        ├── LICENSE 
        └── .gitignore 
```
 
---

## Screenshots 

1. Status Window
![Status Window](./screenshots/status-window.png)
2. Soul Work module
![Soul Work module](./screenshots/soul-work.png) 
3. Debrief questions
![Debrief questions](./screenshots/debrief-questions.png) 
4. Task logging view 
![Task logging view](./screenshots/task-logging.png) 

---

## Data & Privacy

- All user data is stored locally in JSON files
- You can back up or migrate manually
- Future versions may support encryption or SQLite (if you can, you may work on this)

---

## Limitations

- Minimal CLI interface — designed for speed and simplicity
- No undo or in-app editing (by design)
- Manual testing only — no automated tests yet

---

## License

MIT License — Free to use, modify, or build upon. Mention appreciated if published or monetized.

---

## About the Author

Self-taught dev passionate about programming and philosophy. Built this to not just track productivity — but to master the self.


# Contributing to Habitrax 

Thank you for considering contributing! Here's a simple workflow: 

## Getting Started 

1. Fork the repo 
2. Clone your fork: 
```bash
git clone https://github.com/YOUR_USERNAME/Habitrax.git 
cd Habitrax
```

- Create a branch for your changes: git checkout -b feat/my-feature 
- Make your changes (code, data, formatting)
- Stage and commit: 
  - git add . 
  - git commit -m "Clear, short description" 
- Push your branch: git push origin feat/my-feature 
- Open a Pull Request (PR) on GitHub — describe your change clearly
- Optional: add a minimal test in tests/

--- 

## Code Style
- Keep naming consistent with existing files
- Minimal formatting: PEP8 recommended, but readability matters most
- Comments welcome for clarity

---

## Testing

- There's no automated testing yet
- Please run python run.py to make sure your changes don't break the app

---

## Suggested First Contributions

Even if you've never seen the code before, here are 2 tasks anyone can try:
- Improve Debrief Randomization – Add optional filters for categories
- Add a CLI Shortcut

These tasks are small, self-contained, and won't break the core functionality.