# Tima
*Pronounced like "timer" - because that's what it is*

> **A sleek desktop productivity timer that keeps you focused on what matters**

Tima is a modern, minimalist activity timer designed to help you cycle through multiple projects with customizable time allocations. Perfect for time-boxed work sessions, research rotations, or managing multiple concurrent projects.

## Features

### Core Functionality
- **Multi-Project Management** - Track multiple projects simultaneously with individual timers
- **Customizable Durations** - Set default time allocations or customize per-project
- **Pause & Resume** - Flexible control over individual project timers
- **Auto-Cycling** - Automatic notifications and project switching when time expires
- **Persistent State** - All projects and timer states are saved automatically

### User Experience
- **Modern Dark UI** - Easy on the eyes with a sleek, contemporary design
- **Keyboard Shortcuts** - Full keyboard navigation for power users
- **Visual Indicators** - Clear status indicators for current, paused, and running projects
- **Undo Support** - Restore accidentally deleted or renamed projects
- **Import/Export** - Easily share project lists via text files

### Project Controls
- Add, rename, and delete projects on the fly
- Individual pause/resume for each project
- Reset timers to default duration
- Navigate between projects with arrow keys
- Clear visual feedback for all actions

## Installation

### Quick Install

**No system dependencies required!** Just install and run:

```bash
# Using uv (recommended)
uv pip install tima-timer

# Or using pip
pip install tima-timer
```

Tima uses Flet (Flutter for Python), so everything you need is included - no tkinter, no Qt, no external dependencies!

### Running

After installation, simply run:
```bash
tima
```

The modern Flet UI will launch automatically!

## Usage

### Getting Started

1. **Launch Tima** - Run `python tima.py`
2. **Add Projects** - Type project names in the input field and click ADD (or press Enter)
3. **Start Working** - The timer automatically starts with your first project
4. **Stay Focused** - Watch the countdown and receive alerts when time expires

### Managing Projects

#### Adding Projects
- Type the project name in the input field
- Press `Enter` or click the **ADD** button
- New projects start with the default duration (1 hour)

#### Renaming Projects
- Select a project in the list
- Press `F2`, `Enter`, or double-click
- Type the new name and press `Enter` to save

#### Deleting Projects
- Select a project in the list
- Press `Delete`
- Use `Ctrl+Z` to undo if needed

#### Pausing/Resuming
- Press `Space` to pause/resume the current project
- Or use the Timer menu for more options

### Keyboard Shortcuts

#### Global Controls
| Key | Action |
|-----|--------|
| `Space` | Pause/Resume current project |
| `↑` / `Page Up` | Previous project |
| `↓` / `Page Down` | Next project |
| `Delete` | Delete selected project |
| `Ctrl+Z` | Undo last delete/rename |
| `?` | Show keyboard shortcuts help |

#### Project List
| Key | Action |
|-----|--------|
| `Enter` | Rename selected project |
| `F2` | Rename selected project |
| `Double-click` | Rename selected project |

#### Text Entry
| Key | Action |
|-----|--------|
| `Enter` | Add project (when focused on input field) |

### Menu Bar Options

#### File Menu
- **Import Projects** - Load project list from a text file
- **Export Projects** - Save project list to a text file
- **Exit** - Close the application

#### Project Menu
- **Rename Selected** - Rename the selected project
- **Delete Selected** - Remove the selected project
- **Reset Selected** - Reset selected project timer to default
- **Pause/Resume Selected** - Toggle pause state for selected project

#### Timer Menu
- **Pause/Resume Current** - Toggle current project timer
- **Reset Current** - Reset current project to default duration
- **Next Project** - Move to next project in the list
- **Previous Project** - Move to previous project

#### Settings Menu
- **Set Default Duration** - Configure default time allocation for new projects

#### Help Menu
- **Keyboard Shortcuts** - Display all available keyboard shortcuts

## Configuration

### Default Duration
- Navigate to `Settings` → `Set Default Duration`
- Enter hours and minutes
- New projects will use this duration
- Existing projects keep their current settings

### Data Persistence
All data is automatically saved to `tima_projects.json` including:
- Project names and order
- Individual project timer states
- Pause states
- Current project index
- Default duration setting

### Color Scheme
The application uses a modern dark theme with carefully chosen colors:
- Dark background for reduced eye strain
- Purple primary accent for active elements
- Color-coded status indicators (green for running, orange for paused, red for ended)

## Technical Details

### Architecture
- Built with **Flet** (Flutter for Python) for modern, cross-platform UI
- **Modular design**: Separated UI, business logic, and data layers
- JSON-based data persistence
- Async timer system using Python's asyncio
- Undo stack implementation for reversible operations
- Material Design components

### File Structure
```
tima/
├── src/tima_timer/
│   ├── app_flet.py             # Flet UI implementation
│   ├── models.py               # Data models and state
│   ├── timer_logic.py          # Business logic
│   └── __init__.py             # Package entry point
├── ~/.tima/
│   └── tima_projects.json      # User project data (auto-saved)
├── MIGRATION.md                # Migration documentation
└── README.md                   # This file
```

### Platform Support
- ✅ **Windows**: Full support with native sound notifications
- ✅ **macOS**: Full support
- ✅ **Linux**: Full support (no system dependencies!)
- 🌐 **Web**: Can run as web app
- 📱 **Mobile**: iOS/Android support possible (future)

## Tips & Tricks

1. **Focus Mode** - Pause all non-essential projects to focus on one task
2. **Daily Rotation** - Set up recurring daily projects and cycle through them
3. **Research Sessions** - Perfect for managing multiple research papers or study topics
4. **Sprint Planning** - Use for time-boxed development sprints across features
5. **Meeting Prep** - Allocate time for preparing multiple meeting topics

## Customization

Want to change the default settings? Edit these values in `src/tima_timer/app_flet.py`:

```python
# Color scheme (lines 17-28)
COLORS = {
    'bg': '#1e1e2e',           # Dark background
    'primary': '#6c63ff',       # Primary accent color
    # ... customize other colors
}

# Default duration is stored in user data and can be changed via Settings menu
```

## Troubleshooting

### Timer not ticking?
- Ensure you have projects added
- Check if the current project is paused (look for [PAUSED] indicator)

### Sound notifications not working?
- Windows: Ensure `C:/Windows/Media/Alarm04.wav` exists
- macOS/Linux: Console notification will appear (audio support coming soon)

### Projects not saving?
- Check write permissions in the application directory
- Verify `tima_projects.json` is not corrupted

## License

This project is open source. Feel free to use, modify, and distribute as needed.

## Contributing

Contributions are welcome! Some ideas for enhancements:
- Cross-platform sound notifications (beyond Windows)
- Statistics and time tracking reports
- Project categories and tags
- System tray integration
- Light theme option
- Custom alert sounds per project
- Web version deployment
- Mobile apps (iOS/Android)

---

**Stay focused. Stay productive. Use Tima.**
