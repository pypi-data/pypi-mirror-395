from datetime import datetime, time, timedelta
import math
import random
from typing import List, Optional

from marvel_schedule_maker.utils.svg_renderers import create_moon_svg_renderer, create_star_svg_renderer

from marvel_schedule_maker.viewmodels.actionpanelviewmodels.ObserveGraphViewModel import ObserveGraphViewModel

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer, QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QRadialGradient, QPixmap, QFont

from astropy.coordinates import SkyCoord
import astropy.units as u

import pyqtgraph as pg

class ObserveGraph(QWidget):
    """Real-time altitude graph for 'OBSERVE' action."""

    def __init__(self, viewmodel: ObserveGraphViewModel):
        super().__init__()

        self.viewmodel = viewmodel
        
        # Create the plot widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground(None)
        self.plot_widget.setInteractive(False)
        self.plot_widget.showGrid(x=False, y=False)
        self.plot_widget.setFixedHeight(250)

        # Store plot items for later updates
        self.altitude_moon_curve = None
        self.altitude_curve = None
        self.start_marker = None
        self.end_marker = None
        self.min_limit_line = None
        self.max_limit_line = None
        self.observable_regions = []
        self.twilight_regions = []
        
        # Create legend widget
        self.legend_widget = LegendWidget()
        
        self.sky_widget = SkyWidget(viewmodel)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        layout.addWidget(self.plot_widget)
        layout.addWidget(self.legend_widget)
        layout.addWidget(self.sky_widget)
        self.setLayout(layout)

        # Connect ViewModel signals
        self.viewmodel.target_curve_updated.connect(self._draw_altitude_curve)
        self.viewmodel.moon_curve_updated.connect(self._draw_moon_curve)
        self.viewmodel.horizon_limits_updated.connect(self._draw_horizon_limits)
        self.viewmodel.time_markers_updated.connect(self._draw_time_markers)
        self.viewmodel.observable_regions_updated.connect(self._highlight_observable_range)
        self.viewmodel.sky_view_updated.connect(self._update_sky_view)
        self.viewmodel.legend_items_updated.connect(self.legend_widget.update_legend)

        self._configure_axes()
        self._draw_twilight_zones()
        
        # Trigger initial update
        self.viewmodel.update_all()

    #########################
    #                       #
    #   Conversion Methods  #
    #                       #
    #########################

    def _datetime_to_plot_x(self, dt: datetime) -> float:
        """Convert datetime to plot x-coordinate (timestamp)."""
        return dt.timestamp()

    def _plot_x_to_datetime(self, x: float) -> datetime:
        """Convert plot x-coordinate (timestamp) back to datetime."""
        return datetime.fromtimestamp(x)

    def _configure_axes(self) -> None:
        """Configure plot axes with labels and ranges."""
        # Y axis (altitude)
        self.plot_widget.setLabel('left', 'Altitude', units='°')
        self.plot_widget.setYRange(0, 90, padding=0) # type: ignore

        altitude_axis = AltitudeAxisItem(orientation='left')
        self.plot_widget.setAxisItems({'left': altitude_axis})

        self.plot_widget.setLabel('bottom', 'Time')

        # X axis (time)
        start_time = self.viewmodel.services.dates.civil_twilight_start - timedelta(hours=1)
        end_time = self.viewmodel.services.dates.civil_twilight_end + timedelta(hours=1)

        x_min = self._datetime_to_plot_x(start_time)
        x_max = self._datetime_to_plot_x(end_time)

        # Custom time axis formatting
        time_axis = TimeAxisItem(start_time, end_time, orientation='bottom')
        self.plot_widget.setAxisItems({'bottom': time_axis})

        self.plot_widget.setXRange(x_min, x_max, padding=0) # type: ignore

        self.plot_widget.enableAutoRange(enable=False)

    #####################
    #                   #
    #   Drawing Methods #
    #                   #
    #####################

    def _update_sky_view(self, target_curve, moon_curve, min_alt, max_alt):
        """Update the sky view with current curves."""
        self.sky_widget.setCurves(target_curve, moon_curve)
        if min_alt is not None and max_alt is not None:
            self.sky_widget.setMinMaxAltitude(min_alt, max_alt)

    def _draw_moon_curve(self, curve_data: list[tuple[float, float]]):
        """Draw the moon altitude curve."""
        if not curve_data:
            if self.altitude_moon_curve:
                self.plot_widget.removeItem(self.altitude_moon_curve)
                self.altitude_moon_curve = None
            return
        
        start_time = self.viewmodel.services.dates.civil_twilight_start - timedelta(hours=1)
        end_time = self.viewmodel.services.dates.civil_twilight_end + timedelta(hours=1)
        
        timestamps = self.viewmodel._generate_time_points(start_time, end_time)
        altitudes = [alt for alt, az in curve_data]
        x_values = [self._datetime_to_plot_x(t) for t in timestamps]

        if self.altitude_moon_curve is not None:
            self.plot_widget.removeItem(self.altitude_moon_curve)

        pen = pg.mkPen(color="#516F7B", width=2)
        self.altitude_moon_curve = self.plot_widget.plot(
            x=x_values,
            y=altitudes,
            pen=pen,
            name="Altitude Moon Curve"
        )

    def _draw_altitude_curve(self, curve_data: list[tuple[float, float]]):
        """Draw the target altitude curve."""
        if not curve_data:
            if self.altitude_curve:
                self.plot_widget.removeItem(self.altitude_curve)
                self.altitude_curve = None
            return
        
        altitudes = [alt for alt, az in curve_data]
        x_values = [self._datetime_to_plot_x(t) for t in self.viewmodel.time_points]

        if self.altitude_curve:
            self.plot_widget.removeItem(self.altitude_curve)

        pen = pg.mkPen(color='#3A86FF', width=2)
        self.altitude_curve = self.plot_widget.plot(
            x=x_values,
            y=altitudes,
            pen=pen,
            name="Altitude Curve"
        )

    def _draw_time_markers(self, start_time: datetime, end_time: Optional[datetime]):
        """Draw start and end time markers on the plot."""
        if self.start_marker:
            self.plot_widget.removeItem(self.start_marker)
        if self.end_marker:
            self.plot_widget.removeItem(self.end_marker)

        start_x = self._datetime_to_plot_x(start_time)
        pen_start = pg.mkPen('#6A4C93', width=1, style=pg.QtCore.Qt.PenStyle.DashLine)
        self.start_marker = pg.InfiniteLine(
            pos=start_x,
            angle=90,
            pen=pen_start,
            label="Start",
            labelOpts={'position': 0.9, 'color': '#6A4C93', 'fill': '#FFFFFF'}
        )
        self.plot_widget.addItem(self.start_marker)

        if end_time is None:
            return

        end_x = self._datetime_to_plot_x(end_time)
        pen_end = pg.mkPen('#FF6F61', width=1, style=pg.QtCore.Qt.PenStyle.DashLine)
        self.end_marker = pg.InfiniteLine(
            pos=end_x,
            angle=90,
            pen=pen_end,
            label="End",
            labelOpts={'position': 0.9, 'color': '#FF6F61', 'fill': '#FFFFFF'}
        )
        self.plot_widget.addItem(self.end_marker)
        
    def _draw_horizon_limits(self, min_alt: float, max_alt: float):
        """Draw horizontal lines for telescope horizon limits."""
        if self.min_limit_line:
            self.plot_widget.removeItem(self.min_limit_line)
        if self.max_limit_line:
            self.plot_widget.removeItem(self.max_limit_line)

        pen_min = pg.mkPen("#3A2909", width=1, style=pg.QtCore.Qt.PenStyle.DotLine)
        self.min_limit_line = pg.InfiniteLine(
            pos=min_alt,
            angle=0,
            pen=pen_min,
            label="Min Altitude",
            labelOpts={'position': 0.9, 'color': '#FFA500', 'fill': '#FFFFFF'}
        )
        self.plot_widget.addItem(self.min_limit_line)

        pen_max = pg.mkPen("#3F3109", width=1, style=pg.QtCore.Qt.PenStyle.DotLine)
        self.max_limit_line = pg.InfiniteLine(
            pos=max_alt,
            angle=0,
            pen=pen_max,
            label="Max Altitude",
            labelOpts={'position': 0.9, 'color': '#32CD32', 'fill': '#FFFFFF'}
        )
        self.plot_widget.addItem(self.max_limit_line)
    
    def _draw_twilight_zones(self) -> None:
        """Shade twilight zones on the plot."""
        for region in self.twilight_regions:
            self.plot_widget.removeItem(region)
        self.twilight_regions.clear()

        evening_start = self._datetime_to_plot_x(datetime.combine(self.viewmodel.services.get_observation_date() , time(12)))
        evening_end = self._datetime_to_plot_x(self.viewmodel.services.dates.astronomical_twilight_start)
        evening_region = pg.LinearRegionItem(
            values=(evening_start, evening_end),
            brush=pg.mkBrush(QColor(200, 200, 255, 50)),
            movable=False
        )
        self.plot_widget.addItem(evening_region)
        self.twilight_regions.append(evening_region)

        morning_start = self._datetime_to_plot_x(self.viewmodel.services.dates.astronomical_twilight_end)
        morning_end = self._datetime_to_plot_x(datetime.combine(self.viewmodel.services.get_observation_date() +timedelta(days=1), time(12)))
        morning_region = pg.LinearRegionItem(
            values=(morning_start, morning_end),
            brush=pg.mkBrush(QColor(200, 200, 255, 50)),
            movable=False
        )
        self.plot_widget.addItem(morning_region)
        self.twilight_regions.append(morning_region)

    def _highlight_observable_range(self, observable_segments: list[tuple[int, int]]) -> None:
        """Highlight the observable range on the plot."""
        # Clear existing regions
        for region in self.observable_regions:
            self.plot_widget.removeItem(region)
        self.observable_regions = []
        
        if not observable_segments or not self.viewmodel.target_curve:
            return
        
        min_alt = self.viewmodel.min_altitude
        max_alt = self.viewmodel.max_altitude
        
        if min_alt is None or max_alt is None:
            return
        
        start_time = self.viewmodel.services.dates.civil_twilight_start - timedelta(hours=1)
        end_time = self.viewmodel.services.dates.civil_twilight_end + timedelta(hours=1)
        
        timestamps = self.viewmodel._generate_time_points(start_time, end_time)
        altitudes = [alt for alt, az in self.viewmodel.target_curve]

        for seg_start_idx, seg_end_idx in observable_segments:
            segment_times = timestamps[seg_start_idx: seg_end_idx]
            segment_alts = altitudes[seg_start_idx: seg_end_idx]

            x_values = [self._datetime_to_plot_x(t) for t in segment_times]
            y_values = [min(alt, max_alt) for alt in segment_alts]

            fill_item = pg.PlotDataItem(
                x=x_values,
                y=y_values,
                pen=None,
                brush=pg.mkBrush(QColor(100, 255, 100, 100)),
                fillLevel=min_alt
            )

            self.plot_widget.addItem(fill_item)
            self.observable_regions.append(fill_item)

    def clear_plot(self) -> None:
        """Clear all plot items."""
        if self.altitude_moon_curve:
            self.plot_widget.removeItem(self.altitude_moon_curve)
            self.altitude_moon_curve = None
        if self.altitude_curve:
            self.plot_widget.removeItem(self.altitude_curve)
            self.altitude_curve = None
        if self.start_marker:
            self.plot_widget.removeItem(self.start_marker)
            self.start_marker = None
        if self.end_marker:
            self.plot_widget.removeItem(self.end_marker)
            self.end_marker = None
        if self.min_limit_line:
            self.plot_widget.removeItem(self.min_limit_line)
            self.min_limit_line = None
        if self.max_limit_line:
            self.plot_widget.removeItem(self.max_limit_line)
            self.max_limit_line = None
        for region in self.observable_regions:
            self.plot_widget.removeItem(region)
        self.observable_regions.clear()
        for region in self.twilight_regions:
            self.plot_widget.removeItem(region)
        self.twilight_regions.clear()

