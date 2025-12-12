from copy import deepcopy
from pathlib import Path
from numpy import genfromtxt,abs

# PySide6 imports
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QDialog,
                               QTableWidget, QTableWidgetItem, QHeaderView)


class PermittivityEditDialog(QDialog):
    """Dialog for editing layer permittivities"""

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = deepcopy(config)
        self.original_config = config
        self.setWindowTitle("Edit Layer Permittivities")
        self.setModal(True)
        self.resize(800, 600)

        self.setup_ui()
        self.populate_table()

    def setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout(self)

        # Instructions
        instructions = QLabel(
            "Edit permittivity values for each layer. You can enter a numeric value or import from CSV file.")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        # Table for layers (ONLY 3 columns - no thickness)
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Thickness (mm)", "Permittivity", "Action"])

        # Configure table
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)

        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(2, 120)

        layout.addWidget(self.table)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)

        self.apply_btn = QPushButton("Apply")
        self.apply_btn.setObjectName("apply_btn")
        self.apply_btn.clicked.connect(self.apply_changes)
        button_layout.addWidget(self.apply_btn)

        layout.addLayout(button_layout)

    def populate_table(self):
        """Populate the table with layer data"""
        if not self.config or 'mut' not in self.config:
            return

        layers = self.config['mut']
        self.table.setRowCount(len(layers))

        for i, layer in enumerate(layers):
            # Layer index
            layer_item = QTableWidgetItem(f"{layer['thickness'] * 1e3}")
            layer_item.setFlags(layer_item.flags())
            self.table.setItem(i, 0, layer_item)

            # Permittivity - SHOW COMPLEX VALUES PROPERLY
            # Permittivity - SHOW COMPLEX VALUES PROPERLY
            epsilon = layer.get('epsilon_r', 1.0)
            if isinstance(epsilon, str):
                perm_item = QTableWidgetItem(f"CSV: {Path(epsilon).name}")
            elif isinstance(epsilon, (int, float)):
                perm_item = QTableWidgetItem(f"{epsilon:.6f}")
            elif isinstance(epsilon, complex):
                sign = '+' if epsilon.imag >= 0 else '-'
                perm_item = QTableWidgetItem(f"{epsilon.real:.6f} {sign} {abs(epsilon.imag):.6f}j")
            else:
                perm_item = QTableWidgetItem(f"{epsilon}")

            self.table.setItem(i, 1, perm_item)

            # Actions button
            import_btn = QPushButton("Import CSV")
            import_btn.clicked.connect(lambda checked, row=i: self.import_csv_for_layer(row))
            self.table.setCellWidget(i, 2, import_btn)

    def import_csv_for_layer(self, layer_index):
        """Import CSV file for a specific layer"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, f"Import CSV for Layer {layer_index}", "", "CSV Files (*.csv);;All Files (*)"
        )

        if file_path:
            try:
                # Validate CSV format
                data = genfromtxt(file_path, delimiter=',', skip_header=1)
                if data.shape[1] < 3:
                    QMessageBox.warning(self, "Invalid CSV",
                                        "CSV must have at least 3 columns: Frequency, Real_Epsilon, Imag_Epsilon")
                    return

                # Update config
                self.config['mut'][layer_index]['epsilon_r'] = file_path

                # Update table display
                perm_item = QTableWidgetItem(f"CSV: {Path(file_path).name}")
                self.table.setItem(layer_index, 1, perm_item)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error importing CSV:\n{str(e)}")

    def apply_changes(self):
        """Apply changes to the original config"""
        try:
            # Update permittivity values from table
            for i in range(self.table.rowCount()):
                thick_item = self.table.item(i, 0)
                perm_item = self.table.item(i, 1)
                if thick_item:
                    # Try to parse as numeric value
                    try:
                        thick_text = thick_item.text()
                        thick_value = float(thick_text.replace(' ', '')) * 1e-3
                        self.config['mut'][i]['thickness'] = thick_value
                    except ValueError as e:
                        QMessageBox.warning(self, e)
                        return

                if perm_item:
                    perm_text = perm_item.text()

                    if perm_text.startswith("CSV:"):
                        # Keep the CSV file path (already in config)
                        continue
                    else:
                        # Try to parse as numeric value
                        try:
                            perm_value = complex(perm_text.replace(' ', ''))
                            self.config['mut'][i]['epsilon_r'] = perm_value
                        except ValueError as e:
                            QMessageBox.warning(self, e)
                            return

            # Copy changes to original config
            self.original_config['mut'] = deepcopy(self.config['mut'])

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error applying changes:\n{str(e)}")
