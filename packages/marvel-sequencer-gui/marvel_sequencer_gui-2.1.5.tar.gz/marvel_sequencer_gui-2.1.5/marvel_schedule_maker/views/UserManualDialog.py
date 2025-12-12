from datetime import datetime
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTreeWidget, QTreeWidgetItem, QSplitter, QWidget, QLabel, QScrollArea)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

import qtawesome as qta

from marvel_schedule_maker.views.CalendarPopupDialog import CalendarPopupDialog
from marvel_schedule_maker.views.ClickableLabel import ClickableLabel


class UserManualDialog(QDialog):
    """User manual dialog with navigation and content display."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User Manual - Marvel Schedule Maker")
        self.setMinimumSize(1000, 900)

        # Main layout
        main_layout = QVBoxLayout()

        # Splitter for navigation and content
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Navigation tree
        self.nav_tree = QTreeWidget()
        self.nav_tree.setHeaderHidden(True)
        self.nav_tree.setMaximumWidth(300)
        self.nav_tree.itemClicked.connect(self._on_item_clicked)

        # Add spacing between items
        self.nav_tree.setStyleSheet("""
            QTreeWidget::item {
                padding: 8px;
                margin: 2px 0px;
            }
            QTreeWidget::item:hover {
                background-color: #e8e8e8;
            }
            QTreeWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }
        """)

        # Content container with scroll area
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll_area = QScrollArea()
        scroll_area.setWidget(self.content_container)
        scroll_area.setWidgetResizable(True)

        # Add widgets to splitter
        splitter.addWidget(self.nav_tree)
        splitter.addWidget(scroll_area)
        splitter.setStretchFactor(1, 1)

        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)

        # Add to main layout
        main_layout.addWidget(splitter)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Populate navigation
        self._populate_navigation()

        # Load initial content
        self._load_section("welcome")

    def _populate_navigation(self):
        """Populate the navigation tree with manual sections."""
        sections = [
            ("Welcome", "welcome"),
            ("Interface Overview", "interface_overview"),
            ("Selecting Observation Date", "date_selection"),
            ("Managing Schedules", "schedules"),
            ("OBSERVE Action", "observe"),
            ("Celestial Object Catalog", "catalog"),
            ("Telescope Units", "telescope_units"),
            ("Field Formats", "field_formats"),
        ]

        for title, key in sections:
            item = QTreeWidgetItem(self.nav_tree, [title])
            item.setData(0, Qt.ItemDataRole.UserRole, key)

    def _on_item_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle navigation tree item click."""
        section_key = item.data(0, Qt.ItemDataRole.UserRole)
        if section_key:
            self._load_section(section_key)

    def _clear_content(self):
        """Clear all content widgets."""
        while self.content_layout.count():
            if (child := self.content_layout.takeAt(0)) is not None:
                if (widget := child.widget()) is not None:
                    widget.deleteLater()

    def add_widget(self, widget: QWidget):
        """Add a custom widget to the content area."""
        # Disable the widget to make it non-interactive
        widget.setEnabled(False)
        self.content_layout.addWidget(widget)

    def add_heading(self, text: str, level: int = 1):
        """Add a heading to the content.
        level: Heading level (1, 2, or 3)
        """
        label = QLabel(text)
        font = QFont()
        font.setPointSize(18 if level == 1 else 14 if level == 2 else 12)
        font.setBold(True)
        label.setFont(font)
        self.content_layout.addWidget(label)

    def add_text(self, text: str):
        """Add a text paragraph to the content."""
        label = QLabel(text)
        label.setWordWrap(True)
        self.content_layout.addWidget(label)

    def add_spacing(self, height: int = 20):
        """Add vertical spacing."""
        spacer = QWidget()
        spacer.setFixedHeight(height)
        self.content_layout.addWidget(spacer)

    def _load_section(self, section_key: str):
        """Load content for a specific section."""
        self._clear_content()

        if section_key == "welcome":
            self.add_heading("Welcome to Marvel Schedule Maker")
            self.add_text("Marvel Schedule Maker is a tool for planning and scheduling astronomical observations.")
            self.add_text("This manual will guide you through the features of the application.")

        elif section_key == "interface_overview":
            self.add_heading("Interface Overview")
            self.add_text("Content for this section will be added soon.")

        elif section_key == "date_selection":
            self.add_heading("Selecting Observation Date")
            self.add_text("Click on the date display in the top bar to open a calendar.")

            widget = ClickableLabel(datetime.now().strftime('%A, %B %d, %Y'))
            widget.setFixedSize(QSize(250, 70))
            self.add_widget(widget)

            self.add_text("Select the date for which you want to plan observations.")

            widget = CalendarPopupDialog()
            self.add_widget(widget)
            self.add_spacing()

            self.add_text("The solar cycle bar and all visibility calculations will update for the selected date.")

        elif section_key == "schedules":
            self.add_heading("Managing Schedules")

            self.add_spacing(10)
            self.add_heading("Creating a New Schedule", 2)
            self.add_text("Click the New button in the top bar to clear the current schedule and start fresh.")
            new_button = QPushButton()
            new_button.setIcon(qta.icon('fa6.file'))
            new_button.setIconSize(QSize(30,30))
            new_button.setFixedSize(QSize(40,40))
            self.add_widget(new_button)

            self.add_spacing(10)
            self.add_heading("Opening a Schedule", 2)
            self.add_text("Click the Open button to load a schedule CSV file.")
            open_button = QPushButton()
            open_button.setIcon(qta.icon('fa6.folder-open'))
            open_button.setIconSize(QSize(30,30))
            open_button.setFixedSize(QSize(40,40))
            self.add_widget(open_button)

            self.add_spacing(10)
            self.add_heading("Saving a Schedule", 2)
            self.add_text("Click the Save button to save your current schedule to a CSV file.")
            self.add_text("The file will contain all your scheduled actions with their parameters.")
            save_button = QPushButton()
            save_button.setIcon(qta.icon('fa6.floppy-disk'))
            save_button.setIconSize(QSize(30,30))
            save_button.setFixedSize(QSize(40,40))
            self.add_widget(save_button)

        elif section_key == "observe":
            self.add_heading("OBSERVE Action")
            self.add_text("The OBSERVE action schedules observations of celestial targets.")

            self.add_spacing(10)
            self.add_heading("Altitude Graph", 2)
            self.add_text("Shows the target's altitude relative to the telescope throughout the night. The green shaded area indicates when the target is observable (above and below min/max altitude).")

            self.add_spacing(10)
            self.add_heading("Sky View", 2)
            self.add_text("Shows the target and moon position in the sky. The animation shows how positions change throughout the night.")
            self.add_text("The separation value shows the angular distance between target and moon.")

        elif section_key == "catalog":
            self.add_heading("Celestial Object Catalog")
            self.add_text("Click the Settings button in the top bar to open the celestial object catalog.")
            self.add_text("You can search for objects and use their coordinates for observations.")
            self.add_text("The catalog contains common astronomical targets with their RA/DEC coordinates.")

        elif section_key == "telescope_units":
            self.add_heading("Telescope Units")
            self.add_text("Each telescope unit has its own configuration including:")
            self.add_text("• Minimum and maximum altitude limits")
            self.add_text("• Available filters")
            self.add_text("• Exposure time constraints")
            self.add_text("Select the appropriate telescope for your observation.")

        elif section_key == "field_formats":
            self.add_heading("Field Formats")

            self.add_spacing(10)
            self.add_heading("RA (Right Ascension)", 2)
            self.add_text("Format: HH:MM:SS (hours, minutes, seconds)")
            self.add_text("Example: 12:30:45")

            self.add_spacing(10)
            self.add_heading("DEC (Declination)", 2)
            self.add_text("Format: DD:MM:SS (degrees, arcminutes, arcseconds)")
            self.add_text("Example: +45:30:00 or -23:15:30")

            self.add_spacing(10)
            self.add_heading("Exposure Time", 2)
            self.add_text("Enter time in seconds.")
            self.add_text("Example: 300 (for 5 minutes)")

        else:
            self.add_heading(f"Section: {section_key}")
            self.add_text("Content for this section will be added soon.")

        # Add stretch at the end
        self.content_layout.addStretch()