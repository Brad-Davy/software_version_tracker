# HPC Software Version Tracker

This script helps keep track of the **latest stable releases** of common HPC (High Performance Computing) software packages by automatically checking their public Git repositories.

It uses Git tags to determine version numbers and filters out pre-release, development, and non-semantic tags (e.g., `alpha`, `beta`, `rc`, `dev`).

---

## 🧩 How It Works

The script:
1. Connects to a given Git repository using:
   ```bash
   git ls-remote --tags <repo_url>
