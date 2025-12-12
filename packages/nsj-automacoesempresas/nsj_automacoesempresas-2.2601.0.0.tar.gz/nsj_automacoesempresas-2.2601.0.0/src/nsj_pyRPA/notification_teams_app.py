"""
PySide6 UI that mirrors the Windows mockup for notification teams management.
Follows the same UI -> service -> repository flow already used by company_admin.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable, List, Optional

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QAction, QColor, QPalette, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QHeaderView,
    QMainWindow,
    QMessageBox,
    QTableView,
    QToolBar,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QStyle,
)

from nsj_pyRPA.dto.notification_team_dto import NotificationTeamDTO
from nsj_pyRPA.notification_team_editor import TeamMembersDialog
from nsj_pyRPA.services.bootstrap import DatabaseConfig, NotificationTeamServiceFactory
from nsj_pyRPA.services.notification_team_service import NotificationTeamService

ICON_PATH = Path(__file__).resolve().parent / "resources" / "Persona.ico"


def persona_icon() -> QIcon:
    if not ICON_PATH.exists():
        return QIcon()
    return QIcon(str(ICON_PATH))


class NotificationTeamTableModel(QAbstractTableModel):
    HEADERS = ["Código", "Grupo de destinatários", "E-mails", "Destinatários"]
    CODE_COL = 0
    NAME_COL = 1
    EMAIL_COL = 2
    MEMBERS_COL = 3

    def __init__(self, rows: Optional[List[NotificationTeamDTO]] = None, parent=None):
        super().__init__(parent)
        self._rows = rows or []
        self._dirty_flags = [False] * len(self._rows)
        self._new_flags = [dto.equipe_id is None for dto in self._rows]
        self._editing_enabled = False

    def rowCount(self, parent=QModelIndex()) -> int:  # type: ignore[override]
        return len(self._rows)

    def columnCount(self, parent=QModelIndex()) -> int:  # type: ignore[override]
        return len(self.HEADERS)

    def data(self, index: QModelIndex, role=Qt.DisplayRole):  # type: ignore[override]
        if not index.isValid():
            return None

        team = self._rows[index.row()]
        column = index.column()

        if role in (Qt.DisplayRole, Qt.EditRole):
            if column == self.CODE_COL:
                return team.codigo
            if column == self.NAME_COL:
                return team.nome
            if column == self.EMAIL_COL:
                return team.emails
            if column == self.MEMBERS_COL:
                return str(team.membros)
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter if column in (self.CODE_COL, self.MEMBERS_COL) else Qt.AlignVCenter | Qt.AlignLeft
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.HEADERS[section]
        return super().headerData(section, orientation, role)

    def update_rows(self, rows: List[NotificationTeamDTO]):
        self.beginResetModel()
        self._rows = rows
        self._dirty_flags = [False] * len(rows)
        self._new_flags = [dto.equipe_id is None for dto in rows]
        self._editing_enabled = False
        self.endResetModel()

    def row_at(self, index: int) -> NotificationTeamDTO:
        if index < 0 or index >= len(self._rows):
            raise IndexError("Row out of range")
        return self._rows[index]

    def index_of_code(self, codigo: str) -> int:
        for idx, team in enumerate(self._rows):
            if team.codigo == codigo:
                return idx
        return -1

    def add_empty_row(self) -> int:
        row_position = len(self._rows)
        self.beginInsertRows(QModelIndex(), row_position, row_position)
        self._rows.append(NotificationTeamDTO(codigo="", nome="", emails="", membros=0, equipe_id=None))
        self._dirty_flags.append(True)
        self._new_flags.append(True)
        self.endInsertRows()
        return row_position

    def setData(self, index: QModelIndex, value, role=Qt.EditRole):  # type: ignore[override]
        if not index.isValid() or role != Qt.EditRole:
            return False
        row = index.row()
        column = index.column()
        team = self._rows[row]
        text = str(value or "")

        if column == self.CODE_COL:
            team.codigo = text.strip()
        elif column == self.NAME_COL:
            team.nome = text
        else:
            return False

        self._dirty_flags[row] = True
        self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
        return True

    def flags(self, index: QModelIndex):  # type: ignore[override]
        base = Qt.ItemIsSelectable | Qt.ItemIsEnabled
        if not index.isValid():
            return base
        row = index.row()
        editable_columns = (self.CODE_COL, self.NAME_COL)
        if (
            self._editing_enabled
            and row < len(self._new_flags)
            and self._new_flags[row]
            and index.column() in editable_columns
        ):
            return base | Qt.ItemIsEditable
        return base

    def dirty_rows(self) -> List[NotificationTeamDTO]:
        return [
            dto
            for dto, dirty in zip(self._rows, self._dirty_flags)
            if dirty
        ]

    def is_new_row(self, row: int) -> bool:
        if row < 0 or row >= len(self._new_flags):
            return False
        return self._new_flags[row]

    def remove_row(self, row: int) -> None:
        if row < 0 or row >= len(self._rows):
            return
        self.beginRemoveRows(QModelIndex(), row, row)
        self._rows.pop(row)
        self._dirty_flags.pop(row)
        self._new_flags.pop(row)
        self.endRemoveRows()

    def set_editing_enabled(self, enabled: bool) -> None:
        if self._editing_enabled == enabled:
            return
        self._editing_enabled = enabled
        self.layoutChanged.emit()

    def editing_enabled(self) -> bool:
        return self._editing_enabled

    def update_emails(self, row: int, emails: str) -> None:
        if row < 0 or row >= len(self._rows):
            return
        self._apply_email_update(row, emails)

    def _apply_email_update(self, row: int, emails: str) -> None:
        team = self._rows[row]
        team.emails = emails
        team.membros = team.members_from_emails()
        self._dirty_flags[row] = True
        email_index = self.index(row, self.EMAIL_COL)
        members_index = self.index(row, self.MEMBERS_COL)
        self.dataChanged.emit(email_index, email_index, [Qt.DisplayRole, Qt.EditRole])
        self.dataChanged.emit(members_index, members_index, [Qt.DisplayRole])


class NotificationTeamsWindow(QMainWindow):
    def __init__(
        self,
        service: NotificationTeamService,
        dispose_callback: Callable[[], None],
    ):
        super().__init__()
        self.service = service
        self._dispose_callback = dispose_callback
        self.setWindowTitle("Automação - Destinatários de notificação")
        self.setWindowIcon(persona_icon())
        self._create_toolbar()
        self._create_table()
        self._set_theme()
        self._load_teams()

    def _create_toolbar(self):
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
        add_action("Criar", "list-add", QStyle.SP_FileDialogNewFolder, self._create_team)
        add_action("Gravar", "document-save", QStyle.SP_DialogApplyButton, self._save_changes)
        add_action("Cancelar", "edit-clear", QStyle.SP_DialogCancelButton, self._reload)
        add_action("Excluir", "user-trash", QStyle.SP_TrashIcon, self._delete_team)
        add_action("Destinatários", "emblem-shared", QStyle.SP_FileDialogContentsView, self._edit_members)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)
        add_action("Sair", "system-log-out", QStyle.SP_DialogCloseButton, self.close)
        self.addToolBar(toolbar)

    def _create_table(self):
        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(12, 12, 12, 12)

        self.table = QTableView(container)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)

        info = QLabel("Gerencie as destinatários que receberão notificações dos processos.")
        info.setStyleSheet("font-weight: 600; color: #4c4c4c; margin-bottom: 6px;")
        layout.addWidget(info)

        self.model = NotificationTeamTableModel([], self)
        self.table.setModel(self.model)
        self.table.setEditTriggers(QTableView.AllEditTriggers)
        self.table.clicked.connect(self._handle_table_click)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        layout.addWidget(self.table)
        self.setCentralWidget(container)

    def _set_theme(self):
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
                border-bottom: 1px solid #bfc1c7;
                border-top: 1px solid #bfc1c7;
            }
            QTableView {
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
                border-top: 1px solid #bfc1c7;
            }
            QStatusBar {
                background: #e5e6ea;
                color: #2a2a2a;
                border-top: 1px solid #cbcdd3;
            }
            """
        )

    def _selected_index(self) -> Optional[int]:
        selection = self.table.selectionModel()
        if not selection:
            return None
        index = selection.currentIndex()
        if not index.isValid():
            return None
        return index.row()

    def _selected_team(self) -> Optional[NotificationTeamDTO]:
        row = self._selected_index()
        if row is None:
            return None
        try:
            return self.model.row_at(row)
        except IndexError:
            return None

    def _create_team(self):
        if not self.model.editing_enabled():
            self.model.set_editing_enabled(True)
        row = self.model.add_empty_row()
        self.table.selectRow(row)
        index = self.model.index(row, NotificationTeamTableModel.CODE_COL)
        self.table.scrollTo(index)
        self.table.edit(index)
        # informational banner removed per new UX guidelines

    def _save_changes(self):
        dirty_rows = self.model.dirty_rows()
        if not dirty_rows:
            return
        saved = 0
        for team in dirty_rows:
            try:
                self.service.save_team(team)
                saved += 1
            except Exception as exc:
                self._show_error("Erro ao salvar destinatário(s)", str(exc))
                self._load_teams()
                self.model.set_editing_enabled(False)
                return
        self._load_teams()
        self.model.set_editing_enabled(False)

    def _delete_team(self):
        row = self._selected_index()
        if row is None:
            return
        team = self.model.row_at(row)
        if self.model.is_new_row(row) and not team.equipe_id:
            self.model.remove_row(row)
            # self._update_status()
            if not self.model.dirty_rows():
                self.model.set_editing_enabled(False)
            return
        answer = QMessageBox.question(
            self,
            "Excluir destinatário",
            f"Confirma a exclusão do destinatário {team.nome} ({team.codigo})?",
        )
        if answer != QMessageBox.Yes:
            return
        try:
            self.service.delete_team(team.codigo)
        except Exception as exc:
            self._show_error("Erro ao excluir destinatário(s)", str(exc))
            return
        self._load_teams()

    def _reload(self):
        self._load_teams()
        self.model.set_editing_enabled(False)

    def _edit_members(self):
        row = self._selected_index()
        if row is None:
            return
        self._open_members_dialog(row)

    def _handle_table_click(self, index: QModelIndex):
        if not index.isValid():
            return
        if index.column() != NotificationTeamTableModel.EMAIL_COL:
            return
        row = index.row()
        if self.model.is_new_row(row):
            self._open_members_dialog(row)

    def _open_members_dialog(self, row: int):
        try:
            team = self.model.row_at(row)
        except IndexError:
            return
        dialog = TeamMembersDialog(team, self)
        if dialog.exec() != QDialog.Accepted:
            return
        new_emails = dialog.members_text()
        self.model.update_emails(row, new_emails)

    def _load_teams(self, select_code: Optional[str] = None):
        try:
            teams = self.service.list_teams()
        except Exception as exc:
            self._show_error("Erro ao carregar destinatários", str(exc))
            return
        self.model.update_rows(sorted(teams, key=lambda dto: dto.codigo))
        if select_code:
            row = self.model.index_of_code(select_code)
            if row >= 0:
                self.table.selectRow(row)

    def _show_error(self, title: str, message: str):
        QMessageBox.critical(self, title, message)


    def closeEvent(self, event):
        try:
            self._dispose_callback()
        finally:
            super().closeEvent(event)


