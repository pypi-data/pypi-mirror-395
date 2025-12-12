# CHANGELOG


## v0.3.0 (2025-12-05)

### Features

- Add Rich CLI setup wizard with AI-assisted installation
  ([`6120998`](https://github.com/peacockery-studio/mcp-sharepoint-cert/commit/612099858ec04bcf61f511d4d4cdd576b9163967))

- Rewrite setup wizard using Typer + Rich for beautiful interactive CLI - Add AI client selection
  menu (Claude Desktop, Claude Code, Cursor, Windsurf) - Generate INSTALL_WITH_AI.md prompt for
  AI-assisted configuration - Auto-copy prompt to clipboard - Fix logging FileHandler that failed on
  read-only root filesystem

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>


## v0.2.1 (2025-12-05)

### Bug Fixes

- Remove build_command instead of setting false
  ([`71b6b62`](https://github.com/peacockery-studio/mcp-sharepoint-cert/commit/71b6b624ae136985a36385a5fed629486710118a))

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>

### Continuous Integration

- Add manual publish workflow
  ([`539411e`](https://github.com/peacockery-studio/mcp-sharepoint-cert/commit/539411ea540b29b821929d462c846745a9d1716b))

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>


## v0.2.0 (2025-12-05)

### Bug Fixes

- Disable semantic-release build, use uv build in workflow
  ([`ae550a6`](https://github.com/peacockery-studio/mcp-sharepoint-cert/commit/ae550a6a472d6e7046104fb29fc47df5057f0efa))

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>

- Use correct semantic-release action versions
  ([`a5438e4`](https://github.com/peacockery-studio/mcp-sharepoint-cert/commit/a5438e4a1018219a93a99f06b2c271ec8d8ff48a))

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>

### Chores

- Update repo URLs to peacockery-studio org
  ([`494f5e0`](https://github.com/peacockery-studio/mcp-sharepoint-cert/commit/494f5e0d685d6ce6056085d4fa56d0062b2e6400))

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>

### Documentation

- Simplify Azure Portal configuration guide
  ([`4645c56`](https://github.com/peacockery-studio/mcp-sharepoint-cert/commit/4645c56883a8c85577d6812446ab050c8904bd01))

- Remove unnecessary API exposure steps - Focus on essential 3-step setup: create app, add
  Sites.Selected, configure via appinv.aspx - Update XML to use sitecollection/web scope with Write
  permissions - Add App Domain field instructions with verified domain example - Include
  troubleshooting section and security best practices

### Features

- Add certificate authentication and setup command
  ([`020a215`](https://github.com/peacockery-studio/mcp-sharepoint-cert/commit/020a215f52ad87eb3759fd8d026e3d77faaeccfd))

- Add certificate-based authentication for Azure AD app-only access - Add `mcp-sharepoint-setup` CLI
  command to generate certificates - Add auth check on startup with helpful error messages - Add
  graceful Ctrl+C shutdown handling - Consolidate docs into README, remove redundant Azure Portal
  Guide - Update .gitignore for certs, logs, IDE files - Clean up stale validation_report.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>

- Add coverage reporting and badges
  ([`66cb93c`](https://github.com/peacockery-studio/mcp-sharepoint-cert/commit/66cb93c23b6dde787ed9e8ff471b5ec577d65d31))

- Add pytest-cov for coverage reporting - Update CI to upload coverage to Codecov - Add badges:
  Codecov, Python version, Ruff - Only test Python 3.12 (requires-python >= 3.12)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>

- Interactive setup wizard with config generation
  ([`b93be71`](https://github.com/peacockery-studio/mcp-sharepoint-cert/commit/b93be719e32bed897798526df658df079db643ff))

- Wizard walks through Azure setup step by step - Generates claude_mcp_config.json file - Copies
  config to clipboard (macOS/Linux) - Shows config in terminal for easy copy/paste

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>

- Major improvements - Python 3.12, pydantic, ruff, ty, CI/CD
  ([`9617515`](https://github.com/peacockery-studio/mcp-sharepoint-cert/commit/96175159adf09fb56a24bd8d74cb0ddf273853cb))

- Upgrade to Python 3.12 for performance improvements - Add pydantic for input validation and
  settings management - Add ruff for linting and formatting - Add ty for type checking - Add GitHub
  Actions CI workflow (lint, typecheck, test) - Add custom exception classes - Add 31 unit tests -
  Convert to pathlib for file operations - Fix bare exception handling - Remove unused imports -
  Update to modern uv patterns

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>

- Rename package to mcp-sharepoint-cert with semantic release
  ([`79f0aef`](https://github.com/peacockery-studio/mcp-sharepoint-cert/commit/79f0aef2bceb31ea4cb86e12f41b5dcf94992e9a))

- Rename package from mcp-sharepoint to mcp-sharepoint-cert - Bump version to 0.2.0 - Add
  python-semantic-release config for automated versioning - Add release workflow for automated PyPI
  publishing - Add CHANGELOG.md - Update all references in README and setup wizard

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>

- **sharepoint**: Add PDF extraction, folder tree, and document content retrieval
  ([`0687b09`](https://github.com/peacockery-studio/mcp-sharepoint-cert/commit/0687b0994de97780e5e1baa29d86186628f6a452))

Adds new SharePoint features:

PDF text extraction with PyMuPDF

Recursive folder tree builder with metadata

Document content retrieval (PDFs, text files, binaries)

Exposed via Get_SharePoint_Tree tool

- **sharepoint**: Add tools to get and update file metadata
  ([`3ca30a2`](https://github.com/peacockery-studio/mcp-sharepoint-cert/commit/3ca30a23acaa0a840b2bb7256181f8e12e64acde))

- Added `Update_File_Metadata` tool to modify metadata fields for SharePoint files. - Handles
  boolean, list, and string value conversions automatically. - Skips empty metadata updates
  gracefully. - Added `Get_File_Metadata` tool to retrieve all metadata fields from a SharePoint
  file. - Loads and returns all non-null metadata properties. - Ensures both tools return structured
  success messages with file info.

### Testing

- Add real SharePoint integration tests
  ([`8a29af7`](https://github.com/peacockery-studio/mcp-sharepoint-cert/commit/8a29af7a16b0943c26c672eab4670ed55e9106ff))

- Test list folders/documents against real SharePoint - Test upload, read, and delete documents -
  Tests create temp folders and clean up after - Skipped in CI (no credentials), run locally with
  real .env

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>

- Add tests for setup wizard
  ([`f3a4326`](https://github.com/peacockery-studio/mcp-sharepoint-cert/commit/f3a4326e70cb7fe572b68a68736478c3850168a9))

- Test certificate generation (files, content, thumbprint format) - Test clipboard copy fallback
  logic - Test config JSON structure - 10 new tests, 41 total

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
