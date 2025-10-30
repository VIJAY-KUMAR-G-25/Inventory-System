1. Which issues were the easiest to fix, and which were the hardest? Why?

Easiest: The easiest fixes were the stylistic ones reported by `pylint` and `flake8`. Issues like `C0304: Final newline missing`, `E501: Line too long`, or `E302: expected 2 blank lines` were purely mechanical. The tools tell you the exact line and what to do, so they required no real analysis.

Hardest: The hardest fix was definitely `W0603: Using the global statement`. This wasn't a one-line change; it required a significant refactor. I had to change the function signature of *every* function to pass `stock_data` as a parameter and then update the `main()` function to manage the application's state. This was a conceptual change to the code's design, not just a simple syntax fix.

2. Did the static analysis tools report any false positives?

No. In this lab, there were no false positives. Every single issue reported by the tools was a 100% valid problem.
`bandit` was correct about `eval()` being dangerous and the `bare except:` being a bug.
`pylint` was correct about the poor naming, the mutable default argument, the global variable, and the missing docstrings.
`flake8` was correct about all the PEP 8 style violations.

3. How would you integrate static analysis tools into your actual software development workflow?

I would integrate them at two key points:

 Local Development: I would use **pre-commit hooks**. This automatically runs tools like `flake8` and `bandit` on my code *before* I'm even allowed to make a commit. This catches simple errors and security issues instantly, ensuring I never push bad code to the repository. I'd also use IDE extensions for real-time linting.

 Continuous Integration (CI): I would configure a GitHub Action (or similar CI pipeline) to run on every Pull Request. This pipeline would have a "linting" job that runs all three tools (`pylint`, `bandit`, `flake8`). If `bandit` finds a high-severity issue, or the `pylint` score is below a certain threshold (e.g., 9.0/10), the build would **fail**. This blocks the bad code from being merged into the main branch and notifies the team.

4. What tangible improvements did you observe in the code?

The improvements were immediate and significant:

 Robustness: . By fixing the **bare `except:`** (W0702) and adding proper input validation, the program no longer crashes when given bad data (like a non-existent item or an invalid item name). It now handles errors gracefully and logs them.

 Security: The code is objectively safer. Removing the **`eval()` function** (B307) eliminated a critical remote code execution vulnerability.

 Readability & Maintainability: Fixing the `global` variable, adding `docstrings` for every function, and enforcing `snake_case` naming conventions make the code's logic and purpose clear to any new developer.