import signal
import sys

from PyQt6.QtWidgets import QSplashScreen, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QColor

from marvel_schedule_maker.services.ApplicationServices import ApplicationServices
from marvel_schedule_maker.views.MainWindow import MainWindow


def main():
    # Without this ctrl+c doesn't work in cmd when running the app
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    app.setDesktopFileName("Marvel Schedule Maker")

    palette = QPalette()

    palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)

    palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
    
    palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
    
    palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    
    palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.black)
    
    palette.setColor(QPalette.ColorRole.PlaceholderText, Qt.GlobalColor.darkGray)

    app.setPalette(palette)

    # Show splash PNG
    splash_pix = QPixmap(":/assets/splash.png")
    splash = QSplashScreen(splash_pix, Qt.WindowType.WindowStaysOnTopHint)
    splash.showMessage(
        "Loading…",
        Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
        Qt.GlobalColor.white
    )
    splash.show()
    app.processEvents()

    services = ApplicationServices()
    window = MainWindow(services)
    window.show()
    splash.finish(window)

    sys.exit(app.exec())
