from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)

from LMTodo.controllers import todo_controller
from LMTodo.models.qthread_helper import ThreadRunner
from LMTodo.views.translations import translate
from LMTodo.views.widgets import BubbleWidget, TaskBubble, TaskFilterWidget, TaskWidget


class TaskPanel(QFrame):
    def __init__(
        self, main_window, get_current_project_id_func, get_projects_func=None
    ):
        self.main_window = main_window
        self.tasks = []
        self.get_current_project_id = get_current_project_id_func
        self.get_projects_func = get_projects_func

        super().__init__()

        self.setFrameShape(QFrame.StyledPanel)
        task_layout = QVBoxLayout()

        self.filter_widget = TaskFilterWidget(self.display_filtered_tasks)
        task_layout.addWidget(self.filter_widget)
        self.task_list = QListWidget()
        task_layout.addWidget(self.task_list)

        task_bar = QHBoxLayout()
        self.add_task_btn = QPushButton("+")
        self.add_task_btn.setToolTip(translate("Add Task"))
        self.add_task_btn.clicked.connect(self.add_task)
        self.edit_task_btn = QPushButton("✎")
        self.edit_task_btn.setToolTip(translate("Edit Task"))
        self.edit_task_btn.clicked.connect(self.edit_task)
        self.delete_task_btn = QPushButton("🗑")
        self.delete_task_btn.setToolTip(translate("Delete Task"))
        self.delete_task_btn.clicked.connect(self.delete_task)
        self.complete_task_btn = QPushButton("✔")
        self.complete_task_btn.setToolTip(translate("Mark as Completed"))
        self.complete_task_btn.clicked.connect(self.complete_task)
        self.cancel_task_btn = QPushButton("✖")
        self.cancel_task_btn.setToolTip(translate("Mark as Cancelled"))
        self.cancel_task_btn.clicked.connect(self.cancel_task)
        task_bar.addWidget(self.add_task_btn)
        task_bar.addWidget(self.edit_task_btn)
        task_bar.addWidget(self.delete_task_btn)
        task_bar.addWidget(self.complete_task_btn)
        task_bar.addWidget(self.cancel_task_btn)
        task_layout.addLayout(task_bar)
        self.setLayout(task_layout)

        self.task_list.itemSelectionChanged.connect(self.set_task_buttons_state)
        self.set_task_buttons_state()

    def load_tasks(self, result=None):
        ThreadRunner(todo_controller.get_tasks, self.on_tasks_loaded).start()

    def on_tasks_loaded(self, tasks):
        self.tasks = tasks
        self.display_filtered_tasks()

    def display_filtered_tasks(self):
        prev_task_id = None
        if self.task_list.selectedIndexes():
            prev_task_id = self.filtered_tasks[self.task_list.currentRow()][0]

        self.task_list.clear()
        current_task_filter = (
            self.filter_widget.get_current_filter()
        )  # ["All", "On Time", "Overdue", "Open", "Finished", "Cancelled"]
        self.filtered_tasks = []
        for (
            tid,
            title,
            status,
            creation_date,
            due_date,
            close_date,
            pid,
            comments,
        ) in self.tasks:
            if self.do_task_must_be_shown(
                self.get_current_project_id(),
                current_task_filter,
                tid,
                title,
                status,
                creation_date,
                due_date,
                close_date,
                pid,
            ):
                self.filtered_tasks.append(
                    (
                        tid,
                        title,
                        status,
                        creation_date,
                        due_date,
                        close_date,
                        pid,
                        comments,
                    )
                )

        sort_method = "creation"
        try:
            sort_method = self.filter_widget.get_sort_method()
        except Exception:
            sort_method = "creation"

        if sort_method == "creation":
            self.filtered_tasks.sort(key=lambda t: t[0])
        elif sort_method == "due":

            def due_key(t):
                dd = t[4] or ""
                return (dd == "", dd)

            self.filtered_tasks.sort(key=due_key)
        elif sort_method == "status":
            order = {"open": 0, "complete": 1, "cancelled": 2}
            self.filtered_tasks.sort(key=lambda t: order.get(t[2], 99))

        for (
            tid,
            title,
            status,
            creation_date,
            due_date,
            close_date,
            pid,
            comments,
        ) in self.filtered_tasks:

            def _on_save_comments(tid_arg, text):
                try:
                    ThreadRunner(
                        todo_controller.update_task_comments,
                        self.load_tasks,
                        tid_arg,
                        text,
                    ).start()
                except Exception:
                    pass

            task_widget = TaskWidget(
                self.main_window,
                next(
                    (
                        second
                        for first, second in self.get_projects_func()
                        if first == pid
                    ),
                    None,
                ),
                tid,
                title,
                status,
                due_date,
                close_date,
                creation_date,
                comments,
                on_save_comments=_on_save_comments,
            )
            item = QListWidgetItem()
            item.setSizeHint(task_widget.sizeHint())
            self.task_list.addItem(item)
            self.task_list.setItemWidget(item, task_widget)

        # Restore last selected Task if possible
        if prev_task_id is not None:
            for index, (tid, _, _, _, _, _, _, _) in enumerate(self.filtered_tasks):
                if tid == prev_task_id:
                    self.task_list.setCurrentRow(index)
                    break

        self.set_task_buttons_state()

    def do_task_must_be_shown(
        self,
        current_project_id,
        current_task_filter,
        tid,
        title,
        status,
        creation_date,
        due_date,
        close_date,
        pid,
    ):
        if not current_project_id == None and not current_project_id == pid:
            return False
        match current_task_filter:
            case "On Time":
                if not (
                    status == "open"
                    and QDate.fromString(due_date, "yyyy-MM-dd") >= QDate.currentDate()
                ):
                    return False
            case "Overdue":
                if not (
                    status == "open"
                    and QDate.fromString(due_date, "yyyy-MM-dd") < QDate.currentDate()
                ):
                    return False
            case "Open":
                if not status == "open":
                    return False
            case "Finished":
                if not status == "complete":
                    return False
            case "Cancelled":
                if not status == "cancelled":
                    return False
            case _:
                ...
        return True

    def set_task_buttons_state(self):
        selected_task = self.task_list.currentRow()
        is_task_selected = selected_task >= 0

        # Enable or disable task buttons based on selection
        self.edit_task_btn.setEnabled(is_task_selected)
        self.delete_task_btn.setEnabled(is_task_selected)
        self.complete_task_btn.setEnabled(is_task_selected)
        self.cancel_task_btn.setEnabled(is_task_selected)

    def add_task(self):
        # gather projects list from provided callback (list of (pid, name))
        projects = []
        try:
            if callable(self.get_projects_func):
                projects = self.get_projects_func() or []
        except Exception:
            projects = []

        selected_pid = None
        try:
            selected_pid = self.get_current_project_id()
        except Exception:
            selected_pid = None

        bubble = TaskBubble(
            self,
            self.add_task_btn,
            title=translate("Add Task"),
            action_text=translate("Add"),
            projects=projects,
            selected_project_id=selected_pid,
        )
        btn_pos = self.add_task_btn.mapToGlobal(self.add_task_btn.rect().bottomLeft())
        bubble.move(btn_pos.x() - 10, btn_pos.y() - bubble.height() - 30)

        def on_add():
            desc = bubble.desc_input.text().strip()
            due = bubble.due_input.date().toString("yyyy-MM-dd")
            # Determine selected project (from dropdown if present)
            if hasattr(bubble, "project_combo") and bubble.project_combo is not None:
                project_id = bubble.project_combo.currentData()
            else:
                project_id = self.get_current_project_id()

            if desc and project_id is not None:
                ThreadRunner(
                    todo_controller.add_task, self.load_tasks, desc, due, project_id
                ).start()
            bubble.close()

        bubble.action_btn.clicked.connect(on_add)
        bubble.show()

    def edit_task(self):
        (
            task_id,
            title,
            status,
            creation_date,
            due_date,
            close_date,
            project_id,
            comments,
        ) = self.filtered_tasks[self.task_list.currentRow()]

        bubble = TaskBubble(
            self,
            self.edit_task_btn,
            title=translate("Edit Task"),
            action_text=translate("Save"),
            initial_desc=title,
            initial_due_date=QDate.fromString(due_date, "yyyy-MM-dd"),
            projects=(
                self.get_projects_func() if callable(self.get_projects_func) else None
            ),
            selected_project_id=project_id,
        )
        btn_pos = self.edit_task_btn.mapToGlobal(self.edit_task_btn.rect().bottomLeft())
        bubble.move(btn_pos.x() - 10, btn_pos.y() - bubble.height() - 30)

        def on_save():
            desc = bubble.desc_input.text().strip()
            due = bubble.due_input.date().toString("yyyy-MM-dd")
            if desc:
                ThreadRunner(
                    todo_controller.edit_task,
                    self.load_tasks,
                    task_id,
                    desc,
                    due,
                    bubble.project_combo.currentData(),
                ).start()
            bubble.close()

        bubble.action_btn.clicked.connect(on_save)
        bubble.show()

    def delete_task(self):
        # Get task details from filtered tasks
        (
            task_id,
            title,
            status,
            creation_date,
            due_date,
            close_date,
            project_id,
            comments,
        ) = self.filtered_tasks[self.task_list.currentRow()]

        # Confirmation bubble with two buttons, no input
        bubble = BubbleWidget(
            self,
            f"{translate('Delete task')} '{title}'?",
            translate("Delete"),
            self.delete_task_btn,
            show_input=False,
            cancel_text=translate("Cancel"),
            warning_text=translate("This action can't be undone."),
        )
        btn_pos = self.delete_task_btn.mapToGlobal(
            self.delete_task_btn.rect().bottomLeft()
        )
        bubble.move(btn_pos.x() - 10, btn_pos.y() - bubble.height() - 30)

        def on_confirm():
            ThreadRunner(todo_controller.delete_task, self.load_tasks, task_id).start()
            bubble.close()

        def on_cancel():
            bubble.close()

        bubble.action_btn.clicked.connect(on_confirm)
        bubble.cancel_btn.clicked.connect(on_cancel)
        bubble.show()

    def update_task_status(self, new_status):
        # Get task details from filtered tasks
        (
            task_id,
            title,
            status,
            creation_date,
            due_date,
            close_date,
            project_id,
            comments,
        ) = self.filtered_tasks[self.task_list.currentRow()]

        if status != new_status:
            # Update the task status
            ThreadRunner(
                todo_controller.update_task_status, self.load_tasks, task_id, new_status
            ).start()
        else:
            # If the current status is the same as the new status, revert to 'open'
            ThreadRunner(
                todo_controller.update_task_status, self.load_tasks, task_id, "open"
            ).start()

    def complete_task(self):
        self.update_task_status("complete")

    def cancel_task(self):
        self.update_task_status("cancelled")
