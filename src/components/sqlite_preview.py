from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QComboBox
from .preview_base import PreviewBase
import sqlite3

class SqlitePreview(PreviewBase):
    def __init__(self):
        super().__init__()
        self.allowed_file_types = ['db', 'sqlite', 'sqlite3', 'db3']

        self.table_selection = QComboBox()
        self.table_selection.currentIndexChanged.connect(self.on_table_changed)
        self._toolbar.addWidget(self.table_selection)

        self.table = QTableWidget()

        self.base.addWidget(self.table)

    def on_table_changed(self):
        if self.table_selection.count() >= 1:
            self.set_file_based_on_table(self.get_file_full_path(), self.table_selection.currentText())

    def set_file_based_on_table(self, file_full_path, table_name):
        db = sqlite3.connect(file_full_path)
        cursor = db.cursor()

        content = cursor.execute(f"SELECT * FROM {table_name}")
        content_rows = content.fetchall()
        headers = [description[0] for description in content.description]

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        row_count = 0
        column_count = 0
        for i in content_rows:
            row_count+=1
            column_count = 0
            self.table.setRowCount(row_count)
            for x in i:
                self.table.setItem(row_count-1, column_count, QTableWidgetItem(str(x)))
                column_count+=1

        
        cursor.close()
        db.close()
    
    def set_file(self, file_full_path):
        super().set_file(file_full_path)
        self.table_selection.clear()
        db = sqlite3.connect(file_full_path)
        cursor = db.cursor()
        
        tables = cursor.execute("SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_'").fetchall()
        rows = [r[0] for r in tables]
        self.table_selection.addItems(rows)

        current_table = self.table_selection.currentText()
        self.set_file_based_on_table(file_full_path, current_table)

        cursor.close()
        db.close()
        