"""
Company settings dialog used by the Qt front-end.
It receives DTO data from the service layer and simply returns user edits so
controllers can persist them via the shared business services.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Dict, List, Optional

from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QScrollArea,
    QSpinBox,
    QTabWidget,
    QTimeEdit,
    QToolBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QStyle,
)

from nsj_pyRPA.dto.company_dto import CompanyDTO, CompanySettingsDTO, ScheduleConfig
from nsj_pyRPA.dto.notification_team_dto import NotificationTeamDTO
from nsj_pyRPA.resources.automation_types import (
    AUTOMATION_TYPES,
    automation_default_values,
    automation_type_label
)

ICON_PATH = Path(__file__).resolve().parent / "resources" / "Persona.ico"


def persona_icon() -> QIcon:
    if not ICON_PATH.exists():
        return QIcon()
    return QIcon(str(ICON_PATH))


@dataclass
class SectionDefinition:
    label: str
    automation_type: str


@dataclass
class SectionWidgets:
    group: QGroupBox
    enabled: QCheckBox
    frequency: QComboBox
    day_month: Optional[QSpinBox]
    day_month_row: Optional[QWidget]
    day_week: Optional[QComboBox]
    day_week_row: Optional[QWidget]
    time: QTimeEdit
    time_row: QWidget
    summary: QLabel
    allowed_frequencies: List[str]


class CompanyEditorDialog(QDialog):
    def __init__(
        self,
        company: CompanyDTO,
        settings: CompanySettingsDTO,
        assigned_team: Optional[NotificationTeamDTO] = None,
        available_teams: Optional[List[NotificationTeamDTO]] = None,
        parent=None,
    ):
        super().__init__(parent)
        self.setWindowIcon(persona_icon())
        self.company = company
        self.company_ref = company.automacaoempresa
        self.settings = settings
        self.updated_settings: Optional[CompanySettingsDTO] = None
        self.updated_use_default: bool = company.use_default
        self.updated_notified_teams: str = company.notified_teams
        self.updated_team_id: Optional[str] = assigned_team.equipe_id if assigned_team else None
        self.selected_team: Optional[NotificationTeamDTO] = assigned_team
        self._available_teams: List[NotificationTeamDTO] = sorted(
            available_teams or [],
            key=lambda dto: (dto.codigo or "").lower(),
        )
        self.combo_days = ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
        self.combo_frequency = ["Mensalmente", "Semanalmente", "Diariamente"]
        self.section_list = AUTOMATION_TYPES
        self.section_defs = list()
        for i in self.section_list: 
            self.section_defs.append(SectionDefinition(automation_type_label(i), i))
        self.sections: Dict[str, SectionWidgets] = {}
        self.setWindowTitle(f"Editar Empresa - {company.nome}")
        self.resize(1200, 500)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        toolbar = QToolBar("Ações", self)
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        toolbar.setIconSize(toolbar.iconSize())

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

        add_action("Gravar", "document-save", QStyle.SP_DialogApplyButton, self._handle_save)
        add_action("Cancelar", "edit-clear", QStyle.SP_DialogCancelButton, self.reject)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)
        add_action("Sair", "system-log-out", QStyle.SP_DialogCloseButton, self.close)
        layout.addWidget(toolbar)

        info = QLabel("Itens e periodicidade (marcados = automatizados; desmarcados = execução manual)")
        info.setStyleSheet("padding: 6px 12px; font-weight: 600; color: #4c4c4c;")
        layout.addWidget(info)

        tabs = QTabWidget(self)
        tabs.setTabPosition(QTabWidget.South)
        tabs.setStyleSheet(
            """
            QTabBar::tab {
                background: #e3e4e8;
                border: 1px solid #bfc1c7;
                padding: 6px 14px;
                margin: 0 2px;
                min-width: 140px;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                color: #1e1e1e;
            }
            QTabWidget::pane {
                border-top: 1px solid #2b2b2b;
            }
            """
        )
        tabs.addTab(self._build_schedule_tab(), "Cálculo Folhas")
        tabs.addTab(self._placeholder_tab("Demais cálculos em desenvolvimento"), "Demais Cálculos")
        tabs.addTab(self._placeholder_tab("Configurações do E-social em desenvolvimento"), "E-social")

        layout.addWidget(tabs)

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
                border-bottom: 1px solid #bfc1c7;
                padding: 4px 10px;
                spacing: 8px;
            }
            """
        )

    def _build_schedule_tab(self) -> QWidget:
        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        header_row = QHBoxLayout()
        header_row.addWidget(self._build_default_section(), 1)
        header_row.addWidget(self._build_notifications_section(), 1)
        layout.addLayout(header_row)

        sections_grid = QGridLayout()
        sections_grid.setSpacing(12)
        sections_grid.setColumnStretch(0, 1)
        sections_grid.setColumnStretch(1, 1)
        sections_grid.setContentsMargins(0, 0, 0, 0)
        for idx, definition in enumerate(self.section_defs):
            section_widget = self._build_schedule_section(definition)
            sections_grid.addWidget(section_widget, idx // 2, idx % 2)
        layout.addLayout(sections_grid)
        layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)
        return scroll

    def _open_team_selector(self):
        if not self._available_teams:
            QMessageBox.information(
                self,
                "Destinatários notificados",
                "Nenhum grupo de destinatários cadastrado. Cadastre destinatários antes de vinculá-los.",
            )
            return
        dialog = NotificationTeamSelectorDialog(
            self._available_teams,
            self.selected_team,
            self,
        )
        if dialog.exec() == QDialog.Accepted and dialog.selected_team:
            self._set_selected_team(dialog.selected_team)

    def _selected_team_label(self) -> str:
        if not self.selected_team:
            return ""
        base = f"{self.selected_team.codigo} - {self.selected_team.nome}"
        if self.selected_team.membros:
            return f"{base} ({self.selected_team.membros} membros)"
        return base

    def _set_selected_team(self, team: Optional[NotificationTeamDTO]) -> None:
        self.selected_team = team
        self.updated_team_id = team.equipe_id if team else None
        if hasattr(self, "notified_teams_edit"):
            self.notified_teams_edit.setText(self._selected_team_label())
        if hasattr(self, "clear_team_btn"):
            self.clear_team_btn.setEnabled(team is not None)

    def _clear_selected_team(self) -> None:
        self._set_selected_team(None)

    def _build_default_section(self) -> QGroupBox:
        box = QGroupBox("Configuração padrão")
        box.setStyleSheet("QGroupBox { font-weight: 600; }")
        layout = QHBoxLayout(box)
        layout.setContentsMargins(12, 8, 12, 8)
        self.use_default_cb = QCheckBox()
        self.use_default_cb.setChecked(self.company.use_default)
        layout.addWidget(self.use_default_cb)
        layout.addWidget(QLabel("Usar configuração da empresa marcada como padrão"))
        layout.addStretch()
        return box

    def _build_notifications_section(self) -> QGroupBox:
        box = QGroupBox("Destinatários notificados")
        form = QHBoxLayout(box)
        form.setContentsMargins(12, 8, 12, 8)
        initial_team_text = self._selected_team_label() or self.company.notified_teams
        self.notified_teams_edit = QLineEdit(initial_team_text)
        self.notified_teams_edit.setReadOnly(True)
        self.notified_teams_edit.setPlaceholderText("Selecione um destinatário para notificações")
        self.notified_teams_edit.setStyleSheet("background: #f6f6f6;")
        form.addWidget(self.notified_teams_edit, 1)

        icon_users = QIcon.fromTheme("system-users", self.style().standardIcon(QStyle.SP_FileDialogListView))
        teams_btn = QToolButton()
        teams_btn.setIcon(icon_users)
        teams_btn.setToolTip("")
        teams_btn.setCursor(Qt.PointingHandCursor)
        teams_btn.clicked.connect(self._open_team_selector)
        form.addWidget(teams_btn)

        icon_clear = QIcon.fromTheme("edit-clear", self.style().standardIcon(QStyle.SP_DialogResetButton))
        self.clear_team_btn = QToolButton()
        self.clear_team_btn.setIcon(icon_clear)
        self.clear_team_btn.setToolTip("")
        self.clear_team_btn.setCursor(Qt.PointingHandCursor)
        self.clear_team_btn.clicked.connect(self._clear_selected_team)
        self.clear_team_btn.setEnabled(self.selected_team is not None)
        form.addWidget(self.clear_team_btn)
        return box

    def _schedule_for(self, automation_type: str) -> ScheduleConfig:
        defaults = automation_default_values(automation_type)
        schedule = self.settings.schedules.get(automation_type)
        allowed = list(defaults["allowed_frequencies"])
        if schedule:
            if schedule.allowed_frequencies:
                return schedule
            return replace(schedule, allowed_frequencies=allowed)
        return ScheduleConfig(
            enabled=defaults["enabled"],
            frequency=defaults["frequency"],
            day_of_month=defaults["day_of_month"],
            weekday=defaults["weekday"],
            time=defaults["time"],
            allowed_frequencies=allowed,
        )

    def _build_schedule_section(self, definition: SectionDefinition) -> QGroupBox:
        config = self._schedule_for(definition.automation_type)
        box = QGroupBox()
        box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        box.setStyleSheet(
            "QGroupBox { background: #ffffff; border: 1px solid #d0d2d8; padding: 6px 10px; }"
        )
        form = QVBoxLayout(box)
        form.setSpacing(4)
        form.setContentsMargins(6, 4, 6, 4)

        header = QHBoxLayout()
        enabled_cb = self._styled_checkbox()
        enabled_cb.setChecked(config.enabled)
        header.addWidget(enabled_cb)
        section_label = QLabel(definition.label)
        section_label.setStyleSheet("font-weight: 600;")
        header.addWidget(section_label)
        header.addStretch()
        summary_label = self._schedule_summary_label()
        summary_label.setStyleSheet("color: #4c4c4c; font-weight: 600;")
        header.addWidget(summary_label)
        form.addLayout(header)

        allowed_options = config.allowed_frequencies or self.combo_frequency
        allowed_options = list(allowed_options)
        current_frequency = config.frequency if config.frequency in allowed_options else allowed_options[0]
        frequency_combo = self._combo(allowed_options, current_frequency)
        control_row = QHBoxLayout()
        control_row.setSpacing(12)

        freq_field = self._inline_field("Executar:", frequency_combo)
        freq_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        control_row.addWidget(freq_field, 1)
        show_day_month = "Mensalmente" in allowed_options
        show_day_week = "Semanalmente" in allowed_options

        day_month = None
        day_month_row = None
        if show_day_month:
            day_month = QSpinBox()
            day_month.setRange(1, 31)
            day_month.setValue(config.day_of_month or 1)
            day_month_row = self._inline_field("Dia do mês:", day_month)
            control_row.addWidget(day_month_row, 1)

        day_week = None
        day_week_row = None
        if show_day_week:
            day_week = self._combo(self.combo_days, config.weekday or "Segunda")
            day_week_row = self._inline_field("Dia da semana:", day_week)
            control_row.addWidget(day_week_row, 1)

        time_edit = self._time_edit(config.time)
        time_row = self._inline_field("Horário:", time_edit)
        control_row.addWidget(time_row, 1)

        form.addLayout(control_row)

        widgets = SectionWidgets(
            group=box,
            enabled=enabled_cb,
            frequency=frequency_combo,
            day_month=day_month,
            day_month_row=day_month_row,
            day_week=day_week,
            day_week_row=day_week_row,
            time=time_edit,
            time_row=time_row,
            summary=summary_label,
            allowed_frequencies=allowed_options,
        )
        key = definition.automation_type
        self.sections[key] = widgets
        self._register_section_signals(key, widgets)
        self._apply_section_enabled_state(key)
        return box

    def _register_section_signals(self, key: str, widgets: SectionWidgets) -> None:
        widgets.enabled.toggled.connect(lambda checked, k=key: self._apply_section_enabled_state(k))
        widgets.frequency.currentTextChanged.connect(lambda value, k=key: self._handle_frequency_change(k, value))
        if widgets.day_month is not None:
            widgets.day_month.valueChanged.connect(lambda _=0, k=key: self._update_schedule_summary(k))
        if widgets.day_week is not None:
            widgets.day_week.currentTextChanged.connect(lambda _=0, k=key: self._update_schedule_summary(k))
        widgets.time.timeChanged.connect(lambda _=0, k=key: self._update_schedule_summary(k))

    def _placeholder_tab(self, text: str) -> QWidget:
        tab = QWidget(self)
        layout = QVBoxLayout(tab)
        label = QLabel(text)
        label.setStyleSheet("color: #666;")
        layout.addWidget(label, alignment=Qt.AlignTop)
        layout.addStretch()
        return tab

    def _combo(self, values, current):
        combo = QComboBox()
        combo.addItems(values)
        idx = combo.findText(current)
        if idx >= 0:
            combo.setCurrentIndex(idx)
        combo.setMinimumWidth(130)
        return combo

    def _labeled_field(self, label_text: str, widget: QWidget) -> QWidget:
        wrapper_widget = QWidget()
        wrapper = QVBoxLayout(wrapper_widget)
        wrapper.setSpacing(2)
        label = QLabel(label_text)
        label.setStyleSheet("color: #4a4a4a;")
        wrapper.addWidget(label)
        wrapper.addWidget(widget)
        return wrapper_widget

    def _inline_field(self, label_text: str, widget: QWidget) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        label = QLabel(label_text)
        label.setStyleSheet("color: #4a4a4a;")
        layout.addWidget(label)
        layout.addWidget(widget)
        return container

    @staticmethod
    def _styled_checkbox() -> QCheckBox:
        cb = QCheckBox()
        cb.setCursor(Qt.PointingHandCursor)
        cb.setStyleSheet(
            """
            QCheckBox {
                spacing: 6px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1px solid #8c8f94;
                border-radius: 3px;
                background: #fdfdfd;
            }
            QCheckBox::indicator:hover {
                border: 1px solid #3b7bd4;
            }
            QCheckBox::indicator:checked {
                border: 1px solid #2a5dbe;
                background-color: #3b7bd4;
            }
            """
        )
        return cb

    def _row(self, label: str, widget: QWidget) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLabel(label))
        layout.addWidget(widget)
        layout.addStretch()
        return container

    @staticmethod
    def _schedule_summary_label() -> QLabel:
        label = QLabel()
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setMinimumWidth(180)
        label.setStyleSheet("color: #555; font-style: italic;")
        return label

    def _time_edit(self, value: str) -> QTimeEdit:
        editor = QTimeEdit()
        editor.setDisplayFormat("HH:mm")
        try:
            hour, minute = map(int, value.split(":"))
        except ValueError:
            hour, minute = (8, 0)
        editor.setTime(QTime(hour, minute))
        editor.setMinimumWidth(50)
        return editor

    def _handle_save(self):
        schedules = {
            definition.automation_type: self._collect_schedule(definition.automation_type)
            for definition in self.section_defs
        }
        new_settings = CompanySettingsDTO(
            automacaoempresa=self.company_ref,
            schedules=schedules,
        )
        self.updated_settings = new_settings
        self.updated_use_default = self.use_default_cb.isChecked()
        self.updated_notified_teams = self.notified_teams_edit.text()
        self.updated_team_id = self.selected_team.equipe_id if self.selected_team else None
        self.settings = new_settings
        self.accept()

    def _handle_frequency_change(self, key: str, frequency: str):
        self._toggle_schedule_rows(frequency, key)
        widgets = self.sections[key]
        self._set_schedule_inputs_enabled(key, widgets.enabled.isChecked())
        self._update_schedule_summary(key)

    def _toggle_schedule_rows(self, frequency: str, key: str):
        show_month = frequency == "Mensalmente"
        show_week = frequency == "Semanalmente"
        widgets = self.sections[key]
        if widgets.day_month_row is not None:
            widgets.day_month_row.setVisible(show_month)
        if widgets.day_week_row is not None:
            widgets.day_week_row.setVisible(show_week)

    def _collect_schedule(self, key: str) -> ScheduleConfig:
        widgets = self.sections[key]
        enabled = widgets.enabled.isChecked()
        frequency = widgets.frequency.currentText()
        day_of_month = widgets.day_month.value() if widgets.day_month is not None else None
        weekday = widgets.day_week.currentText() if widgets.day_week is not None else None
        time_value = widgets.time.time().toString("HH:mm")
        config = ScheduleConfig(
            enabled=enabled,
            frequency=frequency,
            day_of_month=day_of_month,
            weekday=weekday,
            time=time_value,
            allowed_frequencies=list(widgets.allowed_frequencies),
        )
        return self._normalize_schedule(config)

    def _apply_section_enabled_state(self, key: str) -> None:
        widgets = self.sections[key]
        self._toggle_schedule_rows(widgets.frequency.currentText(), key)
        self._set_schedule_inputs_enabled(key, widgets.enabled.isChecked())
        self._update_schedule_summary(key)

    def _set_schedule_inputs_enabled(self, key: str, enabled: bool) -> None:
        widgets = self.sections[key]
        widgets.frequency.setEnabled(enabled)
        widgets.time.setEnabled(enabled)
        widgets.time_row.setEnabled(enabled)

        frequency = widgets.frequency.currentText()
        show_month = frequency == "Mensalmente"
        show_week = frequency == "Semanalmente"

        if widgets.day_month_row is not None:
            widgets.day_month_row.setVisible(show_month)
        if widgets.day_week_row is not None:
            widgets.day_week_row.setVisible(show_week)

        if widgets.day_month_row is not None:
            widgets.day_month_row.setEnabled(enabled)
        if widgets.day_month is not None:
            widgets.day_month.setEnabled(enabled and show_month)

        if widgets.day_week_row is not None:
            widgets.day_week_row.setEnabled(enabled)
        if widgets.day_week is not None:
            widgets.day_week.setEnabled(enabled and show_week)

        bg = "#f1f1f1" if enabled else "#e3e4e8"
        combo_bg = "#ffffff" if enabled else bg
        widgets.group.setStyleSheet(
            f"""
            QGroupBox {{ 
                border: 1px solid #d5d5d5;
                margin-top: 6px; 
                background: {bg}; 
            }} 
            
            QWidget, QLabel {{ 
                background: {bg};
            }}
            
            QComboBox QAbstractItemView {{
                background: #ffffff;
                color: #1e1e1e;
                selection-background-color: #cfdcf4;
            }}
            
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 22px;
                border-left: 1px solid #bfc1c7;
                background: {combo_bg};
            }}
            
            QComboBox::down-arrow {{
                width: 2px;
                height: 10px;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #4a4a4a;
                margin-right: 6px;
            }}
            
            QLineEdit, QComboBox, QSpinBox, QTimeEdit {{ 
                background: {combo_bg};
                border: 1px solid #bfc1c7;
                border-radius: 2px;
                padding: 3px;
            }}
            
            QSpinBox::up-button,
            QSpinBox::down-button,
            QTimeEdit::up-button,
            QTimeEdit::down-button {{
                width: 0px;
                border: none;
            }}

            QSpinBox::up-arrow,
            QSpinBox::down-arrow,
            QTimeEdit::up-arrow,
            QTimeEdit::down-arrow {{
                width: 0;
                height: 0;
            }}
            """
        )
        widgets.summary.setStyleSheet("color: #2f2f2f; font-style: normal;" if enabled else "color: #7a1f1f; font-style: italic;")
        self._update_schedule_summary(key)

    def _update_schedule_summary(self, key: str) -> None:
        widgets = self.sections[key]
        if not widgets.enabled.isChecked():
            widgets.summary.setText("Ação manual")
            widgets.summary.setStyleSheet("color: #7a1f1f; font-style: italic;")
            return
        summary = self._summarize_schedule(key)
        widgets.summary.setText(summary)
        widgets.summary.setStyleSheet("color: #2f2f2f; font-style: normal;")

    def _summarize_schedule(self, key: str) -> str:
        widgets = self.sections[key]
        frequency = widgets.frequency.currentText()
        time_text = widgets.time.time().toString("HH:mm")
        if frequency == "Mensalmente":
            day = widgets.day_month.value() if widgets.day_month is not None else 1
            return f"Todo dia {day} às {time_text}"
        if frequency == "Semanalmente":
            weekday = widgets.day_week.currentText().lower() if widgets.day_week is not None else "segunda"
            return f"Toda {weekday} às {time_text}"
        return f"Diariamente às {time_text}"

    @staticmethod
    def _normalize_schedule(config: ScheduleConfig) -> ScheduleConfig:
        if config.frequency == "Mensalmente":
            return replace(config, weekday=None)
        if config.frequency == "Semanalmente":
            return replace(config, day_of_month=None)
        return replace(config, day_of_month=None, weekday=None)


