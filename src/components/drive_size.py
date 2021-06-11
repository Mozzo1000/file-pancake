from PyQt5.QtWidgets import QLabel
from threading import Timer
import shutil

class DriveSize(QLabel):
    def __init__(self, path):
        super().__init__()
        self.path = path
        
        self.get_harddrive_space()

    # Note: generally it would be better for the thread to be started globally and not
    # on a per class basis. This class will possibly be invoked multiple times in a single
    # application. Not a huge problem but would save some processing power if it ran globally.
    def get_harddrive_space(self, interval=300):
        """Start thread to get harddrive usage and set text.

        Args:
            interval (int, optional): How often this function will run (in seconds). Defaults to 300.
        """
        thread = Timer(interval, self.get_harddrive_space, [interval])
        thread.daemon = True
        thread.start()
        total, used, free = shutil.disk_usage(self.path)
        self.setText(f"Free: {(free // (2**30))} GiB of {(total // (2**30))} GiB")

    def update_path(self, new_path):
        self.path = new_path