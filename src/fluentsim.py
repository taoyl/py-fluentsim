# -*- coding: gb18030 -*-
# -*- coding: utf-8 -*-

"""
Module implementing FluentSim.
"""


import re
import os

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow

from newprojdialog import NewProjDialog
from uimainwindow import UiMainWindow

from models import JouFileModel


class FluentSim(QMainWindow, UiMainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # initiate models
        self.jou_model = JouFileModel()
    
    @pyqtSignature("")
    def on_btn_run_sim_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSignature("")
    def on_btn_load_jou_param_clicked(self):
        """
        Load paramters from the journal file to widgets.
        """
        fname = self.le_fluent_jou_file.text()
        # check if file name is empty
        if fname == '':
            msg = u'Jou�ļ���Ϊ��, ���ȴ�һ��Jou�ļ�!'
            self._show_tips(msg, tip_type=1)
            return
        # check if file path exists
        if not os.path.exists(fname):  
            msg = u'Jou�ļ�·��������, ���һ����ЧJou�ļ�·��!'
            self._show_tips(msg, tip_type=1)
            return
        params = self.jou_model.read_params(fname)
        if params != None:
            # update widgets
            self.fresh_fluent_param_widgets(params)
            msg = u'Fluent Journal�ļ����سɹ�'
            self._show_tips(msg)
        else:
            msg = u'Fluent Journal�ļ�����ʧ��, ��ȷ��Journal�ļ�����Ч��!'
            self._show_tips(msg, tip_type=1)

    @pyqtSignature("")
    def on_btn_load_udf_param_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("")
    def on_btn_save_jou_param_clicked(self):
        """
        Save all fluent journal params to file.
        """
        # first, get params from widgets
        params = self.get_fluent_param_from_widgets()
        # second, modify the jou file
        fname = self.le_fluent_jou_file.text()
        if fname == '':
            msg = u'Jou�ļ���Ϊ��, ��������һ����Ч��Jou�ļ�'
            self._show_tips(msg, tip_type=1)
            return
        # check if file path exists
        if not os.path.exists(fname):  
            msg = u'Jou�ļ�·��������, ���һ����Ч��Jou�ļ�!'
            self._show_tips(msg, tip_type=1)
            return

        result = self.jou_model.write_params(params, fname)
        if result == True:
            msg = u'�ļ�%s���³ɹ�' % fname
            self._show_tips(msg)
        else:
            msg = u'�ļ�����ʧ��, ��ȷ��%s����Ч��Jou�ļ�' % fname
            self._show_tips(msg, tip_type=1)
    
    @pyqtSignature("")
    def on_btn_save_udf_param_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("")
    def on_btn_open_fluent_cas_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.le_fluent_cas_file.text() != '':
            msg = u'Case�ļ��Ѵ򿪣�ȷ������һ���滻��?'
            reply = self.show_yesno_msgbox(msg)
            if reply == 0:
                return
        fname = self.show_file_dialog('Fluent case file (*.cas)')
        if fname != '':
            self.le_fluent_cas_file.setText(fname)
            msg = u'�µ�Case�ļ��Ѵ�, ���뱣������ǰ���̣��������湤�̰�ť'
            self._show_tips(msg)
    
    @pyqtSignature("")
    def on_btn_open_fluent_jou_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.le_fluent_jou_file.text() != '':
            msg = u'Jou�ļ��Ѵ򿪣�ȷ������һ���滻��?'
            reply = self.show_yesno_msgbox(msg)
            if reply == 0:
                return
        fname = self.show_file_dialog('Fluent journal file (*.jou)')
        if fname != '':
            self.le_fluent_jou_file.setText(fname)
            msg = u'�µ�Jou�ļ��Ѵ�, ���뱣������ǰ���̣��������湤�̰�ť'
            self._show_tips(msg)
    
    @pyqtSignature("")
    def on_btn_open_fluent_udf_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.le_fluent_udf_file.text() != '':
            msg = u'UDF�ļ��Ѵ򿪣�ȷ������һ���滻��?'
            reply = self.show_yesno_msgbox(msg)
            if reply == 0:
                return
        fname = self.show_file_dialog('Fluent udf file (*.c)')
        if fname != '':
            self.le_fluent_udf_file.setText(fname)
            msg = u'�µ�UDF�ļ��Ѵ�, ���뱣������ǰ���̣��������湤�̰�ť'
            self._show_tips(msg)
    
    @pyqtSignature("")
    def on_btn_open_fluent_load_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.le_fluent_load_file.text() != '':
            msg = u'���������ļ��Ѵ򿪣�ȷ������һ���滻��?'
            reply = self.show_yesno_msgbox(msg)
            if reply == 0:
                return
        fname = self.show_file_dialog('Fluent load file (*)')
        if fname != '':
            self.le_fluent_load_file.setText(fname)
            msg = u'�µĽ��������ļ��Ѵ�, ���뱣������ǰ���̣��������湤�̰�ť'
            self._show_tips(msg)

    @pyqtSignature("")
    def on_btn_open_fluent_path_clicked(self):
        """
        Slot documentation goes here.
        """
        fname = self.show_file_dialog('Fluent exe file (*.exe)')
        if fname != '':
            self.le_fluent_path.setText(fname)
            msg = u'Fluent����·��������'
            self._show_tips(msg)
    
    @pyqtSignature("")
    def on_btn_open_proj_clicked(self):
        """
        open project file button is clicked
        """
        # open file dialog and get the slected file name
        fname = self.show_file_dialog('Project File (*.proj)')
        if fname == '':
            return
        # read the project file
        if self.read_proj_file(fname) == False:
            msg = u"��Ч�����ļ�����ѡ���µ��ļ����½�һ������"
            self._show_tips(msg, tip_type=1)
        else:
            self.statusbar.showMessage(u"����%s�Ѽ��سɹ�" % self.proj_name)
            # set window title and line edit widgets
            self.setWindowTitle(u'���� - %s' % self.proj_name)
            self.le_proj_file.setText(fname)
            self.le_fluent_jou_file.setText(self.fluent_jou_file)
            self.le_fluent_cas_file.setText(self.fluent_cas_file)
            self.le_fluent_udf_file.setText(self.fluent_udf_file)
            self.le_fluent_load_file.setText(self.fluent_load_file)
            self.le_fluent_path.setText(self.fluent_exe_path)
    
    @pyqtSignature("")
    def on_btn_new_proj_clicked(self):
        """
        New a project
        """
        dialog = NewProjDialog(self)
        dialog.show()
    
    @pyqtSignature("")
    def on_btn_save_proj_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("")
    def on_action_menu_quit_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("")
    def on_action_menu_about_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    def _get_dict_val(self, d, key):
        if d.has_key(key):
            return d[key]
        else:
            return ''
    
    def _show_tips(self, msg, tip_type=0):
        """
        Pop information tips.

        @param tip_type: 0=information, 1=warning.
        """
        self.statusbar.showMessage(msg)
        if tip_type == 0:
            QtGui.QMessageBox.information(self, 'Information', msg, 
                            QtGui.QMessageBox.Ok)
        else:
            QtGui.QMessageBox.warning(self, 'Warning', msg, 
                            QtGui.QMessageBox.Ok)

    def show_yesno_msgbox(self, msg):
        """
        Show Yes/No message box and return user's selection.
        """
        reply = QtGui.QMessageBox.question(self, 'Message', msg,
                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                        QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.No:
            return 0
        else:
            return 1

    def show_file_dialog(self, file_filter=''):
        """
        Show open file dialog and return the selected file name
        """
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                        './', file_filter)
        return fname

    def read_proj_file(self, fname):
        """
        Read the project file
        """
        with open(fname) as fh:
             lines_list = fh.readlines()
        lines = ''.join(lines_list)
        res = re.findall(r"\[(\w+)\]\s*=\s*(.*)", lines)
        if len(res) == 0:
            return False
        config_dict = dict((key,val) for key,val in res)
        self.proj_name        = self._get_dict_val(config_dict, 'ProjectName')
        self.fluent_jou_file  = self._get_dict_val(config_dict, 'FluentJournal')
        self.fluent_cas_file  = self._get_dict_val(config_dict, 'FluentCase')
        self.fluent_udf_file  = self._get_dict_val(config_dict, 'FluentUdf')
        self.fluent_load_file = self._get_dict_val(config_dict, 'FluentLoadData')
        self.fluent_exe_path  = self._get_dict_val(config_dict, 'FluentExePath')
        return True

    def fresh_fluent_param_widgets(self, params):
        """
        Set all line edit widgets of fluent parameters.
        """
        self.le_backfill_heat_coeff.setText(params['backfill_heat_coeff'])
        self.le_backfill_density.setText(params['backfill_density'])
        self.le_backfill_spec_heat.setText(params['backfill_spec_heat'])
        self.le_pipe_heat_coeff.setText(params['pipe_heat_coeff'])
        self.le_pipe_density.setText(params['pipe_density'])
        self.le_pipe_spec_heat.setText(params['pipe_spec_heat'])
        self.le_soil_heat_coeff.setText(params['soil_heat_coeff'])
        self.le_soil_density.setText(params['soil_density'])
        self.le_soil_spec_heat.setText(params['soil_spec_heat'])
        self.le_init_ground_temp.setText(params['ground_temp'])
        self.le_loop_velocity.setText(params['loop_velocity'])
        self.le_loop_hydr_diameter.setText(params['loop_diameter'])
        percent = float(params['loop_intensity']) * 100
        self.le_loop_intensity.setText('%s' % percent)

        # iterate time
        self.le_fluent_time_step.setText(params['time_step'])
        self.le_fluent_time_year.setText(params['time_year'])
        self.le_fluent_time_month.setText(params['time_month'])
        self.le_fluent_time_day.setText(params['time_day'])
        self.le_fluent_time_hour.setText(params['time_hour'])

    def get_fluent_param_from_widgets(self):
        """
        Get fluent paramters from line edits.
        """
        params = {}

        # file
        params['case_file'] = self.le_fluent_cas_file.text()
        params['udf_file'] = self.le_fluent_udf_file.text()
        # simualtion paramters
        params['backfill_heat_coeff'] = self.le_backfill_heat_coeff.text()
        params['backfill_density'] = self.le_backfill_density.text()
        params['backfill_spec_heat'] = self.le_backfill_spec_heat.text()
        params['pipe_heat_coeff'] = self.le_pipe_heat_coeff.text()
        params['pipe_density'] = self.le_pipe_density.text()
        params['pipe_spec_heat'] = self.le_pipe_spec_heat.text()
        params['soil_heat_coeff'] = self.le_soil_heat_coeff.text()
        params['soil_density'] = self.le_soil_density.text()
        params['soil_spec_heat'] = self.le_soil_spec_heat.text()
        params['ground_temp'] = self.le_init_ground_temp.text()
        params['loop_velocity'] = self.le_loop_velocity.text()
        params['loop_diameter'] = self.le_loop_hydr_diameter.text()
        conv_float = float(self.le_loop_intensity.text()) / 100.0
        params['loop_intensity'] = '%s' % conv_float
        # iterate time
        params['time_step'] = self.le_fluent_time_step.text()
        params['time_year'] = self.le_fluent_time_year.text()
        params['time_month'] = self.le_fluent_time_month.text()
        params['time_day'] = self.le_fluent_time_day.text()
        params['time_hour'] = self.le_fluent_time_hour.text()
        return params


if __name__ == "__main__":
    import sys
    app= QtGui.QApplication(sys.argv)
    mw = FluentSim()
    mw.show()
    sys.exit(app.exec_())
