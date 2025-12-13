#!/usr/bin/env python3
"""
Tima - Activity Timer
A desktop productivity timer that cycles through your projects with customizable durations.
"""

import json
import os
import tkinter as tk
import winsound  # For Windows alarm sound (use 'playsound' library for cross-platform)
from datetime import datetime, timedelta
from pathlib import Path
from tkinter import ttk, messagebox, filedialog
from io import BytesIO


from PIL import Image, ImageDraw
PIL_AVAILABLE = True



class TimaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tima")
        self.root.geometry("400x500")
        self.root.minsize(350, 450)

        # Modern color scheme
        self.colors = {
            'bg': '#1e1e2e',           # Dark background
            'surface': '#2a2a3e',       # Surface elements
            'primary': '#6c63ff',       # Primary accent
            'secondary': '#4a9eff',     # Secondary accent
            'success': '#00d4aa',       # Success/active
            'warning': '#ffb86c',       # Warning
            'danger': '#ff6b6b',        # Danger/delete
            'text': '#e0e0e0',          # Main text
            'text_dim': '#a0a0b0',      # Dimmed text
            'border': '#3a3a4e'         # Borders
        }

        self.root.configure(bg=self.colors['bg'])
        self.root.resizable(True, True)

        # Set custom icon
        self.set_window_icon()

        # App state
        self.projects = []
        self.current_project_index = 0
        self.default_duration = 3600  # 1 hour in seconds
        self.project_times = {}  # Track remaining time for each project
        self.project_paused = {}  # Track pause state for each project
        self.timer_running = False

        # Use user's home directory for data storage
        config_dir = Path.home() / ".tima"
        config_dir.mkdir(exist_ok=True)
        self.data_file = str(config_dir / "tima_projects.json")

        # Timer state
        self.last_update_time = None
        self.after_id = None

        # Undo stack for delete/rename operations
        self.undo_stack = []
        self.max_undo_stack_size = 10

        # Load saved projects
        self.load_projects()

        # Create GUI
        self.setup_gui()

        # Start the timer
        self.start_timer()

        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Bind global keyboard shortcuts
        self.setup_global_shortcuts()

    def set_window_icon(self):
        """Set a custom window icon"""
        try:
            # Create a 64x64 icon with a modern clock design
            size = 64
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # Parse primary color
            primary_rgb = tuple(int(self.colors['primary'][i:i+2], 16) for i in (1, 3, 5))

            # Draw circle background
            padding = 4
            draw.ellipse(
                [padding, padding, size-padding, size-padding],
                fill=primary_rgb,
                outline=None
            )

            # Draw clock hands (simplified)
            center = size // 2
            # Hour hand (pointing up-right)
            draw.line([center, center, center + 8, center - 10], fill='white', width=4)
            # Minute hand (pointing right)
            draw.line([center, center, center + 14, center - 6], fill='white', width=3)
            # Center dot
            draw.ellipse([center-3, center-3, center+3, center+3], fill='white')

            # Save as .ico file in user's config directory
            config_dir = Path.home() / ".tima"
            config_dir.mkdir(exist_ok=True)
            icon_path = str(config_dir / 'tima_icon.ico')
            img.save(icon_path, format='ICO', sizes=[(64, 64)])

            # Use iconbitmap for better Windows taskbar support
            self.root.iconbitmap(icon_path)

        except Exception as e:
            print(f"Could not set icon: {e}")
            # Fallback to iconphoto if ico fails
            try:
                bio = BytesIO()
                img.save(bio, format='PNG')
                bio.seek(0)
                photo = tk.PhotoImage(data=bio.getvalue())
                self.root.iconphoto(True, photo)
                self.root._icon_photo = photo
            except:
                pass

    def create_menu_bar(self):
        """Create the application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import Projects...", command=self.import_projects)
        file_menu.add_command(label="Export Projects...", command=self.export_projects)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)

        # Project menu
        project_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Project", menu=project_menu)
        project_menu.add_command(label="Rename Selected", command=self.rename_project, accelerator="F2")
        project_menu.add_command(label="Delete Selected", command=self.delete_project, accelerator="Del")
        project_menu.add_separator()
        project_menu.add_command(label="Reset Selected", command=self.reset_selected_project)
        project_menu.add_command(label="Pause/Resume Selected", command=self.toggle_selected_project)

        # Timer menu
        timer_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Timer", menu=timer_menu)
        timer_menu.add_command(label="Pause/Resume Current", command=self.toggle_current_project, accelerator="Space")
        timer_menu.add_command(label="Reset Current", command=self.reset_current_project)
        timer_menu.add_separator()
        timer_menu.add_command(label="Next Project", command=self.next_project, accelerator="Down")
        timer_menu.add_command(label="Previous Project", command=self.previous_project, accelerator="Up")

        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Set Default Duration...", command=self.show_duration_dialog)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_help, accelerator="?")

    def setup_gui(self):
        # Create menu bar
        self.create_menu_bar()

        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'], padx=15, pady=12)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Current activity display
        self.activity_frame = tk.Frame(main_frame, bg=self.colors['surface'], relief=tk.FLAT, bd=0)
        self.activity_frame.pack(fill=tk.X, pady=(0, 12))

        self.activity_label = tk.Label(
            self.activity_frame,
            text="Loading...",
            font=('Segoe UI', 13, 'bold'),
            bg=self.colors['surface'],
            fg=self.colors['text'],
            pady=12
        )
        self.activity_label.pack()

        # Timer display
        self.timer_label = tk.Label(
            main_frame,
            text="00:30:00",
            font=('Segoe UI', 42, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        )
        self.timer_label.pack(pady=(8, 8))

        # Status container (combined status + action status)
        status_container = tk.Frame(main_frame, bg=self.colors['bg'])
        status_container.pack(fill=tk.X, pady=(0, 10))

        self.status_label = tk.Label(
            status_container,
            text="",
            font=('Segoe UI', 9),
            bg=self.colors['bg'],
            fg=self.colors['text_dim']
        )
        self.status_label.pack()

        # Action status message (for showing temporary feedback)
        self.action_status_label = tk.Label(
            status_container,
            text="",
            font=('Segoe UI', 9),
            bg=self.colors['bg'],
            fg=self.colors['success'],
            height=1
        )
        self.action_status_label.pack()
        self.action_status_timer = None

        # Project management section
        project_frame = tk.LabelFrame(
            main_frame,
            text="  PROJECTS  ",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text_dim'],
            labelanchor='n',
            relief=tk.FLAT,
            bd=0,
            padx=0,
            pady=8
        )
        project_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 0))

        # Add project controls
        add_frame = tk.Frame(project_frame, bg=self.colors['bg'])
        add_frame.pack(fill=tk.X, pady=(0, 8), padx=10)

        self.project_entry = tk.Entry(
            add_frame,
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            bg=self.colors['surface'],
            fg=self.colors['text'],
            insertbackground=self.colors['primary'],
            bd=0,
            highlightthickness=1,
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['primary']
        )
        self.project_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6), ipady=6)
        self.project_entry.bind('<Return>', lambda e: self.add_project())

        tk.Button(
            add_frame,
            text="ADD",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.colors['secondary'],
            activeforeground='white',
            relief=tk.FLAT,
            bd=0,
            padx=16,
            pady=6,
            cursor='hand2',
            command=self.add_project
        ).pack(side=tk.RIGHT)

        # Project list with scrollbar
        list_frame = tk.Frame(project_frame, bg=self.colors['bg'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        self.project_listbox = tk.Listbox(
            list_frame,
            font=('Segoe UI', 10),
            height=8,
            relief=tk.FLAT,
            bd=0,
            selectmode=tk.SINGLE,
            exportselection=False,
            highlightthickness=0,
            bg=self.colors['surface'],
            fg=self.colors['text'],
            selectbackground=self.colors['primary'],
            selectforeground='white',
            activestyle='none'
        )
        self.project_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(
            list_frame,
            orient=tk.VERTICAL,
            bg=self.colors['surface'],
            troughcolor=self.colors['bg'],
            activebackground=self.colors['primary'],
            bd=0,
            width=12
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(4, 0))

        self.project_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.project_listbox.yview)

        # Bind keyboard shortcuts for project management
        self.project_listbox.bind('<F2>', lambda e: self.rename_project())
        self.project_listbox.bind('<Return>', lambda e: self.rename_project())
        self.project_listbox.bind('<Double-Button-1>', lambda e: self.rename_project())

        # Initial render
        self.render_projects()

    def setup_global_shortcuts(self):
        """Setup global keyboard shortcuts"""
        # Space: Pause/Resume current project
        self.root.bind('<space>', lambda e: self.toggle_current_project())

        # Arrow keys and Page Up/Down: Navigate projects
        self.root.bind('<Up>', lambda e: self.previous_project())
        self.root.bind('<Down>', lambda e: self.next_project())
        self.root.bind('<Prior>', lambda e: self.previous_project())  # Page Up
        self.root.bind('<Next>', lambda e: self.next_project())  # Page Down

        # Delete: Delete selected project
        self.root.bind('<Delete>', lambda e: self.delete_project())

        # Ctrl+Z: Undo last delete/rename (use bind_all to work even when entry has focus)
        self.root.bind_all('<Control-z>', self.handle_undo_key)

        # ?: Show help
        self.root.bind('?', lambda e: self.show_help())

    def show_help(self):
        """Show keyboard shortcuts help dialog"""
        help_dialog = tk.Toplevel(self.root)
        help_dialog.title("Keyboard Shortcuts")
        help_dialog.geometry("380x300")
        help_dialog.configure(bg='#f4f7f6')
        help_dialog.transient(self.root)
        help_dialog.grab_set()

        # Center the dialog
        help_dialog.update_idletasks()
        x = (help_dialog.winfo_screenwidth() // 2) - (help_dialog.winfo_width() // 2)
        y = (help_dialog.winfo_screenheight() // 2) - (help_dialog.winfo_height() // 2)
        help_dialog.geometry(f"+{x}+{y}")

        # Dialog content
        frame = tk.Frame(help_dialog, bg='#f4f7f6', padx=16, pady=12)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            frame,
            text="Keyboard Shortcuts",
            bg='#f4f7f6',
            font=('Arial', 12, 'bold'),
            fg='#2c3e50'
        ).pack(pady=(0, 10))

        # Create shortcuts text
        shortcuts_text = tk.Text(
            frame,
            font=('Courier New', 9),
            bg='white',
            relief=tk.SOLID,
            bd=1,
            wrap=tk.WORD,
            height=13,
            width=42
        )
        shortcuts_text.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        help_content = """GLOBAL SHORTCUTS:
  Space              Pause/Resume current project
  Up / Page Up       Previous project
  Down / Page Down   Next project
  Delete             Delete selected project
  Ctrl+Z             Undo last delete/rename
  ?                  Show this help screen

