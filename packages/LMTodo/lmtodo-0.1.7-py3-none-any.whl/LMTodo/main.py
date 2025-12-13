import base64
import sys

from PySide6.QtCore import QByteArray, QRect
from PySide6.QtGui import QGuiApplication, QIcon, QKeySequence, QPixmap, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QListWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from LMTodo.controllers import todo_controller
from LMTodo.models.parser import TodoConfigParser
from LMTodo.models.qthread_helper import ThreadRunner
from LMTodo.views.lmtodo_icons import base64_app_icon
from LMTodo.views.settings_panel import SettingsPanel
from LMTodo.views.task_panel import TaskPanel
from LMTodo.views.translations import translate
from LMTodo.views.widgets import BubbleWidget


class MainWindow(QMainWindow):
    """Main application window for the Todo app."""

    def __init__(self):
        self.tasks = []
        self.configs = TodoConfigParser()
        todo_controller.init_db(self.configs.db_path)

        super().__init__()

        icon_bytes = QByteArray(base64.b64decode(base64_app_icon))
        pixmap = QPixmap()
        pixmap.loadFromData(icon_bytes)
        self.setWindowIcon(QIcon(pixmap))

        self.setWindowTitle(translate("Todo App"))

        window_settings = self.configs.get_window_settings()
        # Validate the saved window position
        saved_geometry = QRect(
            window_settings["x"],
            window_settings["y"],
            window_settings["width"],
            window_settings["height"],
        )

        if not any(
            screen.geometry().intersects(saved_geometry)
            for screen in QGuiApplication.screens()
        ):
            default_settings = self.configs.DEFAULTS["Window"]
            # Use default settings if the saved position is invalid
            self.setGeometry(
                int(default_settings["x"]),
                int(default_settings["y"]),
                int(default_settings["width"]),
                int(default_settings["height"]),
            )
        else:
            # Use saved settings
            self.setGeometry(saved_geometry)

        # Main layout
        main_widget = QWidget()
        self.main_layout = QHBoxLayout()
        main_widget.setLayout(self.main_layout)
        self.setCentralWidget(main_widget)
        # Left panel: Projects (fixed width)
        self.project_panel = QFrame()
        self.project_panel.setFrameShape(QFrame.StyledPanel)
        self.project_panel.setFixedWidth(220)
        project_layout = QVBoxLayout()
        top_bar = QHBoxLayout()
        self.all_projects_btn = QPushButton(translate("all_projects"))
        self.all_projects_btn.setCheckable(True)
        self.all_projects_btn.clicked.connect(self.on_all_projects_clicked)
        top_bar.addWidget(self.all_projects_btn)
        self.config_btn = QPushButton("⚙")
        self.config_btn.setCheckable(True)
        self.config_btn.setMaximumWidth(45)
        self.config_btn.setToolTip(translate("Open Configurations"))
        self.config_btn.clicked.connect(self.toggle_config_panel)
        top_bar.addWidget(self.config_btn)
        project_layout.addLayout(top_bar)
        # Add project list
        self.project_list = QListWidget()
        self.project_list.setMinimumWidth(200)
        self.project_list.setStyleSheet("QListWidget::item {    padding: 6px 12px;}")
        self.project_list.itemSelectionChanged.connect(self.on_project_selected)
        project_layout.addWidget(self.project_list)
        # Bottom bar for project management
        project_bar = QHBoxLayout()
        self.add_project_btn = QPushButton("+")
        self.add_project_btn.setToolTip(translate("Add Project"))
        self.add_project_btn.clicked.connect(self.add_project)
        self.edit_project_btn = QPushButton("✎")
        self.edit_project_btn.setToolTip(translate("Edit Project"))
        self.edit_project_btn.clicked.connect(self.edit_project)
        self.delete_project_btn = QPushButton("🗑")
        self.delete_project_btn.setToolTip(translate("Delete Project"))
        self.delete_project_btn.clicked.connect(self.delete_project)
        project_bar.addWidget(self.add_project_btn)
        project_bar.addWidget(self.edit_project_btn)
        project_bar.addWidget(self.delete_project_btn)
        project_layout.addLayout(project_bar)
        self.project_panel.setLayout(project_layout)
        self.main_layout.addWidget(self.project_panel)
        # Right panel: Tasks (expands dynamically)
        self.task_panel = TaskPanel(
            self, self.get_current_project_id, self.get_projects
        )
        self.main_layout.addWidget(self.task_panel, stretch=1)

        # Create the configuration panel with animation
        self.config_panel = SettingsPanel(self.configs, self)
        self.config_panel.setFixedWidth(375)
        self.config_panel.hide()
        self.main_layout.insertWidget(1, self.config_panel)

        # Load Projects
        self.load_projects()

        # Set shortcuts
        self.set_shortcuts()

    def load_projects(self, result=None):
        ThreadRunner(todo_controller.get_projects, self.on_projects_loaded).start()

    def on_projects_loaded(self, projects):
        # Store the ID of the currently selected project
        prev_project_id = None
        if self.project_list.selectedIndexes():
            prev_project_id = self.projects[self.project_list.currentRow()][0]

        self.project_list.clear()
        for pid, name in projects:
            self.project_list.addItem(name)
        self.projects = projects

        # Restore previous selection based on project ID
        if prev_project_id is not None:
            for index, (pid, _) in enumerate(self.projects):
                if pid == prev_project_id:
                    self.project_list.setCurrentRow(index)
                    break

        # If there's no previous selection, try to apply configured default project
        if prev_project_id is None:
            default_project_name = self.configs.get(
                "General",
                "default_project",
                fallback=self.configs.DEFAULTS["General"].get(
                    "default_project", "All Projects"
                ),
            )
            if default_project_name and default_project_name != "All Projects":
                # find project by name
                found = False
                for index, (_pid, name) in enumerate(self.projects):
                    if name == default_project_name:
                        self.project_list.setCurrentRow(index)
                        found = True
                        break
                if not found:
                    # fallback to All Projects and save fallback
                    self.configs.set("General", "default_project", "All Projects")
                    self.configs.save()

        self.set_projects_buttons_state()
        self.task_panel.load_tasks()

    def on_project_selected(self):
        self.set_projects_buttons_state()
        self.task_panel.display_filtered_tasks()

    def set_projects_buttons_state(self):
        if not self.project_list.selectedIndexes():
            self.all_projects_btn.setChecked(True)
            self.all_projects_btn.setStyleSheet(
                "background-color: palette(highlight); color: palette(highlightedText); font-weight: bold;"
            )

            self.task_panel.add_task_btn.setEnabled(False)
            self.edit_project_btn.setEnabled(False)
            self.delete_project_btn.setEnabled(False)
        else:
            self.all_projects_btn.setChecked(False)
            self.all_projects_btn.setStyleSheet("")  # Reset to default style

            self.task_panel.add_task_btn.setEnabled(True)
            self.edit_project_btn.setEnabled(True)
            self.delete_project_btn.setEnabled(True)

    def on_all_projects_clicked(self):
        if self.all_projects_btn.isChecked():
            self.project_list.clearSelection()

    def get_current_project_id(self):
        if self.project_list.selectedIndexes():
            return self.projects[self.project_list.currentRow()][0]
        return None

    def get_projects(self):
        """Return the current list of projects as (pid, name) tuples.
        Used by TaskPanel to populate project-selection dropdowns.
        """
        return getattr(self, "projects", [])

    def add_project(self):
        bubble = BubbleWidget(
            self,
            translate("Enter project name:"),
            translate("Add"),
            self.add_project_btn,
        )
        btn_pos = self.add_project_btn.mapToGlobal(
            self.add_project_btn.rect().bottomLeft()
        )
        bubble.move(btn_pos.x() - 10, btn_pos.y() - bubble.height() - 30)

        def on_add():
            name = bubble.name_input.text().strip()
            if name:
                ThreadRunner(
                    todo_controller.add_project, self.load_projects, name
                ).start()
                bubble.close()

        bubble.action_btn.clicked.connect(on_add)
        bubble.show()

    def edit_project(self):
        project_id, current_name = self.projects[self.project_list.currentRow()]
        bubble = BubbleWidget(
            self,
            translate("Edit project name:"),
            translate("Save"),
            self.edit_project_btn,
            initial_text=current_name,
        )
        btn_pos = self.edit_project_btn.mapToGlobal(
            self.edit_project_btn.rect().bottomLeft()
        )
        bubble.move(btn_pos.x() - 10, btn_pos.y() - bubble.height() - 30)

        def on_save():
            name = bubble.name_input.text().strip()
            if not name:
                return
            ThreadRunner(
                todo_controller.edit_project, self.load_projects, project_id, name
            ).start()
            bubble.close()

        bubble.action_btn.clicked.connect(on_save)
        bubble.show()

    def delete_project(self):
        project_id, project_name = self.projects[self.project_list.currentRow()]
        # Confirmation bubble with two buttons, no input
        bubble = BubbleWidget(
            self,
            f"{translate('Delete project')} '{project_name}'?",
            translate("Delete"),
            self.delete_project_btn,
            show_input=False,
            cancel_text=translate("Cancel"),
            warning_text=translate("This action can't be undone."),
        )
        btn_pos = self.delete_project_btn.mapToGlobal(
            self.delete_project_btn.rect().bottomLeft()
        )
        bubble.move(btn_pos.x() - 10, btn_pos.y() - bubble.height() - 30)

        def on_confirm():
            ThreadRunner(
                todo_controller.delete_project, self.load_projects, project_id
            ).start()
            bubble.close()

        def on_cancel():
            bubble.close()

        bubble.action_btn.clicked.connect(on_confirm)
        bubble.cancel_btn.clicked.connect(on_cancel)
        bubble.show()

    def toggle_config_panel(self):
        if self.config_panel.isVisible():
            self.config_panel.hide()
            self.config_btn.setChecked(False)
            self.config_btn.setStyleSheet("")
        else:
            self.config_panel.show()
            self.config_btn.setChecked(True)
            self.config_btn.setStyleSheet(
                "background-color: palette(highlight); color: palette(highlightedText); font-weight: bold;"
            )

    def set_shortcuts(self):
        """Set all shortcuts from the configuration parser."""
        shortcuts = self.configs.get_shortcuts()

        self.add_project_btn.setShortcut(shortcuts["add_project"])
        self.edit_project_btn.setShortcut(shortcuts["edit_project"])
        self.delete_project_btn.setShortcut(shortcuts["delete_project"])
        self.task_panel.add_task_btn.setShortcut(shortcuts["add_task"])
        self.task_panel.edit_task_btn.setShortcut(shortcuts["edit_task"])
        self.task_panel.delete_task_btn.setShortcut(shortcuts["remove_task"])
        self.task_panel.complete_task_btn.setShortcut(shortcuts["mark_completed"])
        self.task_panel.cancel_task_btn.setShortcut(shortcuts["mark_canceled"])
        self.all_projects_btn.setShortcut(shortcuts["all_projects"])
        self.config_btn.setShortcut(shortcuts["config_panel"])
        self.task_panel.filter_widget.buttons["All"].setShortcut(
            shortcuts["filter_all"]
        )  # ["All", "On Time", "Overdue", "Open", "Finished", "Cancelled"]
        self.task_panel.filter_widget.buttons["On Time"].setShortcut(
            shortcuts["on_time"]
        )
        self.task_panel.filter_widget.buttons["Overdue"].setShortcut(
            shortcuts["overdue"]
        )
        self.task_panel.filter_widget.buttons["Open"].setShortcut(
            shortcuts["filter_active"]
        )
        self.task_panel.filter_widget.buttons["Finished"].setShortcut(
            shortcuts["filter_completed"]
        )
        self.task_panel.filter_widget.buttons["Cancelled"].setShortcut(
            shortcuts["filter_canceled"]
        )
        self.select_projects_shortcut = QShortcut(
            QKeySequence(shortcuts["select_project"]), self
        )
        self.select_projects_shortcut.activated.connect(self.project_list.setFocus)
        self.select_tasks_shortcut = QShortcut(
            QKeySequence(shortcuts["select_tasks"]), self
        )
        self.select_tasks_shortcut.activated.connect(self.task_panel.task_list.setFocus)

    def update_shortcut(self, action, new_shortcut):
        """Update a specific shortcut in the configuration and apply it.

        Only the affected shortcut/widget is updated to avoid clobbering
        or reapplying all shortcuts when a single one changes.
        """
        # Persist the change
        self.configs.set("Shortcuts", action, new_shortcut)
        self.configs.save()

        # Apply the updated shortcut to the corresponding widget
        try:
            if action == "add_project":
                self.add_project_btn.setShortcut(new_shortcut)
            elif action == "edit_project":
                self.edit_project_btn.setShortcut(new_shortcut)
            elif action == "delete_project":
                self.delete_project_btn.setShortcut(new_shortcut)
            elif action == "add_task":
                self.task_panel.add_task_btn.setShortcut(new_shortcut)
            elif action == "edit_task":
                self.task_panel.edit_task_btn.setShortcut(new_shortcut)
            elif action == "remove_task":
                self.task_panel.delete_task_btn.setShortcut(new_shortcut)
            elif action == "mark_completed":
                self.task_panel.complete_task_btn.setShortcut(new_shortcut)
            elif action == "mark_canceled":
                self.task_panel.cancel_task_btn.setShortcut(new_shortcut)
            elif action == "all_projects":
                self.all_projects_btn.setShortcut(new_shortcut)
            elif action == "config_panel":
                self.config_btn.setShortcut(new_shortcut)
            elif action == "filter_all":
                self.task_panel.filter_widget.buttons["All"].setShortcut(new_shortcut)
            elif action == "on_time":
                self.task_panel.filter_widget.buttons["On Time"].setShortcut(
                    new_shortcut
                )
            elif action == "overdue":
                self.task_panel.filter_widget.buttons["Overdue"].setShortcut(
                    new_shortcut
                )
            elif action == "filter_active":
                self.task_panel.filter_widget.buttons["Open"].setShortcut(new_shortcut)
            elif action == "filter_completed":
                self.task_panel.filter_widget.buttons["Finished"].setShortcut(
                    new_shortcut
                )
            elif action == "filter_canceled":
                self.task_panel.filter_widget.buttons["Cancelled"].setShortcut(
                    new_shortcut
                )
            elif action == "select_project":
                if (
                    hasattr(self, "select_projects_shortcut")
                    and self.select_projects_shortcut
                ):
                    self.select_projects_shortcut.setKey(QKeySequence(new_shortcut))
                else:
                    self.select_projects_shortcut = QShortcut(
                        QKeySequence(new_shortcut), self
                    )
                    self.select_projects_shortcut.activated.connect(
                        self.project_list.setFocus
                    )
            elif action == "select_tasks":
                if (
                    hasattr(self, "select_tasks_shortcut")
                    and self.select_tasks_shortcut
                ):
                    self.select_tasks_shortcut.setKey(QKeySequence(new_shortcut))
                else:
                    self.select_tasks_shortcut = QShortcut(
                        QKeySequence(new_shortcut), self
                    )
                    self.select_tasks_shortcut.activated.connect(
                        self.task_panel.task_list.setFocus
                    )
        except Exception:
            # Fallback: reapply all shortcuts if something goes wrong
            self.set_shortcuts()

    def closeEvent(self, event):
        """Save the current window position and size to the .ini file."""
        geometry = self.geometry()
        self.configs.save_window_settings(
            geometry.width(), geometry.height(), geometry.x(), geometry.y()
        )
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
