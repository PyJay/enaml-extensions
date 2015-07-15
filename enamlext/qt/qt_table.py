# TODO: import from Enaml's abstraction layer of Qt (so it works with PySide)
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from enaml.qt.qt_control import QtControl
from atom.api import Typed

from enamlext.widgets.table import ProxyTable


class TableModel(QAbstractTableModel):
    def __init__(self, columns=None, rows=None, parent=None):
        super(TableModel, self).__init__(parent=parent)
        self.columns = columns or []
        self.rows = rows or []

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, columns):
        self._columns = columns
        self.reset()

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, rows):
        self._rows = rows
        self.reset()

    def rowCount(self, parent=None):
        return len(self.rows)

    def columnCount(self, parent=None):
        return len(self.columns)

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            value = self.get_value(index.row(), index.column())
            return value

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                column = self.get_column(section)
                return column.title

        return super(TableModel, self).headerData(section, orientation, role)

    def get_value(self, row_index, column_index):
        column = self.get_column(column_index)
        row = self.get_row(row_index)
        return column.get_value(row)

    def get_column(self, column_index):
        return self.columns[column_index]

    def get_row(self, row_index):
        return self.rows[row_index]


class QTable(QTableView):
    def __init__(self, columns=None, rows=None, parent=None):
        super(QTable, self).__init__(parent=parent)
        model = TableModel(columns=columns, rows=rows, parent=self)
        self.setModel(model)

    def setColumns(self, columns):
        self.model().columns = columns

    def setRows(self, rows):
        self.model().rows = rows


class QtTable(QtControl, ProxyTable):
    widget = Typed(QTable)

    def create_widget(self):
        self.widget = QTable(parent=self.parent_widget())

    def init_widget(self):
        super(QtTable, self).init_widget()
        d = self.declaration
        self.set_columns(d.columns)
        self.set_rows(d.rows)

    def set_columns(self, columns):
        self.widget.setColumns(columns)

    def set_rows(self, rows):
        self.widget.setRows(rows)