class AltitudeAxisItem(pg.AxisItem):
    """Custom axis item for displaying altitude labels."""
    def tickStrings(self, values, scale, spacing):
        strings = []
        for v in values:
            strings.append(f"{v:.0f}°")
        return strings
    
    def tickValues(self, minVal, maxVal, size):
        """Generate ticks at every 20 degrees."""
        ticks = []
        current = (minVal // 20) * 20
        if current < minVal:
            current += 20
        while current <= maxVal:
            ticks.append(current)
            current += 20
        return [(20, ticks)]

class TimeAxisItem(pg.AxisItem):
    """Custom axis item for displaying time labels."""
    def __init__(self, start_time: datetime, end_time: datetime, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = start_time
        self.end_time = end_time

    def tickStrings(self, values, scale, spacing):
        strings = []
        for v in values:
            dt = datetime.fromtimestamp(v)
            strings.append(dt.strftime("%H"))
        return strings

    def tickValues(self, minVal, maxVal, size):
        """Generate ticks at even hours only."""
        # Convert timestamps to datetime
        start_dt = datetime.fromtimestamp(minVal)
        end_dt = datetime.fromtimestamp(maxVal)
        
        # Round start to next even hour
        start_hour = start_dt.hour
        if start_hour % 2 != 0:
            start_hour += 1
        
        # Create first tick at even hour
        first_tick = start_dt.replace(hour=start_hour, minute=0, second=0, microsecond=0)
        if first_tick < start_dt:
            first_tick += timedelta(hours=2)
        
        # Generate ticks every 2 hours
        ticks = []
        current = first_tick
        
        while current <= end_dt:
            ticks.append(current.timestamp())
            current += timedelta(hours=2)
        
        return [(2 * 3600, ticks)]

class SkyWidget(QWidget):
    
    def __init__(self, viewmodel: ObserveGraphViewModel):
        super().__init__()
        self.viewmodel = viewmodel
        self.curve = []
        self.moon_curve = []
        self.minAlt = None
        self.maxAlt = None
        self.current_index = 0
        self._direction = 1

        self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Fixed)
        self.setFixedHeight(400)

        self.center = 200
        self.centerPointF = QPointF(self.center, self.center)
        
        self.star_icon = create_star_svg_renderer()
        self.moon_size = 30
        self.moon_pixmap = self._create_moon_pixmap(self.moon_size)

        # Stars
        self.stars: List[tuple[QPointF, float]] = []
        for _ in range(60):
            alt = (random.random() ** 2) * 90
            az = random.uniform(0, 359)
            radius = self.alt_to_radius(alt)
            center = self.az_radius_to_QPointF(az, radius)
            size = random.uniform(2, 8)
            self.stars.append((center, size))

        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self._advance_animation)
        self.animation_timer.setInterval(20)  # 1ms = 10fps

        self._background_cache = None
        self._background_needs_update = True

    def alt_to_radius(self, alt: float) -> float:
        return (1 - alt / 90.0) * (self.center * 0.9)
    
    def az_radius_to_QPointF(self, az: float, radius: float) -> QPointF:
        az = -az
        angle = math.radians(az)
        x = self.centerPointF.x() + radius * math.sin(angle)
        y = self.centerPointF.y() - radius * math.cos(angle)
        return QPointF(x, y)

    def _calculate_separation(self) -> Optional[float]:
        """Calculate angular separation between target and moon at current index."""
        if not self.curve or not self.moon_curve:
            return None
        
        if self.current_index >= len(self.curve) or self.current_index >= len(self.moon_curve):
            return None
        
        target_alt, target_az = self.curve[self.current_index]
        moon_alt, moon_az = self.moon_curve[self.current_index]
        
        # Only calculate if both are above horizon
        if target_alt < 0 or moon_alt < 0:
            return None
        
        # Create SkyCoord objects using alt-az coordinates
        target_coord = SkyCoord(alt=target_alt * u.deg, az=target_az * u.deg, frame='altaz')
        moon_coord = SkyCoord(alt=moon_alt * u.deg, az=moon_az * u.deg, frame='altaz')
        
        # Calculate separation
        separation = target_coord.separation(moon_coord)
        return separation.deg # type: ignore

    def setMinMaxAltitude(self, minAlt, maxAlt):
        self.minAlt = minAlt
        self.maxAlt = maxAlt
        self._background_needs_update = True
        self.update()

    def resizeEvent(self, event):
        self.center = min(self.width(), self.height()) / 2
        self.centerPointF = QPointF(self.width() / 2, self.height() / 2)
        self._background_needs_update = True
        super().resizeEvent(event)

    def setCurves(self, curve, moon_curve):
        self.curve = curve if curve else []
        self.moon_curve = moon_curve if moon_curve else []
        self.current_index = 0

        if self.curve or self.moon_curve:
            self.animation_timer.start()
        else:
            self.animation_timer.stop()

        self.update()

    def _advance_animation(self):
        """Move to next point in the curve."""
        if not self.curve and not self.moon_curve:
            self.animation_timer.stop()
            return
        max_len = max(len(self.curve), len(self.moon_curve))
        if max_len == 0:
            return

        self.current_index += self._direction

        # Reverse direction at ends
        if self.current_index >= max_len - 1:
            self.current_index = max_len - 1
            self._direction = -1
        elif self.current_index <= 0:
            self.current_index = 0
            self._direction = 1

        self.update()

    def _draw_static_background(self):
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        radius = self.alt_to_radius(0)

        grad = QRadialGradient(self.centerPointF, radius)
        grad.setColorAt(0.0, QColor("#101830"))
        grad.setColorAt(1.0, QColor("#000010"))

        painter.setBrush(QBrush(grad))
        painter.drawEllipse(self.centerPointF, radius, radius)
        
        if self.minAlt is not None and self.maxAlt is not None:
            minAltRadius = self.alt_to_radius(self.minAlt)
            maxAltRadius = self.alt_to_radius(self.maxAlt)

            painter.setPen(Qt.PenStyle.NoPen)

            painter.setBrush(QBrush(QColor(255, 0, 0, 255), Qt.BrushStyle.BDiagPattern))
            painter.drawEllipse(self.centerPointF, radius, radius)

            # Background gradient night sky
            painter.setBrush(QBrush(grad))
            painter.drawEllipse(self.centerPointF, minAltRadius, minAltRadius)

            painter.setBrush(QBrush(QColor(255, 0, 0, 255), Qt.BrushStyle.BDiagPattern))
            painter.drawEllipse(self.centerPointF, maxAltRadius, maxAltRadius)

            painter.setPen(QPen(QColor(255, 0, 0, 255), 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(self.centerPointF, minAltRadius, minAltRadius)
            painter.drawEllipse(self.centerPointF, maxAltRadius, maxAltRadius)
        
        for center, size in self.stars:
            half = size / 2
            rect = QRectF(center.x() - half, center.y() - half, size, size)
            self.star_icon.render(painter, rect)

        # Draw circles
        painter.setPen(QPen(Qt.GlobalColor.gray, 2))
        painter.setBrush(QBrush(QColor(255, 255, 255, 30)))
        painter.drawEllipse(self.centerPointF, radius, radius)
        painter.setPen(QPen(Qt.GlobalColor.gray, 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        _66altline = self.alt_to_radius(66)
        _33altline = self.alt_to_radius(33)
        painter.drawEllipse(self.centerPointF, _66altline, _66altline)
        painter.drawEllipse(self.centerPointF, _33altline, _33altline)
        painter.drawPoint(self.centerPointF)

        return pixmap
    
    def _create_moon_pixmap(self, size) -> QPixmap:
        pix = QPixmap(size, size)
        pix.fill(Qt.GlobalColor.transparent)
        p = QPainter(pix)
        create_moon_svg_renderer().render(p, QRectF(0, 0, size, size))
        return pix
    
    def _draw_pixmap_centered(self, painter: QPainter, center: QPointF, pixmap: QPixmap):
        half_w = pixmap.width() / 2
        half_h = pixmap.height() / 2
        painter.drawPixmap(QPointF(center.x() - half_w, center.y() - half_h), pixmap)

    def _get_timestamp(self) -> str:
        """Get the current timestamp as HH:MM string."""
        if not self.viewmodel.time_points or self.current_index >= len(self.viewmodel.time_points):
            return "00:00"
        
        current_time = self.viewmodel.time_points[self.current_index]
        return current_time.strftime("%H:%M")

    def _draw_timestamp_info(self, painter: QPainter):
        """Draw timestamp info in bottom-left corner."""
        timestamp = self._get_timestamp()

        # Position in bottom-left corner
        box_width = 80
        box_height = 50
        x = 10
        y = 10

        # Draw semi-transparent background box
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
        painter.drawRoundedRect(int(x), int(y), box_width, box_height, 6, 6)
        
        # Draw label text
        painter.setPen(QPen(QColor(200, 200, 200)))
        label_font = QFont("Arial", 9)
        painter.setFont(label_font)
        label_rect = QRectF(x, y + 8, box_width, 15)
        painter.drawText(label_rect, Qt.AlignmentFlag.AlignCenter, "Time")
        
        # Draw value text
        painter.setPen(QPen(QColor(255, 255, 255)))
        value_font = QFont("Arial", 12, QFont.Weight.Bold)
        painter.setFont(value_font)
        value_rect = QRectF(x, y + 25, box_width, 20)
        painter.drawText(value_rect, Qt.AlignmentFlag.AlignCenter, timestamp)

    def paintEvent(self, event):
        if self._background_needs_update or self._background_cache is None:
            self._background_cache = self._draw_static_background()
            self._background_needs_update = False

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawPixmap(0, 0, self._background_cache)
        
        if self.curve and self.current_index < len(self.curve):
            alt, az = self.curve[self.current_index]
            if alt >= 0:
                radius = self.alt_to_radius(alt)
                center = self.az_radius_to_QPointF(az, radius)
                
                # Use target color from ViewModel
                target_color = QColor(self.viewmodel.TARGET_CURVE_COLOR)
                
                grad = QRadialGradient(center, 6)
                grad.setColorAt(0.0, target_color.lighter(180))
                grad.setColorAt(0.5, target_color)
                grad.setColorAt(1.0, QColor(target_color.red(), target_color.green(), target_color.blue(), 0))
                
                painter.setBrush(QBrush(grad))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(center, 6, 6)

        if self.moon_curve and self.current_index < len(self.moon_curve):
            alt, az = self.moon_curve[self.current_index]
            if alt >= 0:
                radius = self.alt_to_radius(alt)
                center = self.az_radius_to_QPointF(az, radius)
                self._draw_pixmap_centered(painter, center, self.moon_pixmap)
        
        # Draw only timestamp info (separation removed)
        self._draw_timestamp_info(painter)
   
    def hideEvent(self, event):
        """Stop animation when widget is hidden."""
        self.animation_timer.stop()
        super().hideEvent(event)
    
    def showEvent(self, event):
        """Resume animation when widget is shown."""
        if self.curve:
            self.animation_timer.start()
        super().showEvent(event)

class LegendWidget(QWidget):
    """Simple legend widget to display curve labels and colors."""
    
    def __init__(self):
        super().__init__()
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(10, 5, 10, 5)
        self.main_layout.setSpacing(20)
        self.main_layout.addStretch()
        self.setLayout(self.main_layout)
        
        self.legend_items = []
    
    def update_legend(self, items: list[dict]):
        """Update legend with new items."""
        # Clear existing items
        for item_widget in self.legend_items:
            self.main_layout.removeWidget(item_widget)
            item_widget.deleteLater()
        self.legend_items.clear()
        
        # Create new items
        for item in items:
            # Check if item has a color (curve item) or not (text-only item)
            if item.get('color'):
                item_widget = self._create_legend_item(item['label'], item['color'])
            else:
                item_widget = self._create_text_only_item(item['label'])
            
            self.main_layout.insertWidget(self.main_layout.count() - 1, item_widget)
            self.legend_items.append(item_widget)
    
    def _create_legend_item(self, label: str, color: str) -> QWidget:
        """Create a single legend item with color box and label."""
        container = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Color box
        color_box = QLabel()
        color_box.setFixedSize(16, 16)
        color_box.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                border: 1px solid #888;
                border-radius: 2px;
            }}
        """)
        
        # Label
        text_label = QLabel(label)
        text_label.setStyleSheet("QLabel { color: #333; }")
        
        layout.addWidget(color_box)
        layout.addWidget(text_label)
        container.setLayout(layout)
        
        return container
    
    def _create_text_only_item(self, label: str) -> QWidget:
        """Create a text-only legend item (no color box)."""
        text_label = QLabel(label)
        text_label.setStyleSheet("QLabel { color: #666; font-style: italic; }")
        return text_label


