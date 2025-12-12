from datetime import datetime, timedelta, timezone
from typing import List, Optional
from PyQt6.QtWidgets import QLabel, QPushButton, QSlider, QWidget, QMenu, QGraphicsScene, QGridLayout, QGraphicsItem, QGraphicsTextItem, QHBoxLayout, QGraphicsRectItem, QGraphicsView, QGraphicsSceneMouseEvent, QGraphicsDropShadowEffect
from PyQt6.QtCore import pyqtSignal, QPoint, Qt, QTimer, QRectF
from PyQt6.QtGui import QResizeEvent, QPainter, QColor, QPen, QBrush, QPolygon, QLinearGradient

import qtawesome as qta

from marvel_schedule_maker.models.ActionRegistry import ACTION_REGISTRY
from marvel_schedule_maker.services.ApplicationServices import ApplicationServices
from marvel_schedule_maker.viewmodels.TimelinePanelViewModel import TimelinePanelViewModel



class TimelineControlBar(QWidget):
    """Control bar for zoom controls - uses config."""
    
    zoom_changed = pyqtSignal(float) # pixels per second scale
    
    def __init__(self, ui_config) -> None:
        super().__init__()
        self._ui_config = ui_config
        self.setFixedHeight(ui_config.control_bar_height)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)

        layout.addStretch()

        # Zoom controls
        zoom_label = QLabel("Zoom:")
        layout.addWidget(zoom_label)
        
        self.zoom_out_btn = QPushButton()
        self.zoom_out_btn.setIcon(qta.icon('fa6s.magnifying-glass-minus'))
        self.zoom_out_btn.setFixedSize(30, 30)
        self.zoom_out_btn.clicked.connect(self._on_zoom_out)
        layout.addWidget(self.zoom_out_btn)
        
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setMinimum(ui_config.zoom_slider_min)
        self.zoom_slider.setMaximum(ui_config.zoom_slider_max)
        self.zoom_slider.setValue(ui_config.zoom_slider_default)
        self.zoom_slider.setFixedWidth(300)
        self.zoom_slider.valueChanged.connect(self._on_zoom_slider)
        layout.addWidget(self.zoom_slider)
        
        self.zoom_in_btn = QPushButton()
        self.zoom_in_btn.setIcon(qta.icon('fa6s.magnifying-glass-plus'))
        self.zoom_in_btn.setFixedSize(30, 30)
        self.zoom_in_btn.clicked.connect(self._on_zoom_in)
        layout.addWidget(self.zoom_in_btn)

    def _on_zoom_slider(self, value: int):
        """Set zoom to value"""
        self.zoom_changed.emit(value / 100)

    def _on_zoom_in(self):
        """Increase zoom."""
        current = self.zoom_slider.value()
        self.zoom_slider.setValue(min(current + self._ui_config.zoom_step, self.zoom_slider.maximum()))
    
    def _on_zoom_out(self):
        """Decrease zoom."""
        current = self.zoom_slider.value()
        self.zoom_slider.setValue(max(current - self._ui_config.zoom_step, self.zoom_slider.minimum()))
    
    def set_zoom_value(self, pixels_per_second: float):
        """Set zoom slider to specific value."""
        slider_value = int(pixels_per_second * 100)
        self.zoom_slider.blockSignals(True)
        self.zoom_slider.setValue(slider_value)
        self.zoom_slider.blockSignals(False)

