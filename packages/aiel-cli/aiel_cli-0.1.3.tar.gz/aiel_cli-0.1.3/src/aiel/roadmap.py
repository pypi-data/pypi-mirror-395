from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

@dataclass(frozen=True)
class CommandPlan:
    command: str          # e.g. "aiel file ls"
    sprint: int           # e.g. 3
    intent: str           # what it will do

# Update sprint numbers / wording here only.
PLAN: Dict[str, CommandPlan] = {
    # Sprint 0
    "aiel roadmap": CommandPlan("aiel roadmap", 0, "Show the command roadmap and sprint plan."),
    "aiel version": CommandPlan("aiel version", 0, "Print CLI version and build info."),

    # Sprint 1
    "aiel init": CommandPlan("aiel init", 1, "Initialize local context file (aiel.toml) with base_url/tenant/workspace/project."),
    "aiel auth login": CommandPlan("aiel auth login", 1, "Authenticate and store token securely (env/keychain/file fallback)."),
    "aiel auth status": CommandPlan("aiel auth status", 1, "Show whether auth is configured and valid."),
    "aiel auth logout": CommandPlan("aiel auth logout", 1, "Remove stored credentials."),
    "aiel context show": CommandPlan("aiel context show", 1, "Show current tenant/workspace/project context."),
    "aiel context set": CommandPlan("aiel context set", 1, "Set default tenant/workspace/project context."),

    # Sprint 2
    "aiel workspace ls": CommandPlan("aiel workspace ls", 2, "List available workspaces for the authenticated user."),
    "aiel workspace use": CommandPlan("aiel workspace use", 2, "Set active workspace in the project context."),
    "aiel project ls": CommandPlan("aiel project ls", 2, "List projects in the current workspace."),
    "aiel project create": CommandPlan("aiel project create", 2, "Create a new project in the current workspace."),

    # Sprint 3
    "aiel file ls": CommandPlan("aiel file ls", 3, "List remote files stored in the workspace (backed by GCS)."),
    "aiel file cat": CommandPlan("aiel file cat", 3, "Print the contents of a remote file."),
    "aiel file write": CommandPlan("aiel file write", 3, "Write/update a remote file (via stdin/text)."),
    "aiel file rm": CommandPlan("aiel file rm", 3, "Delete a remote file."),
    "aiel sdk pin": CommandPlan("aiel sdk pin", 3, "Pin a remote SDK artifact (GCS URI + sha256) for reproducible runs."),
    "aiel sdk status": CommandPlan("aiel sdk status", 3, "Show the pinned SDK and verification status."),

    # Sprint 4
    "aiel run": CommandPlan("aiel run", 4, "Trigger remote execution via POST /sandbox/flows/run."),
    "aiel logs": CommandPlan("aiel logs", 4, "Stream logs for a run (SSE/WebSocket; polling fallback)."),
    "aiel doctor": CommandPlan("aiel doctor", 4, "Connectivity/auth/context diagnostics + actionable fixes."),
}

def by_sprint() -> dict[int, list[CommandPlan]]:
    out: dict[int, list[CommandPlan]] = {}
    for p in PLAN.values():
        out.setdefault(p.sprint, []).append(p)
    for s in out:
        out[s] = sorted(out[s], key=lambda x: x.command)
    return dict(sorted(out.items(), key=lambda kv: kv[0]))
