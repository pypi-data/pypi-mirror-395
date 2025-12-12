"""
Lightweight PyQt5 UI that mirrors the company selection grid used by the CLI.
It now relies on CLI flags to bootstrap database connections so the UI stays
focused on controller‑style interactions and can later share the same service
layer with future REST endpoints.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable, List, Optional

from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QSortFilterProxyModel, QEvent, QRect
from PyQt5.QtGui import QColor, QPalette, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QAction,
    QDialog,
    QHeaderView,
    QLineEdit,
    QMainWindow,
    QTableView,
    QToolBar,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionButton,
    QMessageBox,
)

from nsj_pyRPA.company_editor import CompanyEditorDialog
from nsj_pyRPA.dto.company_dto import CompanyDTO
from nsj_pyRPA.services.bootstrap import CompanyServiceFactory, DatabaseConfig
from nsj_pyRPA.services.company_service import CompanyService

ICON_PATH = Path(__file__).resolve().parent / "resources" / "Persona.ico"


def persona_icon() -> QIcon:
    if not ICON_PATH.exists():
        return QIcon()
    return QIcon(str(ICON_PATH))


class CompanyTableModel(QAbstractTableModel):
    HEADERS = ["Codigo", "Empresa", "Padrao", "Ativo"]

    def __init__(
        self,
        data: Optional[List[CompanyDTO]] = None,
        parent=None,
        active_changed: Optional[Callable[[CompanyDTO, bool], bool]] = None,
    ):
        super().__init__(parent)
        self._rows: List[CompanyDTO] = data or []
        self._active_changed = active_changed

    def rowCount(self, parent=QModelIndex()) -> int:  # type: ignore[override]
        return len(self._rows)

    def columnCount(self, parent=QModelIndex()) -> int:  # type: ignore[override]
        return len(self.HEADERS)

    def data(self, index: QModelIndex, role=Qt.DisplayRole):  # type: ignore[override]
        if not index.isValid():
            return None

        row = self._rows[index.row()]
        column = index.column()

        if role == Qt.DisplayRole:
            if column == 0:
                return row.codigo
            if column == 1:
                return row.nome
            if column == 2 and row.padrao:
                return "\u2605"
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter if column != 1 else Qt.AlignVCenter | Qt.AlignLeft
        if role == Qt.ForegroundRole and column == 2 and row.padrao:
            return Qt.GlobalColor.darkYellow
        if role == Qt.CheckStateRole and column == 3:
            return Qt.Checked if row.ativo else Qt.Unchecked
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.DisplayRole):  # type: ignore[override]
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.HEADERS[section]
        return super().headerData(section, orientation, role)

    def flags(self, index: QModelIndex):  # type: ignore[override]
        if not index.isValid():
            return Qt.ItemIsEnabled
        base = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if index.column() == 3:
            base |= Qt.ItemIsUserCheckable
        return base

    def setData(self, index: QModelIndex, value, role=Qt.EditRole):  # type: ignore[override]
        if not index.isValid() or index.column() != 3 or role != Qt.CheckStateRole:
            return False
        company = self._rows[index.row()]
        desired_state = value == Qt.Checked
        if company.ativo == desired_state:
            return True
        if self._active_changed and not self._active_changed(company, desired_state):
            return False
        company.ativo = desired_state
        self.dataChanged.emit(index, index, [Qt.CheckStateRole])
        return True

    def set_default(self, row: int):
        if row < 0 or row >= len(self._rows):
            return
        for idx, entry in enumerate(self._rows):
            is_default = idx == row
            if entry.padrao != is_default:
                entry.padrao = is_default
                model_index = self.index(idx, 2)
                self.dataChanged.emit(
                    model_index, model_index, [Qt.DisplayRole, Qt.ForegroundRole]
                )

    def update_rows(self, rows: List[CompanyDTO]):
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()

    def company_at(self, row: int) -> CompanyDTO:
        return self._rows[row]


class ContainsFilterProxy(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._needle = ""
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)

    def set_search_term(self, text: str):
        self._needle = text.strip()
        self.invalidateFilter()

    def filterAcceptsRow(self, row: int, parent: QModelIndex) -> bool:  # type: ignore[override]
        if not self._needle:
            return True
        model = self.sourceModel()
        for column in range(model.columnCount()):
            idx = model.index(row, column, parent)
            value = model.data(idx, Qt.DisplayRole)
            if value and self._needle.lower() in str(value).lower():
                return True
        return False


class CenteredCheckDelegate(QStyledItemDelegate):
    """Renders table checkboxes centered and handles toggling without external data deps."""

    def paint(self, painter, option, index):
        if not index.flags() & Qt.ItemIsUserCheckable:
            super().paint(painter, option, index)
            return

        check_rect = self._checkbox_rect(option)
        state = QStyle.State_On if index.data(Qt.CheckStateRole) == Qt.Checked else QStyle.State_Off
        if option.state & QStyle.State_Enabled:
            state |= QStyle.State_Enabled

        opt = QStyleOptionButton()
        opt.state = state
        opt.rect = check_rect
        QApplication.style().drawControl(QStyle.CE_CheckBox, opt, painter)

    def editorEvent(self, event, model, option, index):
        if not index.flags() & Qt.ItemIsUserCheckable:
            return False

        event_type = event.type()
        if event_type == QEvent.MouseButtonPress:
            # Swallow presses so we only toggle once on release.
            return True

        if event_type == QEvent.MouseButtonRelease:
            if event.button() != Qt.LeftButton:
                return False
        elif event_type == QEvent.MouseButtonDblClick:
            return True
        elif event_type == QEvent.KeyPress:
            if event.key() not in (Qt.Key_Space, Qt.Key_Select):
                return False
        else:
            return False

        current = index.data(Qt.CheckStateRole)
        new_state = Qt.Unchecked if current == Qt.Checked else Qt.Checked
        return model.setData(index, new_state, Qt.CheckStateRole)

    @staticmethod
    def _checkbox_rect(option):
        indicator = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, option)
        x = option.rect.x() + (option.rect.width() - indicator.width()) // 2
        y = option.rect.y() + (option.rect.height() - indicator.height()) // 2
        return QRect(x, y, indicator.width(), indicator.height())


class MainWindow(QMainWindow):
    def __init__(self, company_service: CompanyService, dispose_callback: Callable[[], None]):
        super().__init__()
        self.setWindowTitle("Automacao - Empresas")
        self.setWindowIcon(persona_icon())
        self.company_service = company_service
        self._dispose_callback = dispose_callback
        self._create_toolbar()
        self._create_table()
        self._set_theme()
        self._load_companies()

    def _create_toolbar(self):
        toolbar = QToolBar("Ações", self)
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        def themed_icon(name: str, fallback: QStyle.StandardPixmap):
            icon = QIcon.fromTheme(name)
            return icon if not icon.isNull() else self.style().standardIcon(fallback)

        def action(text: str, icon_name: str, fallback: QStyle.StandardPixmap, handler):
            act = QAction(themed_icon(icon_name, fallback), text, self)
            act.triggered.connect(handler)
            return act

        toolbar.addAction(action("Marcar padrão", "emblem-favorite", QStyle.SP_DialogApplyButton, self._mark_default))
        toolbar.addAction(action("Copiar configuração", "edit-copy", QStyle.SP_FileDialogNewFolder, self._copy_config))
        toolbar.addAction(action("Editar", "system-file-manager", QStyle.SP_FileDialogDetailedView, self._edit_selected))
        toolbar.addAction(action("Atualizar", "sync-synchronizing", QStyle.SP_BrowserReload, self._load_companies))

        self.search_action = action("Localizar", "edit-find", QStyle.SP_FileDialogContentsView, self._toggle_search)
        toolbar.addAction(self.search_action)

        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText("Localizar")
        self.search_field.setClearButtonEnabled(True)
        self.search_field.setFixedWidth(self.width() * self.width()//5)
        self.search_field.textChanged.connect(self._handle_search_text)
        self.search_widget_action = toolbar.addWidget(self.search_field)
        self._set_search_visibility(False)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)
        toolbar.addAction(action("Sair", "system-log-out", QStyle.SP_DialogCloseButton, self.close))

        self.addToolBar(toolbar)

    def _create_table(self):
        container = QWidget(self)
        layout = QVBoxLayout(container)
        # layout.setContentsMargins(12, 12, 12, 12)

        self.table = QTableView(container)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.table.verticalHeader().setVisible(False)

        self.model = CompanyTableModel([], self, self._handle_active_toggle)
        self.proxy = ContainsFilterProxy(self)
        self.proxy.setSourceModel(self.model)
        self.table.setModel(self.proxy)
        self.checkbox_delegate = CenteredCheckDelegate(self.table)
        self.table.setItemDelegateForColumn(3, self.checkbox_delegate)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
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
            QLineEdit {
                background: #ffffff;
                border: 1px solid #b7b8bc;
                border-radius: 4px;
                padding: 4px 6px;
                min-width: 200px;
                color: #1e1e1e;
            }
            QLineEdit:focus {
                border: 1px solid #3b7bd4;
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
            }
            QStatusBar {
                background: #e5e6ea;
                color: #2a2a2a;
                border-top: 1px solid #cbcdd3;
            }
            """
        )

    def _handle_search_text(self, text: str):
        self.proxy.set_search_term(text)
        self._update_status()

    def _toggle_search(self):
        visible = not self.search_field.isVisible()
        self._set_search_visibility(visible)

    def _set_search_visibility(self, visible: bool):
        self.search_field.setVisible(visible)
        if hasattr(self, "search_widget_action"):
            self.search_widget_action.setVisible(visible)
        if visible:
            self.search_field.setFocus()
        else:
            self.search_field.clear()
            if hasattr(self, "proxy"):
                self.proxy.set_search_term("")
                self._update_status()

    def _mark_default(self):
        index = self.table.selectionModel().currentIndex()
        if not index.isValid():
            QMessageBox.information(self, "Automação - Empresas", "Selecione uma empresa para definir como padrão")
            return
        source_index = self.proxy.mapToSource(index)
        company = self.model.company_at(source_index.row())
        if not company.automacaoempresa:
            QMessageBox.information(self, "Automação - Empresas", "Empresa sem automação configurada")
            return
        try:
            self.company_service.set_default_company(company.codigo)
        except Exception as exc:
            self._show_error("Erro ao marcar padrao", str(exc))
            return
        QMessageBox.information(self, "Automação - Empresas", f"{company.nome} marcada como padrão")
        self._load_companies()

    def _copy_config(self):
        # Placeholder for future business logic
        QMessageBox.information(self, "Automação - Empresas", "Copiar configuração ainda não implementado")

    def _edit_selected(self):
        index = self.table.selectionModel().currentIndex()
        if not index.isValid():
            QMessageBox.information(self, "Automação - Empresas", "Selecione uma empresa para editar")
            return
        source_index = self.proxy.mapToSource(index)
        company = self.model.company_at(source_index.row())
        if not company.automacaoempresa:
            try:
                company = self.company_service.ensure_company_automation(company)
                # refresh local model reference
                self.model._rows[source_index.row()] = company
            except Exception as exc:
                self._show_error("Erro ao preparar automacao", str(exc))
                return
        try:
            settings = self.company_service.get_company_settings(company.automacaoempresa)
        except Exception as exc:
            self._show_error("Erro ao carregar configuracoes", str(exc))
            return
        try:
            assigned_team = self.company_service.get_assigned_notification_team(company.automacaoempresa)
            available_teams = self.company_service.list_notification_teams()
        except Exception as exc:
            self._show_error("Erro ao carregar equipes", str(exc))
            return
        dialog = CompanyEditorDialog(company, settings, assigned_team, available_teams, self)
        if dialog.exec() == QDialog.Accepted and dialog.updated_settings:
            try:
                self.company_service.save_company_settings(dialog.updated_settings)
                updated_company = self.company_service.update_company_preferences(
                    company,
                    dialog.updated_use_default,
                    dialog.updated_notified_teams,
                )
                self.company_service.save_notification_team_assignment(
                    company.automacaoempresa,
                    dialog.updated_team_id,
                )
            except Exception as exc:
                self._show_error("Erro ao salvar configuracoes", str(exc))
                return
            company.use_default = updated_company.use_default
            company.notified_teams = dialog.updated_notified_teams
            QMessageBox.information(self, "Automação - Empresas", f"Configurações salvas para {company.nome}")

    def _handle_active_toggle(self, company: CompanyDTO, ativo: bool) -> bool:
        try:
            updated = self.company_service.set_company_active(company, ativo)
        except Exception as exc:
            self._show_error("Erro ao atualizar empresa", str(exc))
            return False
        company.ativo = updated.ativo
        self._update_status()
        return True

    def _load_companies(self):
        try:
            companies = self.company_service.list_companies()
        except Exception as exc:
            self._show_error("Erro ao carregar empresas", str(exc))
            return
        companies = sorted(companies, key=lambda dto: dto.codigo)
        self.model.update_rows(companies)
        self._update_status()

    def _show_error(self, title: str, message: str):
        QMessageBox.critical(self, title, message)

    def _update_status(self):
        pass

    def closeEvent(self, event):
        try:
            self._dispose_callback()
        finally:
            super().closeEvent(event)