class TimeRulerWidget(QWidget):
    """Vertical time axis showing hours and grid lines - presentation only."""
    
    def __init__(self, ui_config):
        super().__init__()
        self._ui_config = ui_config
        self.setFixedWidth(ui_config.ruler_width)
        
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.pixels_per_second = ui_config.default_zoom
        self.scroll_offset = 0
        
        self.current_time = datetime.now(timezone.utc).replace(tzinfo=None)
        
        self.setStyleSheet(f"background-color: {ui_config.ruler_background_color}; border-right: 1px solid {ui_config.ruler_border_color};")

    def update_display(self, start_time: datetime, end_time: datetime, pixels_per_second: float, scroll_offset: int):
        """Update all display data and repaint."""
        self.start_time = start_time
        self.end_time = end_time
        self.pixels_per_second = pixels_per_second
        self.scroll_offset = scroll_offset
        self.current_time = datetime.now(timezone.utc).replace(tzinfo=None)
        self.update()
    
    def time_to_y(self, dt: datetime) -> float:
        """Convert datetime to Y coordinate."""
        if not self.start_time:
            return 0
        delta_seconds = (dt - self.start_time).total_seconds()
        return delta_seconds * self.pixels_per_second - self.scroll_offset
    
    def _calculate_interval(self) -> float:
        """Calculate appropriate time interval based on zoom level.
        
        Returns interval in minutes (can be fractional for sub-minute intervals).
        """
        # Target: show marker approximately every 80-100 pixels
        target_pixels = 90
        
        # Calculate how many seconds would span target_pixels at current zoom
        seconds_per_marker = target_pixels / self.pixels_per_second
        minutes_per_marker = seconds_per_marker / 60
        
        # Round to nice intervals
        if minutes_per_marker >= 120:
            return 120  # 2 hours
        elif minutes_per_marker >= 60:
            return 60   # 1 hour
        elif minutes_per_marker >= 30:
            return 30   # 30 minutes
        elif minutes_per_marker >= 15:
            return 15   # 15 minutes
        elif minutes_per_marker >= 10:
            return 10   # 10 minutes
        elif minutes_per_marker >= 5:
            return 5    # 5 minutes
        elif minutes_per_marker >= 2:
            return 2    # 2 minutes
        elif minutes_per_marker >= 1:
            return 1    # 1 minute
        elif minutes_per_marker >= 0.5:
            return 0.5  # 30 seconds
        elif minutes_per_marker >= 0.25:
            return 0.25 # 15 seconds
        elif minutes_per_marker >= 0.166:
            return 0.166 # 10 seconds
        else:
            return 0.083 # 5 seconds
    
    def paintEvent(self, event):
        """Draw time ruler."""
        super().paintEvent(event)
        
        if not self.start_time or not self.end_time:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Calculate dynamic interval based on zoom level
        interval_minutes = self._calculate_interval()
        
        # Calculate time range
        current_time = self.start_time
        
        # Draw time labels and grid lines
        while current_time <= self.end_time:
            y = self.time_to_y(current_time)
            
            # Only draw if visible
            if -20 <= y <= self.height() + 20:
                # Determine if this is a major marker (hour boundary)
                is_major = current_time.minute == 0
                
                # Format time string - always show HH:MM
                time_str = current_time.strftime("%H:%M")
                
                # Major hour lines
                if is_major:
                    painter.setPen(QPen(QColor("#495057"), 2))
                    font = painter.font()
                    font.setBold(True)
                    painter.setFont(font)
                else:
                    painter.setPen(QPen(QColor("#6c757d"), 1))
                    font = painter.font()
                    font.setBold(False)
                    painter.setFont(font)

                # Draw text
                text_rect = QRectF(5, y - 10, 50, 20)
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, time_str)
            
            # Increment by calculated interval
            if interval_minutes >= 1:
                current_time += timedelta(minutes=interval_minutes)
            else:
                # Sub-minute intervals
                current_time += timedelta(seconds=interval_minutes * 60)

        # Draw current time arrow
        painter.setPen(QPen(QColor("#FF0000"), 2))
        painter.drawPolygon(self._arrow(85, int(self.time_to_y(self.current_time))))

        painter.end()
    
    def _arrow(self, x, y):
        """Create arrow polygon for current time indicator."""
        points: QPolygon = QPolygon()
        points.append(QPoint(x-20, y+3))
        points.append(QPoint(x-20, y+8))
        points.append(QPoint(x-10, y))
        points.append(QPoint(x-20, y-8))
        points.append(QPoint(x-20, y-3))
        points.append(QPoint(x-30, y-3))
        points.append(QPoint(x-30, y+3))
        return points

class TelescopeHeaderWidget(QWidget):
    """Horizontal header showing telescope names - uses config."""
    
    def __init__(self, ui_config, column_width: float):
        super().__init__()
        self._ui_config = ui_config
        self._column_width = column_width
        
        self.setFixedHeight(ui_config.header_height)
        self.setStyleSheet(f"background-color: {ui_config.header_background_color}; border-bottom: 2px solid {ui_config.header_border_color};")
    
    def update_column_width(self, column_width: float):
        """Update column width when viewport resizes."""
        self._column_width = column_width
        self.update()
    
    def paintEvent(self, event):
        """Draw telescope headers."""
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        font = painter.font()
        font.setBold(True)
        font.setPointSize(11)
        painter.setFont(font)
        painter.setPen(QColor("#212529"))
        
        for i, name in enumerate(self._ui_config.telescope_names):
            x = i * (self._column_width + self._ui_config.column_spacing)
            rect = QRectF(x, 0, self._column_width, self.height())
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, name)
        
        painter.end()

