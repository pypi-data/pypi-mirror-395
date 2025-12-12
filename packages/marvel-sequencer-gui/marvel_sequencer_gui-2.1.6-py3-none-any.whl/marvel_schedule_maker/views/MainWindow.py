from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QResizeEvent

from marvel_schedule_maker.__version__ import __version__
from marvel_schedule_maker.models.NotificationTypes import NotificationType
from marvel_schedule_maker.services.ApplicationServices import ApplicationServices

from marvel_schedule_maker.viewmodels.MainWindowViewModel import MainWindowViewModel

from marvel_schedule_maker.views.ActionPanelView import ActionPanelView
from marvel_schedule_maker.views.CelestialObjectModal import CelestialObjectModal
from marvel_schedule_maker.views.NotificationPopup import NotificationPopup
from marvel_schedule_maker.views.TimelinePanelView import TimelinePanelView
from marvel_schedule_maker.views.TopBarView import TopBarView
from marvel_schedule_maker.views.UserManualDialog import UserManualDialog


class MainWindow(QMainWindow):
    def __init__(self, services: ApplicationServices):
        super().__init__()

        self.setWindowTitle(f"Marvel Schedule Maker v{__version__}")
        
        self.toast = NotificationPopup(self)

        self._services = services
        self._viewmodel = MainWindowViewModel(self._services)

        self._services.signals.notification_requested.connect(self._show_notification)
        
        # Central widget in vertical layout
        central_widget = QWidget()
        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Create views with ViewModels from parent ViewModel
        topBarView = TopBarView(self._services)
        topBarView.celestial_object_modal_requested.connect(self._viewmodel.open_celestial_object_modal)
        topBarView.user_manual_requested.connect(self._open_user_manual)
        
        actionPanelView = ActionPanelView(self._services)
        
        timelinePanelView = TimelinePanelView(self._services)

        root_layout.addWidget(actionPanelView)
        actionPanelView.setMinimumWidth(450)
        root_layout.addLayout(content_layout, stretch=1)

        content_layout.addWidget(topBarView)
        content_layout.addWidget(timelinePanelView, stretch=1)
        
        self.setCentralWidget(central_widget)

        self._celestial_object_modal = CelestialObjectModal(central_widget)
        self._celestial_object_modal.closed.connect(self._viewmodel.close_celestial_object_modal)

        self._viewmodel.celestial_object_modal_visible_changed.connect(self._on_celestial_object_modal_visibility_changed)
        
        self.showMaximized()

    def _show_notification(self, message: str, type: NotificationType):
        self.toast.show_message(message, type)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        super().resizeEvent(a0)

    def _on_celestial_object_modal_visibility_changed(self, visible: bool):
        """Handle settings modal visibility changes from viewmodel."""
        if visible:
            self._celestial_object_modal.show_modal()

    def _open_user_manual(self):
        """Open the user manual dialog."""
        dialog = UserManualDialog(self)
        dialog.exec()
