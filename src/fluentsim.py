# -*- coding: gb18030 -*-
# -*- coding: utf-8 -*-

"""
Module implementing FluentSim.

Author: taoyl <nerotao@foxmail.com>
Date  : Apr 21, 2015
"""


import re
import os

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignature, pyqtSlot
from PyQt4.QtGui import QMainWindow

from newprojdialog import NewProjDialog
from uimainwindow import UiMainWindow

from models import JouFileModel, UdfFileModel


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
        self.udf_model = UdfFileModel()

        # arritures
        self.proj_name = ''
    
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
            msg = u'Jou文件名为空, 请先打开一个Jou文件!'
            self._show_tips(msg, tip_type=1)
            return
        # check if file path exists
        if not os.path.exists(fname):  
            msg = u'Jou文件路径不存在, 请打开一个有效Jou文件路径!'
            self._show_tips(msg, tip_type=1)
            return
        params = self.jou_model.read_params(fname)
        if params != None:
            # update widgets
            self.fresh_fluent_param_widgets(params)
            msg = u'Fluent Journal文件%s加载成功' % fname
            self._show_tips(msg)
        else:
            msg = u'Journal文件加载失败, 请检查Journal文件%s的有效性!' % fname
            self._show_tips(msg, tip_type=1)

    @pyqtSignature("")
    def on_btn_load_udf_param_clicked(self):
        """
        Slot documentation goes here.
        """
        fname = self.le_fluent_udf_file.text()
        # check if file name is empty
        if fname == '':
            msg = u'UDF文件名为空, 请先打开一个UDF文件!'
            self._show_tips(msg, tip_type=1)
            return
        # check if file path exists
        if not os.path.exists(fname):  
            msg = u'UDF文件路径不存在, 请打开一个有效UDF文件路径!'
            self._show_tips(msg, tip_type=1)
            return
        params = self.udf_model.read_params(fname)
        if params != None:
            # update widgets
            self.fresh_udf_param_widgets(params)
            msg = u'UDF文件%s加载成功' % fname
            self._show_tips(msg)
        else:
            msg = u'UDF文件加载失败, 请检查UDF文件%s的有效性!' % fname
            self._show_tips(msg, tip_type=1)

    
    @pyqtSignature("")
    def on_btn_save_jou_param_clicked(self):
        """
        Save all fluent journal params to file.
        """
        msg = u'保存所有Jou文件参数，确定吗?'
        reply = self.show_yesno_msgbox(msg)
        if reply == 0:
            return
        # first, get params from widgets
        params = self.get_fluent_param_from_widgets()
        # second, modify the jou file
        fname = self.le_fluent_jou_file.text()
        if fname == '':
            msg = u'Jou文件名为空, 请先设置一个有效的Jou文件'
            self._show_tips(msg, tip_type=1)
            return
        # check if file path exists
        if not os.path.exists(fname):  
            msg = u'Jou文件路径不存在, 请打开一个有效的Jou文件!'
            self._show_tips(msg, tip_type=1)
            return

        result = self.jou_model.write_params(params, fname)
        if result == True:
            msg = u'文件%s更新成功' % fname
            self._show_tips(msg)
        else:
            msg = u'文件更新失败, 请确保%s是有效的Jou文件' % fname
            self._show_tips(msg, tip_type=1)
    
    @pyqtSignature("")
    def on_btn_save_udf_param_clicked(self):
        """
        Slot documentation goes here.
        """
        msg = u'保存参数并同时更新UDF中建筑负载文件名，确定吗?'
        reply = self.show_yesno_msgbox(msg)
        if reply == 0:
            return
        # first, get params from widgets
        params = self.get_udf_param_from_widgets()
        # second, modify the udf file
        fname = self.le_fluent_udf_file.text()
        if fname == '':
            msg = u'UDF文件名为空, 请先设置一个有效的UDF文件'
            self._show_tips(msg, tip_type=1)
            return
        # check if file path exists
        if not os.path.exists(fname):  
            msg = u'UDF文件路径不存在, 请打开一个有效的UDF文件!'
            self._show_tips(msg, tip_type=1)
            return

        result = self.udf_model.write_params(params, fname)
        if result == True:
            msg = u'文件%s更新成功' % fname
            self._show_tips(msg)
        else:
            msg = u'文件更新失败, 请确保%s是有效的UDF文件' % fname
            self._show_tips(msg, tip_type=1)
    
    @pyqtSignature("")
    def on_btn_open_fluent_cas_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.le_fluent_cas_file.text() != '':
            msg = u'Case文件已打开，确定打开另一个替换吗?'
            reply = self.show_yesno_msgbox(msg)
            if reply == 0:
                return
        fname = self.show_file_dialog('Fluent case file (*.cas)')
        if fname != '':
            self.le_fluent_cas_file.setText(fname)
            msg = u'新的Case文件已打开, 若想保存至当前工程，请点击保存工程按钮'
            self._show_tips(msg)
    
    @pyqtSignature("")
    def on_btn_open_fluent_jou_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.le_fluent_jou_file.text() != '':
            msg = u'Jou文件已打开，确定打开另一个替换吗?'
            reply = self.show_yesno_msgbox(msg)
            if reply == 0:
                return
        fname = self.show_file_dialog('Fluent journal file (*.jou)')
        if fname != '':
            self.le_fluent_jou_file.setText(fname)
            msg = u'新的Jou文件已打开, 若想保存至当前工程，请点击保存工程按钮'
            self._show_tips(msg)
    
    @pyqtSignature("")
    def on_btn_open_fluent_udf_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.le_fluent_udf_file.text() != '':
            msg = u'UDF文件已打开，确定打开另一个替换吗?'
            reply = self.show_yesno_msgbox(msg)
            if reply == 0:
                return
        fname = self.show_file_dialog('Fluent udf file (*.c)')
        if fname != '':
            self.le_fluent_udf_file.setText(fname)
            msg = u'新的UDF文件已打开, 若想保存至当前工程，请点击保存工程按钮'
            self._show_tips(msg)
    
    @pyqtSignature("")
    def on_btn_open_fluent_load_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.le_fluent_load_file.text() != '':
            msg = u'建筑负载文件已打开，确定打开另一个替换吗?'
            reply = self.show_yesno_msgbox(msg)
            if reply == 0:
                return
        fname = self.show_file_dialog('Fluent load file (*)')
        if fname != '':
            self.le_fluent_load_file.setText(fname)
            msg = u'新的建筑负荷文件已打开, 若想保存至当前工程，请点击保存工程按钮'
            self._show_tips(msg)

    @pyqtSignature("")
    def on_btn_open_fluent_path_clicked(self):
        """
        Slot documentation goes here.
        """
        fname = self.show_file_dialog('Fluent exe file (*.exe)')
        if fname != '':
            self.le_fluent_path.setText(fname)
            msg = u'Fluent程序路径已设置'
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
            msg = u"无效工程文件，请选择新的文件或新建一个工程"
            self._show_tips(msg, tip_type=1)
        else:
            self.statusbar.showMessage(u"工程%s已加载成功" % self.proj_name)
            # set window title and line edit widgets
            self.setWindowTitle(u'工程 - %s' % self.proj_name)
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
        proj_fname = self.le_proj_file.text()
        if proj_fname == '':
            msg = u'项目文件名不能为空, 请输入一个项目文件路径或者新建一个项目文件'
            self._show_tips(msg, tip_type=1)
            return
        if self.proj_name == '':
            msg = u'项目名称为空，请新建一个项目'
            self._show_tips(msg, tip_type=1)
            return
        msg = u'确定保存项目文件吗?'
        reply = self.show_yesno_msgbox(msg)
        if reply == 0:
            return
        res = self.write_proj_file(proj_fname)
        if res == True:
            msg = u'项目文件%s保存成功' % proj_fname
            self._show_tips(msg)
        else:
            msg = u'项目文件%s保存失败' % proj_fname
            self._show_tips(msg, tip_type=1)
    
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

    @pyqtSlot(str)
    def change_proj_name(self, name):
        self.proj_name = name
        print 'change_proj_name is called'

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
        with open(fname, 'r') as fh:
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

    def write_proj_file(self, fname):
        """
        Read the project file
        """
        lines = []
        lines.append("[ProjectName]=%s\n" % self.le_proj_file.text())
        lines.append("[FluentJournal]=%s\n" % self.le_fluent_jou_file.text())
        lines.append("[FluentCase]=%s\n" % self.le_fluent_cas_file.text())
        lines.append("[FluentUdf]=%s\n" % self.le_fluent_udf_file.text())
        lines.append("[FluentLoadData]=%s\n" % self.le_fluent_load_file.text())
        lines.append("[FluentExePath]=%s\n" % self.le_fluent_path.text())
        with open(fname, 'w') as fh:
            fh.write(''.join(lines))
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
        params['case_file'] = str(self.le_fluent_cas_file.text())
        params['udf_file'] = str(self.le_fluent_udf_file.text())
        # simualtion paramters
        params['backfill_heat_coeff'] = str(self.le_backfill_heat_coeff.text())
        params['backfill_density'] = str(self.le_backfill_density.text())
        params['backfill_spec_heat'] = str(self.le_backfill_spec_heat.text())
        params['pipe_heat_coeff'] = str(self.le_pipe_heat_coeff.text())
        params['pipe_density'] = str(self.le_pipe_density.text())
        params['pipe_spec_heat'] = str(self.le_pipe_spec_heat.text())
        params['soil_heat_coeff'] = str(self.le_soil_heat_coeff.text())
        params['soil_density'] = str(self.le_soil_density.text())
        params['soil_spec_heat'] = str(self.le_soil_spec_heat.text())
        params['ground_temp'] = str(self.le_init_ground_temp.text())
        params['loop_velocity'] = str(self.le_loop_velocity.text())
        params['loop_diameter'] = str(self.le_loop_hydr_diameter.text())
        conv_float = float(self.le_loop_intensity.text()) / 100.0
        params['loop_intensity'] = '%s' % conv_float
        # iterate time
        params['time_step'] = str(self.le_fluent_time_step.text())
        params['time_year'] = str(self.le_fluent_time_year.text())
        params['time_month'] = str(self.le_fluent_time_month.text())
        params['time_day'] = str(self.le_fluent_time_day.text())
        params['time_hour'] = str(self.le_fluent_time_hour.text())
        return params

    def fresh_udf_param_widgets(self, params):
        """
        Set all line edit widgets of udf parameters.
        """
        self.le_formula_copc_f.setText(params['copc_f'])
        self.le_formula_copc_m.setText(params['copc_m'])
        self.le_formula_copc_n.setText(params['copc_n'])
        self.le_formula_copc_a.setText(params['copc_a'])
        self.le_formula_copc_b.setText(params['copc_b'])
        self.le_formula_copc_c.setText(params['copc_c'])
        self.le_formula_copc_d.setText(params['copc_d'])
        self.le_formula_copc_e.setText(params['copc_e'])
        self.le_formula_coph_f.setText(params['coph_f'])
        self.le_formula_coph_m.setText(params['coph_m'])
        self.le_formula_coph_n.setText(params['coph_n'])
        self.le_formula_coph_a.setText(params['coph_a'])
        self.le_formula_coph_b.setText(params['coph_b'])
        self.le_formula_coph_c.setText(params['coph_c'])
        self.le_formula_coph_d.setText(params['coph_d'])
        self.le_formula_coph_e.setText(params['coph_e'])

    def get_udf_param_from_widgets(self):
        """
        Get udf paramters from line edits.
        """
        params = {}
        params['copc_f'] = str(self.le_formula_copc_f.text())
        params['copc_m'] = str(self.le_formula_copc_m.text())
        params['copc_n'] = str(self.le_formula_copc_n.text())
        params['copc_a'] = str(self.le_formula_copc_a.text())
        params['copc_b'] = str(self.le_formula_copc_b.text())
        params['copc_c'] = str(self.le_formula_copc_c.text())
        params['copc_d'] = str(self.le_formula_copc_d.text())
        params['copc_e'] = str(self.le_formula_copc_e.text())
        params['coph_f'] = str(self.le_formula_coph_f.text())
        params['coph_m'] = str(self.le_formula_coph_m.text())
        params['coph_n'] = str(self.le_formula_coph_n.text())
        params['coph_a'] = str(self.le_formula_coph_a.text())
        params['coph_b'] = str(self.le_formula_coph_b.text())
        params['coph_c'] = str(self.le_formula_coph_c.text())
        params['coph_d'] = str(self.le_formula_coph_d.text())
        params['coph_e'] = str(self.le_formula_coph_e.text())
        load_fname = str(self.le_fluent_load_file.text())
        load_fname = re.sub(r'/', r'\\\\\\\\', load_fname)
        print load_fname
        params['load_file'] = load_fname
        return params


if __name__ == "__main__":
    import sys
    app= QtGui.QApplication(sys.argv)
    mw = FluentSim()
    mw.show()
    sys.exit(app.exec_())
