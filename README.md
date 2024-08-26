# 20-20-20 Reminder

Quike look:

This is a simple application to remind you to take a 20-second break every 20 minutes and look at something 20 feet away.

## Requirements

To run this application, you need to install the following Python libraries:

- `ttkbootstrap`
- `pystray`
- `Pillow`

## Installation

You can install the required libraries using the following command:

```bash
pip install ttkbootstrap pystray pillow


Full detail:

## Overview

The **20-20-20 Reminder** application is designed to help users take regular breaks to reduce eye strain. It reminds users to take a 20-second break every 20 minutes and look at something 20 feet away. The application features a modern and user-friendly interface using `ttkbootstrap`, system tray integration with `pystray`, and visual and audio reminders.

## Features

- **Customizable Timer**: Set to remind every 20 minutes.
- **Visual Countdown**: Displays remaining time using a meter.
- **System Tray Integration**: Minimize to system tray and restore easily.
- **Audio Alerts**: Plays a sound when the timer reaches zero.
- **User-Friendly Interface**: Modern design with `ttkbootstrap`.

## Installation

### Prerequisites

Ensure you have Python installed. You also need to install the following libraries:

```bash
pip install ttkbootstrap pystray pillow
```

### Running the Application

1. Clone the repository or download the source code.
2. Navigate to the directory containing the source code.
3. Run the application using the following command:

```bash
python reminder20.py
```

## Code Explanation

### Imports

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pystray
from pystray import MenuItem as Item
from PIL import Image, ImageTk
import winsound
import time
```

### TimerApp Class

#### Initialization

```python
class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("20-20-20 Reminder")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
```

- **root**: Main application window.
- **title**: Sets the window title.
- **geometry**: Sets the window size.
- **resizable**: Disables window resizing.

#### Custom Icon

```python
self.icon = Image.open("icon2.png")
self.tk_icon = ImageTk.PhotoImage(self.icon)
self.root.iconphoto(False, self.tk_icon)
```

- **icon**: Loads a custom icon for the application.
- **iconphoto**: Sets the window icon.

#### Timer Setup

```python
self.total_time = 20 * 60  # 20 minutes in seconds
self.remaining_time = self.total_time
self.running = False
```

- **total_time**: Total countdown time in seconds.
- **remaining_time**: Time remaining in the countdown.
- **running**: Timer state.

#### Meter Widget

```python
self.meter = ttk.Meter(root,
                       metersize=250,
                       amounttotal=self.total_time,
                       amountused=self.remaining_time,
                       bootstyle=SUCCESS,
                       showtext=False,
                       subtext=self.format_time(self.remaining_time),
                       subtextstyle=DARK,
                       subtextfont=("Helvetica", 48)
                       )
self.meter.pack(pady=25)
```

- **Meter**: Displays the remaining time visually.

#### Buttons

```python
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

self.start_button = ttk.Button(button_frame, text="Start", command=self.start_timer, bootstyle=SUCCESS)
self.start_button.pack(side=ttk.LEFT, padx=5)

self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_timer, bootstyle=WARNING)
self.reset_button.pack(side=ttk.LEFT, padx=5)

self.minimize_button = ttk.Button(button_frame, text="Hide", command=self.minimize_window, bootstyle=INFO)
self.minimize_button.pack(side=ttk.LEFT, padx=5)

self.quit_button = ttk.Button(button_frame, text="Quit", command=self.quit_app, bootstyle=DANGER)
self.quit_button.pack(side=ttk.LEFT, padx=5)
```

- **Buttons**: Start, reset, minimize, and quit buttons with respective commands.

#### System Tray Setup

```python
self.setup_tray()
self.update_timer()
self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
```

- **setup_tray**: Initializes system tray icon.
- **update_timer**: Starts the timer update loop.
- **protocol**: Overrides the window close event.

### Methods

#### Timer Control

```python
def start_timer(self):
    self.running = True
    self.start_time = time.time()
    self.update_timer()

def reset_timer(self):
    self.remaining_time = self.total_time
    self.running = False
    self.meter.configure(amountused=self.remaining_time, subtext=self.format_time(self.remaining_time))

def update_timer(self):
    if self.running:
        elapsed_time = time.time() - self.start_time
        self.remaining_time = max(0, self.total_time - int(elapsed_time))
        self.meter.configure(amountused=self.remaining_time, subtext=self.format_time(self.remaining_time))
        if self.remaining_time == 0:
            self.running = False
            self.show_reminder()
    self.root.after(1000, self.update_timer)
```

- **start_timer**: Starts the countdown.
- **reset_timer**: Resets the timer.
- **update_timer**: Updates the timer every second.

#### Window Management

```python
def minimize_window(self):
    self.root.withdraw()
    self.tray_icon.visible = True

def quit_app(self, icon=None, item=None):
    if self.tray_icon:
        self.tray_icon.stop()
    if self.reminder_window:
        self.reminder_window.destroy()
    self.root.quit()

def on_closing(self):
    self.minimize_window()
```

- **minimize_window**: Minimizes the window to the system tray.
- **quit_app**: Quits the application.
- **on_closing**: Handles window close event.

#### Reminder

```python
def play_sound(self):
    winsound.PlaySound("level-up-191997.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

def show_reminder(self):
    if self.reminder_window is not None and self.reminder_window.winfo_exists():
        self.reminder_window.destroy()
    self.reminder_window = ttk.Toplevel()
    self.reminder_window.title("Reminder")

    message_icon = ImageTk.PhotoImage(self.icon)
    self.reminder_window.iconphoto(False, message_icon)

    frame = ttk.Frame(self.reminder_window, padding=20, bootstyle="primary")
    frame.pack(fill="both", expand=True)

    message_icon = ImageTk.PhotoImage(self.icon)
    icon_label = ttk.Label(frame, image=message_icon)
    icon_label.image = message_icon
    icon_label.pack(side="left", padx=10)

    label = ttk.Label(frame, text="Time's up!\nTake a 20-second break\nand look at something 20 feet away!",
                      font=("Helvetica", 14), bootstyle="inverse-primary")
    label.pack(side="left", padx=10)

    style = ttk.Style()
    style.configure('Large.Danger.TButton', font=('Helvetica', 14), padding=10)

    close_button = ttk.Button(frame, text="Close", command=self.reminder_window.destroy, bootstyle="danger", style='Large.Danger.TButton')
    close_button.pack(side="bottom", pady=10)

    self.play_sound()

    self.reminder_window.update_idletasks()
    window_width = self.reminder_window.winfo_width()
    window_height = self.reminder_window.winfo_height()
    screen_width = self.reminder_window.winfo_screenwidth()
    screen_height = self.reminder_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    self.reminder_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
```

- **play_sound**: Plays a sound when the timer ends.
- **show_reminder**: Displays a reminder window with a message and close button.

#### System Tray

```python
def setup_tray(self):
    self.tray_icon = pystray.Icon("20-20-20 Reminder")
    self.tray_icon.icon = self.icon
    self.tray_icon.menu = pystray.Menu(
        Item('Restore', self.restore_window),
        Item('Quit', self.quit_app)
    )
    self.tray_icon.run_detached()

def restore_window(self, icon=None, item=None):
    self.root.after(0, self._restore_window)

def _restore_window(self):
    self.root.deiconify()
```

- **setup_tray**: Sets up the system tray icon and menu.
- **restore_window**: Restores the main window from the system tray.

### Main Execution

```python
if __name__ == "__main__":
    root = ttk.Window(themename="litera")
    app = TimerApp(root)
    root.mainloop()
```

- **Main Execution**: Initializes the application with a specified theme and starts the main event loop.