def _parse_cli_args(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(description="Automacao - Empresas UI")
    parser.add_argument(
        "--bd-nome",
        "--bd_nome",
        dest="bd_nome",
        default="integratto2_dev",
        help="Nome do banco (default: integratto2_dev)",
    )
    parser.add_argument(
        "--bd-user",
        "--bd_user",
        dest="bd_user",
        default="postgres",
        help="Usuario base (default: postgres)",
    )
    parser.add_argument(
        "--bd-senha",
        "--bd_senha",
        dest="bd_senha",
        default="postgres",
        help="Senha do usuario (default: postgres)",
    )
    parser.add_argument(
        "--bd-host",
        "--bd_host",
        dest="bd_host",
        default="localhost",
        help="Host do banco (default: localhost)",
    )
    parser.add_argument(
        "--bd-porta",
        "--bd_porta",
        dest="bd_porta",
        default="5433",
        help="Porta do banco (default: 5433)",
    )
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
    factory = CompanyServiceFactory(config)
    try:
        service = factory.build()
    except Exception as exc:
        print(f"Erro ao inicializar servico: {exc}", file=sys.stderr)
        return 1

    qt_argv = [sys.argv[0]] + qt_args
    app = QApplication(qt_argv)
    _apply_light_palette(app)
    window = MainWindow(service, factory.dispose)
    window.resize(900, 500)
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
