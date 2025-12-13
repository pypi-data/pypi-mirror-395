import os
import shutil

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from LMTodo.controllers.todo_controller import init_db, update_db_path
from LMTodo.views.translations import translate
from LMTodo.views.widgets import BubbleWidget


class SettingsPanel(QFrame):
    def __init__(self, config_parser, parent=None):
        self._parent = parent
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)

        self.config_parser = config_parser

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Scrollable Content
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(30)

        # Title
        title_label = QLabel(translate("Settings"))
        title_label.setAlignment(Qt.AlignCenter)  # Center the title
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        scroll_layout.addWidget(title_label)

        # Default Language Selection
        language_layout = QHBoxLayout()
        language_label = QLabel(translate("Default Language:"))
        language_label.setStyleSheet(self._get_subtitle_style())
        language_layout.addWidget(language_label)
        # push combo to the right by adding stretch before it
        language_layout.addStretch()

        self.language_combo = QComboBox()
        # Add translated display items but store untranslated values in config
        lang_options = ["System Default", "English", "Brazilian Portuguese"]
        for opt in lang_options:
            self.language_combo.addItem(translate(opt), opt)
        # Set current value from config if available (allow stored untranslated or translated)
        current_lang = self.config_parser.get(
            "General", "default_language", fallback="System Default"
        )
        # Try to find by stored untranslated value in the userData, otherwise by displayed text
        found = False
        for i in range(self.language_combo.count()):
            if (
                self.language_combo.itemData(i) == current_lang
                or self.language_combo.itemText(i) == current_lang
            ):
                self.language_combo.setCurrentIndex(i)
                found = True
                break
        if not found:
            # default to system default
            self.language_combo.setCurrentIndex(0)
        self.language_combo.currentTextChanged.connect(self.update_default_language)
        language_layout.addWidget(self.language_combo)
        scroll_layout.addLayout(language_layout)

        # Default Project Selection
        project_layout = QHBoxLayout()
        project_label = QLabel(translate("Default Project:"))
        project_label.setStyleSheet(self._get_subtitle_style())
        project_layout.addWidget(project_label)
        # push combo to the right
        project_layout.addStretch()

        self.default_project_combo = QComboBox()
        # will be populated when settings panel is shown; include translated 'All Projects'
        all_projects_label = translate("All Projects")
        self.default_project_combo.addItem(all_projects_label, "All Projects")
        # set saved value if present (try matching stored value or translated label)
        saved_project = self.config_parser.get(
            "General", "default_project", fallback="All Projects"
        )
        # If saved_project equals the untranslated key, select it; otherwise try to match displayed text
        if saved_project == "All Projects":
            self.default_project_combo.setCurrentIndex(0)
        else:
            # try to match displayed text
            idx = self.default_project_combo.findText(saved_project)
            if idx != -1:
                self.default_project_combo.setCurrentIndex(idx)
            else:
                # fallback to first
                self.default_project_combo.setCurrentIndex(0)
        self.default_project_combo.currentTextChanged.connect(
            self.update_default_project
        )
        project_layout.addWidget(self.default_project_combo)
        scroll_layout.addLayout(project_layout)

        # Default Task Filter Selection
        filter_layout = QHBoxLayout()
        filter_label = QLabel(translate("Default Task Filter:"))
        filter_label.setStyleSheet(self._get_subtitle_style())
        filter_layout.addWidget(filter_label)
        filter_layout.addStretch()

        self.default_filter_combo = QComboBox()
        filter_options = ["All", "On Time", "Overdue", "Open", "Finished", "Cancelled"]
        for f in filter_options:
            self.default_filter_combo.addItem(translate(f), f)
        saved_filter = self.config_parser.get(
            "General",
            "default_filter",
            fallback=self.config_parser.DEFAULTS["General"].get(
                "default_filter", "Open"
            ),
        )
        # Match saved canonical value or displayed text
        found = False
        for i in range(self.default_filter_combo.count()):
            if (
                self.default_filter_combo.itemData(i) == saved_filter
                or self.default_filter_combo.itemText(i) == saved_filter
            ):
                self.default_filter_combo.setCurrentIndex(i)
                found = True
                break
        if not found:
            self.default_filter_combo.setCurrentIndex(
                self.default_filter_combo.findData("Open")
            )

        def on_default_filter_changed(text):
            idx = self.default_filter_combo.currentIndex()
            key = self.default_filter_combo.itemData(idx) or text
            self.config_parser.set("General", "default_filter", key)
            self.config_parser.save()
            # Apply immediately if parent exists
            if (
                self._parent
                and hasattr(self._parent, "task_panel")
                and hasattr(self._parent.task_panel, "filter_widget")
            ):
                try:
                    self._parent.task_panel.filter_widget.set_default_filter(key)
                except Exception:
                    pass

        self.default_filter_combo.currentTextChanged.connect(on_default_filter_changed)
        filter_layout.addWidget(self.default_filter_combo)
        scroll_layout.addLayout(filter_layout)

        # Default Sort Order Selection
        sort_layout = QHBoxLayout()
        sort_label = QLabel(translate("Sort by:"))
        sort_label.setStyleSheet(self._get_subtitle_style())
        sort_layout.addWidget(sort_label)
        sort_layout.addStretch()

        self.default_sort_combo = QComboBox()
        sort_options = [
            (translate("Creation Date"), "creation"),
            (translate("Due Date"), "due"),
            (translate("Status"), "status"),
        ]
        for label, data in sort_options:
            self.default_sort_combo.addItem(label, data)

        saved_sort = self.config_parser.get(
            "General",
            "default_sort",
            fallback=self.config_parser.DEFAULTS["General"].get(
                "default_sort", "creation"
            ),
        )
        found_sort = False
        for i in range(self.default_sort_combo.count()):
            if (
                self.default_sort_combo.itemData(i) == saved_sort
                or self.default_sort_combo.itemText(i) == saved_sort
            ):
                self.default_sort_combo.setCurrentIndex(i)
                found_sort = True
                break
        if not found_sort:
            # fallback to creation
            idx = self.default_sort_combo.findData("creation")
            if idx != -1:
                self.default_sort_combo.setCurrentIndex(idx)

        self.default_sort_combo.currentTextChanged.connect(self.on_default_sort_changed)
        sort_layout.addWidget(self.default_sort_combo)
        scroll_layout.addLayout(sort_layout)

        scroll_layout.addLayout(self.get_db_location_layout())
        scroll_layout.addLayout(self.get_shortcut_config_layout())

        # Spacer
        scroll_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def on_default_sort_changed(self, text):
        idx = self.default_sort_combo.currentIndex()
        key = self.default_sort_combo.itemData(idx) or text
        self.config_parser.set("General", "default_sort", key)
        self.config_parser.save()

    def update_default_language(self, lang):
        # Save the selected language to config
        lang = self.language_combo.itemData(self.language_combo.findText(lang))
        self.config_parser.set("General", "default_language", lang)
        self.config_parser.save()
        # Show bubble notification

        bubble = BubbleWidget(
            self,
            "The language will change only after you restart the app.",
            "OK",
            self.language_combo,
            show_input=False,
        )
        bubble.action_btn.clicked.connect(bubble.close)
        bubble.show()

    def update_default_project(self, project_name):
        # Save the selected default project to config
        self.config_parser.set("General", "default_project", project_name)
        self.config_parser.save()

    def showEvent(self, event):
        # Populate default project combo with current project list when settings panel is shown
        try:
            if self._parent and hasattr(self._parent, "projects"):
                current_projects = [
                    name for (_id, name) in getattr(self._parent, "projects", [])
                ]
                # Clear but keep 'All Projects'
                current_text = self.default_project_combo.currentText()
                self.default_project_combo.blockSignals(True)
                self.default_project_combo.clear()
                self.default_project_combo.addItem(
                    translate("All Projects"), "All Projetcs"
                )
                for name in current_projects:
                    self.default_project_combo.addItem(name, name)
                # restore selection if present
                idx = self.default_project_combo.findText(
                    self.config_parser.get(
                        "General", "default_project", fallback="All Projects"
                    )
                )
                if idx != -1:
                    self.default_project_combo.setCurrentIndex(idx)
                else:
                    self.default_project_combo.setCurrentText(translate("All Projects"))
                self.default_project_combo.blockSignals(False)
        except Exception:
            pass

    def get_db_location_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(1)

        # Current DB Path Section
        db_path_layout = QHBoxLayout()
        db_path_label = QLabel(translate("Database Path:"))
        db_path_label.setStyleSheet(self._get_subtitle_style())

        db_path_layout.addWidget(db_path_label)
        # db_path_layout.addSpacing(50)
        # push the change button to the right
        db_path_layout.addStretch()
        # Change DB Location Button
        self.change_db_btn = QPushButton(translate("Change"))
        self.change_db_btn.clicked.connect(self.change_db_location)
        db_path_layout.addWidget(self.change_db_btn)
        layout.addLayout(db_path_layout)

        # Current DB Path Display
        self.db_path_value_label = QLabel(self.config_parser.get_db_path())
        self.db_path_value_label.setStyleSheet("font-size: 14px; color: #555;")
        self.db_path_value_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.db_path_value_label.setToolTip(
            self.config_parser.get_db_path()
        )  # Add tooltip for full path
        self.db_path_value_label.setWordWrap(True)
        self.db_path_value_label.setMaximumWidth(350)
        self.db_path_value_label.setFixedHeight(0)
        self.db_path_value_label.setMaximumHeight(16777215)

        layout.addWidget(self.db_path_value_label, 1)
        return layout

    def get_shortcut_config_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Shortcut Configuration Section
        shortcut_label = QLabel(translate("Shortcut Configuration:"))
        shortcut_label.setStyleSheet(self._get_subtitle_style())
        layout.addWidget(shortcut_label)

        shortcuts = self.config_parser.DEFAULTS["Shortcuts"]

        # Shortcut for Add Project Button
        layout.addLayout(
            self._create_shortcut_row(
                translate("Add Project Shortcut:"),
                "add_project",
                shortcuts["add_project"],
            )
        )
        # Shortcut for Edit Project Button
        layout.addLayout(
            self._create_shortcut_row(
                translate("Edit Project Shortcut:"),
                "edit_project",
                shortcuts["edit_project"],
            )
        )
        # Shortcut for Delete Project Button
        layout.addLayout(
            self._create_shortcut_row(
                translate("Delete Project Shortcut:"),
                "delete_project",
                shortcuts["delete_project"],
            )
        )
        # Shortcut for Add Task Button
        layout.addLayout(
            self._create_shortcut_row(
                translate("Add Task Shortcut:"), "add_task", shortcuts["add_task"]
            )
        )
        # Shortcut for Edit Task Button
        layout.addLayout(
            self._create_shortcut_row(
                translate("Edit Task Shortcut:"), "edit_task", shortcuts["edit_task"]
            )
        )
        # Shortcut for Remove Task Button
        layout.addLayout(
            self._create_shortcut_row(
                translate("Remove Task Shortcut:"),
                "remove_task",
                shortcuts["remove_task"],
            )
        )
        # Shortcut for Mark Completed Button
        layout.addLayout(
            self._create_shortcut_row(
                translate("Mark Completed Shortcut:"),
                "mark_completed",
                shortcuts["mark_completed"],
            )
        )
        # Shortcut for Mark Canceled Button
        layout.addLayout(
            self._create_shortcut_row(
                translate("Mark Canceled Shortcut:"),
                "mark_canceled",
                shortcuts["mark_canceled"],
            )
        )
        # Shortcut for All Projects Button
        layout.addLayout(
            self._create_shortcut_row(
                translate("All Projects Shortcut:"),
                "all_projects",
                shortcuts["all_projects"],
            )
        )
        # Shortcut for Config Panel Button
        layout.addLayout(
            self._create_shortcut_row(
                translate("Config Panel Shortcut:"),
                "config_panel",
                shortcuts["config_panel"],
            )
        )
        # Shortcut for Filter Buttons
        layout.addLayout(
            self._create_shortcut_row(
                translate("Filter All Shortcut:"), "filter_all", shortcuts["filter_all"]
            )
        )
        layout.addLayout(
            self._create_shortcut_row(
                translate("On-Time Shortcut:"), "on_time", shortcuts["on_time"]
            )
        )
        layout.addLayout(
            self._create_shortcut_row(
                translate("Overdue Shortcut:"), "overdue", shortcuts["overdue"]
            )
        )
        layout.addLayout(
            self._create_shortcut_row(
                translate("Filter Active Shortcut:"),
                "filter_active",
                shortcuts["filter_active"],
            )
        )
        layout.addLayout(
            self._create_shortcut_row(
                translate("Filter Completed Shortcut:"),
                "filter_completed",
                shortcuts["filter_completed"],
            )
        )
        layout.addLayout(
            self._create_shortcut_row(
                translate("Filter Canceled Shortcut:"),
                "filter_canceled",
                shortcuts["filter_canceled"],
            )
        )
        # Selection shortcuts
        layout.addLayout(
            self._create_shortcut_row(
                translate("Select Project Shortcut:"),
                "select_project",
                shortcuts["select_project"],
            )
        )
        layout.addLayout(
            self._create_shortcut_row(
                translate("Select Tasks Shortcut:"),
                "select_tasks",
                shortcuts["select_tasks"],
            )
        )

        return layout

    def _create_shortcut_row(self, label_text, action, default_shortcut):
        # Use a vertical layout so we can show inline error messages under the row
        container_layout = QVBoxLayout()
        row_layout = QHBoxLayout()
        row_layout.setSpacing(10)

        shortcut_label = QLabel(label_text)
        shortcut_label.setStyleSheet("font-size: 14px;")
        shortcut_label.setFixedWidth(200)

        shortcut_input = QLineEdit(
            self.config_parser.get("Shortcuts", action, fallback=default_shortcut)
        )
        shortcut_input.setStyleSheet(
            "font-size: 14px; border: 1px solid #ccc; border-radius: 4px;"
        )

        # Inline error label
        error_label = QLabel("")
        error_label.setStyleSheet("color: #e57373; font-size: 12px;")
        error_label.setVisible(False)

        def on_shortcut_changed():
            new_val = shortcut_input.text().strip()

            # Empty is invalid
            if not new_val:
                error_label.setText(translate("Shortcut cannot be empty."))
                error_label.setVisible(True)
                return

            # Validate format using QKeySequence
            seq = QKeySequence(new_val)
            if not seq.toString().strip():
                error_label.setText(translate("Invalid shortcut format."))
                error_label.setVisible(True)
                return

            # Check if the shortcut is already used by another action
            current_shortcuts = self.config_parser.get_shortcuts()
            for act, s in current_shortcuts.items():
                if act == action:
                    continue
                if s and s.strip() and s == new_val:
                    # show which action uses it
                    # Use the translation with the action name interpolated
                    error_label.setText(
                        translate("Shortcut already used by '{act}'.").format(act=act)
                    )
                    error_label.setVisible(True)
                    return

            # All good: clear error and propagate change
            error_label.setVisible(False)
            self.update_shortcut(action, new_val)

        shortcut_input.textChanged.connect(on_shortcut_changed)

        row_layout.addWidget(shortcut_label)
        row_layout.addWidget(shortcut_input)
        row_layout.addStretch()

        container_layout.addLayout(row_layout)
        container_layout.addWidget(error_label)

        return container_layout

    def update_shortcut(self, action, new_shortcut):
        """Update a shortcut and notify the main window to apply the change."""
        if self._parent:
            self._parent.update_shortcut(action, new_shortcut)

    def _get_subtitle_style(self):
        return "font-size: 14px; font-weight: bold;"

    def change_db_location(self):
        """Open a file dialog to select a new database location."""
        new_path, _ = QFileDialog.getSaveFileName(
            self,
            "Select New Database Location",
            "",
            "Database Files (*.db);;All Files (*)",
        )

        if new_path:
            current_db_path = self.config_parser.get_db_path()

            if os.path.exists(current_db_path):
                # Ask the user if they want to move the current database
                reply = QMessageBox.question(
                    self,
                    translate("Move Database"),
                    translate(
                        "Do you want to move the current database to the new location?\n\n"
                    )
                    + translate(
                        "Warning: If you press 'No', a new database will be created at the new location, and all current information will be unavailable."
                    ),
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                )

                if reply == QMessageBox.Cancel:
                    return

                if reply == QMessageBox.Yes:
                    try:
                        shutil.move(current_db_path, new_path)
                        update_db_path(new_path)
                    except Exception as e:
                        QMessageBox.critical(
                            self,
                            translate("Error"),
                            f"{translate('Failed to move database')}: {e}",
                        )
                        return
                if reply == QMessageBox.No:
                    init_db(new_path)

            # Update the configuration with the new path
            self.config_parser.save_db_path(new_path)
            self.db_path_value_label.setText(new_path)  # Update the label
            self.db_path_value_label.setToolTip(new_path)  # Update the tooltip
            self._parent.load_projects()
            QMessageBox.information(
                self,
                translate("Success"),
                translate("Database location updated successfully."),
            )
