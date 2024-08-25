import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pystray
from pystray import MenuItem as Item
from PIL import Image, ImageTk
import winsound
import time

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("20-20-20 Reminder")
        self.root.geometry("600x600")

        # Disable window resizing
        self.root.resizable(False, False)

        # Set custom icon for the main window
        self.icon = Image.open("icon2.png")
        self.tk_icon = ImageTk.PhotoImage(self.icon)
        self.root.iconphoto(False, self.tk_icon)

        self.total_time = 1 * 60  # 20 minutes in seconds
        self.remaining_time = self.total_time
        self.running = False

        # Create a meter to display remaining time
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

        # Create a frame for buttons
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)

        # Start button
        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_timer, bootstyle=SUCCESS)
        self.start_button.pack(side=ttk.LEFT, padx=5)

        # Reset button
        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_timer, bootstyle=WARNING)
        self.reset_button.pack(side=ttk.LEFT, padx=5)

        # Minimize button
        self.minimize_button = ttk.Button(button_frame, text="Hide", command=self.minimize_window, bootstyle=INFO)
        self.minimize_button.pack(side=ttk.LEFT, padx=5)

        # Quit button
        self.quit_button = ttk.Button(button_frame, text="Quit", command=self.quit_app, bootstyle=DANGER)
        self.quit_button.pack(side=ttk.LEFT, padx=5)

        self.reminder_window = None
        self.setup_tray()
        self.update_timer()

        # Override window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.minimize_window()

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes):02}:{int(seconds):02}"

    def start_timer(self):
        self.running = True
        self.start_time = time.time()
        self.update_timer()

    def reset_timer(self):
        self.remaining_time = self.total_time  # Reset to 20 minutes
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

    def minimize_window(self):
        self.root.withdraw()
        self.tray_icon.visible = True

    def quit_app(self, icon=None, item=None):
        if self.tray_icon:
            self.tray_icon.stop()
        if self.reminder_window:
            self.reminder_window.destroy()
        self.root.quit()

    def play_sound(self):
        winsound.PlaySound("level-up-191997.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

    def show_reminder(self):
        if self.reminder_window is not None and self.reminder_window.winfo_exists():
            self.reminder_window.destroy()
        self.reminder_window = ttk.Toplevel()
        self.reminder_window.title("Reminder")

        message_icon = ImageTk.PhotoImage(self.icon)
        self.reminder_window.iconphoto(False, message_icon)

        label = ttk.Label(self.reminder_window, text="Take a 20-second break and look at something 20 feet away!")
        label.pack(pady=20, padx=20)

        self.play_sound()

        # Update window to get its width and height
        self.reminder_window.update_idletasks()
        window_width = self.reminder_window.winfo_width()
        window_height = self.reminder_window.winfo_height()

        # Get screen width and height
        screen_width = self.reminder_window.winfo_screenwidth()
        screen_height = self.reminder_window.winfo_screenheight()

        # Calculate x and y coordinates to center the window
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set window position
        self.reminder_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

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

if __name__ == "__main__":
    root = ttk.Window(themename="litera")  # Choose a theme
    app = TimerApp(root)
    root.mainloop()