class NotificationTeamSelectorDialog(QDialog):
    """Lightweight dialog that lists notification teams for selection."""

    def __init__(
        self,
        teams: List[NotificationTeamDTO],
        selected_team: Optional[NotificationTeamDTO] = None,
        parent=None,
    ):
        super().__init__(parent)
        self.setWindowIcon(persona_icon())
        self._teams = teams
        self._selected_id = selected_team.equipe_id if selected_team else None
        self.selected_team: Optional[NotificationTeamDTO] = None
        self.setWindowTitle("Selecionar equipe")
        self.resize(420, 360)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("Filtrar por código, nome ou e-mail")
        self.filter_edit.textChanged.connect(self._apply_filter)
        layout.addWidget(self.filter_edit)

        self.list_widget = QListWidget()
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.itemDoubleClicked.connect(lambda *_: self._accept_current())
        layout.addWidget(self.list_widget, 1)
        self._populate()

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self._accept_current)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setStyleSheet(
            """
            QListWidget {
                background: #ffffff;
                border: 1px solid #bfc1c7;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background: #cfdcf4;
                color: #1e1e1e;
            }
            QLineEdit {
                background: #ffffff;
                border: 1px solid #bfc1c7;
                border-radius: 4px;
                padding: 4px 6px;
            }
            """
        )

    def _populate(self) -> None:
        self.list_widget.clear()
        for team in self._teams:
            display = f"{team.codigo} - {team.nome}"
            if team.membros:
                display = f"{display} ({team.membros} membros)"
            item = QListWidgetItem(display)
            item.setData(Qt.UserRole, team)
            if team.emails:
                item.setToolTip(team.emails)
            self.list_widget.addItem(item)
            if team.equipe_id == self._selected_id:
                self.list_widget.setCurrentItem(item)

    def _apply_filter(self, text: str) -> None:
        needle = text.strip().lower()
        for idx in range(self.list_widget.count()):
            item = self.list_widget.item(idx)
            if not needle:
                item.setHidden(False)
                continue
            team: NotificationTeamDTO = item.data(Qt.UserRole)
            haystack = f"{team.codigo} {team.nome} {team.emails}".lower()
            item.setHidden(needle not in haystack)

    def _accept_current(self) -> None:
        item = self.list_widget.currentItem()
        if item is None:
            QMessageBox.information(
                self,
                "Selecionar equipe",
                "Selecione uma equipe antes de confirmar.",
            )
            return
        self.selected_team = item.data(Qt.UserRole)
        self.accept()
