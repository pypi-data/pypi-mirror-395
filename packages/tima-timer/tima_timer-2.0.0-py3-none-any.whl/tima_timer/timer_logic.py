"""
Timer business logic for Tima.
"""
import platform
from typing import Callable, Optional

try:
    from .models import AppState, DataManager
except ImportError:
    from models import AppState, DataManager


class TimerManager:
    """Manages timer logic and state"""

    def __init__(self, on_update: Callable, on_timer_end: Callable):
        """
        Initialize timer manager.

        Args:
            on_update: Callback when timer updates (called every second)
            on_timer_end: Callback when timer reaches zero
        """
        self.state = AppState()
        self.data_manager = DataManager()
        self.on_update = on_update
        self.on_timer_end = on_timer_end
        self.undo_stack = []
        self.max_undo_stack_size = 10

        # Platform-specific sound support
        self.winsound = None
        if platform.system() == 'Windows':
            try:
                import winsound
                self.winsound = winsound
            except ImportError:
                pass

    def load_data(self):
        """Load saved state"""
        self.state = self.data_manager.load()

    def save_data(self):
        """Save current state"""
        self.data_manager.save(self.state)

    def tick(self):
        """Called every second to update timer"""
        if not self.state.projects:
            return

        if not self.state.is_current_project_paused():
            current_time = self.state.get_current_time_left()
            if current_time > 0:
                self.state.set_current_time_left(current_time - 1)
                self.save_data()
            else:
                # Timer ended
                self.handle_timer_end()
                return

        self.on_update()

    def handle_timer_end(self):
        """Handle timer reaching zero"""
        # Play sound if available
        if self.winsound:
            try:
                self.winsound.PlaySound('C:/Windows/Media/Alarm04.wav',
                                       self.winsound.SND_FILENAME | self.winsound.SND_ASYNC)
            except Exception as e:
                print(f"Could not play sound: {e}")
        else:
            print("Alarm! Timer ended!")

        self.on_timer_end()

    def add_project(self, name: str) -> bool:
        """Add a new project. Returns True if successful."""
        name = name.strip()
        if not name:
            return False

        self.state.add_project(name)
        self.save_data()
        return True

    def delete_project(self, index: int) -> bool:
        """Delete a project. Returns True if successful."""
        if 0 <= index < len(self.state.projects):
            undo_data = self.state.delete_project(index)
            self.push_undo('delete', undo_data)
            self.save_data()
            return True
        return False

    def rename_project(self, index: int, new_name: str) -> bool:
        """Rename a project. Returns True if successful."""
        new_name = new_name.strip()
        if not new_name or index < 0 or index >= len(self.state.projects):
            return False

        old_name = self.state.projects[index]
        if new_name == old_name:
            return False

        undo_data = self.state.rename_project(index, new_name)
        self.push_undo('rename', undo_data)
        self.save_data()
        return True

    def reset_project(self, index: int):
        """Reset a project's timer"""
        self.state.reset_project(index)
        self.save_data()

    def toggle_project_pause(self, index: int):
        """Toggle pause for a project"""
        self.state.toggle_project_pause(index)
        self.save_data()

    def next_project(self):
        """Move to next project"""
        self.state.next_project()
        self.save_data()

    def previous_project(self):
        """Move to previous project"""
        self.state.previous_project()
        self.save_data()

    def reset_current_and_continue(self, move_to_next: bool = False):
        """Reset current project timer and optionally move to next"""
        self.state.reset_project(self.state.current_project_index)
        if move_to_next:
            self.next_project()
        else:
            self.state.set_current_project_paused(False)
        self.save_data()

    def set_default_duration(self, hours: int, minutes: int) -> bool:
        """Set default duration. Returns True if valid."""
        new_duration = hours * 3600 + minutes * 60
        if new_duration <= 0:
            return False

        self.state.default_duration = new_duration
        self.save_data()
        return True

    def import_projects(self, file_path: str) -> int:
        """Import projects from file. Returns number of projects imported."""
        try:
            imported = self.data_manager.import_from_file(file_path)
            if not imported:
                raise Exception("No valid projects found")

            self.state.projects = imported
            self.state.current_project_index = 0
            self.state.project_times = {}
            self.state.project_paused = {}

            for project in self.state.projects:
                self.state.project_times[project] = self.state.default_duration
                self.state.project_paused[project] = False

            self.save_data()
            return len(imported)
        except Exception as e:
            raise e

    def export_projects(self, file_path: str):
        """Export projects to file"""
        if not self.state.projects:
            raise Exception("No projects to export")

        self.data_manager.export_to_file(file_path, self.state.projects)

    def push_undo(self, operation_type: str, data: dict):
        """Push undo operation"""
        self.undo_stack.append({
            'type': operation_type,
            'data': data
        })
        if len(self.undo_stack) > self.max_undo_stack_size:
            self.undo_stack.pop(0)

    def undo(self) -> Optional[str]:
        """Undo last operation. Returns status message or None."""
        if not self.undo_stack:
            return None

        operation = self.undo_stack.pop()
        op_type = operation['type']
        data = operation['data']

        if op_type == 'delete':
            self.state.restore_deleted_project(data)
            self.save_data()
            return f"Restored project: {data['name']}"
        elif op_type == 'rename':
            self.state.restore_renamed_project(data)
            self.save_data()
            return f"Renamed back to: {data['old_name']}"

        return None

    @staticmethod
    def format_time(seconds: int) -> str:
        """Format seconds to HH:MM:SS"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
