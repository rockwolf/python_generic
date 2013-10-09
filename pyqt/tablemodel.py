#/usr/bin/env python
from PyQt4 import QtCore, QtGui, uic
import sys

class TableModel(QtCore.QAbstractTableModel):
    """
        Table model for a TableView, generic reusable code
    """

    def __init__(self, data = [[]], headers = [], parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.__values = data
        self.__headers = headers
   
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section < len(self.__headers):
                    return self.__headers[section]
                else:
                    return "TEMP"
            else:
                return "{}".format(section)

    def rowCount(self, parent):
        return len(self.__values)

    def columnCount(self, parent):
        return len(self.__values[0])

    def data(self, index, role):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            return self.__values[row][column]
        if role == QtCore.Qt.ToolTipRole:
            row = index.row()
            column = index.column()
            return "data: " + self.__values[row][column]
        #if role == QtCore.Qt.DecorationRole:
        # row = index.row()
        # column = index.column()
        # value = self.__values[row][column]
        # pixmap = QtGui.QPixmap(26, 26)
        # pixmap.fill(value)
        # icon = QtGui.QIcon(pixmap)
        # return icon
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__values[row][column]
            return value
   
    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        print("-- test [setData]:", value)
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            #if value.isValid():
            print(value)
            self.__values[row][column] = value
            self.dataChanged.emit(index, index)
            return True
        return False
    
    def insertRows(self, position, rows, values = [], parent = QtCore.QModelIndex()):
        print("-- test [insertRows]:", values)
        self.beginInsertRows(QtCore.QModelIndex(), position, position + rows - 1)
        for i in range(rows):
            #for item in values[i]:
            #print("-- test [insertRows i={}]: {}".format(i, values[i]))
            #defaultValues = ["x" for i in range(self.columnCount(None))]
            #self.__values.insert(position, defaultValues)
            self.__values.insert(position, values[i])
        self.endInsertRows()
        return True

    def insertColumns(self, position, columns, values = [], parent = QtCore.QModelIndex()):
        self.beginInsertColumns(QtCore.QModelIndex(), position, position + columns - 1)
        row_count = len(self.__values)
        for i in range(columns):
            for j in range(row_count):
                self.__values[j].insert(position, values[j])
        self.endInsertColumns()
        return True

    def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginRemoveRows(QtCore.QModelIndex(), position, position + rows - 1)
        for i in range(rows):
            value = self.__values[position]
            self.__values.remove(value)
        self.endRemoveRows()
    
    def clear(self):
        """
Clear the data.
"""
        self.__values = [[]]

    def get_values(self):
        """
Returns the values.
"""
        return self.__values
