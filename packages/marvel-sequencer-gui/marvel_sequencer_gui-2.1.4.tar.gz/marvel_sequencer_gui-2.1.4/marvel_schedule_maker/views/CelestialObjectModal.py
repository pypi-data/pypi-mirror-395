from typing import List, Tuple

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QGraphicsOpacityEffect, QHeaderView
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation
from PyQt6.QtGui import QPainter, QColor, QResizeEvent

from marvel_schedule_maker.services.ApplicationServices import ApplicationServices
from marvel_schedule_maker.viewmodels.CelestialObjectViewModel import CelestialObjectViewModel


class CelestialObjectModal(QWidget):
    """Modal overlay for editing celestial object catalog."""
    
    closed = pyqtSignal()
    
    def __init__(self, parent: QWidget, services: ApplicationServices):
        super().__init__(parent)

        self._services = services
        self._viewmodel = CelestialObjectViewModel(services)
        
        # Connect ViewModel signals
        self._viewmodel.catalog_loaded.connect(self._on_catalog_loaded)
        self._viewmodel.save_completed.connect(self._on_save_completed)
        
        # Setup UI
        self._setup_ui()
        
        # Animation for fade in/out
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(200)
        self.fade_animation.finished.connect(self._on_animation_finished)
        
        self._closing = False
        self.hide()
    
    def _setup_ui(self):
        """Setup the UI layout and widgets."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Dialog container
        dialog = QWidget()
        dialog.setFixedSize(1000, 700)
        dialog.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
            }
        """)
        
        dialog_layout = QVBoxLayout(dialog)
        dialog_layout.setContentsMargins(30, 30, 30, 30)
        dialog_layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Celestial Objects")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #212529;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        close_button = QPushButton("✕")
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 20px;
                color: #6c757d;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-radius: 15px;
            }
        """)
        close_button.clicked.connect(self.close_modal)
        header_layout.addWidget(close_button)
        
        dialog_layout.addLayout(header_layout)
        
        # Description
        description = QLabel(
            "Manage astronomical objects in your catalog. "
            "RA and DEC can be auto-filled by object name in observation forms."
        )
        description.setWordWrap(True)
        description.setStyleSheet("font-size: 13px; color: #6c757d;")
        dialog_layout.addWidget(description)
        
        # Button bar
        button_bar = QHBoxLayout()
        
        self.add_button = QPushButton("Add Object")
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.add_button.clicked.connect(self._on_add_clicked)
        
        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.remove_button.clicked.connect(self._on_remove_clicked)
        
        button_bar.addWidget(self.add_button)
        button_bar.addWidget(self.remove_button)
        button_bar.addStretch()
        
        dialog_layout.addLayout(button_bar)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Object Name", "RA", "DEC"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        horizontalHeader = self.table.horizontalHeader()
        if horizontalHeader:
            horizontalHeader.setStretchLastSection(True)
            horizontalHeader.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            horizontalHeader.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            horizontalHeader.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #dee2e6;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-weight: bold;
            }
        """)
        
        dialog_layout.addWidget(self.table, 1)
        
        # Save button
        save_button_container = QHBoxLayout()
        save_button_container.addStretch()
        
        self.save_button = QPushButton("Save Changes")
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.save_button.clicked.connect(self._on_save_clicked)
        save_button_container.addWidget(self.save_button)
        
        dialog_layout.addLayout(save_button_container)
        
        main_layout.addWidget(dialog)
        self.dialog = dialog
    
    # ==================== Display ====================
    
    def show_modal(self):
        """Show the modal with fade-in animation."""
        # Resize to parent
        parent = self.parent()
        if parent:
            parent_rect = parent.rect() #type: ignore
            self.setGeometry(parent_rect)
        
        # Load data
        self._viewmodel.load_objects()
        
        # Show and animate
        self.show()
        self.raise_()
        
        self.opacity_effect.setOpacity(0)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()
    
    def close_modal(self):
        """Close the modal with fade-out animation."""
        if self._closing:
            return
        
        self._closing = True
        
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.start()
    
    def _on_animation_finished(self):
        """Handle animation completion."""
        if self._closing:
            self.hide()
            self.closed.emit()
            self._closing = False
    
    # ==================== Event Handlers ====================
    
    def paintEvent(self, event):
        """Paint semi-transparent overlay background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 127))
    
    def mousePressEvent(self, event):
        """Close modal when clicking outside dialog."""
        dialog_rect = self.dialog.geometry()
        click_pos = event.pos()
        
        if not dialog_rect.contains(click_pos):
            self.close_modal()
    
    def keyPressEvent(self, event):
        """Handle ESC key to close modal."""
        if event.key() == Qt.Key.Key_Escape:
            self.close_modal()
        else:
            super().keyPressEvent(event)
    
    def resizeEvent(self, event: QResizeEvent):
        """Handle parent window resize."""
        super().resizeEvent(event)
        if self.parent() and self.isVisible():
            parent_rect = self.parent().rect() #type: ignore
            self.setGeometry(parent_rect)
    
    # ==================== User Actions ====================
    
    def _on_add_clicked(self):
        """Handle add button click."""
        # Get default values from ViewModel
        name, ra, dec = self._viewmodel.add_new_object()
        
        # Add row to table
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        
        self.table.setItem(row_count, 0, QTableWidgetItem(name))
        self.table.setItem(row_count, 1, QTableWidgetItem(ra))
        self.table.setItem(row_count, 2, QTableWidgetItem(dec))
        
        # Select and edit the new row
        self.table.selectRow(row_count)
        self.table.editItem(self.table.item(row_count, 0))
    
    def _on_remove_clicked(self):
        """Handle remove button click."""
        selected_rows = set()
        for item in self.table.selectedItems():
            selected_rows.add(item.row())
        
        if not selected_rows:
            return
        
        # Remove rows in reverse order
        for row in sorted(selected_rows, reverse=True):
            self.table.removeRow(row)
    
    def _on_save_clicked(self):
        """Handle save button click."""
        # Collect table data
        table_data: List[Tuple[str, str, str]] = []
        
        for row in range(self.table.rowCount()):
            name_item = self.table.item(row, 0)
            ra_item = self.table.item(row, 1)
            dec_item = self.table.item(row, 2)
            
            if not name_item or not ra_item or not dec_item:
                continue
            
            name = name_item.text().strip()
            ra = ra_item.text().strip()
            dec = dec_item.text().strip()
            
            table_data.append((name, ra, dec))
        
        # Send to ViewModel
        self._viewmodel.save_all(table_data)
    
    # ==================== ViewModel Signal Handlers ====================
    
    def _on_catalog_loaded(self, data: List[Tuple[str, str, str]]):
        """Handle catalog data loaded from ViewModel."""
        self.table.setRowCount(len(data))
        
        for row, (name, ra, dec) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(ra))
            self.table.setItem(row, 2, QTableWidgetItem(dec))
    
    def _on_save_completed(self, success: bool, message: str):
        """Handle save completion from ViewModel."""
        # Reload table to show what was actually saved
        self._viewmodel.load_objects()