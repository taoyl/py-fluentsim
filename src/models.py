# -*- coding: gb18030 -*-
# -*- coding: utf-8 -*-

"""
Module implementing models for updating files.

Author: taoyl <nerotao@foxmail.com>
Date  : Apr 21, 2015
"""

import re
import os


class JouFileModel(object):
    """
    Model for fluent journal file.
    """
    def __init__(self, parent=None):
        """
        Constructor
        """
        super(JouFileModel, self).__init__()

        # jou file name
        self.filename = ''

    def set_filename(self, path):
        self.filename = path

    def get_filename(self, path):
        return self.filename

    def _read_file(self, fname=None):
        """Read all file lines"""
        if fname == None:
            if self.filename == '':
                return False
            else:
                fname = self.filename
        # read all lines and merge it into a single string
        with open(fname, 'r') as rfh:
            lines = rfh.readlines()
        return ''.join(lines)

    def _write_file(self, fname, lines):
        """Write all lines into a file"""
        backup_fname = '%s.old' % fname
        if os.path.exists(backup_fname):
            os.remove(backup_fname)
        os.rename(fname, backup_fname)
        with open(fname, 'w') as wfh:
             wfh.write(lines)
        # TODO
        os.remove(backup_fname)
        return True

    def read_params(self, fname=None):
        """
        Read fluent journal file.
        """
        # read all lines
        lines = self._read_file(fname)

        # define regex patterns
        pmat_axis_z = (r"Scale Grid.*Scale Factors.*\(Z\).*\(\s*([0-9.]+)\)")
        pmat_materials = (r"Materials\*Table1\*Frame1\*Table1\*DropDownList4"
                        "\(Materials\).*?(\d)(.*?)\(Change/Create\)")
        pmat_mat_attr = (r"Materials\*Frame2\(Properties\)\*Table2\(Properties\)"
                        "\*Frame(\d)\*Frame2\*RealEntry3.*?\(\s*([0-9.]+)\)")
        pmat_velocity = (r"Velocity Magnitude.*\(\s*([0-9.]+)\)")
        pmat_temperature = (r"Solution Initialization.*\(Temperature\)"
                        ".*\(\s*([0-9.]+)\)")

        params = {}
        # search axis z
        res = re.search(pmat_axis_z, lines)
        if res:
            params['pipe_depth'] = '%s' % (float(res.group(1)) * 100)
        else:
            print 'Axis Z not found'
        # search materials paramters
        # ignore \n
        res = re.findall(pmat_materials, lines, re.S)
        for num, text in res:
            # backfill
            res1 = re.findall(pmat_mat_attr, text)
            if len(res1) == 3:
                material_dict = dict((key,val) for key, val in res1)
                if num == '0':
                    params['backfill_density']    = material_dict['4']
                    params['backfill_spec_heat']  = material_dict['8']
                    params['backfill_heat_coeff'] = material_dict['9']
                elif num == '1':
                    params['pipe_density']    = material_dict['4']
                    params['pipe_spec_heat']  = material_dict['8']
                    params['pipe_heat_coeff'] = material_dict['9']
                elif num == '2':
                    params['soil_density']    = material_dict['4']
                    params['soil_spec_heat']  = material_dict['8']
                    params['soil_heat_coeff'] = material_dict['9']
                else:
                    print 'Invalid material number'
            else:
                print 'Shall have three materials'

        # search boundary conditions of inlet
        res = re.findall(pmat_velocity, lines)
        if len(res) >= 2:
            # two velocities are same, just pick one
            params['loop_velocity'] = res[0]
        else:
            print 'Velocity not found'

        # search initial groud temperature
        res = re.search(pmat_temperature, lines)
        if res:
            params['ground_temp'] = res.group(1)
        else:
            print 'Ground temperature not found!'
        return params

    def write_params(self, params, fname=None):
        """
        Update fluent jou file using the input paramters.
        If file name is not specified, use self.filename.
        """
        # cannot call this function before initiating file name
        if fname == None:
            if self.filename == '':
                return False
            else:
                fname = self.filename
        # read all lines and marge it into a single string
        with open(fname, 'r') as rfh:
            lines = rfh.readlines()
        lines = ''.join(lines)

        # define regex patterns
        psub_input_case = re.compile((r'(Select File\*FilterText"\s*").*?'
                '(".*?Select File\*Text"\s*").*?\.cas'), re.S)
        psub_output_case = re.compile((r'(MenuBar\*WriteSubMenu\*Case.*?'
                '"Select File\*Text"\s*").*?\.cas'), re.S)
        psub_axis_z = re.compile((r'(Scale Grid.*Scale Factors.*\(Z\)'
                '.*\(\s*)[0-9.]+'))
        psub_backfill_density = re.compile((r'(Materials\*Table1\*Frame1\*'
                'Table1\*DropDownList4\(Materials\).*?\(\s*0\).*?'
                'Frame4\*Frame2\*RealEntry3.*?)\d+'), re.S)
        psub_backfill_spec_heat = re.compile((r'(Materials\*Table1\*Frame1\*'
                'Table1\*DropDownList4\(Materials\).*?\(\s*0\).*?'
                'Frame8\*Frame2\*RealEntry3.*?)\d+'), re.S)
        psub_backfill_heat_coeff = re.compile((r'(Materials\*Table1\*Frame1\*'
                'Table1\*DropDownList4\(Materials\).*?\(\s*0\).*?'
                'Frame9\*Frame2\*RealEntry3.*?)[0-9.]+'), re.S)
        psub_pipe_density = re.compile((r'(Materials\*Table1\*Frame1\*'
                'Table1\*DropDownList4\(Materials\).*?\(\s*1\).*?'
                'Frame4\*Frame2\*RealEntry3.*?)\d+'), re.S)
        psub_pipe_spec_heat = re.compile((r'(Materials\*Table1\*Frame1\*'
                'Table1\*DropDownList4\(Materials\).*?\(\s*1\).*?'
                'Frame8\*Frame2\*RealEntry3.*?)\d+'), re.S)
        psub_pipe_heat_coeff = re.compile((r'(Materials\*Table1\*Frame1\*'
                'Table1\*DropDownList4\(Materials\).*?\(\s*1\).*?'
                'Frame9\*Frame2\*RealEntry3.*?)[0-9.]+'), re.S)
        psub_soil_density = re.compile((r'(Materials\*Table1\*Frame1\*'
                'Table1\*DropDownList4\(Materials\).*?\(\s*2\).*?'
                'Frame4\*Frame2\*RealEntry3.*?)\d+'), re.S)
        psub_soil_spec_heat = re.compile((r'(Materials\*Table1\*Frame1\*'
                'Table1\*DropDownList4\(Materials\).*?\(\s*2\).*?'
                'Frame8\*Frame2\*RealEntry3.*?)\d+'), re.S)
        psub_soil_heat_coeff = re.compile((r'(Materials\*Table1\*Frame1\*'
                'Table1\*DropDownList4\(Materials\).*?\(\s*2\).*?'
                'Frame9\*Frame2\*RealEntry3.*?)[0-9.]+'), re.S)
        psub_velocity = re.compile((r'(Velocity\s+Magnitude.*\(\s*)[0-9.]+'))
        psub_temperature = re.compile((r'(Solution Initialization.*Temp'
                'erature.*\(\s*)[0-9.]+'))

        # update case file
        case_fpath = params['input_case_file'].split(r'/')
        case_fname = case_fpath[-1]
        # approved that '/' is okay
        case_fpath = '/'.join(case_fpath[0:-1])
        repl = r'\g<1>%s\g<2>%s' % (case_fpath + '/*', case_fname)
        lines = psub_input_case.sub(repl, lines, 1)
        case_fpath = params['output_case_file'].split(r'/')
        repl = r'\g<1>%s' % case_fpath[-1]
        lines = psub_output_case.sub(repl, lines, 1)
        # update axis z
        axis_z = float(params['pipe_depth']) / 100.0
        repl = r'\g<1>%s' % axis_z
        lines = psub_axis_z.sub(repl, lines, 1)
        # update materials
        # backfill
        repl = r'\g<1>%s' % params['backfill_density']
        lines = psub_backfill_density.sub(repl, lines, 1)
        repl = r'\g<1>%s' % params['backfill_spec_heat']
        lines = psub_backfill_spec_heat.sub(repl, lines, 1)
        repl = r'\g<1>%s' % params['backfill_heat_coeff']
        lines = psub_backfill_heat_coeff.sub(repl, lines, 1)
        # pipe
        repl = r'\g<1>%s' % params['pipe_density']
        lines = psub_pipe_density.sub(repl, lines, 1)
        repl = r'\g<1>%s' % params['pipe_spec_heat']
        lines = psub_pipe_spec_heat.sub(repl, lines, 1)
        repl = r'\g<1>%s' % params['pipe_heat_coeff']
        lines = psub_pipe_heat_coeff.sub(repl, lines, 1)
        # soil
        repl = r'\g<1>%s' % params['soil_density']
        lines = psub_soil_density.sub(repl, lines, 1)
        repl = r'\g<1>%s' % params['soil_spec_heat']
        lines = psub_soil_spec_heat.sub(repl, lines, 1)
        repl = r'\g<1>%s' % params['soil_heat_coeff']
        lines = psub_soil_heat_coeff.sub(repl, lines, 1)

        # update boundary conditions
        # inlet-1 & inlet-2
        repl = r'\g<1>%s' % params['loop_velocity']
        lines = psub_velocity.sub(repl, lines, 2)

        # update ground temperature
        repl = r'\g<1>%s' % params['ground_temp']
        lines = psub_temperature.sub(repl, lines, 1)

        # write file back
        return self._write_file(fname, lines)

    def update_sim_time(self, params, fname=None):
        """
        Update the simulation time in fluent jou file. 
        If file name is not specified, use self.filename.
        """
        lines = self._read_file(fname)
        # define regex patterns
        psub_input_case = re.compile((r'(Select File\*FilterText"\s*").*?'
                '(".*?Select File\*Text"\s*").*?\.cas'), re.S)
        psub_output_case = re.compile((r'(MenuBar\*WriteSubMenu\*Case.*?'
                '"Select File\*Text"\s*").*?\.cas'), re.S)
        psub_udf_path = re.compile((r'(FunctionsSubMenu\*Interpreted.*?'
                'Select File\*FilterText"\s*").*?(".*?Select File\*Text"\s*")'
                '.*?\.c'), re.S)
        psub_udf_file = re.compile((r'(Interpreted UDFs\*TextEntry1\(Source '
                'File Name\)"\s*").*"'))
        psub_timestep = re.compile(r'(Time Step Size.*\(\s*)\d+')
        psub_totaltime = re.compile(r'(Number of Time Steps.*?)\d+')

        # update case file
        case_fpath = params['input_case_file'].split(r'/')
        case_fname = case_fpath[-1]
        # approved that '/' is okay
        case_fpath = '/'.join(case_fpath[0:-1])
        repl = r'\g<1>%s\g<2>%s' % (case_fpath + '/*', case_fname)
        lines = psub_input_case.sub(repl, lines, 1)
        case_fpath = params['output_case_file'].split(r'/')
        repl = r'\g<1>%s' % case_fpath[-1]
        lines = psub_output_case.sub(repl, lines, 1)

        # update udf file
        udf_fpath = params['udf_file'].split(r'/')
        udf_fname = udf_fpath[-1]
        udf_fpath = '/'.join(udf_fpath[0:-1])
        repl = r'\g<1>%s\g<2>%s' % (udf_fpath + '/*', udf_fname)
        lines = psub_udf_path.sub(repl, lines, 1)
        repl = r'\g<1>%s"' % params['udf_file']
        lines = psub_udf_file.sub(repl, lines, 1)

        # update simulation time
        repl = r'\g<1>%s' % params['time_step']
        lines = psub_timestep.sub(repl, lines, 1)
        step_num = int(params['time_hour']) * 3600 / int(params['time_step'])
        repl = r'\g<1>%s' % step_num
        lines = psub_totaltime.sub(repl, lines, 1)

        # write file back
        return self._write_file(fname, lines)


