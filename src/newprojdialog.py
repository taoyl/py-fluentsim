# -*- coding: gb18030 -*-
# -*- coding: utf-8 -*-

"""
Module implementing FluentSim.
"""

from PyQt4 import QtGui
from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt4.QtGui import QDialog

class Communicate(QObject):
    proj_name_changed = pyqtSignal(str,str)


class NewProjDialog(QDialog):
    """
    Dialog for creating a new project.
    """
    def __init__(self, parent=None):
        super(NewProjDialog, self).__init__(parent)

        # create widgets
        lb_proj_name = QtGui.QLabel(u"工程名称:")
        lb_proj_file = QtGui.QLabel(u"工程文件:")
        self.le_proj_name = QtGui.QLineEdit()
        self.le_proj_file = QtGui.QLineEdit()
        self.btn_browse_file = QtGui.QPushButton(u"浏览...")
        self.btn_create = QtGui.QPushButton(u"创建")
        self.btn_cancel = QtGui.QPushButton(u"取消")

        # layout placement
        main_layout = QtGui.QGridLayout()
        main_layout.addWidget(lb_proj_name, 0, 0)
        main_layout.addWidget(self.le_proj_name, 0, 1, 1, 4)
        main_layout.addWidget(lb_proj_file, 1, 0)
        main_layout.addWidget(self.le_proj_file, 1, 1, 1, 4)
        main_layout.addWidget(self.btn_browse_file, 1, 5, 1, 1)
        main_layout.addWidget(self.btn_create, 2, 2, 1, 1)
        main_layout.addWidget(self.btn_cancel, 2, 3, 1, 1)
        self.setLayout(main_layout)

        # conenct signals and slots
        self.btn_browse_file.clicked.connect(self.browse_file)
        self.btn_create.clicked.connect(self.create_proj_file)
        self.btn_cancel.clicked.connect(self.close)

        self.com = Communicate()
        self.com.proj_name_changed[str,str].connect(parent.change_proj_name)

        self.setWindowTitle(u"新建工程")
        self.setFixedSize(600, 100)
        self.setModal(True)

    @pyqtSlot()
    def browse_file(self):
        """
        Create project file.
        """
        fname = QtGui.QFileDialog.getSaveFileName(self, 'New project file', 
                        './', 'Project file (*.proj)')
        self.le_proj_file.setText(fname)

    @pyqtSlot()
    def create_proj_file(self):
        """
        Create project file.
        """
        proj_file = self.le_proj_file.text()
        proj_name = self.le_proj_name.text()
        # check if filename and project name is empty
        if proj_name == '':
            QtGui.QMessageBox.warning(self, 'Warning',
                            u"工程名称不能为空",
                            QtGui.QMessageBox.Ok)
            return
        elif proj_file == '':
            QtGui.QMessageBox.warning(self, 'Warning',
                            u"文件名不能为空",
                            QtGui.QMessageBox.Ok)
            return
        # create and write file
        lines = []
        lines.append("[ProjectName]=%s" % proj_name)
        with open(proj_file, 'w') as fh:
             fh.writelines(lines)
        # notify the parent to update project name
        self.com.proj_name_changed.emit(proj_name, proj_file)
        self.close()

