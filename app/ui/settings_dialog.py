from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QCheckBox, QFileDialog, QGroupBox, QMessageBox
)
from PyQt6.QtCore import Qt
from pathlib import Path

from core.settings import SettingsManager, Settings
from ui.theme import Colors, load_stylesheet


class SettingsDialog(QDialog):
    """Settings dialog for app preferences"""
    
    def __init__(self, parent=None, settings_manager: SettingsManager = None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumWidth(550)
        self.setMinimumHeight(400)
        self.settings_manager = settings_manager
        self.current_settings = settings_manager.get() if settings_manager else Settings()
        
        # Apply stylesheet to dialog
        stylesheet = load_stylesheet()
        self.setStyleSheet(stylesheet)
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Download Folder
        folder_group = QGroupBox("Download Location")
        folder_layout = QVBoxLayout()
        folder_layout.setSpacing(10)
        
        folder_label = QLabel("Folder:")
        folder_label.setMinimumWidth(80)
        self.folder_input = QLineEdit()
        self.folder_input.setText(self.current_settings.download_folder)
        self.folder_input.setReadOnly(True)
        folder_btn = QPushButton("Browse")
        folder_btn.clicked.connect(self.choose_folder)
        folder_btn.setMaximumWidth(100)
        
        folder_row = QHBoxLayout()
        folder_row.setSpacing(10)
        folder_row.addWidget(folder_label)
        folder_row.addWidget(self.folder_input)
        folder_row.addWidget(folder_btn)
        folder_layout.addLayout(folder_row)
        folder_group.setLayout(folder_layout)
        layout.addWidget(folder_group)
        
        # Video Quality & Format
        quality_group = QGroupBox("Download Quality")
        quality_layout = QVBoxLayout()
        quality_layout.setSpacing(10)
        
        quality_label = QLabel("Quality:")
        quality_label.setMinimumWidth(80)
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(Settings.QUALITY_OPTIONS)
        self.quality_combo.setCurrentText(self.current_settings.video_quality)
        self.quality_combo.setMinimumWidth(150)
        
        quality_row = QHBoxLayout()
        quality_row.setSpacing(10)
        quality_row.addWidget(quality_label)
        quality_row.addWidget(self.quality_combo)
        quality_row.addStretch()
        quality_layout.addLayout(quality_row)
        
        format_label = QLabel("Format:")
        format_label.setMinimumWidth(80)
        self.format_combo = QComboBox()
        self.format_combo.addItems(Settings.FORMAT_OPTIONS)
        self.format_combo.setCurrentText(self.current_settings.format)
        self.format_combo.setMinimumWidth(150)
        
        format_row = QHBoxLayout()
        format_row.setSpacing(10)
        format_row.addWidget(format_label)
        format_row.addWidget(self.format_combo)
        format_row.addStretch()
        quality_layout.addLayout(format_row)
        
        quality_group.setLayout(quality_layout)
        layout.addWidget(quality_group)
        
        # Preferences
        pref_group = QGroupBox("Preferences")
        pref_layout = QVBoxLayout()
        pref_layout.setSpacing(10)
        
        self.auto_start_check = QCheckBox("Auto-start downloads when queue is added")
        self.auto_start_check.setChecked(self.current_settings.auto_start)
        pref_layout.addWidget(self.auto_start_check)
        
        self.dark_mode_check = QCheckBox("Dark mode (coming soon)")
        self.dark_mode_check.setChecked(self.current_settings.dark_mode)
        self.dark_mode_check.setEnabled(False)  # Not implemented yet
        pref_layout.addWidget(self.dark_mode_check)
        
        pref_group.setLayout(pref_layout)
        layout.addWidget(pref_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_settings)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.clicked.connect(self.reset_defaults)
        
        btn_layout.addStretch()
        btn_layout.addWidget(reset_btn)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Download Folder",
            self.folder_input.text()
        )
        if folder:
            self.folder_input.setText(folder)
    
    def save_settings(self):
        """Save settings and close dialog"""
        new_settings = Settings(
            download_folder=self.folder_input.text(),
            video_quality=self.quality_combo.currentText(),
            format=self.format_combo.currentText(),
            auto_start=self.auto_start_check.isChecked(),
            dark_mode=self.dark_mode_check.isChecked(),
        )
        
        if self.settings_manager.save(new_settings):
            QMessageBox.information(self, "Success", "Settings saved successfully.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Failed to save settings.")
    
    def reset_defaults(self):
        """Reset all settings to defaults"""
        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "Are you sure you want to reset all settings to defaults?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            defaults = Settings()
            self.folder_input.setText(defaults.download_folder)
            self.quality_combo.setCurrentText(defaults.video_quality)
            self.format_combo.setCurrentText(defaults.format)
            self.auto_start_check.setChecked(defaults.auto_start)
            self.dark_mode_check.setChecked(defaults.dark_mode)
