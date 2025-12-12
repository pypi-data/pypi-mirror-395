from __future__ import annotations

PROJECT_GITIGNORE_DEFAULT = [
    # Editors / IDE
    "/.idea/",
    "/.vscode/",
    "/.history/",
    "/*.code-workspace",
    "*.swp",
    "*~",
    "*.orig",
    "*.tmp",
    "*.bak",
    # OS files
    ".DS_Store",
    "Thumbs.db",
    "Desktop.ini",
    ".Spotlight-V100",
    ".Trashes",
    # Git / credentials
    ".git-credentials",
    # Environment files
    ".env",
    ".env.*",
    ".env.local",
    ".env.*.local",
    # Logs
    "*.log",
    "logs/",
    "log/",
    # Caches and temp
    ".cache/",
    "cache/",
    "tmp/",
    "temp/",
    # Build artifacts
    "build/",
    "dist/",
    "out/",
    # Test coverage
    "coverage/",
    "coverage-*.json",
    "coverage*.lcov",
    # Locks and PID files
    "*.pid",
    "*.pid.lock",
]
