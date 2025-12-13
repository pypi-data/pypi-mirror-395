"""
Data models for Tima timer application.
"""
from dataclasses import dataclass, field
from typing import Dict, List
from pathlib import Path
import json


@dataclass
class AppState:
    """Application state"""
    projects: List[str] = field(default_factory=list)
    current_project_index: int = 0
    default_duration: int = 3600  # 1 hour in seconds
    project_times: Dict[str, int] = field(default_factory=dict)
    project_paused: Dict[str, bool] = field(default_factory=dict)

    def get_current_project(self) -> str:
        """Get the current project name"""
        if self.projects and 0 <= self.current_project_index < len(self.projects):
            return self.projects[self.current_project_index]
        return ""

    def get_current_time_left(self) -> int:
        """Get time left for current project"""
        project = self.get_current_project()
        if project:
            return self.project_times.get(project, self.default_duration)
        return 0

    def set_current_time_left(self, time_left: int):
        """Set time left for current project"""
        project = self.get_current_project()
        if project:
            self.project_times[project] = time_left

    def is_current_project_paused(self) -> bool:
        """Check if current project is paused"""
        project = self.get_current_project()
        if project:
            return self.project_paused.get(project, False)
        return False

    def set_current_project_paused(self, paused: bool):
        """Set pause state for current project"""
        project = self.get_current_project()
        if project:
            self.project_paused[project] = paused

    def add_project(self, name: str):
        """Add a new project"""
        self.projects.append(name)
        self.project_times[name] = self.default_duration
        self.project_paused[name] = False

    def delete_project(self, index: int) -> dict:
        """Delete a project and return undo data"""
        if 0 <= index < len(self.projects):
            project = self.projects[index]
            undo_data = {
                'index': index,
                'name': project,
                'time': self.project_times.get(project, self.default_duration),
                'paused': self.project_paused.get(project, False)
            }

            self.projects.pop(index)
            if project in self.project_times:
                del self.project_times[project]
            if project in self.project_paused:
                del self.project_paused[project]

            # Adjust current index
            if index == self.current_project_index:
                if self.current_project_index >= len(self.projects):
                    self.current_project_index = max(0, len(self.projects) - 1)
            elif index < self.current_project_index:
                self.current_project_index -= 1

            return undo_data
        return {}

    def rename_project(self, index: int, new_name: str) -> dict:
        """Rename a project and return undo data"""
        if 0 <= index < len(self.projects):
            old_name = self.projects[index]
            undo_data = {
                'index': index,
                'old_name': old_name,
                'new_name': new_name
            }

            self.projects[index] = new_name
            if old_name in self.project_times:
                self.project_times[new_name] = self.project_times.pop(old_name)
            if old_name in self.project_paused:
                self.project_paused[new_name] = self.project_paused.pop(old_name)

            return undo_data
        return {}

    def restore_deleted_project(self, undo_data: dict):
        """Restore a deleted project"""
        index = undo_data['index']
        name = undo_data['name']
        time = undo_data['time']
        paused = undo_data['paused']

        self.projects.insert(index, name)
        self.project_times[name] = time
        self.project_paused[name] = paused

        if index <= self.current_project_index:
            self.current_project_index += 1

    def restore_renamed_project(self, undo_data: dict):
        """Restore a renamed project"""
        index = undo_data['index']
        old_name = undo_data['old_name']
        new_name = undo_data['new_name']

        self.projects[index] = old_name
        if new_name in self.project_times:
            self.project_times[old_name] = self.project_times.pop(new_name)
        if new_name in self.project_paused:
            self.project_paused[old_name] = self.project_paused.pop(new_name)

    def next_project(self):
        """Move to next project"""
        if self.projects:
            current = self.get_current_project()
            if current:
                self.project_paused[current] = True

            self.current_project_index = (self.current_project_index + 1) % len(self.projects)

            new_project = self.get_current_project()
            if new_project:
                self.project_paused[new_project] = False

    def previous_project(self):
        """Move to previous project"""
        if self.projects:
            current = self.get_current_project()
            if current:
                self.project_paused[current] = True

            self.current_project_index = (self.current_project_index - 1) % len(self.projects)

            new_project = self.get_current_project()
            if new_project:
                self.project_paused[new_project] = False

    def reset_project(self, index: int):
        """Reset a project's timer"""
        if 0 <= index < len(self.projects):
            project = self.projects[index]
            self.project_times[project] = self.default_duration
            self.project_paused[project] = False

    def toggle_project_pause(self, index: int):
        """Toggle pause state for a project"""
        if 0 <= index < len(self.projects):
            project = self.projects[index]
            current_state = self.project_paused.get(project, False)
            self.project_paused[project] = not current_state

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'projects': self.projects,
            'current_index': self.current_project_index,
            'default_duration': self.default_duration,
            'project_times': self.project_times,
            'project_paused': self.project_paused
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'AppState':
        """Create from dictionary"""
        return cls(
            projects=data.get('projects', []),
            current_project_index=data.get('current_index', 0),
            default_duration=data.get('default_duration', 3600),
            project_times=data.get('project_times', {}),
            project_paused=data.get('project_paused', {})
        )


class DataManager:
    """Manages data persistence"""

    def __init__(self):
        self.config_dir = Path.home() / ".tima"
        self.config_dir.mkdir(exist_ok=True)
        self.data_file = self.config_dir / "tima_projects.json"
        self.default_projects_file = Path(__file__).parent.parent.parent / "tima_projects.json"

    def load(self) -> AppState:
        """Load app state from file"""
        # Try user config first
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    return AppState.from_dict(data)
            except Exception as e:
                print(f"Error loading from {self.data_file}: {e}")

        # Try default projects file
        if self.default_projects_file.exists():
            try:
                with open(self.default_projects_file, 'r') as f:
                    data = json.load(f)
                    return AppState.from_dict(data)
            except Exception as e:
                print(f"Error loading from {self.default_projects_file}: {e}")

        # Return default state
        state = AppState()
        state.projects = ['Develop new feature', 'Review research papers', 'Team meeting prep']
        for project in state.projects:
            state.project_times[project] = state.default_duration
            state.project_paused[project] = False
        return state

    def save(self, state: AppState):
        """Save app state to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(state.to_dict(), f, indent=2)
        except Exception as e:
            print(f"Error saving: {e}")

    def import_from_file(self, file_path: str) -> List[str]:
        """Import projects from text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return [line.strip() for line in content.split('\n') if line.strip()]
        except Exception as e:
            raise Exception(f"Failed to import: {e}")

    def export_to_file(self, file_path: str, projects: List[str]):
        """Export projects to text file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(projects))
        except Exception as e:
            raise Exception(f"Failed to export: {e}")
