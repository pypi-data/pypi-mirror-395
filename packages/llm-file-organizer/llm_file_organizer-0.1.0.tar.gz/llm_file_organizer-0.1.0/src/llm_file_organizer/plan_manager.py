"""Plan status tracking and management."""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Literal

PlanStatusType = Literal["pending", "executing", "executed", "partial", "undone"]


@dataclass
class PlanInfo:
    """Information about a single plan."""

    file: str
    created: str  # ISO format
    status: PlanStatusType
    total_moves: int
    description: str = ""
    executed_at: str | None = None
    success_count: int | None = None
    error_count: int | None = None
    can_undo: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "PlanInfo":
        return cls(**data)

    @property
    def created_dt(self) -> datetime:
        return datetime.fromisoformat(self.created)

    @property
    def executed_dt(self) -> datetime | None:
        if self.executed_at:
            return datetime.fromisoformat(self.executed_at)
        return None

    def format_created(self) -> str:
        """Human-readable created date."""
        dt = self.created_dt
        return dt.strftime("%b %d, %Y at %I:%M%p").replace(" 0", " ").lower()

    def format_status(self) -> str:
        """Status with emoji."""
        icons = {
            "pending": "⏳",
            "executing": "⚡",
            "executed": "✓",
            "partial": "⚠",
            "undone": "↩",
        }
        return f"{icons.get(self.status, '?')} {self.status}"


@dataclass
class PlanIndex:
    """Index of all plans for a target directory."""

    target_dir: str
    plans: list[PlanInfo] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "target_dir": self.target_dir,
            "updated": datetime.now().isoformat(),
            "plans": [p.to_dict() for p in self.plans],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PlanIndex":
        return cls(
            target_dir=data["target_dir"],
            plans=[PlanInfo.from_dict(p) for p in data.get("plans", [])],
        )


class PlanManager:
    """Manages plan status and history for a target directory."""

    def __init__(self, config_dir: Path, target_dir: Path):
        self.config_dir = config_dir
        self.target_dir = target_dir
        self.index_file = config_dir / "index.json"

    def _load_index(self) -> PlanIndex:
        """Load or create the plan index."""
        if self.index_file.exists():
            try:
                with open(self.index_file, encoding="utf-8") as f:
                    return PlanIndex.from_dict(json.load(f))
            except (json.JSONDecodeError, KeyError):
                pass
        return PlanIndex(target_dir=str(self.target_dir))

    def _save_index(self, index: PlanIndex) -> None:
        """Save the plan index."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(index.to_dict(), f, indent=2)

    def register_plan(
        self,
        plan_file: Path,
        total_moves: int,
        description: str = "",
    ) -> PlanInfo:
        """Register a new plan in the index."""
        index = self._load_index()

        # Remove any existing entry for this file
        index.plans = [p for p in index.plans if p.file != plan_file.name]

        # Add new entry
        info = PlanInfo(
            file=plan_file.name,
            created=datetime.now().isoformat(),
            status="pending",
            total_moves=total_moves,
            description=description or f"{self.target_dir.name} organization",
        )
        index.plans.insert(0, info)  # Newest first

        self._save_index(index)
        return info

    def mark_executing(self, plan_file: Path) -> None:
        """Mark a plan as currently executing."""
        self._update_status(plan_file.name, "executing")

    def mark_executed(
        self,
        plan_file: Path,
        success_count: int,
        error_count: int,
    ) -> None:
        """Mark a plan as executed."""
        index = self._load_index()

        for plan in index.plans:
            if plan.file == plan_file.name:
                plan.status = "executed" if error_count == 0 else "partial"
                plan.executed_at = datetime.now().isoformat()
                plan.success_count = success_count
                plan.error_count = error_count
                plan.can_undo = success_count > 0
                break

        self._save_index(index)

    def mark_undone(self, plan_file: Path | None = None) -> None:
        """Mark a plan as undone. If no file specified, marks the latest undoable."""
        index = self._load_index()

        for plan in index.plans:
            if plan_file and plan.file != plan_file.name:
                continue
            if plan.can_undo:
                plan.status = "undone"
                plan.can_undo = False
                break

        self._save_index(index)

    def _update_status(self, filename: str, status: PlanStatusType) -> None:
        """Update status for a plan."""
        index = self._load_index()
        for plan in index.plans:
            if plan.file == filename:
                plan.status = status
                break
        self._save_index(index)

    def get_all_plans(self) -> list[PlanInfo]:
        """Get all plans, newest first."""
        return self._load_index().plans

    def get_pending_plans(self) -> list[PlanInfo]:
        """Get all pending plans."""
        return [p for p in self.get_all_plans() if p.status == "pending"]

    def get_latest_pending(self) -> PlanInfo | None:
        """Get the most recent pending plan."""
        pending = self.get_pending_plans()
        return pending[0] if pending else None

    def get_undoable_plan(self) -> PlanInfo | None:
        """Get the most recent plan that can be undone."""
        for plan in self.get_all_plans():
            if plan.can_undo:
                return plan
        return None

    def get_plan_info(self, plan_file: Path) -> PlanInfo | None:
        """Get info for a specific plan file."""
        for plan in self.get_all_plans():
            if plan.file == plan_file.name:
                return plan
        return None

    def cleanup_old_plans(self, keep_last: int = 10) -> int:
        """Remove old plan files, keeping the most recent N. Returns count deleted."""
        index = self._load_index()
        deleted = 0

        # Keep pending and recent executed, delete old ones
        to_keep = []
        to_delete = []

        for plan in index.plans:
            # Always keep pending plans
            if plan.status == "pending":
                to_keep.append(plan)
            elif len(to_keep) < keep_last:
                to_keep.append(plan)
            else:
                to_delete.append(plan)

        # Delete old plan files
        for plan in to_delete:
            plan_path = self.config_dir / plan.file
            if plan_path.exists():
                plan_path.unlink()
                deleted += 1

        # Update index
        index.plans = to_keep
        self._save_index(index)

        return deleted

    def has_plans(self) -> bool:
        """Check if there are any plans for this target."""
        return len(self.get_all_plans()) > 0


def get_all_targets_with_plans(app_dir: Path) -> list[tuple[Path, PlanManager]]:
    """Get all target directories that have plans."""
    plans_dir = app_dir / "plans"
    if not plans_dir.exists():
        return []

    results = []
    for target_slug_dir in plans_dir.iterdir():
        if target_slug_dir.is_dir():
            index_file = target_slug_dir / "index.json"
            if index_file.exists():
                try:
                    with open(index_file, encoding="utf-8") as f:
                        data = json.load(f)
                    target_dir = Path(data.get("target_dir", ""))
                    manager = PlanManager(target_slug_dir, target_dir)
                    if manager.has_plans():
                        results.append((target_dir, manager))
                except (json.JSONDecodeError, KeyError):
                    pass

    return results
