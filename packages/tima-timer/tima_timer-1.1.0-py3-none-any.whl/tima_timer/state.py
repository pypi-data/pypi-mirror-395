"""Unified state management for Tima."""
import json
import platform
from pathlib import Path
from typing import Callable, Optional


class TimaState:
    """All application state and logic in one place."""

    def __init__(self, on_update: Callable, on_timer_end: Callable):
        self.on_update = on_update
        self.on_timer_end = on_timer_end

        # State
        self.projects = []
        self.current_index = 0
        self.default_duration = 3600
        self.project_times = {}
        self.project_paused = {}
        self.undo_stack = []

        # Paths
        self.config_dir = Path.home() / ".tima"
        self.config_dir.mkdir(exist_ok=True)
        self.data_file = self.config_dir / "tima_projects.json"
        self.default_file = Path(__file__).parent.parent.parent / "tima_projects.json"

        # Sound support
        self.winsound = None
        if platform.system() == 'Windows':
            try:
                import winsound
                self.winsound = winsound
            except ImportError:
                pass

    # Data persistence
    def load(self):
        """Load state from disk."""
        for path in [self.data_file, self.default_file]:
            if path.exists():
                try:
                    with open(path) as f:
                        data = json.load(f)
                        self.projects = data.get('projects', [])
                        self.current_index = data.get('current_index', 0)
                        self.default_duration = data.get('default_duration', 3600)
                        self.project_times = data.get('project_times', {})
                        self.project_paused = data.get('project_paused', {})
                        return
                except Exception as e:
                    print(f"Error loading from {path}: {e}")

        # Fallback defaults
        self.projects = ['Quantum entanglement simulation', 'Neural network architecture design',
                        'Distributed systems protocol analysis']
        for p in self.projects:
            self.project_times[p] = self.default_duration
            self.project_paused[p] = False

    def save(self):
        """Save state to disk."""
        try:
            with open(self.data_file, 'w') as f:
                json.dump({
                    'projects': self.projects,
                    'current_index': self.current_index,
                    'default_duration': self.default_duration,
                    'project_times': self.project_times,
                    'project_paused': self.project_paused
                }, f, indent=2)
        except Exception as e:
            print(f"Error saving: {e}")

    # Getters
    def current_project(self) -> str:
        return self.projects[self.current_index] if 0 <= self.current_index < len(self.projects) else ""

    def current_time(self) -> int:
        p = self.current_project()
        return self.project_times.get(p, self.default_duration) if p else 0

    def is_paused(self) -> bool:
        p = self.current_project()
        return self.project_paused.get(p, False) if p else False

    # Timer
    def tick(self):
        """Called every second."""
        if not self.projects or self.is_paused():
            self.on_update()
            return

        if self.current_time() > 0:
            p = self.current_project()
            self.project_times[p] -= 1
            self.save()
            self.on_update()
        else:
            self.handle_timer_end()

    def handle_timer_end(self):
        """Timer reached zero."""
        if self.winsound:
            try:
                self.winsound.PlaySound('C:/Windows/Media/Alarm04.wav',
                                       self.winsound.SND_FILENAME | self.winsound.SND_ASYNC)
            except:
                pass
        self.on_timer_end()

    # Project operations
    def add(self, name: str) -> bool:
        if not (name := name.strip()):
            return False
        self.projects.append(name)
        self.project_times[name] = self.default_duration
        self.project_paused[name] = False
        self.save()
        return True

    def delete(self, idx: int) -> bool:
        if not 0 <= idx < len(self.projects):
            return False
        p = self.projects[idx]
        self.undo_stack.append(('delete', {
            'index': idx, 'name': p,
            'time': self.project_times.get(p, self.default_duration),
            'paused': self.project_paused.get(p, False)
        }))
        self.projects.pop(idx)
        self.project_times.pop(p, None)
        self.project_paused.pop(p, None)
        if idx == self.current_index and self.current_index >= len(self.projects):
            self.current_index = max(0, len(self.projects) - 1)
        elif idx < self.current_index:
            self.current_index -= 1
        self.save()
        return True

    def rename(self, idx: int, new_name: str) -> bool:
        if not (new_name := new_name.strip()) or not 0 <= idx < len(self.projects):
            return False
        old = self.projects[idx]
        if new_name == old:
            return False
        self.undo_stack.append(('rename', {'index': idx, 'old_name': old, 'new_name': new_name}))
        self.projects[idx] = new_name
        self.project_times[new_name] = self.project_times.pop(old, self.default_duration)
        self.project_paused[new_name] = self.project_paused.pop(old, False)
        self.save()
        return True

    def toggle_pause(self, idx: int):
        if 0 <= idx < len(self.projects):
            p = self.projects[idx]
            self.project_paused[p] = not self.project_paused.get(p, False)
            self.save()

    def reset(self, idx: int):
        if 0 <= idx < len(self.projects):
            p = self.projects[idx]
            self.project_times[p] = self.default_duration
            self.project_paused[p] = False
            self.save()

    def next_project(self):
        if self.projects:
            if p := self.current_project():
                self.project_paused[p] = True
            self.current_index = (self.current_index + 1) % len(self.projects)
            if p := self.current_project():
                self.project_paused[p] = False
            self.save()

    def prev_project(self):
        if self.projects:
            if p := self.current_project():
                self.project_paused[p] = True
            self.current_index = (self.current_index - 1) % len(self.projects)
            if p := self.current_project():
                self.project_paused[p] = False
            self.save()

    def undo(self) -> Optional[str]:
        if not self.undo_stack:
            return None
        op, data = self.undo_stack.pop()
        if op == 'delete':
            self.projects.insert(data['index'], data['name'])
            self.project_times[data['name']] = data['time']
            self.project_paused[data['name']] = data['paused']
            if data['index'] <= self.current_index:
                self.current_index += 1
            self.save()
            return f"Restored: {data['name']}"
        elif op == 'rename':
            self.projects[data['index']] = data['old_name']
            self.project_times[data['old_name']] = self.project_times.pop(data['new_name'], self.default_duration)
            self.project_paused[data['old_name']] = self.project_paused.pop(data['new_name'], False)
            self.save()
            return f"Renamed back to: {data['old_name']}"
        return None

    def set_duration(self, hours: int, minutes: int) -> bool:
        duration = hours * 3600 + minutes * 60
        if duration <= 0:
            return False
        self.default_duration = duration
        self.save()
        return True

    def import_from_file(self, path: str) -> int:
        with open(path, 'r', encoding='utf-8') as f:
            projects = [line.strip() for line in f if line.strip()]
        if not projects:
            raise ValueError("No projects found")
        self.projects = projects
        self.current_index = 0
        self.project_times = {p: self.default_duration for p in projects}
        self.project_paused = {p: False for p in projects}
        self.save()
        return len(projects)

    def export_to_file(self, path: str):
        if not self.projects:
            raise ValueError("No projects to export")
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.projects))

    @staticmethod
    def format_time(seconds: int) -> str:
        h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"
