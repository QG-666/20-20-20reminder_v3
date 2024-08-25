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
        self.root.geometry("600x750")

        # 禁用最大化按钮
        self.root.resizable(False, False)

        # 设置主界面的自定义图标
        self.icon = Image.open("icon2.png")
        self.tk_icon = ImageTk.PhotoImage(self.icon)
        self.root.iconphoto(False, self.tk_icon)

        self.remaining_time = 1 * 60  # 20 minutes in seconds
        self.running = False

        self.label = ttk.Label(root, text=self.format_time(self.remaining_time), font=("Helvetica", 48))
        self.label.pack(pady=10)

        self.meter = ttk.Meter(root,
                               metersize=250,
                               amounttotal=1 * 60,
                               amountused=self.remaining_time,
                               bootstyle=SUCCESS,
                               showtext=False,
                               subtext=self.format_time(self.remaining_time),
                               subtextstyle=SUCCESS,
                               subtextfont=("Helvetica", 48)

                               )
        self.meter.pack(pady=15)

        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)

        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_timer, bootstyle=SUCCESS)
        self.start_button.pack(side=ttk.LEFT, padx=5)

        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_timer, bootstyle=WARNING)
        self.reset_button.pack(side=ttk.LEFT, padx=5)

        self.minimize_button = ttk.Button(button_frame, text="Minimize", command=self.minimize_window, bootstyle=INFO)
        self.minimize_button.pack(side=ttk.LEFT, padx=5)

        self.quit_button = ttk.Button(button_frame, text="Quit", command=self.quit_app, bootstyle=DANGER)
        self.quit_button.pack(side=ttk.LEFT, padx=5)

        self.reminder_window = None
        self.setup_tray()
        self.update_timer()

        # 重载窗口关闭事件
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
        self.remaining_time = 1 * 60  # Reset to 20 minutes
        self.running = False
        self.label.config(text=self.format_time(self.remaining_time))
        self.meter.configure(amountused=self.remaining_time,subtext=self.format_time(self.remaining_time))

    def update_timer(self):
        if self.running:
            elapsed_time = time.time() - self.start_time
            self.remaining_time = max(0, 1 * 60 - int(elapsed_time))
            self.label.config(text=self.format_time(self.remaining_time))
            self.meter.configure(amountused=self.remaining_time,subtext=self.format_time(self.remaining_time))
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

        # 更新窗口以获取其宽度和高度
        self.reminder_window.update_idletasks()
        window_width = self.reminder_window.winfo_width()
        window_height = self.reminder_window.winfo_height()

        # 获取屏幕宽度和高度
        screen_width = self.reminder_window.winfo_screenwidth()
        screen_height = self.reminder_window.winfo_screenheight()

        # 计算窗口的x和y坐标
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # 设置窗口位置
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
    root = ttk.Window(themename="litera")  # 选择一个主题
    app = TimerApp(root)
    root.mainloop()