class UdfFileModel(object):
    """
    Model for udf file.
    """
    def __init__(self, parent=None):
        """
        Constructor
        """
        super(UdfFileModel, self).__init__()

        # file name
        self.filename = ''
        self.param_names = set([
                'copc_f', 'copc_m', 'copc_n', 'copc_a', 'copc_b', 'copc_c',
                'copc_d', 'copc_e', 'coph_f', 'coph_m', 'coph_n', 'coph_a',
                'coph_b', 'coph_c', 'coph_d', 'coph_e', 
                'copc_max_q', 'coph_max_q'
                ])

    def read_params(self, fname=None):
        """
        Read udf file and extract the params.
        """
        if fname == None:
            if self.filename == '':
                return None
            fname = self.filename
        # read all lines
        params = {}
        with open(fname, 'r') as rfh:
            lines = rfh.readlines()
        lines = ''.join(lines)

        for param in self.param_names:
            res = re.search(r'%s\s*=\s*([-.\d]+)' % param, lines)
            if res:
                params[param] = res.group(1)
        return params

    def write_params(self, params, fname=None):
        """
        Update udf file using the input params.
        """
        if fname == None:
            if self.filename == '':
                return False
            fname = self.filename
        # read all lines and update param value
        with open(fname, 'r') as rfh:
            lines = rfh.readlines()
        lines = ''.join(lines)
        # replace the load file name, remove the absolute path
        load_fname = params['load_file'].split(r'/')[-1]
        lines = re.sub(r'(\*fname\s*=\s*").*"', 
                        r'\g<1>%s"' % load_fname, lines)
        # calculate the max q
#        (copc_max_q, coph_max_q) = self.calc_max_min_q(fname=params['load_file'])
#        params['copc_max_q'] = copc_max_q
#        params['coph_max_q'] = coph_max_q
        for param in self.param_names:
            # any paramter is not found, stop update
            if not params.has_key(param):
                return False
            lines = re.sub(r'(%s\s*=\s*)[-.\d]+' % param, 
                    r'\g<1>%s' % params[param], lines)
        # write lines back
        return self._write_file(fname, lines)

    def _write_file(self, fname, lines):
        """Write all lines into a file"""
        backup_fname = '%s.old' % fname
        if os.path.exists(backup_fname):
            os.remove(backup_fname)
        os.rename(fname, backup_fname)
        with open(fname, 'w') as wfh:
             wfh.write(lines)
        # TODO
        os.remove(backup_fname)
        return True

    def calc_max_min_q(self, fname):
        """
        Calculate the max and min Q value of load.
        """
        max_q = 0.0
        min_q = 0.0
        with open(fname, 'r') as rfh:
            for line in rfh:
                val = float(line)
                print val
                if val > max_q:
                    max_q = val
                if val < min_q:
                    min_q = val
        print 'max=', max_q, 'min=', min_q
        return (max_q, min_q)


    