class TimelinePanelView(QWidget):
    """Time-proportional timeline viewer - MVVM pattern with full refresh."""
    
    def __init__(self, services: ApplicationServices):
        super().__init__()
        
        self._services = services
        self._viewmodel = TimelinePanelViewModel(services)
        
        # Create UI configuration
        ui_config = self._viewmodel.get_ui_config()
        
        # Create grid layout
        self.grid_layout = QGridLayout(self)
        
        # Initialize sub-widgets with config
        self.control_bar = TimelineControlBar(ui_config)
        self.header_widget = TelescopeHeaderWidget(ui_config, self._viewmodel.get_column_width())
        self.ruler_widget = TimeRulerWidget(ui_config)
        self.graphics_widget = TimelineGraphicsWidget()
        
        # Layout widgets
        self.grid_layout.addWidget(self.control_bar, 0, 0, 1, 2)
        self.grid_layout.addWidget(self.header_widget, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.ruler_widget, 2, 0, 1, 1)
        self.grid_layout.addWidget(self.graphics_widget, 2, 1, 1, 1)
        
        # Connect ViewModel signals
        self._viewmodel.display_data_changed.connect(self.refresh)
        self._viewmodel.zoom_changed.connect(self._on_zoom_changed)
        self._viewmodel.scroll_to_entry_requested.connect(self._on_scroll_to_entry_requested)
        
        # Connect View signals to ViewModel
        self.control_bar.zoom_changed.connect(self._viewmodel.set_zoom)
        self.graphics_widget.task_context_menu.connect(self._on_task_context_menu)
        self.graphics_widget.scroll_ratio_changed.connect(self._viewmodel.set_scroll_ratio)
        
        # Connect schedule signals for scroll to entry
        self._services.schedule.entry_added.connect(self._on_entry_added)
        
        # Initial refresh
        self.refresh()
    
    def refresh(self):
        """Full refresh - get all data from ViewModel and redraw everything."""
        # Get all display data from ViewModel
        start_time, end_time = self._viewmodel.get_time_range()
        task_display_data = self._viewmodel.get_task_display_data()
        pixels_per_second = self._viewmodel.get_pixels_per_second()
        scene_width, scene_height = self._viewmodel.get_scene_dimensions()
        scroll_ratio = self._viewmodel.get_scroll_ratio()
        task_ui_config = self._viewmodel.get_task_ui_config()
        column_width = self._viewmodel.get_column_width()
        
        # Update all widgets with pre-calculated data
        if start_time and end_time:
            scrollbar = self.graphics_widget.verticalScrollBar()
            current_scroll_offset = scrollbar.value() if scrollbar else 0
            
            self.ruler_widget.update_display(start_time, end_time, pixels_per_second, current_scroll_offset)
            self.graphics_widget.refresh(task_display_data, scene_width, scene_height, task_ui_config, scroll_ratio)
            self.header_widget.update_column_width(column_width)
            self.control_bar.set_zoom_value(pixels_per_second)
            
            # Connect scrollbar to ruler widget for real-time sync
            if scrollbar:
                scrollbar.valueChanged.connect(self._sync_ruler_scroll)
    
    def _sync_ruler_scroll(self, value: int):
        """Sync ruler widget with graphics widget scroll."""
        start_time, end_time = self._viewmodel.get_time_range()
        pixels_per_second = self._viewmodel.get_pixels_per_second()
        if start_time and end_time:
            self.ruler_widget.update_display(start_time, end_time, pixels_per_second, value)
    
    def _on_zoom_changed(self, pixels_per_second: float):
        """Handle zoom change from ViewModel - just update control bar."""
        self.control_bar.set_zoom_value(pixels_per_second)
    
    def _on_entry_added(self, entry_id: str):
        """Handle entry added - request scroll to new entry."""
        QTimer.singleShot(100, lambda: self._viewmodel.request_scroll_to_entry(entry_id))
    
    def _on_scroll_to_entry_requested(self, entry_id: str):
        """Handle scroll to entry request from ViewModel."""
        self.graphics_widget.scroll_to_entry(entry_id)
    
    def _on_task_context_menu(self, entry_id: str, action_type: str, pos: QPoint):
        """Show context menu for task - delegate actions to ViewModel."""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #adb5bd;
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 25px;
                border-radius: 3px;
            }
            QMenu::item:selected {
                background-color: #e2e6ea;
            }
            QMenu::separator {
                height: 1px;
                background-color: #ced4da;
                margin: 5px 10px;
            }
        """)
        
        edit_action = menu.addAction("Edit")
        edit_action.triggered.connect(lambda: self._viewmodel.handle_edit(entry_id, action_type)) # type: ignore
        
        copy_action = menu.addAction("Copy")
        copy_action.triggered.connect(lambda: self._viewmodel.handle_copy(entry_id)) # type: ignore
        
        menu.addSeparator()
        
        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(lambda: self._viewmodel.handle_delete(entry_id)) # type: ignore
        
        menu.addSeparator()
        
        insert_above_action = menu.addAction("Insert Above")
        insert_above_action.triggered.connect(lambda: self._viewmodel.handle_insert_above(entry_id)) # type: ignore
        
        insert_below_action = menu.addAction("Insert Below")
        insert_below_action.triggered.connect(lambda: self._viewmodel.handle_insert_below(entry_id)) # type: ignore
        
        if self._viewmodel.has_clipboard():
            menu.addSeparator()
            
            insert_copied_above_action = menu.addAction("Insert Copied Above")
            insert_copied_above_action.triggered.connect(lambda: self._viewmodel.handle_insert_copied_above(entry_id)) # type: ignore
            
            insert_copied_below_action = menu.addAction("Insert Copied Below")
            insert_copied_below_action.triggered.connect(lambda: self._viewmodel.handle_insert_copied_below(entry_id)) # type: ignore
        
        menu.exec(pos)
    
    def resizeEvent(self, event):
        """Handle resize - update ViewModel with new viewport width."""
        super().resizeEvent(event)
        viewport_width = self.graphics_widget.viewport().width() # type: ignore
        self._viewmodel.set_viewport_width(viewport_width)

class TaskRectItem(QGraphicsRectItem):
    """Visual representation of a single scheduled task - presentation only."""
    
    def __init__(self, display_data, ui_config):
        """
        Initialize TaskRectItem from pre-calculated display data.
        
        Args:
            display_data: TaskDisplayData with all position/state information
            ui_config: TaskRectUIConfig with visual styling configuration
        """
        super().__init__(display_data.x, display_data.y, display_data.width, display_data.height)
        
        self.entry = display_data.entry
        self.entry_id = display_data.entry_id
        self.is_copied = display_data.is_copied
        self.is_editing = display_data.is_editing
        self.is_hovered = False
        self._is_being_deleted = False
        self._ui_config = ui_config
        
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)

        # Add drop shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(ui_config.shadow_blur_radius)
        shadow.setXOffset(ui_config.shadow_x_offset)
        shadow.setYOffset(ui_config.shadow_y_offset)
        shadow.setColor(ui_config.shadow_color)
        self.setGraphicsEffect(shadow)
        
        # Create text items
        self.text_item = QGraphicsTextItem(self)
        
        # Apply initial appearance
        self._update_appearance()
        
        # Show tooltip
        start_str = self.entry.start_time.strftime("%H:%M:%S")
        end_str = self.entry.end_time.strftime("%H:%M:%S")
        duration = self.entry.end_time - self.entry.start_time
        self.setToolTip(f"{start_str} - {end_str}\nDuration: {duration}")

    def cleanup(self):
        """Properly clean up resources before deletion."""
        self._is_being_deleted = True
        
        # Clear graphics effect to avoid Qt issues
        self.setGraphicsEffect(None)
        
        # Remove child items
        if self.text_item:
            scene = self.text_item.scene()
            if scene:
                scene.removeItem(self.text_item)
            self.text_item.setParentItem(None)
            self.text_item = None
    
    def _update_appearance(self):
        """Update the visual appearance based on state from config."""
        if self._is_being_deleted:
            return
        
        # Determine state and get colors from config
        if self.is_copied:
            border_color = self._ui_config.copied_border
            fill_color = self._ui_config.copied_fill
            border_width = self._ui_config.copied_border_width
        elif self.is_editing:
            border_color = self._ui_config.editing_border
            fill_color = self._ui_config.editing_fill
            border_width = self._ui_config.editing_border_width
        elif self.is_hovered:
            border_color = self._ui_config.hover_border
            fill_color = self._ui_config.hover_fill
            border_width = self._ui_config.hover_border_width
        else:
            border_color = self._ui_config.normal_border
            fill_color = self._ui_config.normal_fill
            border_width = self._ui_config.normal_border_width
        
        # Check for zero duration error
        if self.entry.start_time == self.entry.end_time:
            border_color = self._ui_config.error_border
            border_width = self._ui_config.error_border_width
        
        # Apply visual styling
        pen = QPen(border_color, border_width)
        self.setPen(pen)
        gradient = QLinearGradient(0, 0, 0, self.rect().height())
        gradient.setColorAt(0.0, fill_color.lighter(105))
        gradient.setColorAt(1.0, fill_color)
        self.setBrush(QBrush(fill_color))

    def hoverEnterEvent(self, event):
        """Handle mouse hover enter."""
        if self._is_being_deleted:
            return
        self.is_hovered = True
        self._update_appearance()
        super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event):
        """Handle mouse hover leave."""
        if self._is_being_deleted:
            return
        self.is_hovered = False
        self._update_appearance()
        super().hoverLeaveEvent(event)

    def itemChange(self, change, value):
        if self._is_being_deleted:
            return super().itemChange(change, value)
            
        # Called whenever the item is added/removed/moved in a scene
        if change == QGraphicsItem.GraphicsItemChange.ItemSceneHasChanged and value is not None:
            # Defer update until next event loop tick (scene is fully ready)
            QTimer.singleShot(0, self._update_text)
        return super().itemChange(change, value)
    
    def _update_text(self):
        """Update text label."""
        parent_rect = self.rect()

        if self._is_being_deleted:
            return
        
        assert self.text_item is not None

        # Hide text entirely if rect is too small
        if parent_rect.width() < self._ui_config.min_visible_width or parent_rect.height() < self._ui_config.min_visible_height:
            self.text_item.setVisible(False)
            return
        else:
            self.text_item.setVisible(True)
            
        display_text = self._get_display_text()
        
        # Set display text and color from config
        self.text_item.setPlainText(display_text)
        self.text_item.setDefaultTextColor(self._ui_config.text_color)
        text_font = self.text_item.font()
        text_font.setBold(self._ui_config.font_bold)
        text_font.setPointSize(self._ui_config.font_size)
        self.text_item.setFont(text_font)      

        # Get dimensions
        text_rect = self.text_item.boundingRect()

        # Compute top-left starting point for centering
        start_x = parent_rect.left() + (parent_rect.width() - text_rect.width()) / 2
        start_y = parent_rect.top() + (parent_rect.height() - text_rect.height()) / 2

        # Optional visible-portion adjustment
        if self.scene() and self.scene().views(): # type: ignore
            view = self.scene().views()[0]# type: ignore
            visible_scene_rect = view.mapToScene(view.viewport().rect()).boundingRect()# type: ignore
            item_scene_rect = self.mapToScene(parent_rect).boundingRect()
            visible_part = visible_scene_rect.intersected(item_scene_rect)

            # Only adjust vertically if there's a visible overlap
            if visible_part.isValid() and visible_part.height() >= 30:
                visible_top_left = self.mapFromScene(visible_part.topLeft())
                visible_bottom_right = self.mapFromScene(visible_part.bottomRight())
                visible_height = visible_bottom_right.y() - visible_top_left.y()
                start_y = visible_top_left.y() + (visible_height - text_rect.height()) / 2

        text_x = start_x - text_rect.left()
        text_y = start_y - text_rect.top()

        # Apply positions
        self.text_item.setPos(text_x, text_y)
    
    def _get_display_text(self) -> str:
        """Get formatted display name for task."""
        action_data = self.entry.action_data
        if action_data.get('type') is None:
            return "~INSERTING NEW~"
        else:
            timeline_name = ACTION_REGISTRY[action_data['type']]['timeline_name']
            for k, v in action_data.items():
                timeline_name = timeline_name.replace(f"<{k}>", str(v))
            return timeline_name

    def paint(self, painter: QPainter, option, widget=None):
        """Custom paint with rounded corners from config."""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        
        # Draw rounded rectangle
        painter.setPen(self.pen())
        painter.setBrush(self.brush())
        painter.drawRoundedRect(rect, self._ui_config.corner_radius, self._ui_config.corner_radius)

class TimelineGraphicsWidget(QGraphicsView):
    """Custom graphics view for timeline - presentation only."""
    
    task_context_menu = pyqtSignal(str, str, QPoint)  # entry_id, action_type, Position
    scroll_ratio_changed = pyqtSignal(float)  # scroll position ratio
    
    def __init__(self):
        self._scene = QGraphicsScene()
        super().__init__(self._scene)
        
        self.task_items: List[TaskRectItem] = []

        # View settings
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setStyleSheet("""
            /* Chrome-style scrollbar */
            QScrollBar:vertical {
                background: transparent;
                width: 14px;
                margin: 0px;
                border: none;
            }
            
            QScrollBar::handle:vertical {
                background: #5f6368;
                min-height: 30px;
                margin: 2px 2px 2px 2px;
                border-radius: 7px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #80868b;
            }
            
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }
            
            QScrollBar::up-arrow:vertical,
            QScrollBar::down-arrow:vertical {
                background: none;
            }
        """)
        
        # Mouse tracking
        self.setMouseTracking(True)
    
    def refresh(self, task_display_data: List, scene_width: float, scene_height: float, 
                task_ui_config, scroll_ratio: float):
        """Full refresh from pre-calculated ViewModel data."""
        # Clear existing items
        self._clear_all_items()
        
        # Set scene size
        self._scene.setSceneRect(0, 0, scene_width, scene_height)
        
        # Create all task items from display data
        for data in task_display_data:
            task_item = TaskRectItem(data, task_ui_config)
            
            # Connect click events
            task_item.mousePressEvent = lambda event, eid=data.entry_id, action_type=data.entry.action_data.get('type'): self._on_task_clicked(eid, action_type, event)
            
            self._scene.addItem(task_item)
            self.task_items.append(task_item)
        
        # Restore scroll position
        self._restore_scroll_position(scroll_ratio)
    
    def scroll_to_entry(self, entry_id: str):
        """Scroll to make the specified entry visible."""
        for task_item in self.task_items:
            if task_item._is_being_deleted:
                continue
            if task_item.entry_id == entry_id:
                item_rect = task_item.sceneBoundingRect()
                self.centerOn(item_rect.center())
                break
    
    def _on_task_clicked(self, entry_id: str, action_type: str, event: Optional[QGraphicsSceneMouseEvent]):
        """Handle task click."""
        if event is not None and event.button() == Qt.MouseButton.RightButton:
            self.task_context_menu.emit(entry_id, action_type, event.screenPos())
    
    def _restore_scroll_position(self, scroll_ratio: float):
        """Restore scroll position after refresh."""
        scrollbar = self.verticalScrollBar()
        if scrollbar and scrollbar.maximum() > 0:
            new_scroll_value = int(scroll_ratio * scrollbar.maximum())
            scrollbar.setValue(new_scroll_value)
    
    def _clear_all_items(self):
        """Remove all items from scene."""
        # Create a copy of the list to iterate over
        task_items_to_remove = self.task_items.copy()

        # Clear the list first
        self.task_items.clear()
        
        # Then remove items from scene
        for item in task_items_to_remove:
            item.cleanup()
            
            if item.scene() is self._scene:
                self._scene.removeItem(item)
            # Explicitly delete the item
            item.setParentItem(None)
            del item
    
    def scrollContentsBy(self, dx: int, dy: int):
        """Override to emit scroll ratio changes."""
        super().scrollContentsBy(dx, dy)
        
        # Emit scroll ratio for ViewModel to track
        scrollbar = self.verticalScrollBar()
        if scrollbar and scrollbar.maximum() > 0:
            ratio = scrollbar.value() / scrollbar.maximum()
            self.scroll_ratio_changed.emit(ratio)

    def resizeEvent(self, event: QResizeEvent | None) -> None:
        """Handle resize - parent view will trigger refresh."""
        super().resizeEvent(event)
