"""
This module provides the graphical user interface (GUI) for the BaseBender
tool.

It allows users to interactively rebase strings between different digit sets,
manage digit set presets, and view rebase results.
"""

from __future__ import annotations

import sys
from typing import Any, Dict, List, Optional

from PySide6.QtCore import QEvent, QObject, QSize, Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from basebender.rebaser.config_loader import load_ui_state, save_ui_state
from basebender.rebaser.digit_set_rebaser import DigitSetRebaser
from basebender.rebaser.digit_sets import get_predefined_digit_sets
from basebender.rebaser.generated import app_resources_rc
from basebender.rebaser.models import DigitSet

ICON_INPUT_QRC_PATH = ":/app/icons/input.svg"
ICON_OUTPUT_QRC_PATH = ":/app/icons/output.svg"
ICON_SOURCE_QRC_PATH = ":/app/icons/source.svg"
ICON_TARGET_QRC_PATH = ":/app/icons/target.svg"


TEXT_EDIT_FIXED_HEIGHT = 30


class MainWindow(QMainWindow):
    """
    Main window for the BaseBender GUI application.

    Provides an interactive interface for rebaseing strings between different
    digit sets.
    """

    def __init__(self) -> None:
        super().__init__()
        app_resources_rc.qInitResources()
        self.setWindowTitle("BaseBender")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget: QWidget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout: QVBoxLayout = QVBoxLayout(self.central_widget)

        self._setup_ui()
        self._connect_signals()
        self._load_initial_state()
        self.status_bar: QStatusBar = self.statusBar()  # Initialize status bar

    def _load_svg_icon(self, qrc_path: str, size: int = 20) -> QSvgWidget:
        """
        Loads an SVG icon from the Qt Resource System (QRC).

        Args:
            qrc_path: The path to the SVG icon within the Qt Resource System.
            size: The desired size (width and height) for the SVG icon.
                  Defaults to 20.
        Returns:
            A QSvgWidget instance displaying the loaded SVG icon.
        """
        # Create a QSvgWidget to render the SVG
        svg_widget: QSvgWidget = QSvgWidget(qrc_path)
        svg_widget.setFixedSize(QSize(size, size))
        return svg_widget

    def _setup_ui(self) -> None:
        """
        Sets up the user interface elements of the main window.
        This includes input/output fields, digit set controls, and rebase buttons.
        """
        # Input String Area
        input_layout: QHBoxLayout = QHBoxLayout()
        self.input_label: QLabel = QLabel("Input String:")
        input_icon: QSvgWidget = self._load_svg_icon(ICON_INPUT_QRC_PATH)
        input_layout.addWidget(input_icon)
        input_layout.addWidget(self.input_label)
        input_layout.addStretch()
        self.input_text_edit: QTextEdit = QTextEdit()
        self.input_text_edit.setPlaceholderText("Enter string to rebase...")
        self.main_layout.addLayout(input_layout)
        self.main_layout.addWidget(self.input_text_edit)

        # Digit Set Layout (Source and Target)
        digit_set_layout: QHBoxLayout = QHBoxLayout()
        self.main_layout.addLayout(digit_set_layout)

        # Source Digit Set
        input_digit_set_group_layout: QVBoxLayout = QVBoxLayout()
        input_label_layout: QHBoxLayout = QHBoxLayout()
        input_digit_set_label: QLabel = QLabel("Input Digit Set:")
        input_icon = self._load_svg_icon(
            ICON_SOURCE_QRC_PATH
        )  # Reusing source icon for input digit set
        input_label_layout.addWidget(input_icon)
        input_label_layout.addWidget(input_digit_set_label)
        input_label_layout.addStretch()

        # Input Digit Set Text Edit and Controls
        input_digit_set_edit_layout = QHBoxLayout()
        self.input_digit_set_text_edit: QTextEdit = QTextEdit()
        self.input_digit_set_text_edit.setFixedHeight(TEXT_EDIT_FIXED_HEIGHT)
        self.input_digit_set_text_edit.setPlaceholderText(
            (
                "Enter input digit set or select preset (or leave empty for "
                "dynamic derivation)..."
            )
        )
        self.input_digit_set_text_edit.setToolTip(
            (
                "Define the set of characters used in the input string. Leave "
                "empty for dynamic derivation."
            )
        )
        input_digit_set_edit_layout.addWidget(self.input_digit_set_text_edit)

        self.input_digit_set_tool_button = QToolButton()
        self.input_digit_set_tool_button.setText("...")
        self.input_digit_set_tool_button.setToolTip(
            "Digit Set Manipulation Options"
        )
        self.input_digit_set_tool_button.setPopupMode(QToolButton.InstantPopup)
        self.input_digit_set_tool_button.setSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed
        )
        self._setup_digit_set_menu(
            self.input_digit_set_tool_button, self.input_digit_set_text_edit
        )
        input_digit_set_edit_layout.addWidget(self.input_digit_set_tool_button)

        self.input_digit_set_preset_combo: QComboBox = QComboBox()
        self.input_digit_set_preset_combo.addItem("Select Preset...")
        self.input_digit_set_preset_combo.addItem("Derived from Input")
        self._populate_digit_set_presets(self.input_digit_set_preset_combo)
        self.input_digit_set_preset_combo.setToolTip(
            "Select a predefined digit set or choose to derive from input."
        )

        input_digit_set_group_layout.addLayout(input_label_layout)
        input_digit_set_group_layout.addLayout(input_digit_set_edit_layout)
        input_digit_set_group_layout.addWidget(
            self.input_digit_set_preset_combo
        )
        digit_set_layout.addLayout(input_digit_set_group_layout)

        # Output Digit Set
        output_digit_set_group_layout: QVBoxLayout = QVBoxLayout()
        output_label_layout: QHBoxLayout = QHBoxLayout()
        output_digit_set_label: QLabel = QLabel("Output Digit Set:")
        output_icon = self._load_svg_icon(
            ICON_TARGET_QRC_PATH
        )  # Reusing target icon for output digit set
        output_label_layout.addWidget(output_icon)
        output_label_layout.addWidget(output_digit_set_label)
        output_label_layout.addStretch()

        # Output Digit Set Text Edit and Controls
        output_digit_set_edit_layout = QHBoxLayout()
        self.output_digit_set_text_edit: QTextEdit = QTextEdit()
        self.output_digit_set_text_edit.setFixedHeight(TEXT_EDIT_FIXED_HEIGHT)
        self.output_digit_set_text_edit.setPlaceholderText(
            "Enter output digit set or select preset..."
        )
        self.output_digit_set_text_edit.setToolTip(
            "Define the set of characters for the rebased output string."
        )
        output_digit_set_edit_layout.addWidget(self.output_digit_set_text_edit)

        self.output_digit_set_tool_button = QToolButton()
        self.output_digit_set_tool_button.setText("...")
        self.output_digit_set_tool_button.setToolTip(
            "Digit Set Manipulation Options"
        )
        self.output_digit_set_tool_button.setPopupMode(QToolButton.InstantPopup)
        self.output_digit_set_tool_button.setSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed
        )
        self._setup_digit_set_menu(
            self.output_digit_set_tool_button, self.output_digit_set_text_edit
        )
        output_digit_set_edit_layout.addWidget(
            self.output_digit_set_tool_button
        )

        self.output_digit_set_preset_combo: QComboBox = QComboBox()
        self.output_digit_set_preset_combo.addItem("Select Preset...")
        self._populate_digit_set_presets(self.output_digit_set_preset_combo)
        self.output_digit_set_preset_combo.setToolTip(
            "Select a predefined digit set for the output."
        )

        output_digit_set_group_layout.addLayout(output_label_layout)
        output_digit_set_group_layout.addLayout(output_digit_set_edit_layout)
        output_digit_set_group_layout.addWidget(
            self.output_digit_set_preset_combo
        )
        digit_set_layout.addLayout(output_digit_set_group_layout)

        # Rebase Trigger and Real-time Checkbox
        rebase_control_layout: QHBoxLayout = QHBoxLayout()
        self.rebase_button: QPushButton = QPushButton("Rebase")
        self.rebase_button.setToolTip(
            "Perform the rebase operation based on current inputs."
        )
        self.realtime_checkbox: QCheckBox = QCheckBox("Real-time Rebase")
        self.realtime_checkbox.setToolTip(
            "Enable or disable automatic rebase as you type."
        )
        rebase_control_layout.addWidget(self.rebase_button)
        rebase_control_layout.addWidget(self.realtime_checkbox)
        self.main_layout.addLayout(rebase_control_layout)

        # Output String Display Area
        output_layout: QHBoxLayout = QHBoxLayout()
        self.output_label: QLabel = QLabel("Rebased String:")
        output_icon = self._load_svg_icon(ICON_OUTPUT_QRC_PATH)
        output_layout.addWidget(output_icon)
        output_layout.addWidget(self.output_label)
        output_layout.addStretch()
        self.output_text_edit: QTextEdit = QTextEdit()
        self.output_text_edit.setReadOnly(True)
        self.output_text_edit.setPlaceholderText(
            "Rebased output will appear here..."
        )
        self.output_text_edit.setToolTip("The result of the rebase operation.")
        self.main_layout.addLayout(output_layout)
        self.main_layout.addWidget(self.output_text_edit)

    def _populate_digit_set_presets(self, combo_box: QComboBox) -> None:
        """
        Populates the given QComboBox with predefined digit set names.

        Args:
            combo_box: The QComboBox widget to populate.
        """
        digit_sets: Dict[str, DigitSet] = get_predefined_digit_sets()
        for name in sorted(digit_sets.keys()):
            combo_box.addItem(name)

    def _connect_signals(self) -> None:
        """
        Connects UI signals to their respective slots for interactive behavior.
        """
        self.rebase_button.clicked.connect(self._perform_rebase)
        self.input_digit_set_preset_combo.currentIndexChanged.connect(
            self._update_input_ds_from_preset
        )
        self.output_digit_set_preset_combo.currentIndexChanged.connect(
            self._update_output_ds_from_preset
        )
        self.realtime_checkbox.stateChanged.connect(
            self._toggle_realtime_rebase
        )
        self.input_text_edit.textChanged.connect(self._on_input_changed)
        self.input_digit_set_text_edit.textChanged.connect(
            self._on_digit_set_changed
        )
        self.input_digit_set_text_edit.textChanged.connect(
            self._handle_input_ds_dynamic_state
        )
        # Connect focusInEvent for clearing dynamic state
        self.input_digit_set_text_edit.installEventFilter(self)
        self.output_digit_set_text_edit.textChanged.connect(
            self._on_digit_set_changed
        )

    def _update_input_ds_from_preset(self, index: int) -> None:
        """
        Updates the input digit set text edit based on the selected preset
        from the input digit set combo box.

        Args:
            index: The index of the selected item in the combo box.
        """
        if index > 0:  # Skip "Select Preset..."
            selected_name: str = self.input_digit_set_preset_combo.currentText()
            if selected_name == "Derived from Input":
                input_string_content: str = self.input_text_edit.toPlainText()

                input_digit_set_map: Dict[str, int] = {
                    char: i
                    for i, char in enumerate(
                        dict.fromkeys(input_string_content)
                    )
                }

                derived_digit_sets: List[str] = list(input_digit_set_map.keys())

                if derived_digit_sets:
                    self.input_digit_set_text_edit.setText(
                        "".join(derived_digit_sets)
                    )
                else:
                    self.input_digit_set_text_edit.clear()
                self.input_digit_set_text_edit.setPlaceholderText(
                    "Enter input digit set or select preset (or leave empty "
                    "for dynamic derivation)..."
                )
                self.input_digit_set_text_edit.setStyleSheet("")

            else:
                digit_sets: Dict[str, DigitSet] = get_predefined_digit_sets()
                digit_set_obj: Optional[DigitSet] = digit_sets.get(
                    selected_name
                )

                if digit_set_obj:
                    self.input_digit_set_text_edit.setText(digit_set_obj.digits)
                else:
                    self.input_digit_set_text_edit.clear()
                self.input_digit_set_text_edit.setPlaceholderText(
                    "Enter input digit set or select preset (or leave empty "
                    "for dynamic derivation)..."
                )
                self.input_digit_set_text_edit.setStyleSheet("")

    def _update_output_ds_from_preset(self, index: int) -> None:
        """
        Updates the output digit set text edit based on the selected preset
        from the output digit set combo box.

        Args:
            index: The index of the selected item in the combo box.
        """
        if index > 0:
            selected_name: str = (
                self.output_digit_set_preset_combo.currentText()
            )

            digit_sets: Dict[str, DigitSet] = get_predefined_digit_sets()
            digit_set_obj: Optional[DigitSet] = digit_sets.get(selected_name)
            if digit_set_obj:
                self.output_digit_set_text_edit.setText(digit_set_obj.digits)
            else:
                self.output_digit_set_text_edit.clear()
            self.output_digit_set_text_edit.setStyleSheet("")

    def _toggle_realtime_rebase(self, state: int) -> None:
        """
        Toggles real-time rebase functionality based on the checkbox state.

        Args:
            state: The new state of the checkbox (Qt.Checked or Qt.Unchecked).
        """
        if state == Qt.Checked:
            self.rebase_button.setEnabled(False)
            self._perform_rebase()  # Perform initial rebase
        else:
            self.rebase_button.setEnabled(True)

    def _on_input_changed(self) -> None:
        """
        Handles changes in the input string text edit.
        Triggers rebase if real-time rebase is enabled and updates dynamic state.
        """
        if self.realtime_checkbox.isChecked():
            self._perform_rebase()
        self._handle_input_ds_dynamic_state()

    def _on_digit_set_changed(self) -> None:
        """
        Handles changes in the digit set text edits (input and output).
        Triggers rebase if real-time rebase is enabled and updates dynamic state.
        """
        if self.realtime_checkbox.isChecked():
            self._perform_rebase()
        self._handle_input_ds_dynamic_state()

    def _handle_input_ds_dynamic_state(self) -> None:
        """
        Manages the dynamic placeholder text and styling for the input digit set
        text edit based on the content of the input string.

        If the input digit set field is empty and the input string is not empty,
        it derives and displays a "Derived:" placeholder. Otherwise, it resets
        the placeholder and styling.
        """
        input_string_content: str = self.input_text_edit.toPlainText()
        if (
            not self.input_digit_set_text_edit.toPlainText()
        ):  # If input digit set field is empty
            if input_string_content:  # If input string is not empty
                input_digit_set_map: Dict[str, int] = {
                    char: i for i, char in enumerate(input_string_content)
                }
                derived_digit_sets: List[str] = list(input_digit_set_map.keys())

                if derived_digit_sets:
                    self.input_digit_set_text_edit.setPlaceholderText(
                        f"Derived: {''.join(derived_digit_sets)}"
                    )
                    self.input_digit_set_text_edit.setStyleSheet(
                        "background-color: lightyellow;"
                    )
                else:
                    self.input_digit_set_text_edit.setPlaceholderText(
                        (
                            "Enter input digit set or select preset (or leave empty "
                            "for dynamic derivation)..."
                        )
                    )
                    self.input_digit_set_text_edit.setStyleSheet("")
            else:
                self.input_digit_set_text_edit.setPlaceholderText(
                    (
                        "Enter input digit set or select preset (or leave empty "
                        "for dynamic derivation)..."
                    )
                )
                self.input_digit_set_text_edit.setStyleSheet("")
        else:
            self.input_digit_set_text_edit.setPlaceholderText(
                (
                    "Enter input digit set or select preset (or leave empty for "
                    "dynamic derivation)..."
                )
            )
            self.input_digit_set_text_edit.setStyleSheet("")

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """
        Filters events for specific UI elements, primarily to handle focus
        events for the input digit set text edit.

        Args:
            obj: The object for which the event occurred.
            event: The event that occurred.

        Returns:
            True if the event was handled, False otherwise.
        """
        if (
            obj == self.input_digit_set_text_edit
            and event.type() == QEvent.FocusIn
        ):
            # If currently showing a derived placeholder
            # and user focuses, clear it
            if (
                self.input_digit_set_text_edit.toPlainText() == ""
                and self.input_digit_set_text_edit.placeholderText().startswith(
                    "Derived:"
                )
            ):
                self.input_digit_set_text_edit.setPlaceholderText(
                    (
                        "Enter input digit set or select preset (or leave empty "
                        "for dynamic derivation)..."
                    )
                )
                self.input_digit_set_text_edit.setStyleSheet("")
                if (
                    self.input_digit_set_preset_combo.currentText()
                    == "Derived from Input"
                ):
                    self.input_digit_set_preset_combo.setCurrentIndex(0)
        return super().eventFilter(obj, event)

    def _perform_rebase(self) -> None:
        """
        Performs the rebase operation based on the current input string,
        source digit set, and target digit set from the UI.
        Displays the rebased string or an error message in the status bar.
        """
        input_string: str = self.input_text_edit.toPlainText()
        input_digit_set_str: Optional[str] = (
            self.input_digit_set_text_edit.toPlainText()
        )
        output_digit_set_str: Optional[str] = (
            self.output_digit_set_text_edit.toPlainText()
        )

        input_digit_set_obj: Optional[DigitSet] = None
        output_digit_set_obj: Optional[DigitSet] = None

        # Determine input digit set object
        if input_digit_set_str:
            input_digit_set_obj = DigitSet(
                name="Custom Input",
                digits=input_digit_set_str,
                source="gui_input",
            )

        # Determine output digit set object
        if output_digit_set_str:
            if len(set(output_digit_set_str)) == 1:
                output_digit_set_obj = None
            else:
                output_digit_set_obj = DigitSet(
                    name="Custom Output",
                    digits=output_digit_set_str,
                    source="gui_input",
                )

        self.status_bar.clearMessage()  # Clear any previous messages
        self.output_text_edit.clear()  # Clear output on new rebase attempt

        try:
            rebaser = DigitSetRebaser(
                out_digit_set=output_digit_set_obj,
                in_digit_set=input_digit_set_obj,
            )
            rebased_string: str = rebaser.rebase(input_string)
            self.output_text_edit.setText(rebased_string)
            self.status_bar.clearMessage()
        except ValueError as exc:
            error_message: str = f"Error: {exc}"
            self.status_bar.showMessage(error_message)
            print(error_message, file=sys.stderr)
        except IndexError as exc:
            error_message = f"Error: {exc}"
            self.status_bar.showMessage(error_message)
            print(error_message, file=sys.stderr)
        except (
            RuntimeError
        ) as err:  # Catching RuntimeError as an isolation point for unexpected errors.
            error_message = f"An unexpected error occurred: {err}"
            self.status_bar.showMessage(error_message)
            print(error_message, file=sys.stderr)

    def _setup_digit_set_menu(
        self, button: QToolButton, text_edit: QTextEdit
    ) -> None:
        """
        Sets up the context menu for digit set text edits, providing options
        like Clear, Sort, and Deduplicate.

        Args:
            button: The QToolButton to attach the menu to.
            text_edit: The QTextEdit associated with the digit set.
        """
        menu = QMenu(self)

        clear_action = menu.addAction("Clear")
        clear_action.setToolTip("Clear the content of the digit set field.")
        clear_action.triggered.connect(text_edit.clear)

        sort_action = menu.addAction("Sort")
        sort_action.setToolTip(
            "Sort the characters in the digit set alphabetically."
        )
        sort_action.triggered.connect(
            lambda: self._sort_digit_set_text(text_edit)
        )

        deduplicate_action = menu.addAction("Deduplicate")
        deduplicate_action.setToolTip(
            "Remove duplicate characters from the digit set, preserving order "
            "of first appearance."
        )
        deduplicate_action.triggered.connect(
            lambda: self._deduplicate_digit_set_text(text_edit)
        )

        button.setMenu(menu)

    def _sort_digit_set_text(self, text_edit: QTextEdit) -> None:
        """
        Sorts the characters in the given QTextEdit alphabetically.

        Args:
            text_edit: The QTextEdit widget whose content needs to be sorted.
        """
        current_text = text_edit.toPlainText()
        if current_text:
            sorted_chars = sorted(list(current_text))
            text_edit.setText("".join(sorted_chars))

    def _deduplicate_digit_set_text(self, text_edit: QTextEdit) -> None:
        """
        Removes duplicate characters from the given QTextEdit, preserving
        the order of their first appearance.

        Args:
            text_edit: The QTextEdit widget whose content needs to be deduplicated.
        """
        current_text = text_edit.toPlainText()
        if current_text:
            deduplicated_chars = "".join(dict.fromkeys(current_text))
            text_edit.setText(deduplicated_chars)

    def _load_initial_state(self) -> None:
        """
        Loads the saved UI state (input string, digit sets, real-time setting)
        from the configuration file and applies it to the UI elements.
        """
        state: Dict[str, Any] = load_ui_state()
        if state:
            self.input_text_edit.setText(state.get("last_input", ""))
            self.input_digit_set_text_edit.setText(
                state.get("last_source_digit_set", "")
            )
            self.output_digit_set_text_edit.setText(
                state.get("last_target_digit_set", "")
            )
            self.realtime_checkbox.setChecked(
                state.get("realtime_enabled", False)
            )
        self._handle_input_ds_dynamic_state()

    def closeEvent(self, event: QEvent) -> None:
        """
        Overrides the default close event to save the current UI state
        before the application exits.

        Args:
            event: The close event.
        """
        state_data: Dict[str, Any] = {
            "last_input": self.input_text_edit.toPlainText(),
            "last_source_digit_set": self.input_digit_set_text_edit.toPlainText(),
            "last_target_digit_set": self.output_digit_set_text_edit.toPlainText(),
            "realtime_enabled": self.realtime_checkbox.isChecked(),
        }
        save_ui_state(state_data)
        event.accept()


def run_gui() -> None:
    """
    Runs the BaseBender GUI application.

    Initializes the QApplication, creates and shows the MainWindow,
    and starts the application's event loop.
    """
    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.show()
    # sys.exit() is used here as it's the standard way to exit a Qt application's event loop.
    sys.exit(app.exec())


if __name__ == "__main__":
    run_gui()
