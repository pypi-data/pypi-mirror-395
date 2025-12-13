#!/usr/bin/env python3
"""
Tima - Activity Timer (Flet Version)
A desktop productivity timer that cycles through your projects with customizable durations.
"""
import flet as ft
from typing import Optional
import asyncio

try:
    from .timer_logic import TimerManager
except ImportError:
    from timer_logic import TimerManager


# Modern color scheme (matching original)
COLORS = {
    'bg': '#1e1e2e',
    'surface': '#2a2a3e',
    'primary': '#6c63ff',
    'secondary': '#4a9eff',
    'success': '#00d4aa',
    'warning': '#ffb86c',
    'danger': '#ff6b6b',
    'text': '#e0e0e0',
    'text_dim': '#a0a0b0',
    'border': '#3a3a4e'
}


class TimaApp:
    """Main Tima application"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.timer_manager = TimerManager(
            on_update=self.on_timer_update,
            on_timer_end=self.on_timer_end
        )

        # UI references
        self.activity_label: Optional[ft.Text] = None
        self.timer_label: Optional[ft.Text] = None
        self.status_label: Optional[ft.Text] = None
        self.action_status_label: Optional[ft.Text] = None
        self.project_list: Optional[ft.ListView] = None
        self.project_entry: Optional[ft.TextField] = None
        self.selected_project_index: int = 0

        # Setup page
        self.setup_page()

        # Load data
        self.timer_manager.load_data()

        # Build UI
        self.build_ui()

        # Set initial selection to current project
        self.selected_project_index = self.timer_manager.state.current_project_index

        # Start timer using page.run_task
        page.run_task(self.timer_loop)

    def setup_page(self):
        """Configure page settings"""
        self.page.title = "Tima"
        self.page.window.width = 700
        self.page.window.height = 500
        self.page.window.min_width = 600
        self.page.window.min_height = 450
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = COLORS['bg']
        self.page.padding = 15

        # Set theme
        self.page.theme = ft.Theme(color_scheme_seed=COLORS['primary'])

        # Window close handler
        self.page.on_close = self.on_closing

        # Keyboard event handler
        self.page.on_keyboard_event = self.on_keyboard

    def build_ui(self):
        """Build the user interface"""
        # Menu bar
        self.page.appbar = self.create_appbar()

        # Main content - two panel layout
        self.page.add(
            ft.Row(
                controls=[
                    # Left panel - Current project and timer
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                # Current activity
                                self.create_activity_section(),

                                # Timer display
                                self.create_timer_section(),

                                # Status
                                self.create_status_section(),
                            ],
                            spacing=12,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            expand=True
                        ),
                        expand=2,
                        padding=ft.padding.only(right=12)
                    ),

                    # Divider
                    ft.VerticalDivider(width=1, color=COLORS['border']),

                    # Right panel - Projects list
                    ft.Container(
                        content=self.create_projects_section(),
                        expand=3,
                        padding=ft.padding.only(left=12)
                    ),
                ],
                spacing=0,
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START
            )
        )

        self.update_display()

    def create_appbar(self) -> ft.AppBar:
        """Create application menu bar"""
        return ft.AppBar(
            title=ft.Text("Tima", weight=ft.FontWeight.BOLD),
            center_title=False,
            bgcolor=COLORS['surface'],
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Import Projects", on_click=self.import_projects_dialog),
                        ft.PopupMenuItem(text="Export Projects", on_click=self.export_projects_dialog),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(text="Settings", on_click=self.show_settings_dialog),
                        ft.PopupMenuItem(text="Keyboard Shortcuts", on_click=self.show_help_dialog),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(text="Exit", on_click=lambda _: self.page.window.close()),
                    ]
                )
            ]
        )

    def create_activity_section(self) -> ft.Container:
        """Create current activity display"""
        self.activity_label = ft.Text(
            "Loading...",
            size=16,
            weight=ft.FontWeight.BOLD,
            color=COLORS['text'],
            text_align=ft.TextAlign.CENTER
        )

        return ft.Container(
            content=self.activity_label,
            bgcolor=COLORS['surface'],
            padding=12,
            border_radius=8,
            alignment=ft.alignment.center
        )

    def create_timer_section(self) -> ft.Container:
        """Create timer display"""
        self.timer_label = ft.Text(
            "00:00:00",
            size=42,
            weight=ft.FontWeight.BOLD,
            color=COLORS['primary'],
            text_align=ft.TextAlign.CENTER
        )

        return ft.Container(
            content=self.timer_label,
            padding=ft.padding.symmetric(vertical=8),
            alignment=ft.alignment.center
        )

    def create_status_section(self) -> ft.Column:
        """Create status display"""
        self.status_label = ft.Text(
            "",
            size=11,
            color=COLORS['text_dim'],
            text_align=ft.TextAlign.CENTER
        )

        self.action_status_label = ft.Text(
            "",
            size=11,
            color=COLORS['success'],
            text_align=ft.TextAlign.CENTER
        )

        return ft.Column(
            controls=[self.status_label, self.action_status_label],
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def create_projects_section(self) -> ft.Container:
        """Create projects management section"""
        # Add project controls
        self.project_entry = ft.TextField(
            hint_text="Enter project name",
            bgcolor=COLORS['surface'],
            border_color=COLORS['border'],
            focused_border_color=COLORS['primary'],
            color=COLORS['text'],
            cursor_color=COLORS['primary'],
            text_size=12,
            height=45,
            on_submit=lambda _: self.add_project(),
            expand=True
        )

        add_button = ft.ElevatedButton(
            "ADD",
            bgcolor=COLORS['primary'],
            color="white",
            on_click=lambda _: self.add_project(),
            height=45
        )

        add_row = ft.Row(
            controls=[self.project_entry, add_button],
            spacing=8
        )

        # Project list
        self.project_list = ft.ListView(
            spacing=4,
            padding=8,
            expand=True,
            auto_scroll=False
        )

        list_container = ft.Container(
            content=self.project_list,
            bgcolor=COLORS['surface'],
            border_radius=8,
            expand=True,
            padding=4
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "PROJECTS",
                        size=11,
                        weight=ft.FontWeight.BOLD,
                        color=COLORS['text_dim'],
                        text_align=ft.TextAlign.CENTER
                    ),
                    add_row,
                    list_container
                ],
                spacing=8,
                expand=True
            ),
            expand=True
        )

    def render_projects(self):
        """Render the project list"""
        self.project_list.controls.clear()

        state = self.timer_manager.state
        for i, project in enumerate(state.projects):
            time_left = state.project_times.get(project, state.default_duration)
            is_paused = state.project_paused.get(project, False)
            is_current = i == state.current_project_index
            is_selected = i == self.selected_project_index

            # Build status prefix
            prefix = "> " if is_current else "  "
            if is_paused:
                prefix += "[PAUSED] "

            time_str = TimerManager.format_time(time_left)
            display_text = f"{prefix}{project} ({time_str})"

            # Determine colors based on state
            if is_current:
                bg_color = COLORS['primary']
                text_color = "white"
                text_weight = ft.FontWeight.BOLD
                border = None
            elif is_selected:
                bg_color = COLORS['surface']
                text_color = COLORS['text']
                text_weight = ft.FontWeight.NORMAL
                border = ft.border.all(2, COLORS['secondary'])
            else:
                bg_color = "transparent"
                text_color = COLORS['text']
                text_weight = ft.FontWeight.NORMAL
                border = None

            # Create list item with context menu
            item = ft.Container(
                content=ft.Text(
                    display_text,
                    size=12,
                    color=text_color,
                    weight=text_weight
                ),
                bgcolor=bg_color,
                border=border,
                padding=8,
                border_radius=4,
                on_click=lambda e, idx=i: self.select_project(idx),
                ink=True,
            )

            self.project_list.controls.append(item)

        self.page.update()

    def select_project(self, index: int):
        """Select a project in the list"""
        self.selected_project_index = index
        self.render_projects()

    def add_project(self):
        """Add a new project"""
        name = self.project_entry.value
        if self.timer_manager.add_project(name):
            self.project_entry.value = ""
            self.show_status(f"Added project: {name}")
            self.update_display()

    def delete_selected_project(self):
        """Delete the selected project"""
        if self.timer_manager.delete_project(self.selected_project_index):
            project_name = self.timer_manager.state.projects[self.selected_project_index] if self.selected_project_index < len(self.timer_manager.state.projects) else "project"
            self.show_status(f"Deleted project", color=COLORS['danger'])
            self.update_display()

    def rename_selected_project(self):
        """Show dialog to rename selected project"""
        if 0 <= self.selected_project_index < len(self.timer_manager.state.projects):
            old_name = self.timer_manager.state.projects[self.selected_project_index]

            def on_rename(e):
                new_name = rename_field.value
                if self.timer_manager.rename_project(self.selected_project_index, new_name):
                    self.show_status(f"Renamed to: {new_name}", color=COLORS['secondary'])
                    self.update_display()
                    dialog.open = False
                    self.page.update()

            def on_cancel(e):
                dialog.open = False
                self.page.update()

            rename_field = ft.TextField(
                value=old_name,
                autofocus=True,
                on_submit=on_rename
            )

            dialog = ft.AlertDialog(
                title=ft.Text("Rename Project"),
                content=rename_field,
                actions=[
                    ft.TextButton("Cancel", on_click=on_cancel),
                    ft.TextButton("Rename", on_click=on_rename),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            self.page.overlay.append(dialog)
            dialog.open = True
            self.page.update()

    def reset_selected_project(self):
        """Reset selected project timer"""
        self.timer_manager.reset_project(self.selected_project_index)
        self.update_display()

    def toggle_selected_project(self):
        """Toggle pause for selected project"""
        self.timer_manager.toggle_project_pause(self.selected_project_index)
        project = self.timer_manager.state.projects[self.selected_project_index]
        paused = self.timer_manager.state.project_paused.get(project, False)
        self.show_status(f"{'Paused' if paused else 'Resumed'}: {project}")
        self.update_display()

    def toggle_current_project(self):
        """Toggle pause for current project"""
        self.timer_manager.toggle_project_pause(self.timer_manager.state.current_project_index)
        project = self.timer_manager.state.get_current_project()
        paused = self.timer_manager.state.is_current_project_paused()
        self.show_status(f"{'Paused' if paused else 'Resumed'}: {project}")
        self.update_display()

    def next_project(self):
        """Move to next project"""
        self.timer_manager.next_project()
        self.update_display()

    def previous_project(self):
        """Move to previous project"""
        self.timer_manager.previous_project()
        self.update_display()

    def undo_last_operation(self):
        """Undo last operation"""
        message = self.timer_manager.undo()
        if message:
            self.show_status(message, color=COLORS['secondary'])
            self.update_display()
        else:
            self.show_status("Nothing to undo!", color=COLORS['text_dim'])

    def update_display(self):
        """Update all display elements"""
        state = self.timer_manager.state

        # Update activity
        if self.activity_label:
            current = state.get_current_project()
            self.activity_label.value = current if current else "No Projects"

        # Update timer
        if self.timer_label:
            time_left = state.get_current_time_left()
            self.timer_label.value = TimerManager.format_time(time_left)

            # Flash red when time is up
            if time_left <= 0 and not state.is_current_project_paused():
                # Timer will alternate colors automatically via timer_tick
                pass
            else:
                self.timer_label.color = COLORS['primary']

        # Update status
        if self.status_label:
            if state.projects:
                if state.is_current_project_paused():
                    self.status_label.value = "[PAUSED]"
                    self.status_label.color = COLORS['warning']
                else:
                    self.status_label.value = "[RUNNING]"
                    self.status_label.color = COLORS['success']
            else:
                self.status_label.value = "No projects"
                self.status_label.color = COLORS['text_dim']

        # Render projects
        self.render_projects()

    def on_timer_update(self):
        """Called when timer ticks"""
        self.update_display()

    def on_timer_end(self):
        """Called when timer reaches zero"""
        current_project = self.timer_manager.state.get_current_project()

        def on_yes(e):
            dialog.open = False
            self.page.update()
            self.timer_manager.reset_current_and_continue(move_to_next=True)
            self.update_display()

        def on_no(e):
            dialog.open = False
            self.page.update()
            self.timer_manager.reset_current_and_continue(move_to_next=False)
            self.update_display()

        dialog = ft.AlertDialog(
            title=ft.Text("Timer Ended!"),
            content=ft.Text(f"Time's up for: {current_project}\n\nMove to next project?"),
            actions=[
                ft.TextButton("No", on_click=on_no),
                ft.TextButton("Yes", on_click=on_yes),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def show_status(self, message: str, color: str = None, duration: int = 3000):
        """Show temporary status message"""
        if color is None:
            color = COLORS['success']

        if self.action_status_label:
            self.action_status_label.value = message
            self.action_status_label.color = color
            self.page.update()

            # Schedule clear after duration
            async def clear_after_delay():
                await asyncio.sleep(duration / 1000)
                if self.action_status_label:
                    self.action_status_label.value = ""
                    self.page.update()

            self.page.run_task(clear_after_delay)

    def show_settings_dialog(self, e):
        """Show settings dialog"""
        current_hours = self.timer_manager.state.default_duration // 3600
        current_minutes = (self.timer_manager.state.default_duration % 3600) // 60

        hours_field = ft.TextField(
            label="Hours",
            value=str(current_hours),
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER
        )

        minutes_field = ft.TextField(
            label="Minutes",
            value=str(current_minutes),
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER
        )

        def on_save(e):
            try:
                hours = int(hours_field.value or 0)
                minutes = int(minutes_field.value or 0)

                if self.timer_manager.set_default_duration(hours, minutes):
                    self.show_status(f"Default duration set to {hours}h {minutes}m", color=COLORS['secondary'])
                    dialog.open = False
                    self.page.update()
                else:
                    # Show error
                    pass
            except ValueError:
                pass

        def on_cancel(e):
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Set Default Duration"),
            content=ft.Column(
                controls=[
                    ft.Text("Set default duration for new projects:"),
                    ft.Row(
                        controls=[hours_field, minutes_field],
                        spacing=8
                    )
                ],
                tight=True,
                spacing=12
            ),
            actions=[
                ft.TextButton("Cancel", on_click=on_cancel),
                ft.TextButton("Save", on_click=on_save),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def show_help_dialog(self, e):
        """Show keyboard shortcuts help"""
        help_text = """GLOBAL SHORTCUTS:
