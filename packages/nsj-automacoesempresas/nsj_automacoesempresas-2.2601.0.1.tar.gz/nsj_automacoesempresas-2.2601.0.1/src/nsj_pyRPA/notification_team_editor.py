from __future__ import annotations

from typing import Optional, List
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QAction,
    QDialog,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QStyle,
)

from nsj_pyRPA.dto.notification_team_dto import NotificationTeamDTO

ICON_PATH = Path(__file__).resolve().parent / "resources" / "Persona.ico"


def persona_icon() -> QIcon:
    if not ICON_PATH.exists():
        return QIcon()
    return QIcon(str(ICON_PATH))


class TeamMembersDialog(QDialog):
    """Dialog that lets the user edit the email list for a team."""

    def __init__(self, team: NotificationTeamDTO, parent=None):
        super().__init__(parent)
        self.setWindowIcon(persona_icon())
        self.team = team
        heading = team.nome or "Equipe sem nome"
        self.setWindowTitle(f"Membros - {heading}")
        self.members_text_value: Optional[str] = None
        self._build_ui()
        self.resize(420, 320)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        toolbar = QToolBar("Ações", self)
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        def themed_icon(name: str, fallback: QStyle.StandardPixmap):
            icon = QIcon.fromTheme(name)
            return icon if not icon.isNull() else self.style().standardIcon(fallback)

        def add_action(text: str, icon_name: str, fallback: QStyle.StandardPixmap, handler):
            act = QAction(themed_icon(icon_name, fallback), text, self)
            act.triggered.connect(handler)
            toolbar.addAction(act)
            button = toolbar.widgetForAction(act)
            if button:
                button.setToolTip("")
            return act

        add_action("Adicionar", "list-add", QStyle.SP_FileDialogNewFolder, self._add_row)
        add_action("Remover", "list-remove", QStyle.SP_TrashIcon, self._remove_selected)
        add_action("Gravar", "document-save", QStyle.SP_DialogApplyButton, self._handle_save)
        add_action("Sair", "system-log-out", QStyle.SP_DialogCloseButton, self.reject)
        layout.addWidget(toolbar)

        info = QLabel("Adicione os e-mails da equipe.")
        info.setWordWrap(True)
        info.setStyleSheet("padding: 8px 12px; font-weight: 600; color: #4c4c4c;")
        layout.addWidget(info)

        self.table = QTableWidget(0, 1, self)
        self.table.setHorizontalHeaderLabels(["E-mail"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked | QAbstractItemView.EditKeyPressed)
        layout.addWidget(self.table)

        self.counter_label = QLabel()
        self.counter_label.setAlignment(Qt.AlignRight)
        self.counter_label.setStyleSheet("padding: 4px 8px; color: #4c4c4c;")
        layout.addWidget(self.counter_label)

        self._populate_table()
        self._apply_style()

    def _apply_style(self):
        self.setStyleSheet(
            """
            QWidget {
                background: #e3e4e8;
                color: #1e1e1e;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
            }
            QToolBar {
                background: #e3e4e8;
                border: none;
                padding: 4px 10px;
                spacing: 8px;
            }
            QTableWidget {
                background: #ffffff;
                alternate-background-color: #f5f5f7;
                gridline-color: #d0d2d8;
                selection-background-color: #cfdcf4;
                selection-color: #151515;
            }
            QHeaderView::section {
                background: #f0f0f2;
                border: 1px solid #d0d2d8;
                padding: 6px;
                font-weight: 600;
                color: #4a4a4a;
            }
            """
        )

    def _populate_table(self):
        emails = [token.strip() for token in self.team.emails.split(",") if token.strip()]
        if not emails:
            self._add_row()
        else:
            for email in emails:
                self._add_row(email)
        self._update_counter()

    def _add_row(self, value: str = ""):
        row = self.table.rowCount()
        self.table.insertRow(row)
        item = QTableWidgetItem(value)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
        self.table.setItem(row, 0, item)
        self.table.setCurrentCell(row, 0)
        self.table.editItem(item)
        self._update_counter()

    def _remove_selected(self):
        row = self.table.currentRow()
        if row < 0:
            return
        self.table.removeRow(row)
        if self.table.rowCount() == 0:
            self._add_row()
        self._update_counter()

    def _update_counter(self):
        emails = self._collect_emails()
        self.counter_label.setText(f"Total de membros: {len(emails)}")

    def _collect_emails(self) -> List[str]:
        emails: List[str] = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if not item:
                continue
            text = item.text().strip()
            if text:
                emails.append(text)
        return emails

    def _handle_save(self):
        emails = self._collect_emails()
        self.members_text_value = ", ".join(emails)
        self.accept()

    def members_text(self) -> str:
        return self.members_text_value if self.members_text_value is not None else self.team.emails
