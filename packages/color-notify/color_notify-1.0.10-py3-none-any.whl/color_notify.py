#!/usr/bin/env python3
# File: color_notify.py
# Author: Hadi Cahyadi <cumulus13@gmail.com>
# Date: 2025-12-06
# Description: Color Notify - Clipboard Color Notification Tool. Displays notifications when color codes are detected in clipboard
# License: MIT

"""
Color Notify - Clipboard Color Notification Tool
Displays notifications when color codes are detected in clipboard
"""
import sys
import os
import re
HAS_RICH = False
HAS_MAKE_COLORS = False

try:
    from rich.console import Console
    console = Console()
    HAS_RICH=True
except:
    pass

try:
    from make_colors import Console
    console = Console()
    HAS_MAKE_COLORS=True
except:
    class console:
        @classmethod
        def print(cls, *args, **kwargs):
            return print(*args, **kwargs)

import configparser
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QSystemTrayIcon, 
                             QMenu, QAction, QColorDialog, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLineEdit, QMessageBox)
from PyQt5.QtCore import QTimer, Qt, QPoint, QPropertyAnimation, QEasingCurve, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont

# Global hotkey support
try:
    from pynput import keyboard
    GLOBAL_HOTKEY_AVAILABLE = True
except ImportError:
    GLOBAL_HOTKEY_AVAILABLE = False
    print("Warning: pynput not installed. Global hotkey disabled.")
    print("Install with: pip install pynput")

try:
    from version_get import VersionGet
    __version__ = VersionGet().get(True)
except:
    __version__ = "1.0.2"

__author__ = "Hadi Cahyadi"
__email__ = "cumulus13@gmail.com"


class GlobalHotkeyHandler(QObject):
    """Handle global hotkeys using pynput"""
    hotkey_pressed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.listener = None
        self.hotkey = None
        
    def start(self):
        """Start listening for global hotkeys"""
        if not GLOBAL_HOTKEY_AVAILABLE:
            return False
            
        try:
            # Define the hotkey combination: Ctrl+Alt+Shift+C
            self.hotkey = keyboard.HotKey(
                keyboard.HotKey.parse('<ctrl>+<alt>+<shift>+c'),
                self.on_activate
            )
            
            # Start the listener
            self.listener = keyboard.Listener(
                on_press=self.for_canonical(self.hotkey.press),
                on_release=self.for_canonical(self.hotkey.release)
            )
            self.listener.start()
            print("Global hotkey registered: Ctrl+Alt+Shift+C")
            return True
            
        except Exception as e:
            print(f"Failed to register global hotkey: {e}")
            return False
    
    def for_canonical(self, f):
        """Helper for pynput canonical key handling"""
        return lambda k: f(self.listener.canonical(k))
    
    def on_activate(self):
        """Called when hotkey is pressed"""
        self.hotkey_pressed.emit()
    
    def stop(self):
        """Stop the listener"""
        if self.listener:
            try:
                self.listener.stop()
            except:
                pass