PROJECT LIST SHORTCUTS:
  Enter              Rename selected project
  F2                 Rename selected project
  Double-click       Rename selected project

ADD PROJECT:
  Enter              Add project (in text entry field)

RENAME DIALOG:
  Enter              Save new name
  Escape             Cancel rename
"""

        shortcuts_text.insert('1.0', help_content)
        shortcuts_text.config(state=tk.DISABLED)

        # Close button
        tk.Button(
            frame,
            text="Close",
            font=('Arial', 9),
            bg='#3498db',
            fg='white',
            padx=24,
            pady=3,
            command=help_dialog.destroy
        ).pack()

        # Bind Escape to close
        help_dialog.bind('<Escape>', lambda e: help_dialog.destroy())
        help_dialog.focus_set()

    def previous_project(self):
        """Move to the previous project"""
        if self.projects:
            self.current_project_index = (self.current_project_index - 1) % len(self.projects)
            self.save_projects()
            self.update_display()

    def handle_undo_key(self, event):
        """Handle Ctrl+Z - skip if typing in an entry field"""
        focused_widget = self.root.focus_get()
        # If an Entry widget has focus, let it handle Ctrl+Z for text undo
        if isinstance(focused_widget, tk.Entry):
            return
        # Otherwise, handle project undo
        self.undo_last_operation()

    def show_status(self, message, duration=3000, color=None):
        """Show a temporary status message that fades away"""
        if color is None:
            color = self.colors['success']

        # Cancel any existing timer
        if self.action_status_timer:
            self.root.after_cancel(self.action_status_timer)

        # Show the message
        self.action_status_label.config(text=message, fg=color)

        # Schedule fade out after duration
        self.action_status_timer = self.root.after(duration, lambda: self.fade_status(color, 0))

    def fade_status(self, original_color, step):
        """Fade out the status message smoothly"""
        total_steps = 20
        if step >= total_steps:
            self.clear_status()
            return

        # Interpolate between original color and background color
        progress = step / total_steps
        faded_color = self.interpolate_color(original_color, self.colors['bg'], progress)

        self.action_status_label.config(fg=faded_color)

        # Schedule next fade step
        self.action_status_timer = self.root.after(30, lambda: self.fade_status(original_color, step + 1))

    def interpolate_color(self, color1, color2, progress):
        """Interpolate between two hex colors"""
        # Convert hex to RGB
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)

        # Interpolate
        r = int(r1 + (r2 - r1) * progress)
        g = int(g1 + (g2 - g1) * progress)
        b = int(b1 + (b2 - b1) * progress)

        # Convert back to hex
        return f'#{r:02x}{g:02x}{b:02x}'

    def clear_status(self):
        """Clear the action status message"""
        self.action_status_label.config(text="")
        self.action_status_timer = None

    def push_undo(self, operation_type, data):
        """Push an undo operation onto the stack"""
        self.undo_stack.append({
            'type': operation_type,
            'data': data
        })
        # Limit stack size
        if len(self.undo_stack) > self.max_undo_stack_size:
            self.undo_stack.pop(0)

    def undo_last_operation(self):
        """Undo the last delete or rename operation"""
        if not self.undo_stack:
            self.show_status("Nothing to undo!", color=self.colors['text_dim'])
            return

        operation = self.undo_stack.pop()
        op_type = operation['type']
        data = operation['data']

        if op_type == 'delete':
            # Restore deleted project
            index = data['index']
            project_name = data['name']
            project_time = data['time']
            project_paused = data['paused']

            # Insert project back at its original position
            self.projects.insert(index, project_name)
            self.project_times[project_name] = project_time
            self.project_paused[project_name] = project_paused

            # Adjust current project index if needed
            if index <= self.current_project_index:
                self.current_project_index += 1

            self.save_projects()
            self.render_projects()
            self.update_current_activity()
            self.show_status(f"Restored project: {project_name}", color=self.colors['secondary'])

        elif op_type == 'rename':
            # Restore old project name
            index = data['index']
            old_name = data['old_name']
            new_name = data['new_name']

            # Rename back to old name
            self.projects[index] = old_name

            # Restore project data with old name
            if new_name in self.project_times:
                self.project_times[old_name] = self.project_times.pop(new_name)
            if new_name in self.project_paused:
                self.project_paused[old_name] = self.project_paused.pop(new_name)

            self.save_projects()
            self.render_projects()
            self.update_current_activity()
            self.show_status(f"Renamed back to: {old_name}", color=self.colors['secondary'])

    def show_duration_dialog(self):
        """Show dialog to set default duration"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Set Default Duration")
        dialog.geometry("320x140")
        dialog.configure(bg='#f4f7f6')
        dialog.transient(self.root)
        dialog.grab_set()

        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        # Dialog content
        frame = tk.Frame(dialog, bg='#f4f7f6', padx=16, pady=12)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            frame,
            text="Set default duration for new projects:",
            bg='#f4f7f6',
            font=('Arial', 10)
        ).pack(anchor=tk.W, pady=(0, 8))

        # Duration inputs
        input_frame = tk.Frame(frame, bg='#f4f7f6')
        input_frame.pack(pady=(0, 12))

        current_hours = self.default_duration // 3600
        current_minutes = (self.default_duration % 3600) // 60

        hours_var = tk.StringVar(value=str(current_hours))
        minutes_var = tk.StringVar(value=str(current_minutes))

        tk.Entry(input_frame, textvariable=hours_var, width=4, font=('Arial', 10)).pack(side=tk.LEFT, padx=(0, 2))
        tk.Label(input_frame, text="hours", bg='#f4f7f6', font=('Arial', 9)).pack(side=tk.LEFT, padx=(0, 8))

        tk.Entry(input_frame, textvariable=minutes_var, width=4, font=('Arial', 10)).pack(side=tk.LEFT, padx=(0, 2))
        tk.Label(input_frame, text="minutes", bg='#f4f7f6', font=('Arial', 9)).pack(side=tk.LEFT)

        def save_duration():
            try:
                hours = int(hours_var.get() or 0)
                minutes = int(minutes_var.get() or 0)
                new_duration = hours * 3600 + minutes * 60

                if new_duration <= 0:
                    messagebox.showwarning("Invalid Duration", "Duration must be greater than 0!")
                else:
                    self.default_duration = new_duration
                    self.save_projects()
                    self.show_status(f"Default duration set to {hours}h {minutes}m", color=self.colors['secondary'])
                    dialog.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers!")

        # Buttons
        btn_frame = tk.Frame(frame, bg='#f4f7f6')
        btn_frame.pack()

        tk.Button(
            btn_frame,
            text="Save",
            font=('Arial', 9),
            bg='#3498db',
            fg='white',
            padx=16,
            pady=3,
            command=save_duration
        ).pack(side=tk.LEFT, padx=(0, 4))

        tk.Button(
            btn_frame,
            text="Cancel",
            font=('Arial', 9),
            bg='#95a5a6',
            fg='white',
            padx=16,
            pady=3,
            command=dialog.destroy
        ).pack(side=tk.LEFT)

        # Bind Enter and Escape
        dialog.bind('<Return>', lambda e: save_duration())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
        dialog.focus_set()

    def get_current_time_left(self):
        """Get the time left for the current project"""
        if not self.projects or self.current_project_index >= len(self.projects):
            return 0

        project_name = self.projects[self.current_project_index]
        return self.project_times.get(project_name, self.default_duration)

    def set_current_time_left(self, time_left):
        """Set the time left for the current project"""
        if self.projects and self.current_project_index < len(self.projects):
            project_name = self.projects[self.current_project_index]
            self.project_times[project_name] = time_left

    def is_current_project_paused(self):
        """Check if the current project is paused"""
        if not self.projects or self.current_project_index >= len(self.projects):
            return False

        project_name = self.projects[self.current_project_index]
        return self.project_paused.get(project_name, False)

    def set_current_project_paused(self, paused):
        """Set the pause state for the current project"""
        if self.projects and self.current_project_index < len(self.projects):
            project_name = self.projects[self.current_project_index]
            self.project_paused[project_name] = paused

    def load_projects(self):
        """Load projects from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.projects = data.get('projects', [])
                    self.current_project_index = data.get('current_index', 0)
                    self.default_duration = data.get('default_duration', 3600)
                    self.project_times = data.get('project_times', {})
                    self.project_paused = data.get('project_paused', {})

        except Exception as e:
            print(f"Error loading projects: {e}")

        # Default projects if none loaded
        if self.projects is None:
            self.projects = ['Develop new feature', 'Review research papers', 'Team meeting prep']
            self.current_project_index = 0
            # Initialize project times and pause states
            for project in self.projects:
                if project not in self.project_times:
                    self.project_times[project] = self.default_duration
                if project not in self.project_paused:
                    self.project_paused[project] = False

    def save_projects(self):
        """Save projects to JSON file"""
        try:
            data = {
                'projects': self.projects,
                'current_index': self.current_project_index,
                'default_duration': self.default_duration,
                'project_times': self.project_times,
                'project_paused': self.project_paused
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving projects: {e}")

    def format_time(self, seconds):
        """Format seconds into HH:MM:SS"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def render_projects(self):
        """Update the project listbox"""
        # Remember the current selection
        current_selection = self.project_listbox.curselection()
        selected_index = current_selection[0] if current_selection else None

        self.project_listbox.delete(0, tk.END)
        for i, project in enumerate(self.projects):
            time_left = self.project_times.get(project, self.default_duration)
            is_paused = self.project_paused.get(project, False)
            is_current = i == self.current_project_index

            status = ""
            if is_current:
                status += "► "
            else:
                status += "   "

            if is_paused:
                status += "[PAUSED] "

            time_str = self.format_time(time_left)
            display_text = f"{status}{project} ({time_str})"

            self.project_listbox.insert(tk.END, display_text)

        # Restore the previous selection, or select current project if nothing was selected
        if selected_index is not None and 0 <= selected_index < len(self.projects):
            self.project_listbox.selection_set(selected_index)
        elif 0 <= self.current_project_index < len(self.projects):
            self.project_listbox.selection_set(self.current_project_index)

    def add_project(self):
        """Add a new project"""
        project_name = self.project_entry.get().strip()
        if project_name:
            self.projects.append(project_name)
            self.project_times[project_name] = self.default_duration
            self.project_paused[project_name] = False
            self.project_entry.delete(0, tk.END)
            self.save_projects()
            self.render_projects()
            self.show_status(f"Added project: {project_name}")

            # If this is the first project, start the timer
            if len(self.projects) == 1:
                self.current_project_index = 0
                self.update_current_activity()

    def delete_project(self):
        """Delete the selected project"""
        selection = self.project_listbox.curselection()
        if selection:
            actual_index = selection[0]

            if 0 <= actual_index < len(self.projects):
                deleted_project = self.projects[actual_index]

                # Save undo information before deleting
                self.push_undo('delete', {
                    'index': actual_index,
                    'name': deleted_project,
                    'time': self.project_times.get(deleted_project, self.default_duration),
                    'paused': self.project_paused.get(deleted_project, False)
                })

                # Now perform the delete
                self.projects.pop(actual_index)

                # Clean up associated data
                if deleted_project in self.project_times:
                    del self.project_times[deleted_project]
                if deleted_project in self.project_paused:
                    del self.project_paused[deleted_project]

                # Adjust current project index
                if actual_index == self.current_project_index:
                    if self.current_project_index >= len(self.projects):
                        self.current_project_index = max(0, len(self.projects) - 1)
                elif actual_index < self.current_project_index:
                    self.current_project_index -= 1

                self.save_projects()
                self.render_projects()
                self.update_current_activity()

                self.show_status(f"Deleted project: {deleted_project}", color=self.colors['danger'])

    def rename_project(self):
        """Rename the selected project"""
        selection = self.project_listbox.curselection()
        if selection:
            index = selection[0]

            if 0 <= index < len(self.projects):
                old_name = self.projects[index]

                # Create a simple dialog window for renaming
                dialog = tk.Toplevel(self.root)
                dialog.title("Rename Project")
                dialog.geometry("350x110")
                dialog.configure(bg='#f4f7f6')
                dialog.transient(self.root)
                dialog.grab_set()

                # Center the dialog
                dialog.update_idletasks()
                x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
                y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
                dialog.geometry(f"+{x}+{y}")

                # Dialog content
                frame = tk.Frame(dialog, bg='#f4f7f6', padx=16, pady=12)
                frame.pack(fill=tk.BOTH, expand=True)

                tk.Label(
                    frame,
                    text="New project name:",
                    bg='#f4f7f6',
                    font=('Arial', 10)
                ).pack(anchor=tk.W, pady=(0, 6))

                entry = tk.Entry(frame, font=('Arial', 10), width=35)
                entry.pack(fill=tk.X, pady=(0, 10))
                entry.insert(0, old_name)
                entry.select_range(0, tk.END)
                entry.focus_set()

                def save_rename():
                    new_name = entry.get().strip()
                    if new_name and new_name != old_name:
                        # Save undo information before renaming
                        self.push_undo('rename', {
                            'index': index,
                            'old_name': old_name,
                            'new_name': new_name
                        })

                        # Update project name
                        self.projects[index] = new_name

                        # Update project times and paused state
                        if old_name in self.project_times:
                            self.project_times[new_name] = self.project_times.pop(old_name)
                        if old_name in self.project_paused:
                            self.project_paused[new_name] = self.project_paused.pop(old_name)

                        self.save_projects()
                        self.render_projects()
                        self.update_current_activity()
                        dialog.destroy()
                        self.show_status(f"Renamed to: {new_name}", color=self.colors['secondary'])
                    elif not new_name:
                        messagebox.showwarning("Invalid Name", "Project name cannot be empty!")
                    else:
                        dialog.destroy()

                def cancel_rename():
                    dialog.destroy()

                # Buttons
                btn_frame = tk.Frame(frame, bg='#f4f7f6')
                btn_frame.pack(fill=tk.X)

                tk.Button(
                    btn_frame,
                    text="Save",
                    font=('Arial', 9),
                    bg='#3498db',
                    fg='white',
                    padx=16,
                    pady=3,
                    command=save_rename
                ).pack(side=tk.LEFT, padx=(0, 4))

                tk.Button(
                    btn_frame,
                    text="Cancel",
                    font=('Arial', 9),
                    bg='#95a5a6',
                    fg='white',
                    padx=16,
                    pady=3,
                    command=cancel_rename
                ).pack(side=tk.LEFT)

                # Bind Enter and Escape keys
                entry.bind('<Return>', lambda e: save_rename())
                dialog.bind('<Escape>', lambda e: cancel_rename())

    def reset_current_project(self):
        """Reset the current project's timer"""
        if self.projects and 0 <= self.current_project_index < len(self.projects):
            project_name = self.projects[self.current_project_index]
            self.project_times[project_name] = self.default_duration
            self.project_paused[project_name] = False
            self.save_projects()
            self.render_projects()
            self.update_display()

    def reset_selected_project(self):
        """Reset the selected project's timer"""
        selection = self.project_listbox.curselection()
        if selection:
            index = selection[0]
            if 0 <= index < len(self.projects):
                project_name = self.projects[index]
                self.project_times[project_name] = self.default_duration
                self.project_paused[project_name] = False
                self.save_projects()
                self.render_projects()
                if index == self.current_project_index:
                    self.update_display()

    def toggle_current_project(self):
        """Toggle pause/resume for current project"""
        if self.projects and 0 <= self.current_project_index < len(self.projects):
            project_name = self.projects[self.current_project_index]
            current_state = self.project_paused.get(project_name, False)
            self.project_paused[project_name] = not current_state
            self.save_projects()
            self.render_projects()

    def toggle_selected_project(self):
        """Toggle pause/resume for selected project"""
        selection = self.project_listbox.curselection()
        if selection:
            index = selection[0]
            if 0 <= index < len(self.projects):
                project_name = self.projects[index]
                current_state = self.project_paused.get(project_name, False)
                self.project_paused[project_name] = not current_state
                self.save_projects()
                self.render_projects()

    def update_timer_display(self):
        """Update the timer display and status"""
        time_left = self.get_current_time_left()
        self.timer_label.config(text=self.format_time(time_left))

        # Update status
        if self.projects:
            if self.is_current_project_paused():
                self.status_label.config(text="⏸ PAUSED", fg=self.colors['warning'])
            else:
                self.status_label.config(text="▶ RUNNING", fg=self.colors['success'])
        else:
            self.status_label.config(text="No projects", fg=self.colors['text_dim'])

        # Flash when time is up
        if time_left <= 0 and not self.is_current_project_paused():
            current_color = self.timer_label.cget('fg')
            new_color = self.colors['danger'] if current_color == self.colors['primary'] else self.colors['primary']
            self.timer_label.config(fg=new_color)
        else:
            self.timer_label.config(fg=self.colors['primary'])

    def update_current_activity(self):
        """Update the current activity display"""
        if self.projects and 0 <= self.current_project_index < len(self.projects):
            self.activity_label.config(text=self.projects[self.current_project_index])
        else:
            self.activity_label.config(text="No Projects")

    def update_display(self):
        """Update all display elements"""
        self.update_timer_display()
        self.update_current_activity()
        self.render_projects()

    def timer_tick(self):
        """Main timer tick function using tkinter's after method"""
        if self.projects and 0 <= self.current_project_index < len(self.projects):
            if not self.is_current_project_paused():
                current_time = self.get_current_time_left()
                if current_time > 0:
                    self.set_current_time_left(current_time - 1)
                    self.save_projects()
                else:
                    # Timer ended
                    self.timer_ended()
                    return

            self.update_display()

        # Schedule next tick
        self.after_id = self.root.after(1000, self.timer_tick)

    def timer_ended(self):
        """Handle timer end"""
        current_project = self.projects[self.current_project_index] if self.projects else "Current project"

        # Play alarm sound
        try:
            # winsound.PlaySound(r'C:\Windows\Media\')
            winsound.PlaySound('C:/Windows/Media/Alarm04.wav',
                               winsound.SND_FILENAME | winsound.SND_ASYNC)  # , winsound.SND_ALIAS)
            # winsound.Beep(1000, 1000)  # 1000 Hz for 1 second
        except:
            print("Alarm! Timer ended!")  # Fallback for non-Windows

        # Show notification
        result = messagebox.askquestion(
            "Timer Ended!",
            f"Time's up for: {current_project}\n\nMove to next project?",
            icon='question'
        )

        if result == 'yes':
            # Reset the current project before moving to next
            self.reset_current_project()
            self.next_project()
            # Automatically resume the timer for the new project
            self.resume_timer_after_switch()
        else:
            # Reset current project and resume
            self.reset_current_project()
            self.resume_timer_after_switch()

    def resume_timer_after_switch(self):
        """Resume the timer after switching projects or resetting"""
        # Ensure the new current project is not paused
        if self.projects and 0 <= self.current_project_index < len(self.projects):
            project_name = self.projects[self.current_project_index]
            self.project_paused[project_name] = False
            self.save_projects()
            self.update_display()

        # Continue the timer tick
        self.timer_tick()

    def start_timer(self):
        """Start the main timer loop"""
        if not self.timer_running:
            self.timer_running = True
            self.update_current_activity()
            self.timer_tick()

    def stop_timer(self):
        """Stop the timer"""
        self.timer_running = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def next_project(self):
        """Move to the next project"""
        if self.projects:
            self.current_project_index = (self.current_project_index + 1) % len(self.projects)
            self.save_projects()
            self.update_display()

    def import_projects(self):
        """Import projects from a text file"""
        file_path = filedialog.askopenfilename(
            title="Import Projects",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                imported_projects = [line.strip() for line in content.split('\n') if line.strip()]

                if imported_projects:
                    self.projects = imported_projects
                    self.current_project_index = 0

                    # Initialize times and pause states for new projects
                    self.project_times = {}
                    self.project_paused = {}
                    for project in self.projects:
                        self.project_times[project] = self.default_duration
                        self.project_paused[project] = False

                    self.save_projects()
                    self.update_display()
                    messagebox.showinfo("Success", f"Imported {len(imported_projects)} projects!")
                else:
                    messagebox.showwarning("Warning", "No valid projects found in file!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to import file: {str(e)}")

    def export_projects(self):
        """Export projects to a text file"""
        if not self.projects:
            messagebox.showwarning("Warning", "No projects to export!")
            return

        file_path = filedialog.asksaveasfilename(
            title="Export Projects",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(self.projects))

                messagebox.showinfo("Success", f"Exported {len(self.projects)} projects to {file_path}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to export file: {str(e)}")

    def on_closing(self):
        """Handle application closing"""
        self.stop_timer()
        self.save_projects()
        self.root.destroy()


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = TimaApp(root)
    root.mainloop()


if __name__ == "__main__":
    import winsound

    # Play Windows exit sound.

    main()
