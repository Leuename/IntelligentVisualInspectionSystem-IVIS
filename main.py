import sys
import os
from appdirs import user_data_dir

config_dir = user_data_dir("IVIS", "Fastech")
os.makedirs(config_dir, exist_ok=True)
os.environ["YOLO_CONFIG_DIR"] = config_dir

from PySide6.QtWidgets import QApplication
from backend import SplashScreen 

app = QApplication(sys.argv)
window = SplashScreen()
window.show()
sys.exit(app.exec())