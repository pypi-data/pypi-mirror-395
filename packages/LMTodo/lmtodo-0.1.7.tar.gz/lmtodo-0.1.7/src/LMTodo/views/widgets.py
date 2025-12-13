from typing import Optional

from PySide6.QtCore import QDate, QPoint, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QPainter, QPolygon
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from LMTodo.models.parser import get_config_parser
from LMTodo.views.translations import translate


class BubbleWidget(QWidget):
    def __init__(
        self,
        parent,
        label_text,
        button_text,
        anchor_btn,
        initial_text="",
        show_input=True,
        cancel_text=None,
        warning_text=None,
        minWidth=240,
        minHeight=170,
    ):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumWidth(minWidth)
        self.setMinimumHeight(minHeight)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.anchor_btn = anchor_btn
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)
        label = QLabel(translate(label_text))
        label.setStyleSheet("color: #f0f0f0; font-size: 14px;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        if warning_text:
            warning = QLabel(warning_text)
            warning.setStyleSheet(
                "color: #e57373; font-size: 12px; font-style: italic;"
            )
            warning.setAlignment(Qt.AlignCenter)
            layout.addWidget(warning)
        self.name_input = QLineEdit()
        self.name_input.setText(initial_text)
        self.name_input.setStyleSheet(
            "background: #222; color: #f0f0f0; border-radius: 6px; padding: 4px 8px;"
        )
        if show_input:
            layout.addWidget(self.name_input)
        self.action_btn = QPushButton(translate(button_text))
        self.action_btn.setStyleSheet(
            "background: #c00; color: #fff; border-radius: 6px; padding: 4px 12px;"
        )
        # Expose the button row so subclasses (like TaskBubble) can add widgets to the same row
        self.btn_row = QHBoxLayout()
        self.btn_row.addWidget(self.action_btn)
        if cancel_text:
            self.cancel_btn = QPushButton(translate(cancel_text))
            self.cancel_btn.setStyleSheet(
                "background: #444; color: #f0f0f0; border-radius: 6px; padding: 4px 12px;"
            )
            self.btn_row.addWidget(self.cancel_btn)
        layout.addLayout(self.btn_row)
        layout.addStretch(1)
        if show_input:
            self.name_input.returnPressed.connect(self.action_btn.click)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        bubble_color = QColor(40, 40, 48)
        border_color = QColor(80, 80, 96)
        painter.setBrush(QBrush(bubble_color))
        painter.setPen(border_color)
        rect = self.rect().adjusted(0, 0, 0, -14)
        painter.drawRoundedRect(rect, 18, 18)
        # Draw triangle for bubble tail, aligned with anchor_btn
        btn = self.anchor_btn
        btn_pos = btn.mapToGlobal(btn.rect().center())
        bubble_pos = self.mapToGlobal(self.rect().topLeft())
        local_x = btn_pos.x() - bubble_pos.x()
        arrow_x = max(rect.left() + 24, min(local_x, rect.right() - 24))
        points = [
            QPoint(arrow_x - 12, rect.bottom()),
            QPoint(arrow_x + 12, rect.bottom()),
            QPoint(arrow_x, rect.bottom() + 14),
        ]
        polygon = QPolygon(points)
        painter.setBrush(QBrush(bubble_color))
        painter.setPen(border_color)
        painter.drawPolygon(polygon)
        painter.end()

    def showEvent(self, event):
        super().showEvent(event)
        self.name_input.setFocus()


class TaskBubble(BubbleWidget):
    def __init__(
        self,
        parent,
        anchor_btn,
        title="Add Task",
        action_text="Add",
        initial_desc="",
        initial_due_date=None,
        projects=None,
        selected_project_id=None,
    ):
        super().__init__(
            parent, title, action_text, anchor_btn, show_input=False, minWidth=550
        )
        # Task description input
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText(translate("Task description"))
        self.desc_input.setText(initial_desc)
        self.desc_input.setStyleSheet(
            "background: #222; color: #f0f0f0; border-radius: 6px; padding: 4px 8px;"
        )
        self.desc_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout().insertWidget(1, self.desc_input)
        # Due date input
        self.due_input = QDateEdit()
        self.due_input.setCalendarPopup(True)
        self.due_input.setDate(initial_due_date or QDate.currentDate())
        self.due_input.setStyleSheet(
            "background: #222; color: #f0f0f0; border-radius: 6px; padding: 4px 8px;"
        )
        self.due_input.setMaximumWidth(140)
        self.btn_row.insertWidget(0, self.due_input)
        # Projects
        self.project_combo = QComboBox()
        self.project_combo.setMinimumWidth(150)
        if projects:
            for pid, name in projects:
                self.project_combo.addItem(name, pid)
            # select the provided project id, or fallback to first
            if selected_project_id is not None:
                idx = self.project_combo.findData(selected_project_id)
                if idx != -1:
                    self.project_combo.setCurrentIndex(idx)
        self.btn_row.insertWidget(1, self.project_combo)
        # add a stretch so buttons stay to the right
        self.btn_row.insertStretch(2, 1)

        # Set focus on description input
        self.desc_input.setFocus()
        self.desc_input.returnPressed.connect(self.action_btn.click)


class TaskWidget(QWidget):
    def __init__(
        self,
        main_window,
        project_name,
        task_id,
        description,
        status,
        due_date,
        close_date,
        creation_date,
        comments=None,
        on_save_comments=None,
    ):
        super().__init__()
        layout = QVBoxLayout()

        # Title/Description row with comment button at the end
        title_row = QHBoxLayout()
        title_label = QLabel(description)
        title_label.setFont(QFont("Arial", 11, QFont.Bold))
        title_label.setStyleSheet("color: #ffffff;")
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        title_row.addWidget(title_label)

        # Comments button (opens CommentBubble)
        comment_btn = QPushButton("💬")
        comment_btn.setStyleSheet("QPushButton { color: green; }") if comments else None
        comment_btn.setToolTip(translate("Comments"))
        comment_btn.setMaximumWidth(36)
        title_row.addWidget(comment_btn)
        layout.addLayout(title_row)

        # Dates and Status
        dates_status_layout = QHBoxLayout()
        dates_status_layout.setContentsMargins(
            0, 0, 0, 0
        )  # Reduce padding for this row
        creation_date_label = QLabel(f"{translate('Created')}: {creation_date}")
        creation_date_label.setAlignment(Qt.AlignCenter)
        creation_date_label.setStyleSheet("color: #cccccc; padding: 0px 2px;")
        due_date_label = QLabel(f"{translate('Due')}: {due_date}")
        due_date_label.setAlignment(Qt.AlignCenter)

        # Colorize due date based on on-time or overdue, using the same colors as the status field
        if status == "open":
            due_date_obj = QDate.fromString(due_date, "yyyy-MM-dd")
            if due_date_obj < QDate.currentDate():
                due_date_label.setStyleSheet(
                    "color: #ff4444; padding: 0px 2px;"
                )  # Overdue (red)
            else:
                due_date_label.setStyleSheet(
                    "color: #ffaa00; padding: 0px 2px;"
                )  # On time (yellow)
        else:
            due_date_label.setStyleSheet("color: #cccccc; padding: 0px 2px;")

        close_date_label = QLabel(f"{translate('Closed')}: {close_date or ''}")
        close_date_label.setAlignment(Qt.AlignCenter)

        # Colorize close date based on adherence to due date if status is complete
        if status == "complete" and close_date:
            close_date_obj = QDate.fromString(close_date, "yyyy-MM-dd")
            due_date_obj = QDate.fromString(due_date, "yyyy-MM-dd")
            if close_date_obj <= due_date_obj:
                close_date_label.setStyleSheet(
                    "color: #00ff00; padding: 0px 2px;"
                )  # On time (green)
            else:
                close_date_label.setStyleSheet(
                    "color: #ff4444; padding: 0px 2px;"
                )  # Late (red)
        else:
            close_date_label.setStyleSheet("color: #cccccc; padding: 0px 2px;")

        status_label = QLabel(f"{translate('Status')}: {translate(status)}")
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet(
            "color: #00ff00; padding: 0px 2px;"
            if status == "complete"
            else "color: #ff4444; padding: 0px 2px;"
            if status == "cancelled"
            else "color: #ffaa00; padding: 0px 2px;"
        )
        project_name_label = QLabel(
            project_name if len(project_name) <= 16 else project_name[:15]
        )
        project_name_label.setAlignment(Qt.AlignCenter)
        project_name_label.setStyleSheet("color: #cccccc; padding: 0px 2px;")

        dates_status_layout.addWidget(creation_date_label)
        dates_status_layout.addWidget(due_date_label)
        dates_status_layout.addWidget(close_date_label)
        dates_status_layout.addWidget(status_label)
        dates_status_layout.addWidget(project_name_label)
        layout.addLayout(dates_status_layout)

        # Separator
        separator = QFrame()
        separator.setStyleSheet("background-color: #cccccc;")
        layout.addWidget(separator)

        self.setLayout(layout)
        self.setStyleSheet(
            "background-color: #333333; border: 1px solid #555555; border-radius: 8px; padding: 10px;"
        )

        # Wire comment button to open bubble
        def _open_comments():
            def _save_and_refresh(text):
                try:
                    if callable(on_save_comments):
                        on_save_comments(task_id, text)
                except Exception:
                    pass

            # Build content as a QLayout (required by BubbleWidgetV2)
            content_layout = QVBoxLayout()
            comment_edit = QTextEdit()
            comment_edit.setPlainText(comments or "")
            comment_edit.setStyleSheet(
                "background: #222; color: #f0f0f0; border-radius: 6px; padding: 6px;"
            )
            content_layout.addWidget(comment_edit)

            # Create the new bubble variant using the layout content. Use top-right anchor
            # to match prior placement (bubble's top-right aligns with button top-right).
            cb = BubbleWidgetV2(
                self,
                main_window,
                content_layout,
                comment_btn,
                anchor_point="top-right",
                minWidth=840,
                minHeight=173,
                on_close=_save_and_refresh,
            )
            # Ensure bubble has the requested size before computing position
            try:
                cb.resize(cb.minimumWidth(), cb.minimumHeight())
            except Exception:
                pass
            cb.show()

        comment_btn.clicked.connect(_open_comments)


class TaskFilterWidget(QWidget):
    def __init__(self, on_filter_selected):
        super().__init__()
        # Read configured default filter from config.ini (language-neutral canonical value)
        try:
            cfg = get_config_parser()
            default_filter = cfg.get("General", "default_filter", fallback="Open")
        except Exception:
            default_filter = "Open"
        self.current_filter = default_filter
        layout = QHBoxLayout()
        layout.setSpacing(10)

        self.sort_combo = QComboBox()
        self.sort_combo.addItem(translate("Creation Date"), "creation")
        self.sort_combo.addItem(translate("Due Date"), "due")
        self.sort_combo.addItem(translate("Status"), "status")
        layout.addWidget(self.sort_combo)
        # Try to initialize sort combo from saved config (default_sort)
        try:
            cfg = get_config_parser()
            saved_sort = cfg.get("General", "default_sort", fallback="creation")
            idx = self.sort_combo.findData(saved_sort)
            if idx != -1:
                self.sort_combo.setCurrentIndex(idx)
        except Exception:
            pass

        # Connect changes to the provided callback (reapplies filters/sort on change)
        self.sort_combo.currentTextChanged.connect(on_filter_selected)

        # Filter buttons
        self.buttons: dict[str, QPushButton] = {}
        filters = ["All", "On Time", "Overdue", "Open", "Finished", "Cancelled"]
        for filter_name in filters:
            button = QPushButton(translate(filter_name))
            button.setCheckable(True)
            button.setStyleSheet(self.get_button_style(False))
            button.clicked.connect(
                lambda checked, name=filter_name: self.on_button_clicked(
                    name, on_filter_selected
                )
            )
            layout.addWidget(button)
            self.buttons[filter_name] = button

        # Apply provided default filter
        if default_filter in self.buttons:
            self.buttons[default_filter].setChecked(True)
            self.buttons[default_filter].setStyleSheet(self.get_button_style(True))
        else:
            # Fallback to Open
            self.buttons["Open"].setChecked(True)
            self.buttons["Open"].setStyleSheet(self.get_button_style(True))

        self.setLayout(layout)

    def on_button_clicked(self, filter_name, on_filter_selected):
        self.current_filter = filter_name
        # Uncheck all buttons except the selected one
        for name, button in self.buttons.items():
            is_selected = name == filter_name
            button.setChecked(is_selected)
            button.setStyleSheet(self.get_button_style(is_selected))

        # Call the callback with the selected filter
        on_filter_selected()

    def get_button_style(self, is_selected):
        if is_selected:
            return (
                "padding: 5px 10px; border-radius: 5px; "
                "background-color: palette(highlight); color: palette(highlightedText);"
            )
        else:
            return (
                "padding: 5px 10px; border-radius: 5px; "
                "background-color: #444; color: #fff;"
            )

    def get_current_filter(self):
        return self.current_filter

    def get_sort_method(self):
        if self.sort_combo:
            return self.sort_combo.currentData()
        return "creation"  # Default sort method


class BubbleWidgetV2(QWidget):
    """
    BubbleWidgetV2: a flexible bubble that accepts arbitrary content and an anchor point.

    Args:
        parent: parent widget
        content: QLayout containing the bubble contents
        anchor_btn: widget used as anchor/reference for positioning
        anchor_point: one of 'top-right','top-center','top-left','bottom-left','bottom-center','bottom-right'
        minWidth/minHeight: minimum geometry for bubble
    """

    def __init__(
        self,
        main_window,
        parent,
        content,
        anchor_btn,
        anchor_point="bottom-right",
        minWidth=240,
        minHeight=170,
        on_close=None,
    ):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumWidth(minWidth)
        self.setMinimumHeight(minHeight)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.main_window = main_window
        self.anchor_btn = anchor_btn
        self._anchor_point: str = anchor_point.lower()
        self._target_pt: Optional[QPoint] = None
        self._top_tail: Optional[bool] = None

        self._tail_size = 10
        self._tail_offset = 16

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(10)

        container = QWidget()
        container.setLayout(content)
        main_layout.addWidget(container)

        main_layout.addStretch(1)
        # store on_close callback
        self._on_close = on_close

    def closeEvent(self, event):
        # If an on_close callback was provided, try to extract a QTextEdit from
        # the bubble contents and pass its text to the callback.
        try:
            if callable(self._on_close):
                # find the first QTextEdit child
                te = self.findChild(QTextEdit)
                if te is not None:
                    self._on_close(te.toPlainText())
        except Exception:
            pass
        super().closeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        bubble_color = QColor(40, 40, 48)
        border_color = QColor(80, 80, 96)
        painter.setBrush(QBrush(bubble_color))
        painter.setPen(border_color)

        rect = (
            self.rect().adjusted(0, self._tail_size, 0, 0)
            if self._top_tail
            else self.rect().adjusted(0, 0, 0, -self._tail_size)
        )
        painter.drawRoundedRect(rect, 12, 12)

        bubble_pos = self.mapToGlobal(rect.topLeft())
        local_x = self._target_pt.x() - bubble_pos.x()
        arrow_x = max(
            rect.left() + self._tail_offset,
            min(local_x, rect.right() - self._tail_offset),
        )

        points = (
            [
                QPoint(int(arrow_x - self._tail_offset / 2), rect.top()),
                QPoint(int(arrow_x + self._tail_offset / 2), rect.top()),
                QPoint(arrow_x, rect.top() - self._tail_size),
            ]
            if self._top_tail
            else [
                QPoint(int(arrow_x + self._tail_offset / 2), rect.bottom()),
                QPoint(int(arrow_x - self._tail_offset / 2), rect.bottom()),
                QPoint(arrow_x, rect.bottom() + self._tail_size),
            ]
        )

        polygon = QPolygon(points)
        painter.setBrush(QBrush(bubble_color))
        painter.setPen(border_color)
        painter.drawPolygon(polygon)
        painter.end()

    def show(self):
        if self.main_window.window().width() - self.width() < 100:
            self.setFixedWidth(self.main_window.window().width() - 100)
        self._target_pt = self._global_anchor_point(self._anchor_point.split("-")[0])

        if self._anchor_point.startswith("top"):
            self._top_tail = True
            y = self._target_pt.y()
        else:
            self._top_tail = False
            y = self._target_pt.y() - self.height()

        if self._anchor_point.endswith("right"):
            x = self._target_pt.x() - self.width() + self._tail_offset
        elif self._anchor_point.endswith("center"):
            x = self._target_pt.x() - (self.width() // 2)
        else:
            x = self._target_pt.x() - self._tail_offset

        self.move(int(x), int(y))

        if not self.main_window.window().frameGeometry().contains(self.frameGeometry()):
            if self._anchor_point.startswith("top"):
                self._target_pt = self._global_anchor_point("bottom")
                y = self._target_pt.y() - self.height()
                self._top_tail = False
            else:
                self._target_pt = self._global_anchor_point("top")
                y = self._target_pt.y()
                self._top_tail = True
            self.move(int(x), int(y))

        super().show()

    def _global_anchor_point(self, side: str) -> QPoint:
        match side:
            case "top":
                return self.anchor_btn.mapToGlobal(
                    QPoint(
                        self.anchor_btn.rect().center().x(),
                        self.anchor_btn.rect().bottom(),
                    )
                )
            case "bottom":
                return self.anchor_btn.mapToGlobal(
                    QPoint(
                        self.anchor_btn.rect().center().x(),
                        self.anchor_btn.rect().top(),
                    )
                )
            case _:
                raise ValueError("Invalid side for anchor_point")