class ColorPickerDialog(QWidget):
    """Color Picker Dialog Window"""
    def __init__(self, config=None):
        super().__init__()
        self.config = config or {}
        self.init_ui()
        self.clipboard_timer = QTimer(self)
        self.clipboard_timer.timeout.connect(self.check_clipboard)
        self.clipboard_timer.start(1000)  # Check clipboard every second

    def init_ui(self):
        self.setWindowTitle('Color Picker')
        
        # Try to load icon
        ico_path = str(Path(__file__).parent / "icons" / "color-notify_128.ico")
        if os.path.isfile(ico_path):
            self.setWindowIcon(QIcon(ico_path))
        
        self.setFixedSize(300, 300)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        
        # Center the window
        self.center()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        self.setLayout(main_layout)

        # Add stretch at top
        main_layout.addStretch(1)

        # Color Preview
        self.color_widget = QLabel(self)
        self.color_widget.setStyleSheet("background-color: black; border: 1px solid #ccc; border-radius: 5px;")
        self.color_widget.setFixedSize(120, 80)
        main_layout.addWidget(self.color_widget, alignment=Qt.AlignCenter)

        # Color Name Label
        color_layout = QHBoxLayout()
        color_layout.addStretch(1)
        
        color_name_label = QLabel("Color name:", self)
        color_layout.addWidget(color_name_label)

        self.color_name_display = QLabel("BLACK", self)
        self.color_name_display.setFont(QFont("Arial", 10, QFont.Bold))
        color_layout.addWidget(self.color_name_display)
        
        color_layout.addStretch(1)
        main_layout.addLayout(color_layout)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        choose_button = QPushButton('Choose Color', self)
        choose_button.clicked.connect(self.show_color_dialog)
        choose_button.setMinimumHeight(30)
        button_layout.addWidget(choose_button)

        set_button = QPushButton('Set Color', self)
        set_button.clicked.connect(self.set_color_from_input)
        set_button.setMinimumHeight(30)
        button_layout.addWidget(set_button)
        
        main_layout.addLayout(button_layout)

        # Hex Input
        hex_layout = QHBoxLayout()
        hex_layout.addStretch(1)
        
        self.hex_input = QLineEdit(self)
        self.hex_input.setText("#000000")
        self.hex_input.setMaximumWidth(150)
        self.hex_input.setMinimumHeight(25)
        self.hex_input.setAlignment(Qt.AlignCenter)
        self.hex_input.returnPressed.connect(self.set_color_from_input)
        hex_layout.addWidget(self.hex_input)
        
        hex_layout.addStretch(1)
        main_layout.addLayout(hex_layout)

        # Add stretch at bottom
        main_layout.addStretch(1)

    def show_color_dialog(self):
        """Show Qt color picker dialog positioned next to main dialog"""
        # Create color dialog
        color_dialog = QColorDialog(self)
        
        # Get current position and size
        main_pos = self.pos()
        main_width = self.width()
        main_height = self.height()
        
        # Get screen geometry
        screen = QApplication.screenAt(main_pos)
        if screen is None:
            screen = QApplication.primaryScreen()
        screen_geom = screen.availableGeometry()
        
        # Get preferred position from config (default: right)
        preferred_position = self.config.get('color_dialog_position', 'right')
        
        # Calculate position for color dialog
        dialog_width = 480  # Approximate QColorDialog width
        dialog_height = 420  # Approximate QColorDialog height
        gap = 10  # Gap between dialogs
        
        if preferred_position == 'left':
            # Try left first
            left_x = main_pos.x() - dialog_width - gap
            if left_x >= screen_geom.left():
                color_dialog.move(left_x, main_pos.y())
            else:
                # Fallback to right
                right_x = main_pos.x() + main_width + gap
                color_dialog.move(right_x, main_pos.y())
                
        elif preferred_position == 'top':
            # Position above
            top_y = main_pos.y() - dialog_height - gap
            if top_y >= screen_geom.top():
                color_dialog.move(main_pos.x(), top_y)
            else:
                # Fallback to bottom
                bottom_y = main_pos.y() + main_height + gap
                color_dialog.move(main_pos.x(), bottom_y)
                
        elif preferred_position == 'bottom':
            # Position below
            bottom_y = main_pos.y() + main_height + gap
            if bottom_y + dialog_height <= screen_geom.bottom():
                color_dialog.move(main_pos.x(), bottom_y)
            else:
                # Fallback to top
                top_y = main_pos.y() - dialog_height - gap
                color_dialog.move(main_pos.x(), top_y)
                
        else:  # default: 'right'
            # Try right first
            right_x = main_pos.x() + main_width + gap
            if right_x + dialog_width <= screen_geom.right():
                color_dialog.move(right_x, main_pos.y())
            else:
                # Fallback to left
                left_x = main_pos.x() - dialog_width - gap
                if left_x >= screen_geom.left():
                    color_dialog.move(left_x, main_pos.y())
                else:
                    # If neither fits, center it
                    center_x = screen_geom.center().x() - dialog_width // 2
                    color_dialog.move(center_x, main_pos.y())
        
        # Show dialog and get result
        if color_dialog.exec_() == QColorDialog.Accepted:
            color = color_dialog.currentColor()
            if color.isValid():
                self.set_color(color)

    def set_color_from_input(self):
        """Set color from hex input"""
        hex_text = self.hex_input.text().strip()
        try:
            color = QColor(hex_text)
            if color.isValid():
                self.set_color(color)
            else:
                QMessageBox.warning(self, "Invalid Color", "Please enter a valid hex color code.")
        except Exception as e:
            QMessageBox.warning(self, "Invalid Color", f"Error: {e}")

    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        if event.key() == Qt.Key_Q or event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_A and event.modifiers() & Qt.ShiftModifier:
            # Shift+A: Disable always on top
            self.setWindowFlags(Qt.Window)
            self.show()
            self.center_on_current_screen()
        elif event.key() == Qt.Key_A:
            # A: Enable always on top
            self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
            self.show()
            self.center_on_current_screen()

    def set_color(self, color):
        """Set the color and copy to clipboard"""
        self.color_widget.setStyleSheet(
            f"background-color: {color.name()}; border: 1px solid #ccc; border-radius: 5px;"
        )
        self.color_name_display.setText(color.name().upper())
        self.hex_input.setText(color.name().upper())
        
        # Copy to clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(color.name().upper())

    def center(self):
        """Center window on primary screen"""
        screen = QApplication.primaryScreen()
        if screen:
            geometry = screen.availableGeometry()
            self.move(
                geometry.x() + (geometry.width() - self.width()) // 2,
                geometry.y() + (geometry.height() - self.height()) // 2
            )

    def center_on_current_screen(self):
        """Center window on current screen"""
        window_center = self.geometry().center()
        screen = QApplication.screenAt(window_center)
        
        if screen is None:
            screen = QApplication.screenAt(self.pos())
        
        if screen is None:
            screen = QApplication.primaryScreen()
        
        if screen:
            geometry = screen.availableGeometry()
            self.move(
                geometry.x() + (geometry.width() - self.width()) // 2,
                geometry.y() + (geometry.height() - self.height()) // 2
            )

    def check_clipboard(self):
        """Check clipboard for color codes"""
        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text()
        
        if clipboard_text.startswith('#'):
            try:
                color = QColor(clipboard_text)
                if color.isValid():
                    self.set_color(color)
            except:
                pass


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
        
        # Create color picker dialog (but don't show yet)
        self.color_picker = None
        
        # Create system tray
        self.create_tray()
        
        # Setup global hotkey
        self.setup_global_hotkey()
        
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
    
    def setup_global_hotkey(self):
        """Setup global keyboard shortcut"""
        if GLOBAL_HOTKEY_AVAILABLE:
            self.hotkey_handler = GlobalHotkeyHandler()
            self.hotkey_handler.hotkey_pressed.connect(self.show_color_picker)
            success = self.hotkey_handler.start()
            if not success:
                print("Warning: Global hotkey registration failed")
        else:
            self.hotkey_handler = None
            print("Info: Global hotkey not available. Use tray menu to access Color Picker.")

    def candidate_config_file(self):
        """
        Generates a list of cross-platform color-notify.ini path candidates
        """
        return [
            Path.home() / ".color-notify.ini",
            os.path.join(os.getcwd(), 'color-notify.ini'),        
            os.path.join(os.getcwd(), '.color_notify', 'color-notify.ini'),        
            os.path.expanduser("~/color-notify.ini"),
            os.path.expanduser("~/.color_notify/color-notify.ini"),
            os.path.expanduser("$HOME/color-notify.ini"),
            os.path.expanduser("$HOME/.color_notify/color-notify.ini"),
            "/etc/color-notify.ini",
            "/etc/color_notify/color-notify.ini",
            os.path.expandvars("%USERPROFILE%\\color-notify.ini"),
            os.path.expandvars("%USERPROFILE%\\.color_notify\\color-notify.ini"),
            os.path.expandvars("%APPDATA%\\color_notify\\color-notify.ini"),
            os.path.expandvars("%PROGRAMDATA%\\color_notify\\color-notify.ini"),
            str(Path(__file__).parent / "color-notify.ini"),
            str(Path(__file__).parent / ".color_notify" / "color-notify.ini")
        ]
        
    def load_config(self):
        """Load configuration from INI file"""
        config_file = None
        
        for cfile in self.candidate_config_file():
            if os.path.isfile(cfile):
                config_file = cfile
                break    
        
        # Fallback to create new config
        if not config_file or not Path(config_file).exists():
            if sys.platform == 'win32':
                config_dir = os.path.expandvars("%USERPROFILE%\\.color_notify")
                os.makedirs(config_dir, exist_ok=True)
                config_file = os.path.expandvars("%USERPROFILE%\\.color_notify\\color-notify.ini")
            else:
                try:
                    config_dir = os.path.expanduser("~/.color_notify")
                    os.makedirs(config_dir, exist_ok=True)
                    config_file = os.path.expanduser("~/.color_notify/color-notify.ini")
                except:
                    config_file = "/etc/color-notify.ini"
            
            if config_file and not os.path.isfile(config_file):
                self.create_default_config(config_file)
                print(f"Created config file: {config_file}")
            else:
                if HAS_RICH or HAS_MAKE_COLORS:
                    console.print(f"[bold #FFFF00]Using config file:[/] [bold #00FFFF]{config_file}[/]")
                else:
                    print(f"Using config file: {config_file}")
        else:
            if HAS_RICH or HAS_MAKE_COLORS:
                console.print(f"[bold #FFFF00]Using config file:[/] [bold #00FFFF]{config_file}[/]")
            else:
                print(f"Using config file: {config_file}")
            
        config = {
            'position': 'right_center',
            'opacity': 0.95,
            'always_on_top': True,
            'timeout': 3000,
            'margin': 20,
            'detect_hex': True,
            'detect_rgb': True,
            'detect_hsl': False,
            'poll_interval': 1000,
            'sound_enabled': False,
            'color_dialog_position': 'right',  # Position of Qt Color Dialog: left, right, top, bottom
        }
        
        if config_file and Path(config_file).exists():
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
                
            if 'color_picker' in parser:
                sect = parser['color_picker']
                config['color_dialog_position'] = sect.get('color_dialog_position', 'right')
                
            if 'detection' in parser:
                sect = parser['detection']
                config['detect_hex'] = sect.getboolean('detect_hex', True)
                config['detect_rgb'] = sect.getboolean('detect_rgb', True)
                config['detect_hsl'] = sect.getboolean('detect_hsl', False)
                config['poll_interval'] = int(sect.get('poll_interval', '1000'))
            
        return config
        
    def create_default_config(self, config_file):
        """Create default config file"""
        print(f"Creating config file: {config_file}")
        config = configparser.ConfigParser()
        
        config['notification'] = {
            'position': 'right_center',
            'opacity': '0.95',
            'always_on_top': 'True',
            'timeout': '3000',
            'margin': '20',
            'sound_enabled': 'False',
        }
        
        config['color_picker'] = {
            'color_dialog_position': 'right',
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
                f.write("# Timeout: milliseconds (0 = no auto-hide)\n")
                f.write("# Color Dialog Position: left, right, top, bottom (position of Qt Color Dialog relative to Color Picker)\n\n")
                config.write(f)
        except Exception as e:
            print(f"Warning: Could not create config file: {e}")
            
    def create_tray(self):
        """Create system tray icon"""
        ico_path = str(Path(__file__).parent / "icons" / "color-notify_128.ico")
        
        if os.path.isfile(ico_path):
            icon = QIcon(ico_path)
        else:
            pixmap = QPixmap(64, 64)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            
            # Gradient effect
            painter.setBrush(QColor(100, 150, 255))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(8, 8, 48, 48)
            
            # Inner circle
            painter.setBrush(QColor(255, 255, 255, 100))
            painter.drawEllipse(16, 16, 32, 32)
            
            painter.end()
            
            icon = QIcon(pixmap)
        
        # Create tray
        self.tray = QSystemTrayIcon(icon, self)
        self.tray.setToolTip("Color Notify - Monitoring clipboard")
        
        # Create menu
        menu = QMenu()
        
        # Color Picker Dialog action
        if GLOBAL_HOTKEY_AVAILABLE:
            picker_action = QAction("🎨 Color Picker (Ctrl+Alt+Shift+C)", self)
        else:
            picker_action = QAction("🎨 Color Picker", self)
        picker_action.triggered.connect(self.show_color_picker)
        menu.addAction(picker_action)
        
        menu.addSeparator()
        
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
    
    def show_color_picker(self):
        """Show color picker dialog"""
        if self.color_picker is None:
            self.color_picker = ColorPickerDialog(self.config)
        
        self.color_picker.show()
        self.color_picker.raise_()
        self.color_picker.activateWindow()
        
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
        config_file = None
        for cfile in self.candidate_config_file():
            if os.path.isfile(cfile):
                config_file = cfile
                break
        
        if not config_file:
            config_file = Path.home() / ".color-notify.ini"
        
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
        hotkey_info = ""
        if GLOBAL_HOTKEY_AVAILABLE:
            hotkey_info = "\nGlobal Shortcut: Ctrl+Alt+Shift+C\n(Opens Color Picker)\n"
        else:
            hotkey_info = "\nGlobal hotkey disabled\n(Install pynput to enable)\n"
            
        self.tray.showMessage(
            "Color Notify", 
            f"Version {__version__}\n"
            f"By {__author__}\n\n"
            "Clipboard color detection tool\n"
            "Copy a color code to see notification!\n"
            f"{hotkey_info}\n"
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

def get_version():
    """
    Get the version of the ddf module.
    Version is taken from the __version__.py file if it exists.
    The content of __version__.py should be:
    version = "0.33"
    """
    try:
        version_file = Path(__file__).parent / "__version__.py"
        if version_file.is_file():
            with open(version_file, "r") as f:
                for line in f:
                    if line.strip().startswith("version"):
                        parts = line.split("=")
                        if len(parts) == 2:
                            return parts[1].strip().strip('"').strip("'")
    except Exception as e:
        if os.getenv('TRACEBACK') and os.getenv('TRACEBACK') in ['1', 'true', 'True']:
            console.print_exception(show_locals=False)
        else:
            console.log(f"[white on red]ERROR:[/] [white on blue]{e}[/]")

    return "UNKNOWN VERSION"

def _show_config(app):
    config_data = str(app.load_config()).replace("'", '"')
    print("\n")
    if HAS_RICH:
        from rich import print_json
        from rich.pretty import pprint
        try:
            import json5
            print_json(f"[bold #AAAAFF]{json5.loads(config_data)}[/]")
        except:
            pprint(config_data)
    else:
        print(config_data, "[bold #AAAAFF]")

def main():
    import argparse
    HAS_CUSTOM_RICH=False
    try:
        from licface import CustomRichHelpFormatter
        HAS_CUSTOM_RICH=True
    except:
        CustomRichHelpFormatter = argparse.RawTextHelpFormatter

    parser = argparse.ArgumentParser(prog="color-notify", formatter_class=CustomRichHelpFormatter)
    parser.add_argument('-v', '--version', action='version', version=f"version: {get_version()}", help="Show version")
    parser.add_argument('-s', '--show-config', help = 'Show config', action='store_true')

    if len(sys.argv) == 1:
        parser.print_help()
        print("\n")

    args = parser.parse_args()
    app = ColorNotifyApp(sys.argv)

    if args.show_config:
        _show_config(app)
    
    # main(show_version=args.version, show_config=args.show_config)
    else:
        # Cleanup on exit
        def cleanup():
            if hasattr(app, 'hotkey_handler') and app.hotkey_handler:
                app.hotkey_handler.stop()
        
        app.aboutToQuit.connect(cleanup)
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
