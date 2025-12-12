#!/usr/bin/env python3
"""
Color Notify - Clipboard Color Notification Tool
Displays notifications when color codes are detected in clipboard
"""

import sys
import os
import re
import configparser
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QSystemTrayIcon, 
                             QMenu, QAction)
from PyQt5.QtCore import QTimer, Qt, QPoint, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from version_get import VersionGet

__version__ = VersionGet().get(True)
__author__ = "Hadi Cahyadi"
__email__ = "cumulus13@gmail.com"

class ColorNotification(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
        
    def init_ui(self):
        # Window flags - frameless, AOT, no taskbar
        flags = Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint
        if not self.config.get('always_on_top', True):
            flags = Qt.FramelessWindowHint | Qt.Tool
        self.setWindowFlags(flags)
        
        # Transparency
        opacity = self.config.get('opacity', 0.95)
        self.setWindowOpacity(opacity)
        
        # Size
        self.setFixedSize(320, 140)
        
        # Layout
        self.title_label = QLabel(self)
        self.title_label.setGeometry(15, 15, 290, 35)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 15px;")
        
        self.body_label = QLabel(self)
        self.body_label.setGeometry(15, 55, 290, 70)
        self.body_label.setAlignment(Qt.AlignCenter)
        self.body_label.setStyleSheet("font-size: 12px;")
        
        # Shadow effect (simulated with border)
        self.setStyleSheet("border-radius: 12px;")
        
    def show_notification(self, color_code, color_type="HEX"):
        """Display notification with color background"""
        # Parse color
        rgb = self.hex_to_rgb(color_code)
        if not rgb:
            return
            
        # Calculate text color (light or dark)
        luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255
        text_color = "#000000" if luminance > 0.5 else "#FFFFFF"
        
        # Set background color
        bg_color = f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"
        border_color = f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.5)"
        self.setStyleSheet(
            f"background-color: {bg_color}; "
            f"border-radius: 12px; "
            f"border: 2px solid {border_color};"
        )
        
        # Set text
        self.title_label.setText(f"🎨 {color_type}: {color_code.upper()}")
        self.title_label.setStyleSheet(
            f"color: {text_color}; font-weight: bold; font-size: 15px; background: transparent; border: none;"
        )
        
        rgb_text = f"RGB: {rgb[0]}, {rgb[1]}, {rgb[2]}"
        brightness = "LIGHT" if luminance > 0.5 else "DARK"
        lum_bar = "█" * int(luminance * 20)
        self.body_label.setText(
            f"{rgb_text}\n{brightness} • Luminance: {luminance:.2f}\n{lum_bar}"
        )
        self.body_label.setStyleSheet(
            f"color: {text_color}; font-size: 11px; background: transparent; border: none;"
        )
        
        # Position
        self.position_window()
        
        # Show with animation
        self.show()
        self.fade_in()
        
        # Auto hide after timeout
        timeout = self.config.get('timeout', 3000)
        if timeout > 0:  # 0 = no auto-hide
            QTimer.singleShot(timeout, self.fade_out)
        
    def hex_to_rgb(self, hex_color):
        """Convert HEX to RGB"""
        if not hex_color:
            return None
        if hex_color.startswith('#'):
            hex_color = hex_color[1:]
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        try:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        except:
            return None
            
    def position_window(self):
        """Position window based on config"""
        screen = QApplication.desktop().screenGeometry()
        position = self.config.get('position', 'right_center')
        margin = self.config.get('margin', 20)
        
        w, h = self.width(), self.height()
        
        # Horizontal position
        if position.startswith('left'):
            x = margin
        elif position.startswith('right'):
            x = screen.width() - w - margin
        else:  # center
            x = (screen.width() - w) // 2
            
        # Vertical position
        if position.endswith('up'):
            y = margin
        elif position.endswith('down'):
            y = screen.height() - h - margin
        else:  # center
            y = (screen.height() - h) // 2
            
        self.move(x, y)
        
    def fade_in(self):
        """Fade in animation"""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0)
        self.animation.setEndValue(self.config.get('opacity', 0.95))
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()
        
    def fade_out(self):
        """Fade out animation"""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.config.get('opacity', 0.95))
        self.animation.setEndValue(0)
        self.animation.setEasingCurve(QEasingCurve.InCubic)
        self.animation.finished.connect(self.hide)
        self.animation.start()
        
    def mousePressEvent(self, event):
        """Close notification on click"""
        self.fade_out()


class ColorNotifyApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setQuitOnLastWindowClosed(False)
        self.config = self.load_config()
        self.last_clipboard = ""
        
        # Create notification widget
        self.notification = ColorNotification(self.config)
        
        # Create system tray
        self.create_tray()
        
        # Start clipboard monitoring
        self.clipboard_obj = self.clipboard()
        self.clipboard_obj.dataChanged.connect(self.on_clipboard_change)
        
        # Timer for polling (backup) - reduced frequency to avoid conflicts
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_clipboard)
        poll_interval = self.config.get('poll_interval', 1000)  # Increased default to 1000ms
        self.timer.start(poll_interval)
        
        # Error counter for clipboard access
        self.clipboard_error_count = 0
        self.max_clipboard_errors = 3
        
    def load_config(self):
        """Load configuration from INI file"""
        config_file = Path.home() / ".color-notify.ini"
        
        # Fallback to local config
        if not config_file.exists():
            config_file = Path("color-notify.ini")
        
        config = {
            'position': 'right_center',
            'opacity': 0.95,
            'always_on_top': True,
            'timeout': 3000,
            'margin': 20,
            'detect_hex': True,
            'detect_rgb': True,
            'detect_hsl': False,
            'poll_interval': 1000,  # Increased default for stability
            'sound_enabled': False,
        }
        
        if config_file.exists():
            parser = configparser.ConfigParser()
            parser.read(config_file)
            
            if 'notification' in parser:
                sect = parser['notification']
                config['position'] = sect.get('position', 'right_center')
                config['opacity'] = float(sect.get('opacity', '0.95'))
                config['always_on_top'] = sect.getboolean('always_on_top', True)
                config['timeout'] = int(sect.get('timeout', '3000'))
                config['margin'] = int(sect.get('margin', '20'))
                config['sound_enabled'] = sect.getboolean('sound_enabled', False)
                
            if 'detection' in parser:
                sect = parser['detection']
                config['detect_hex'] = sect.getboolean('detect_hex', True)
                config['detect_rgb'] = sect.getboolean('detect_rgb', True)
                config['detect_hsl'] = sect.getboolean('detect_hsl', False)
                config['poll_interval'] = int(sect.get('poll_interval', '500'))
        else:
            self.create_default_config(config_file)
            
        return config
        
    def create_default_config(self, config_file):
        """Create default config file"""
        config = configparser.ConfigParser()
        
        config['notification'] = {
            'position': 'right_center',
            'opacity': '0.95',
            'always_on_top': 'True',
            'timeout': '3000',
            'margin': '20',
            'sound_enabled': 'False',
        }
        
        config['detection'] = {
            'detect_hex': 'True',
            'detect_rgb': 'True',
            'detect_hsl': 'False',
            'poll_interval': '1000',
        }
        
        try:
            with open(config_file, 'w') as f:
                f.write("# Color Notify Configuration\n")
                f.write("# Position: left_up, left_center, left_down, center_up, center_center, center_down, right_up, right_center, right_down\n")
                f.write("# Timeout: milliseconds (0 = no auto-hide)\n\n")
                config.write(f)
        except Exception as e:
            print(f"Warning: Could not create config file: {e}")
            
    def create_tray(self):
        """Create system tray icon"""
        # Create icon
        # pixmap = QPixmap(64, 64)
        # pixmap.fill(Qt.transparent)
        # pixmap = QPixmap(str(Path(__file__).parent / "ICONS" / "color-notify_64.ico")).scaled(
        #     64, 64,
        #     Qt.KeepAspectRatio,
        #     Qt.SmoothTransformation
        # )

        # painter = QPainter(pixmap)
        
        # # Gradient effect
        # painter.setBrush(QColor(100, 150, 255))
        # painter.setPen(Qt.NoPen)
        # painter.drawEllipse(8, 8, 48, 48)
        
        # # Inner circle
        # painter.setBrush(QColor(255, 255, 255, 100))
        # painter.drawEllipse(16, 16, 32, 32)
        
        # painter.end()
        
        # icon = QIcon(pixmap)

        ico_path = str(Path(__file__).parent / "icons" / "color-notify_128.ico")
        # print(f"ico_path is file: {os.path.isfile(ico_path)}")
        icon = QIcon(ico_path)
        # pix = QPixmap(ico_path)
        # print("Pixmap OK:", not pix.isNull(), pix.size())

        # base_icon = QPixmap(ico_path)

        # pixmap = QPixmap(64, 64)
        # pixmap.fill(Qt.transparent)

        # painter = QPainter(pixmap)

        # # gambar icon dari file dulu
        # painter.drawPixmap(0, 0, base_icon.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # # lalu efekmu
        # painter.setBrush(QColor(100, 150, 255))
        # painter.setPen(Qt.NoPen)
        # painter.drawEllipse(8, 8, 48, 48)

        # painter.setBrush(QColor(255, 255, 255, 100))
        # painter.drawEllipse(16, 16, 32, 32)

        # painter.end()

        # icon = QIcon(pixmap)
        
        # Create tray
        self.tray = QSystemTrayIcon(icon, self)
        self.tray.setToolTip("Color Notify - Monitoring clipboard")
        
        # Create menu
        menu = QMenu()
        
        # Test notification action
        test_action = QAction("🧪 Test Notification", self)
        test_action.triggered.connect(self.test_notification)
        menu.addAction(test_action)
        
        menu.addSeparator()
        
        # Toggle monitoring
        self.toggle_action = QAction("⏸️ Pause Monitoring", self)
        self.toggle_action.triggered.connect(self.toggle_monitoring)
        self.monitoring_enabled = True
        menu.addAction(self.toggle_action)
        
        menu.addSeparator()
        
        # Reload config action
        reload_action = QAction("🔄 Reload Config", self)
        reload_action.triggered.connect(self.reload_config)
        menu.addAction(reload_action)
        
        # Open config action
        config_action = QAction("⚙️ Open Config File", self)
        config_action.triggered.connect(self.open_config)
        menu.addAction(config_action)
        
        menu.addSeparator()
        
        # About action
        about_action = QAction("ℹ️ About", self)
        about_action.triggered.connect(self.show_about)
        menu.addAction(about_action)
        
        # Exit action
        exit_action = QAction("❌ Exit", self)
        exit_action.triggered.connect(self.quit)
        menu.addAction(exit_action)
        
        self.tray.setContextMenu(menu)
        self.tray.show()
        
    def toggle_monitoring(self):
        """Toggle clipboard monitoring"""
        self.monitoring_enabled = not self.monitoring_enabled
        if self.monitoring_enabled:
            self.toggle_action.setText("⏸️ Pause Monitoring")
            self.tray.setToolTip("Color Notify - Monitoring clipboard")
            self.tray.showMessage("Color Notify", "Monitoring resumed", 
                                 QSystemTrayIcon.Information, 1500)
        else:
            self.toggle_action.setText("▶️ Resume Monitoring")
            self.tray.setToolTip("Color Notify - Paused")
            self.tray.showMessage("Color Notify", "Monitoring paused", 
                                 QSystemTrayIcon.Information, 1500)
        
    def test_notification(self):
        """Test notification with sample colors"""
        import random
        colors = ["#FF5733", "#33FF57", "#3357FF", "#F0A500", "#9B59B6", "#E74C3C"]
        color = random.choice(colors)
        self.notification.show_notification(color, "HEX")
        
    def reload_config(self):
        """Reload configuration"""
        self.config = self.load_config()
        self.notification.config = self.config
        self.tray.showMessage("Color Notify", "Configuration reloaded ✓", 
                             QSystemTrayIcon.Information, 2000)
        
    def open_config(self):
        """Open config file"""
        config_file = Path.home() / ".color-notify.ini"
        if not config_file.exists():
            config_file = Path("color-notify.ini")
        
        import subprocess
        import platform
        
        try:
            if platform.system() == 'Windows':
                subprocess.run(['notepad', str(config_file)])
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', str(config_file)])
            else:  # Linux
                subprocess.run(['xdg-open', str(config_file)])
        except Exception as e:
            self.tray.showMessage("Error", f"Could not open config: {e}", 
                                 QSystemTrayIcon.Warning, 3000)
        
    def show_about(self):
        """Show about dialog"""
        self.tray.showMessage(
            "Color Notify", 
            f"Version {__version__}\n"
            f"By {__author__}\n\n"
            "Clipboard color detection tool\n"
            "Copy a color code to see notification!\n\n"
            "https://github.com/cumulus13/color-notify",
            QSystemTrayIcon.Information, 
            5000
        )
        
    def on_clipboard_change(self):
        """Handle clipboard change event"""
        if self.monitoring_enabled:
            self.check_clipboard()
        
    def check_clipboard(self):
        """Check clipboard for color codes"""
        if not self.monitoring_enabled:
            return
            
        try:
            # Try to access clipboard with timeout handling
            text = ""
            try:
                text = self.clipboard_obj.text()
                self.clipboard_error_count = 0  # Reset error count on success
            except RuntimeError as e:
                # Clipboard access error - ignore silently
                self.clipboard_error_count += 1
                if self.clipboard_error_count >= self.max_clipboard_errors:
                    # Increase polling interval if persistent errors
                    current_interval = self.timer.interval()
                    if current_interval < 3000:
                        new_interval = min(current_interval * 2, 3000)
                        self.timer.setInterval(new_interval)
                        print(f"Clipboard access issues, reducing polling to {new_interval}ms")
                    self.clipboard_error_count = 0
                return
            
            if not text or text == self.last_clipboard:
                return
                
            self.last_clipboard = text
            
            # Detect HEX color
            if self.config.get('detect_hex', True):
                hex_match = re.search(r'#[0-9A-Fa-f]{3,6}\b', text)
                if hex_match:
                    color_code = hex_match.group()
                    self.notification.show_notification(color_code, "HEX")
                    return
                    
            # Detect RGB color
            if self.config.get('detect_rgb', True):
                rgb_match = re.search(r'rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', text, re.IGNORECASE)
                if rgb_match:
                    r, g, b = rgb_match.groups()
                    if all(0 <= int(v) <= 255 for v in [r, g, b]):
                        hex_color = f"#{int(r):02x}{int(g):02x}{int(b):02x}"
                        self.notification.show_notification(hex_color, "RGB")
                        return
                    
        except Exception as e:
            # Silently ignore other clipboard errors
            pass


def main():
    """Main entry point"""
    app = ColorNotifyApp(sys.argv)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()