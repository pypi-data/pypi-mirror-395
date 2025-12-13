#!/usr/bin/env python3
"""Tima - A lean, modern productivity timer built with Flet."""
import flet as ft
import asyncio
try:
    from .state import TimaState
except ImportError:
    from state import TimaState

COLORS = {
    'bg': '#1e1e2e', 'surface': '#2a2a3e', 'primary': '#6c63ff',
    'secondary': '#4a9eff', 'success': '#00d4aa', 'warning': '#ffb86c',
    'danger': '#ff6b6b', 'text': '#e0e0e0', 'text_dim': '#a0a0b0', 'border': '#3a3a4e'
}


class TimaApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.state = TimaState(on_update=self.update, on_timer_end=self.timer_ended)
        self.selected_idx = 0

        # Setup
        page.title, page.window.width, page.window.height = "Tima", 700, 500
        page.window.min_width, page.window.min_height = 600, 450
        page.theme_mode, page.bgcolor, page.padding = ft.ThemeMode.DARK, COLORS['bg'], 15
        page.theme = ft.Theme(color_scheme_seed=COLORS['primary'])
        page.on_close = lambda _: self.state.save()
        page.on_keyboard_event = self.on_key

        # UI elements
        self.activity = ft.Text("", size=16, weight="bold", color=COLORS['text'])
        self.timer = ft.Text("00:00:00", size=42, weight="bold", color=COLORS['primary'])
        self.status = ft.Text("", size=11, color=COLORS['text_dim'])
        self.action_status = ft.Text("", size=11, color=COLORS['success'])
        self.entry = ft.TextField(hint_text="Project name", bgcolor=COLORS['surface'],
                                  border_color=COLORS['border'], focused_border_color=COLORS['primary'],
                                  color=COLORS['text'], text_size=12, height=45,
                                  on_submit=lambda _: self.add_project(), expand=True, autofocus=False)
        self.projects_view = ft.ListView(spacing=4, padding=8, expand=True, auto_scroll=False)

        # Build UI
        page.appbar = ft.AppBar(
            title=ft.Text("Tima", weight="bold"),
            bgcolor=COLORS['surface'],
            actions=[ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Import", on_click=self.import_dlg),
                    ft.PopupMenuItem(text="Export", on_click=self.export_dlg),
                    ft.PopupMenuItem(),
                    ft.PopupMenuItem(text="Settings", on_click=self.settings_dlg),
                    ft.PopupMenuItem(text="Help", on_click=self.help_dlg),
                    ft.PopupMenuItem(),
                    ft.PopupMenuItem(text="Exit", on_click=lambda _: page.window.close()),
                ],
                tooltip="Menu"
            )]
        )

        # Add invisible focus sink to ensure keyboard events work
        self.focus_sink = ft.TextField(width=0, height=0, opacity=0)
        page.add(self.focus_sink)
        page.add(ft.Row([
            # Left panel
            ft.Container(
                content=ft.Column([
                    ft.Container(self.activity, bgcolor=COLORS['surface'], padding=12, border_radius=8,
                                alignment=ft.alignment.center),
                    ft.Container(self.timer, padding=ft.padding.symmetric(vertical=8),
                                alignment=ft.alignment.center),
                    ft.Column([self.status, self.action_status], spacing=4,
                             horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                ], spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
                expand=2, padding=ft.padding.only(right=12)
            ),
            ft.VerticalDivider(width=1, color=COLORS['border']),
            # Right panel
            ft.Container(
                content=ft.Column([
                    ft.Text("PROJECTS", size=11, weight="bold", color=COLORS['text_dim'],
                           text_align=ft.TextAlign.CENTER),
                    ft.Row([self.entry, ft.ElevatedButton("ADD", bgcolor=COLORS['primary'],
                                                          color="white", on_click=lambda _: self.add_project(),
                                                          height=45, autofocus=False)], spacing=8),
                    ft.Container(self.projects_view, bgcolor=COLORS['surface'], border_radius=8,
                                expand=True, padding=4)
                ], spacing=8, expand=True),
                expand=3, padding=ft.padding.only(left=12)
            )
        ], spacing=0, expand=True))

        self.state.load()
        self.selected_idx = self.state.current_index
        self.update()
        page.run_task(self.timer_loop)

    async def timer_loop(self):
        while True:
            await asyncio.sleep(1)
            self.state.tick()

    def update(self):
        self.activity.value = self.state.current_project() or "No Projects"
        self.timer.value = self.state.format_time(self.state.current_time())
        self.status.value = "[PAUSED]" if self.state.is_paused() else "[RUNNING]"
        self.status.color = COLORS['warning'] if self.state.is_paused() else COLORS['success']
        self.render_projects()

    def render_projects(self):
        self.projects_view.controls.clear()
        for i, p in enumerate(self.state.projects):
            time = self.state.project_times.get(p, self.state.default_duration)
            paused = self.state.project_paused.get(p, False)
            is_current, is_selected = i == self.state.current_index, i == self.selected_idx

            prefix = ("> " if is_current else "  ") + ("[PAUSED] " if paused else "")
            text = f"{prefix}{p} ({self.state.format_time(time)})"

            if is_current:
                bg, color, weight, border = COLORS['primary'], "white", "bold", None
            elif is_selected:
                bg, color, weight = COLORS['surface'], COLORS['text'], "normal"
                border = ft.border.all(2, COLORS['secondary'])
            else:
                bg, color, weight, border = "transparent", COLORS['text'], "normal", None

            self.projects_view.controls.append(ft.Container(
                content=ft.Text(text, size=12, color=color, weight=weight),
                bgcolor=bg, border=border, padding=8, border_radius=4,
                on_click=lambda _, idx=i: self.select(idx), ink=True
            ))
        self.page.update()

    def select(self, idx):
        self.selected_idx = idx
        self.render_projects()

    def add_project(self):
        if self.state.add(self.entry.value):
            self.show_status(f"Added: {self.entry.value}")
            self.entry.value = ""
            self.update()

    def timer_ended(self):
        def yes(_):
            self.state.reset(self.state.current_index)
            self.state.next_project()
            self.update()
            dlg.open = False
            self.page.update()

        def no(_):
            self.state.reset(self.state.current_index)
            self.state.project_paused[self.state.current_project()] = False
            self.state.save()
            self.update()
            dlg.open = False
            self.page.update()

        dlg = self.dialog(f"Time's up for: {self.state.current_project()}\n\nMove to next?",
                         [ft.TextButton("No", on_click=no), ft.TextButton("Yes", on_click=yes)])
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()

    def show_status(self, msg: str, color: str = None, duration: int = 3000):
        """Status message with fade animation."""
        self.action_status.value, self.action_status.color = msg, color or COLORS['success']
        self.page.update()

        async def fade():
            await asyncio.sleep(duration / 1000)
            for step in range(20):
                progress = step / 20
                r1, g1, b1 = int((color or COLORS['success'])[1:3], 16), int((color or COLORS['success'])[3:5], 16), int((color or COLORS['success'])[5:7], 16)
                r2, g2, b2 = int(COLORS['bg'][1:3], 16), int(COLORS['bg'][3:5], 16), int(COLORS['bg'][5:7], 16)
                r, g, b = int(r1+(r2-r1)*progress), int(g1+(g2-g1)*progress), int(b1+(b2-b1)*progress)
                self.action_status.color = f'#{r:02x}{g:02x}{b:02x}'
                self.page.update()
                await asyncio.sleep(0.03)
            self.action_status.value = ""
            self.page.update()

        self.page.run_task(fade)

    def dialog(self, content, actions=None, title=""):
        """Generic dialog helper."""
        return ft.AlertDialog(
            title=ft.Text(title) if title else None,
            content=ft.Text(content) if isinstance(content, str) else content,
            actions=actions or [ft.TextButton("OK", on_click=lambda e: self.close_dialog(e.control.parent.parent))],
            actions_alignment=ft.MainAxisAlignment.END
        )

    def close_dialog(self, dlg):
        dlg.open = False
        self.page.update()

    def settings_dlg(self, _):
        h, m = self.state.default_duration // 3600, (self.state.default_duration % 3600) // 60
        hrs, mins = ft.TextField(label="Hours", value=str(h), width=100, keyboard_type=ft.KeyboardType.NUMBER), \
                    ft.TextField(label="Minutes", value=str(m), width=100, keyboard_type=ft.KeyboardType.NUMBER)

        def save(_):
            try:
                if self.state.set_duration(int(hrs.value or 0), int(mins.value or 0)):
                    self.show_status(f"Duration set to {hrs.value}h {mins.value}m", COLORS['secondary'])
                    dlg.open = False
                    self.page.update()
            except:
                pass

        dlg = self.dialog(ft.Column([ft.Text("Set default duration:"),
                                     ft.Row([hrs, mins], spacing=8)], tight=True, spacing=12),
                         [ft.TextButton("Cancel", on_click=lambda _: self.close_dialog(dlg)),
                          ft.TextButton("Save", on_click=save)], "Settings")
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()

    def help_dlg(self, _):
        dlg = self.dialog(ft.Container(ft.Text(
            "SHORTCUTS:\nSpace - Pause/Resume\n↑/↓ - Navigate\nDelete - Delete project\n"
            "Ctrl+Z - Undo\nF2 - Rename\nQ/Esc - Quit",
            font_family="Courier New", size=11), width=400), title="Help")
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()

    def rename_dlg(self):
        if not 0 <= self.selected_idx < len(self.state.projects):
            return
        old = self.state.projects[self.selected_idx]
        field = ft.TextField(value=old, autofocus=True)

        def save(_):
            if self.state.rename(self.selected_idx, field.value):
                self.show_status(f"Renamed to: {field.value}", COLORS['secondary'])
                self.update()
            dlg.open = False
            self.page.update()

        field.on_submit = save
        dlg = self.dialog(field, [ft.TextButton("Cancel", on_click=lambda _: self.close_dialog(dlg)),
                                  ft.TextButton("Rename", on_click=save)], "Rename")
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()

    def import_dlg(self, _):
        def on_result(e):
            if e.files:
                try:
                    count = self.state.import_from_file(e.files[0].path)
                    self.show_status(f"Imported {count} projects!", COLORS['secondary'])
                    self.update()
                except Exception as ex:
                    self.show_status(f"Import failed: {ex}", COLORS['danger'])

        picker = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(picker)
        self.page.update()
        picker.pick_files(dialog_title="Import", allowed_extensions=["txt"], allow_multiple=False)

    def export_dlg(self, _):
        def on_result(e):
            if e.path:
                try:
                    self.state.export_to_file(e.path)
                    self.show_status("Exported!", COLORS['secondary'])
                except Exception as ex:
                    self.show_status(f"Export failed: {ex}", COLORS['danger'])

        picker = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(picker)
        self.page.update()
        picker.save_file(dialog_title="Export", file_name="tima_projects.txt", allowed_extensions=["txt"])

    def on_key(self, e: ft.KeyboardEvent):
        # Always move focus to invisible sink to prevent buttons from activating
        self.focus_sink.focus()

        if e.key == " ":
            self.state.toggle_pause(self.state.current_index)
            self.update()
            return

        handlers = {
            "Arrow Up": self.state.prev_project, "Page Up": self.state.prev_project,
            "Arrow Down": self.state.next_project, "Page Down": self.state.next_project,
            "Delete": lambda: self.state.delete(self.selected_idx) and self.update(),
            "F2": self.rename_dlg,
            "Q": self.page.window.close, "Escape": self.page.window.close,
            "?": lambda: self.help_dlg(None)
        }
        if e.key in handlers:
            handlers[e.key]() if callable(handlers[e.key]) else None
            self.update()
        elif e.key == "Z" and e.ctrl:
            if msg := self.state.undo():
                self.show_status(msg, COLORS['secondary'])
                self.update()


def main():
    ft.app(target=lambda page: TimaApp(page))


if __name__ == "__main__":
    main()
