from __future__ import annotations

import sys
import json
import traceback
import time
from datetime import datetime
from functools import partial
from typing import List

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QMenu,
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QSpinBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QCheckBox,
    QHeaderView,
    QMessageBox,
    QGroupBox,
    QFormLayout,
    QDoubleSpinBox,
    QFileDialog,
    QDialog,
    QDialogButtonBox,
    QPlainTextEdit,
    QSplitter,
    QMenuBar,
)

from .bus import open_bus
from .engine import CanSimEngine, CanMessageTemplate
from . import profiles as profiles_mod
from .profiles import PROFILE_BUILDERS, DEFAULT_PROFILE_NAME
from . import __version__, __author__


# ---------------------------------------------------------------------------
# Small helper widgets / dialogs
# ---------------------------------------------------------------------------

class CheckBoxWidget(QCheckBox):
    """Simple checkbox used in the message table (per-row enable/disable)."""

    def __init__(self, checked: bool, parent=None):
        super().__init__(parent)
        self.setChecked(checked)
        self.setTristate(False)
        self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)


class RawMessageDialog(QDialog):
    """
    Dialog to create or edit a single-frame raw CAN message.
    Supports standard (11-bit) and extended (29-bit) IDs.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Raw CAN Message")

        layout = QVBoxLayout(self)
        form = QFormLayout()
        layout.addLayout(form)

        # Arbitration ID
        self.id_edit = QLineEdit("18FEF300")
        form.addRow("Arbitration ID (hex):", self.id_edit)

        # ID type
        self.id_type_combo = QComboBox()
        self.id_type_combo.addItems(["Extended (29-bit)", "Standard (11-bit)"])
        form.addRow("ID type:", self.id_type_combo)

        # Data bytes
        self.data_edit = QLineEdit("00 00 00 00 00 00 00 00")
        form.addRow("Data bytes (hex, space-separated):", self.data_edit)

        # Period
        self.period_spin = QSpinBox()
        self.period_spin.setRange(1, 600000)  # 1 ms .. 10 minutes
        self.period_spin.setSingleStep(10)
        self.period_spin.setValue(200)
        form.addRow("Period (ms):", self.period_spin)

        # OK / Cancel
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.result_data: dict | None = None

    def accept(self):
        """Validate inputs and stash result_data; stay open if invalid."""
        try:
            id_text = self.id_edit.text().strip()
            if id_text.lower().startswith("0x"):
                id_text = id_text[2:]
            if not id_text:
                raise ValueError("Arbitration ID is required.")
            arbitration_id = int(id_text, 16)

            is_extended = self.id_type_combo.currentIndex() == 0
            if is_extended:
                if not (0 <= arbitration_id <= 0x1FFFFFFF):
                    raise ValueError("Extended ID must be 0..0x1FFFFFFF.")
            else:
                if not (0 <= arbitration_id <= 0x7FF):
                    raise ValueError("Standard ID must be 0..0x7FF.")

            data_text = self.data_edit.text().strip()
            data_bytes: list[int] = []
            if data_text:
                parts = data_text.replace(",", " ").split()
                for p in parts:
                    b = int(p, 16)
                    if not (0 <= b <= 0xFF):
                        raise ValueError("Data bytes must be in 00..FF.")
                    data_bytes.append(b)
            if len(data_bytes) > 8:
                raise ValueError("Max 8 data bytes for a single CAN frame.")

            period_ms = int(self.period_spin.value())

            self.result_data = {
                "arbitration_id": arbitration_id,
                "is_extended_id": is_extended,
                "data": data_bytes,
                "period_ms": period_ms,
                "name": f"RAW 0x{arbitration_id:08X}",
            }
            super().accept()

        except Exception as e:
            QMessageBox.critical(self, "Invalid input", str(e))


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------

class CanSimWindow(QWidget):
    """
    PyQt GUI for the CAN simulator with:
      - Connection controls
      - Profile selection
      - Live-editable values
      - Message table with enable/disable
      - Start/Stop
      - Save/Load profile JSON
      - Add/edit/delete raw messages
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"CAN Simulator v{__version__}")
        self.resize(1000, 720)

        self.bus = None
        self.engine: CanSimEngine | None = None

        self.current_profile_name: str = DEFAULT_PROFILE_NAME
        self.messages: List[CanMessageTemplate] = PROFILE_BUILDERS[self.current_profile_name]()

        self._build_ui()

        # Timer to keep live lat/lon in sync with moving GNSS
        self.position_timer = QTimer(self)
        self.position_timer.setInterval(200)  # 5 Hz update
        self.position_timer.timeout.connect(self._update_live_position_from_motion)

    # -------------------------------------------------------------------
    # UI construction
    # -------------------------------------------------------------------

    def _build_ui(self):
        root_layout = QVBoxLayout(self)

        # --- Menu bar (Help → About) ---
        menu_bar = QMenuBar(self)

        help_menu = QMenu("Help", self)
        menu_bar.addMenu(help_menu)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

        root_layout.addWidget(menu_bar)

        # --- Top row: Profile + Save/Load + Raw + Connection settings ---
        top_layout = QHBoxLayout()
        root_layout.addLayout(top_layout)

        # Profile selector
        top_layout.addWidget(QLabel("Profile:"))
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(list(PROFILE_BUILDERS.keys()))
        self.profile_combo.setCurrentText(self.current_profile_name)
        self.profile_combo.currentTextChanged.connect(self.on_profile_changed)
        top_layout.addWidget(self.profile_combo)

        # Save / Load buttons
        self.save_button = QPushButton("Save…")
        self.save_button.clicked.connect(self.on_save_clicked)
        top_layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load…")
        self.load_button.clicked.connect(self.on_load_clicked)
        top_layout.addWidget(self.load_button)

        # Add Raw message
        self.add_raw_button = QPushButton("Add Raw…")
        self.add_raw_button.clicked.connect(self.on_add_raw_clicked)
        top_layout.addWidget(self.add_raw_button)

        # Delete Raw message(s)
        self.delete_raw_button = QPushButton("Delete Raw")
        self.delete_raw_button.clicked.connect(self.on_delete_raw_clicked)
        top_layout.addWidget(self.delete_raw_button)

        top_layout.addSpacing(20)

        # Connection settings
        top_layout.addWidget(QLabel("Interface:"))
        self.interface_combo = QComboBox()
        self.interface_combo.addItems(["neovi", "kvaser", "pcan", "socketcan", "virtual"])
        self.interface_combo.setCurrentText("neovi")
        top_layout.addWidget(self.interface_combo)

        top_layout.addWidget(QLabel("Channel:"))
        self.channel_edit = QLineEdit("1")
        self.channel_edit.setFixedWidth(60)
        top_layout.addWidget(self.channel_edit)

        top_layout.addWidget(QLabel("Bitrate:"))
        self.bitrate_spin = QSpinBox()
        self.bitrate_spin.setRange(10000, 1000000)
        self.bitrate_spin.setSingleStep(10000)
        self.bitrate_spin.setValue(250000)
        top_layout.addWidget(self.bitrate_spin)

        top_layout.addStretch(1)

        # --- Start / Stop row ---
        btn_layout = QHBoxLayout()
        root_layout.addLayout(btn_layout)

        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)

        self.start_button.clicked.connect(self.on_start_clicked)
        self.stop_button.clicked.connect(self.on_stop_clicked)

        btn_layout.addWidget(self.start_button)
        btn_layout.addWidget(self.stop_button)
        btn_layout.addStretch(1)

        # --- Live values panel ---
        live_group = QGroupBox("Live Values")
        live_layout = QFormLayout()
        live_group.setLayout(live_layout)
        root_layout.addWidget(live_group)

        # GNSS
        self.lat_spin = QDoubleSpinBox()
        self.lat_spin.setRange(-90.0, 90.0)
        self.lat_spin.setDecimals(6)
        self.lat_spin.setSingleStep(0.0001)
        self.lat_spin.setValue(profiles_mod.LAT_DEG)
        self.lat_spin.valueChanged.connect(self.on_lat_changed)
        live_layout.addRow("Latitude (deg):", self.lat_spin)

        self.lon_spin = QDoubleSpinBox()
        self.lon_spin.setRange(-180.0, 180.0)
        self.lon_spin.setDecimals(6)
        self.lon_spin.setSingleStep(0.0001)
        self.lon_spin.setValue(profiles_mod.LON_DEG)
        self.lon_spin.valueChanged.connect(self.on_lon_changed)
        live_layout.addRow("Longitude (deg):", self.lon_spin)

        self.cog_spin = QDoubleSpinBox()
        self.cog_spin.setRange(0.0, 359.99)
        self.cog_spin.setDecimals(2)
        self.cog_spin.setSingleStep(1.0)
        self.cog_spin.setValue(profiles_mod.COG_DEG)
        self.cog_spin.valueChanged.connect(self.on_cog_changed)
        live_layout.addRow("Heading / COG (deg):", self.cog_spin)

        self.sog_spin = QDoubleSpinBox()
        self.sog_spin.setRange(0.0, 50.0)
        self.sog_spin.setDecimals(2)
        self.sog_spin.setSingleStep(0.1)
        self.sog_spin.setValue(profiles_mod.SOG_MS)
        self.sog_spin.valueChanged.connect(self.on_sog_changed)
        live_layout.addRow("Speed over ground (m/s):", self.sog_spin)

        # Engine / fuel
        self.fuel_level_spin = QDoubleSpinBox()
        self.fuel_level_spin.setRange(0.0, 100.0)
        self.fuel_level_spin.setDecimals(1)
        self.fuel_level_spin.setSingleStep(0.5)
        self.fuel_level_spin.setValue(profiles_mod.FUEL_PERCENT)
        self.fuel_level_spin.valueChanged.connect(self.on_fuel_level_changed)
        live_layout.addRow("Fuel level (%):", self.fuel_level_spin)

        self.engine_load_spin = QDoubleSpinBox()
        self.engine_load_spin.setRange(0.0, 250.0)
        self.engine_load_spin.setDecimals(1)
        self.engine_load_spin.setSingleStep(1.0)
        self.engine_load_spin.setValue(profiles_mod.ENGINE_LOAD_PCT)
        self.engine_load_spin.valueChanged.connect(self.on_engine_load_changed)
        live_layout.addRow("Engine load (%):", self.engine_load_spin)

        self.coolant_temp_spin = QDoubleSpinBox()
        self.coolant_temp_spin.setRange(-40.0, 200.0)
        self.coolant_temp_spin.setDecimals(1)
        self.coolant_temp_spin.setSingleStep(1.0)
        self.coolant_temp_spin.setValue(profiles_mod.ENGINE_COOLANT_TEMP_C)
        self.coolant_temp_spin.valueChanged.connect(self.on_coolant_temp_changed)
        live_layout.addRow("Coolant temp (°C):", self.coolant_temp_spin)

        # --- Message table ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Enabled", "Name", "ID (hex)", "Period (ms)"])

        header = self.table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Double-click to edit raw messages
        self.table.cellDoubleClicked.connect(self.on_table_cell_double_clicked)

        # --- Event log panel ---
        log_group = QGroupBox("Event Log")
        log_layout = QVBoxLayout()
        log_group.setLayout(log_layout)

        self.log_view = QPlainTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        doc = self.log_view.document()
        if doc is not None:
            # limit stored lines; new lines push old ones out
            doc.setMaximumBlockCount(1000)

        log_layout.addWidget(self.log_view)

        # --- Splitter for table + log ---
        bottom_splitter = QSplitter(Qt.Orientation.Vertical)
        bottom_splitter.addWidget(self.table)
        bottom_splitter.addWidget(log_group)

        # Make the table bigger by default
        bottom_splitter.setStretchFactor(0, 3)
        bottom_splitter.setStretchFactor(1, 1)

        root_layout.addWidget(bottom_splitter, stretch=1)

        # --- Status label ---
        self.status_label = QLabel("Status: Idle")
        root_layout.addWidget(self.status_label)

        self._populate_table()

    # -------------------------------------------------------------------
    # Table population
    # -------------------------------------------------------------------

    def _populate_table(self):
        self.table.setRowCount(0)
        self.table.setRowCount(len(self.messages))

        for row, msg in enumerate(self.messages):
            # Enabled checkbox
            chk = CheckBoxWidget(msg.enabled)
            chk.stateChanged.connect(partial(self._on_enabled_checkbox_changed, row))
            self.table.setCellWidget(row, 0, chk)

            # Name + ID (read-only)
            self.table.setItem(row, 1, QTableWidgetItem(msg.name))
            self.table.setItem(row, 2, QTableWidgetItem(f"0x{msg.arbitration_id:08X}"))

            # Period (ms) – editable spinbox
            period_spin = QSpinBox()
            period_spin.setRange(1, 600000)  # 1 ms .. 10 minutes
            period_spin.setSingleStep(10)
            period_spin.setValue(int(msg.period_ms))
            period_spin.valueChanged.connect(partial(self._on_period_changed, row))
            self.table.setCellWidget(row, 3, period_spin)

    # -------------------------------------------------------------------
    # State helpers
    # -------------------------------------------------------------------

    def _set_status(self, text: str):
        """Update status label and append to event log."""
        self.status_label.setText(f"Status: {text}")
        print(text)  # console
        self._append_log(text)

    def _append_log(self, text: str):
        """
        Append a line to the event log with a timestamp.
        Safe to call even before log_view is created.
        """
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {text}"

        log_widget = getattr(self, "log_view", None)
        if log_widget is not None:
            log_widget.appendPlainText(line)
        else:
            # Fallback: just print if log_view isn't ready yet
            print(line)

    def _set_controls_enabled(self, enabled: bool):
        """
        Enable/disable controls that should not be changed while running.
        Save remains enabled so you can snapshot state mid-run.
        """
        self.interface_combo.setEnabled(enabled)
        self.channel_edit.setEnabled(enabled)
        self.bitrate_spin.setEnabled(enabled)
        self.table.setEnabled(enabled)
        self.profile_combo.setEnabled(enabled)
        self.load_button.setEnabled(enabled)
        self.add_raw_button.setEnabled(enabled)
        self.delete_raw_button.setEnabled(enabled)

    def _update_live_position_from_motion(self):
        """
        If the engine is running, compute the current moving lat/lon
        and reflect them into the Live Values spin boxes.

        This makes the panel behave as a read-only 'view' of the
        simulated GNSS position while running.
        """
        if self.engine is None:
            return

        now = time.time()
        lat, lon = profiles_mod.compute_moving_lat_lon(now)

        # Update the spin boxes without firing valueChanged back into profiles_mod
        self.lat_spin.blockSignals(True)
        self.lon_spin.blockSignals(True)
        self.lat_spin.setValue(lat)
        self.lon_spin.setValue(lon)
        self.lat_spin.blockSignals(False)
        self.lon_spin.blockSignals(False)

    # -------------------------------------------------------------------
    # Profile handling
    # -------------------------------------------------------------------

    def on_profile_changed(self, name: str):
        """
        Reload selected profile into self.messages and refresh table.
        Only allowed while simulator is stopped.
        """
        if self.engine is not None:
            # revert selection and warn
            self.profile_combo.blockSignals(True)
            self.profile_combo.setCurrentText(self.current_profile_name)
            self.profile_combo.blockSignals(False)

            QMessageBox.warning(
                self,
                "Profile in use",
                "Stop the simulator before changing profiles.",
            )
            return

        if name not in PROFILE_BUILDERS:
            QMessageBox.critical(self, "Error", f"Unknown profile: {name}")
            return

        self.current_profile_name = name
        builder = PROFILE_BUILDERS[name]
        self.messages = builder()
        self._populate_table()
        self._set_status(f"Profile changed to: {name}")

    # -------------------------------------------------------------------
    # Live value callbacks – update profiles_mod globals
    # -------------------------------------------------------------------

    def on_lat_changed(self, value: float):
        profiles_mod.LAT_DEG = float(value)

    def on_lon_changed(self, value: float):
        profiles_mod.LON_DEG = float(value)

    def on_cog_changed(self, value: float):
        profiles_mod.COG_DEG = float(value)

    def on_sog_changed(self, value: float):
        profiles_mod.SOG_MS = float(value)

    def on_fuel_level_changed(self, value: float):
        profiles_mod.FUEL_PERCENT = float(value)

    def on_engine_load_changed(self, value: float):
        profiles_mod.ENGINE_LOAD_PCT = float(value)

    def on_coolant_temp_changed(self, value: float):
        profiles_mod.ENGINE_COOLANT_TEMP_C = float(value)

    def _sync_live_controls_from_profiles(self):
        """
        When we load a profile from JSON, update spinboxes to reflect new values.
        """
        self.lat_spin.blockSignals(True)
        self.lon_spin.blockSignals(True)
        self.cog_spin.blockSignals(True)
        self.sog_spin.blockSignals(True)
        self.fuel_level_spin.blockSignals(True)
        self.engine_load_spin.blockSignals(True)
        self.coolant_temp_spin.blockSignals(True)

        self.lat_spin.setValue(profiles_mod.LAT_DEG)
        self.lon_spin.setValue(profiles_mod.LON_DEG)
        self.cog_spin.setValue(profiles_mod.COG_DEG)
        self.sog_spin.setValue(profiles_mod.SOG_MS)
        self.fuel_level_spin.setValue(profiles_mod.FUEL_PERCENT)
        self.engine_load_spin.setValue(profiles_mod.ENGINE_LOAD_PCT)
        self.coolant_temp_spin.setValue(profiles_mod.ENGINE_COOLANT_TEMP_C)

        self.lat_spin.blockSignals(False)
        self.lon_spin.blockSignals(False)
        self.cog_spin.blockSignals(False)
        self.sog_spin.blockSignals(False)
        self.fuel_level_spin.blockSignals(False)
        self.engine_load_spin.blockSignals(False)
        self.coolant_temp_spin.blockSignals(False)

    # -------------------------------------------------------------------
    # Save / Load JSON handlers
    # -------------------------------------------------------------------

    def on_save_clicked(self):
        """
        Save current profile state (base profile + live values + enabled flags) to JSON.
        """
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Profile",
            "",
            "JSON Files (*.json);;All Files (*)",
        )
        if not filename:
            return

        try:
            # Live values we care about (extend later if needed)
            live_keys = [
                "LAT_DEG",
                "LON_DEG",
                "COG_DEG",
                "SOG_MS",
                "FUEL_PERCENT",
                "ENGINE_LOAD_PCT",
                "ENGINE_COOLANT_TEMP_C",
            ]
            live_values = {
                key: getattr(profiles_mod, key)
                for key in live_keys
                if hasattr(profiles_mod, key)
            }

            messages_data = []
            for msg in self.messages:
                entry = {
                    "arbitration_id": msg.arbitration_id,
                    "enabled": msg.enabled,
                    "period_ms": int(msg.period_ms),
                    "is_extended_id": bool(msg.is_extended_id),
                    "name": msg.name,
                }

                raw = getattr(msg, "raw_data", None)
                if raw is not None:
                    entry["kind"] = "raw"
                    entry["dlc"] = int(msg.dlc)
                    entry["raw_data"] = [int(b) & 0xFF for b in raw]

                messages_data.append(entry)

            data = {
                "base_profile": self.current_profile_name,
                "live_values": live_values,
                "messages": messages_data,
            }

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            self._set_status(f"Profile saved to {filename}")

        except Exception as e:
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to save profile:\n{e}")

    def on_load_clicked(self):
        """
        Load profile state from JSON.
        Only allowed while simulator is stopped.
        """
        if self.engine is not None:
            QMessageBox.warning(
                self,
                "Simulator running",
                "Stop the simulator before loading a profile.",
            )
            return

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Load Profile",
            "",
            "JSON Files (*.json);;All Files (*)",
        )
        if not filename:
            return

        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            base_profile = data.get("base_profile", DEFAULT_PROFILE_NAME)
            if base_profile not in PROFILE_BUILDERS:
                raise ValueError(f"Unknown base_profile '{base_profile}' in file.")

            # Rebuild messages from the chosen base profile
            self.current_profile_name = base_profile
            builder = PROFILE_BUILDERS[base_profile]
            self.messages = builder()

            # Apply live values
            live_values = data.get("live_values", {})
            for key, val in live_values.items():
                if hasattr(profiles_mod, key):
                    setattr(profiles_mod, key, float(val))

            # Map JSON messages by arbitration_id
            msg_map: dict[int, dict] = {}
            for entry in data.get("messages", []):
                try:
                    aid = int(entry["arbitration_id"])
                except Exception:
                    continue
                msg_map[aid] = entry

            # Apply overrides to base-profile messages
            for msg in self.messages:
                entry = msg_map.get(msg.arbitration_id)
                if not entry:
                    continue

                if "enabled" in entry:
                    msg.enabled = bool(entry["enabled"])

                if "period_ms" in entry:
                    try:
                        msg.period_ms = int(entry["period_ms"])
                    except Exception:
                        pass

            # Append any raw messages that don't exist in base profile
            existing_ids = {m.arbitration_id for m in self.messages}

            for entry in data.get("messages", []):
                kind = entry.get("kind")
                has_raw = "raw_data" in entry

                if not (kind == "raw" or has_raw):
                    continue

                try:
                    aid = int(entry["arbitration_id"])
                except Exception:
                    continue

                # avoid duplicate IDs for now
                if aid in existing_ids:
                    continue

                is_extended_id = bool(entry.get("is_extended_id", True))
                period_ms = int(entry.get("period_ms", 1000))
                enabled = bool(entry.get("enabled", True))
                name = entry.get("name") or f"RAW 0x{aid:08X}"

                raw_list = entry.get("raw_data", [])
                raw_bytes = bytes(int(b) & 0xFF for b in raw_list)
                dlc = len(raw_bytes)

                def payload_func(now: float, raw=raw_bytes) -> bytes:
                    return raw

                tmpl = CanMessageTemplate(
                    name=name,
                    arbitration_id=aid,
                    is_extended_id=is_extended_id,
                    dlc=dlc,
                    payload_func=payload_func,
                    period_ms=period_ms,
                    start_delay_ms=0,
                    max_count=None,
                    enabled=enabled,
                )
                tmpl.raw_data = raw_bytes

                self.messages.append(tmpl)
                existing_ids.add(aid)

            # Update UI
            self.profile_combo.blockSignals(True)
            self.profile_combo.setCurrentText(base_profile)
            self.profile_combo.blockSignals(False)

            self._sync_live_controls_from_profiles()
            self._populate_table()

            self._set_status(f"Profile loaded from {filename} (base: {base_profile})")

        except Exception as e:
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to load profile:\n{e}")

    # -------------------------------------------------------------------
    # Raw messages: add / delete / edit
    # -------------------------------------------------------------------

    def on_add_raw_clicked(self):
        """
        Add a new single-frame raw CAN message via dialog.
        Only allowed while stopped.
        """
        if self.engine is not None:
            QMessageBox.warning(
                self,
                "Simulator running",
                "Stop the simulator before adding raw messages.",
            )
            return

        dlg = RawMessageDialog(self)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return

        info = dlg.result_data
        if not info:
            return

        arbitration_id = info["arbitration_id"]
        is_extended_id = info["is_extended_id"]
        data_bytes = info["data"]
        period_ms = info["period_ms"]
        name = info["name"]

        raw_payload = bytes(data_bytes)

        def payload_func(now: float, raw=raw_payload) -> bytes:
            return raw

        tmpl = CanMessageTemplate(
            name=name,
            arbitration_id=arbitration_id,
            is_extended_id=is_extended_id,
            dlc=len(raw_payload),
            payload_func=payload_func,
            period_ms=period_ms,
            start_delay_ms=0,
            max_count=None,
            enabled=True,
        )
        # Mark as raw so Save/Load & delete logic knows this is user-added
        tmpl.raw_data = raw_payload

        self.messages.append(tmpl)
        self._populate_table()
        self._set_status(f"Added raw message {name} (ID=0x{arbitration_id:08X})")

    def on_delete_raw_clicked(self):
        """
        Delete selected raw message rows.
        Built-in profile messages (without raw_data) are protected.
        """
        if self.engine is not None:
            QMessageBox.warning(
                self,
                "Simulator running",
                "Stop the simulator before deleting messages.",
            )
            return

        selected_indexes = self.table.selectedIndexes()
        if not selected_indexes:
            QMessageBox.information(
                self,
                "No selection",
                "Select one or more rows to delete.",
            )
            return

        # Unique row indices, sorted descending so we can delete safely
        rows = sorted({idx.row() for idx in selected_indexes}, reverse=True)

        deleted_any = False
        blocked_non_raw = False

        for row in rows:
            if not (0 <= row < len(self.messages)):
                continue

            msg = self.messages[row]
            raw = getattr(msg, "raw_data", None)

            if raw is None:
                blocked_non_raw = True
                continue

            # Delete this raw message
            del self.messages[row]
            deleted_any = True

        if deleted_any:
            self._populate_table()
            self._set_status("Deleted selected raw message(s).")

        if blocked_non_raw and not deleted_any:
            # Only tried to delete non-raw rows
            QMessageBox.information(
                self,
                "Cannot delete",
                "Only raw messages can be deleted. Built-in profile messages are fixed.",
            )
        elif blocked_non_raw and deleted_any:
            # Mixed selection: some deleted, some protected
            QMessageBox.information(
                self,
                "Some rows not deleted",
                "Raw messages were deleted. Built-in profile messages were kept.",
            )

    # -------------------------------------------------------------------
    # Table callbacks
    # -------------------------------------------------------------------

    def _on_enabled_checkbox_changed(self, index: int, state: int):
        if 0 <= index < len(self.messages):
            self.messages[index].enabled = (state == Qt.CheckState.Checked.value)

    def _on_period_changed(self, index: int, value: int):
        """Update message period when the spinbox is changed."""
        if 0 <= index < len(self.messages):
            self.messages[index].period_ms = int(value)

    def on_table_cell_double_clicked(self, row: int, column: int):
        """
        Double-click handler: if this row is a raw message, open the RawMessageDialog
        pre-filled and update the message in place.
        """
        if not (0 <= row < len(self.messages)):
            return

        msg = self.messages[row]

        # Only raw messages are editable this way
        raw = getattr(msg, "raw_data", None)
        if raw is None:
            QMessageBox.information(
                self,
                "Not editable",
                "Only raw messages can be edited. Built-in profile messages are fixed.",
            )
            return

        if self.engine is not None:
            QMessageBox.warning(
                self,
                "Simulator running",
                "Stop the simulator before editing messages.",
            )
            return

        # Pre-fill dialog with current values
        dlg = RawMessageDialog(self)

        # ID
        dlg.id_edit.setText(f"{msg.arbitration_id:08X}")

        # ID type
        if msg.is_extended_id:
            dlg.id_type_combo.setCurrentIndex(0)  # Extended (29-bit)
        else:
            dlg.id_type_combo.setCurrentIndex(1)  # Standard (11-bit)

        # Data bytes
        if raw:
            dlg.data_edit.setText(" ".join(f"{b:02X}" for b in raw))
        else:
            dlg.data_edit.setText("")

        # Period
        dlg.period_spin.setValue(int(msg.period_ms))

        if dlg.exec() != QDialog.DialogCode.Accepted:
            return

        info = dlg.result_data
        if not info:
            return

        # Apply changes back into the template
        arbitration_id = info["arbitration_id"]
        is_extended_id = info["is_extended_id"]
        data_bytes = info["data"]
        period_ms = info["period_ms"]

        raw_payload = bytes(data_bytes)

        def payload_func(now: float, raw=raw_payload) -> bytes:
            return raw

        msg.arbitration_id = arbitration_id
        msg.is_extended_id = is_extended_id
        msg.dlc = len(raw_payload)
        msg.payload_func = payload_func
        msg.period_ms = period_ms
        msg.raw_data = raw_payload
        # Preserve msg.name; could be updated if you want ID reflected in name

        self._populate_table()
        self._set_status(f"Edited raw message (ID=0x{arbitration_id:08X})")

    # -------------------------------------------------------------------
    # Help → About
    # -------------------------------------------------------------------
    def show_about_dialog(self):
        QMessageBox.information(
            self,
            "About CAN Simulator",
            (
                f"CAN Simulator\n"
                f"Version: {__version__}\n"
                f"Author: {__author__}\n\n"
                "A lightweight CAN message generator for testing and prototyping."
            ),
        )


    # -------------------------------------------------------------------
    # Start / stop
    # -------------------------------------------------------------------

    def on_start_clicked(self):
        if self.engine is not None:
            return  # already running

        interface = self.interface_combo.currentText()
        channel = self.channel_edit.text().strip()
        bitrate = int(self.bitrate_spin.value())

        try:
            profiles_mod.reset_motion_origin()
            self._set_status(f"Connecting to CAN... (Profile: {self.current_profile_name})")
            self.bus = open_bus(interface, channel, bitrate)

            self.engine = CanSimEngine(self.bus)
            self.engine.set_messages(self.messages)
            self.engine.start()
            self.position_timer.start()

            self._set_status(f"Running (Profile: {self.current_profile_name})")

            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self._set_controls_enabled(False)

        except Exception as e:
            self._set_status(f"ERROR: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to start simulator:\n{e}")

            # Ensure everything is cleaned up and UI is restored
            self._stop_engine()
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self._set_controls_enabled(True)

    def on_stop_clicked(self):
        self._stop_engine()
        self._set_status("Stopped")

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self._set_controls_enabled(True)

    def _stop_engine(self):
        """Stop engine thread, shut down bus, and stop position timer."""
        if self.engine is not None:
            try:
                self.engine.stop()
            except Exception:
                traceback.print_exc()
            self.engine = None

        if self.bus is not None:
            try:
                self.bus.shutdown()
            except Exception:
                traceback.print_exc()
            self.bus = None

        if hasattr(self, "position_timer"):
            self.position_timer.stop()

    # -------------------------------------------------------------------
    # Qt lifecycle
    # -------------------------------------------------------------------

    def closeEvent(self, event):
        self._stop_engine()
        event.accept()


def main():
    app = QApplication(sys.argv)
    win = CanSimWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