def _parse_cli_args(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(description="Automação - Destinatários de notificação UI")
    parser.add_argument("--bd-nome", dest="bd_nome", default="integratto2_dev", help="Nome do banco")
    parser.add_argument("--bd-user", dest="bd_user", default="postgres", help="Usuário base")
    parser.add_argument("--bd-senha", dest="bd_senha", default="postgres", help="Senha")
    parser.add_argument("--bd-host", dest="bd_host", default="localhost", help="Host")
    parser.add_argument("--bd-porta", dest="bd_porta", default="5433", help="Porta")
    return parser.parse_known_args(argv)


def main(argv: Optional[List[str]] = None):
    args, qt_args = _parse_cli_args(argv)
    config = DatabaseConfig(
        database=args.bd_nome,
        user=args.bd_user,
        password=args.bd_senha,
        host=args.bd_host,
        port=args.bd_porta,
    )
    factory = NotificationTeamServiceFactory(config)
    try:
        service = factory.build()
    except Exception as exc:
        print(f"Erro ao inicializar serviço: {exc}", file=sys.stderr)
        return 1

    qt_argv = [sys.argv[0]] + qt_args
    app = QApplication(qt_argv)
    _apply_light_palette(app)
    window = NotificationTeamsWindow(service, factory.dispose)
    window.resize(800, 420)
    window.show()
    exit_code = app.exec()
    factory.dispose()
    return exit_code


def _apply_light_palette(app: QApplication) -> None:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#f2f2f4"))
    palette.setColor(QPalette.Base, QColor("#f2f2f4"))
    palette.setColor(QPalette.AlternateBase, QColor("#f5f5f7"))
    palette.setColor(QPalette.Text, QColor("#1e1e1e"))
    palette.setColor(QPalette.WindowText, QColor("#1e1e1e"))
    palette.setColor(QPalette.Button, QColor("#e3e4e8"))
    palette.setColor(QPalette.ButtonText, QColor("#1e1e1e"))
    palette.setColor(QPalette.Highlight, QColor("#3b7bd4"))
    palette.setColor(QPalette.HighlightedText, QColor("#f2f2f4"))
    app.setPalette(palette)


if __name__ == "__main__":
    raise SystemExit(main())