Space              Pause/Resume current project
Up / Page Up       Previous project
Down / Page Down   Next project
Delete             Delete selected project
Ctrl+Z             Undo last delete/rename
Q / Esc            Quit application

PROJECT LIST:
Click              Select project
Double-click       Rename project
F2                 Rename selected project

ADD PROJECT:
Enter              Add project (in text entry field)
"""

        dialog = ft.AlertDialog(
            title=ft.Text("Keyboard Shortcuts"),
            content=ft.Container(
                content=ft.Text(help_text, font_family="Courier New", size=11),
                width=400
            ),
            actions=[
                ft.TextButton("Close", on_click=lambda e: self.close_dialog(dialog)),
            ],
        )

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def import_projects_dialog(self, e):
        """Show import projects dialog"""
        def on_file_result(e: ft.FilePickerResultEvent):
            if e.files:
                try:
                    count = self.timer_manager.import_projects(e.files[0].path)
                    self.show_status(f"Imported {count} projects!", color=COLORS['secondary'])
                    self.update_display()
                except Exception as ex:
                    self.show_status(f"Import failed: {ex}", color=COLORS['danger'])

        file_picker = ft.FilePicker(on_result=on_file_result)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files(
            dialog_title="Import Projects",
            allowed_extensions=["txt"],
            allow_multiple=False
        )

    def export_projects_dialog(self, e):
        """Show export projects dialog"""
        def on_file_result(e: ft.FilePickerResultEvent):
            if e.path:
                try:
                    self.timer_manager.export_projects(e.path)
                    self.show_status("Projects exported!", color=COLORS['secondary'])
                except Exception as ex:
                    self.show_status(f"Export failed: {ex}", color=COLORS['danger'])

        file_picker = ft.FilePicker(on_result=on_file_result)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.save_file(
            dialog_title="Export Projects",
            file_name="tima_projects.txt",
            allowed_extensions=["txt"]
        )

    def close_dialog(self, dialog):
        """Close a dialog"""
        dialog.open = False
        self.page.update()

    def on_keyboard(self, e: ft.KeyboardEvent):
        """Handle keyboard events"""
        # Space: pause/resume current
        if e.key == " " and not e.ctrl and not e.shift and not e.alt:
            self.toggle_current_project()
            return

        # Arrow keys: navigate projects
        if e.key == "Arrow Up" or e.key == "Page Up":
            self.previous_project()
        elif e.key == "Arrow Down" or e.key == "Page Down":
            self.next_project()

        # Delete: delete selected project
        elif e.key == "Delete":
            self.delete_selected_project()

        # Ctrl+Z: undo
        elif e.key == "Z" and e.ctrl:
            self.undo_last_operation()

        # F2: rename selected
        elif e.key == "F2":
            self.rename_selected_project()

        # Q or Escape: quit
        elif e.key == "Q" or e.key == "Escape":
            self.page.window.close()

        # ?: help
        elif e.key == "?":
            self.show_help_dialog(None)

    async def timer_loop(self):
        """Main timer loop"""
        while True:
            await asyncio.sleep(1)
            self.timer_manager.tick()

    def on_closing(self, e):
        """Handle window close"""
        self.timer_manager.save_data()


def main():
    """Main entry point"""
    def app_main(page: ft.Page):
        TimaApp(page)

    ft.app(target=app_main)


if __name__ == "__main__":
    main()
