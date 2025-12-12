from dataclasses import dataclass, field
from PyQt6.QtGui import QColor


@dataclass
class TaskRectUIConfig:
    """UI configuration for TaskRectItem visual styling."""
    
    # Normal state colors
    normal_border: QColor = field(default_factory=lambda: QColor("#90a4ae"))
    normal_fill: QColor = field(default_factory=lambda: QColor("#ffffff"))
    normal_border_width: int = 1
    
    # Hover state colors
    hover_border: QColor = field(default_factory=lambda: QColor("#2196f3"))
    hover_fill: QColor = field(default_factory=lambda: QColor("#e3f2fd"))
    hover_border_width: int = 2
    
    # Copied state colors
    copied_border: QColor = field(default_factory=lambda: QColor("#ffc107"))
    copied_fill: QColor = field(default_factory=lambda: QColor("#fff9e6"))
    copied_border_width: int = 2
    
    # Editing state colors
    editing_border: QColor = field(default_factory=lambda: QColor("#180808"))
    editing_fill: QColor = field(default_factory=lambda: QColor("#675E5E"))
    editing_border_width: int = 5
    
    # Error state colors (zero duration)
    error_border: QColor = field(default_factory=lambda: QColor("#dc3545"))
    error_border_width: int = 3
    
    # Text styling
    font_size: int = 9
    font_bold: bool = True
    text_color: QColor = field(default_factory=lambda: QColor("#212529"))
    
    # Layout
    corner_radius: int = 6
    shadow_blur_radius: int = 8
    shadow_x_offset: int = 0
    shadow_y_offset: int = 2
    shadow_color: QColor = field(default_factory=lambda: QColor(0, 0, 0, 40))
    
    # Visibility thresholds
    min_visible_width: int = 10
    min_visible_height: int = 10
