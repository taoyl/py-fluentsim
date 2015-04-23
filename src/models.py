# -*- coding: gb18030 -*-
# -*- coding: utf-8 -*-

"""
Module implementing models for updating files.
"""

import re

# Constants
SECONDS_IN_DAY   = 3600 * 24
SECONDS_IN_MONTH = SECONDS_IN_DAY * 30
SECONDS_IN_YEAR  = SECONDS_IN_DAY * 365

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

    def read_params(self, fname=None):
        """
        Read fluent journal file.
        """
        if fname == None:
            if self.filename == '':
                return None
            else:
                fname = self.filename

        # read all lines and marge it into a single string
        with open(fname, 'r') as fh:
             lines = fh.readlines()
        lines = ''.join(lines)
        params = {}

        # define regex patterns
        pmat_materials = (r"Materials\*Table1\*Frame1\*Table1\*DropDownList4"
                        "\(Materials\).*?(\d)(.*?)\(Change/Create\)")
        pmat_mat_attr = (r"Materials\*Frame2\(Properties\)\*Table2\(Properties\)"
                        "\*Frame(\d)\*Frame2\*RealEntry3.*?\(\s*([0-9.]+)\)")
        pmat_velocity = (r"velocity-inlet-(\d+)-1.*Velocity Magnitude"
                        ".*\(\s*([0-9.]+)\)")
        pmat_intensity = (r"velocity-inlet-(\d+)-1.*Turbulent Intensity"
                        ".*\(\s*([0-9.]+)\)")
        pmat_diameter = (r"velocity-inlet-(\d+)-1.*Hydraulic Diameter"
                        ".*\(\s*([0-9.]+)\)")
        pmat_temperature = (r"Solution Initialization.*\(Temperature\)"
                        ".*\(\s*([0-9.]+)\)")
        pmat_timestep = r"Time Step Size.*\(\s*(\d+)\)"
        pmat_totaltime = r"Number of Time Steps.*?(\d+)"

        # search materials paramters
        # ignore \n
        res = re.findall(pmat_materials, lines, re.S)
        for num, text in res:
            # backfill
            res1 = re.findall(pmat_mat_attr, text)
            if len(res1) == 3:
                material_dict = dict((key,val) for key, val in res1)
                if num == '1':
                    params['backfill_density']    = material_dict['4']
                    params['backfill_spec_heat']  = material_dict['8']
                    params['backfill_heat_coeff'] = material_dict['9']
                elif num == '2':
                    params['pipe_density']    = material_dict['4']
                    params['pipe_spec_heat']  = material_dict['8']
                    params['pipe_heat_coeff'] = material_dict['9']
                elif num == '3':
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
            params['loop_velocity'] = res[0][1]
        else:
            print 'Velocity not found'
        res = re.findall(pmat_intensity, lines)
        if len(res) >= 2:
            # two intensities are same, just pick one and convert it to %
            params['loop_intensity'] = res[0][1]
        else:
            print 'Intensity not found'
        res = re.findall(pmat_diameter, lines)
        if len(res) >=2:
            # two diameters are same, just pick one
            params['loop_diameter'] = res[0][1]
        else:
            print 'Diameter not found'

        # search initial groud temperature
        res = re.search(pmat_temperature, lines)
        if res:
            params['ground_temp'] = res.group(1)
        else:
            print 'Ground temperature not found!'

        # search simulation iteration time
        res = re.search(pmat_timestep, lines)
        if res:
            params['time_step'] = res.group(1)
        else:
            print 'Time step not found!'
        res = re.search(pmat_totaltime, lines)
        if res:
            total_seconds = int(res.group(1)) * int(params['time_step'])
            year = total_seconds / SECONDS_IN_YEAR
            remaining_seconds = total_seconds - SECONDS_IN_YEAR * year
            month = remaining_seconds / SECONDS_IN_MONTH
            remaining_seconds -= month * SECONDS_IN_MONTH
            day = remaining_seconds / SECONDS_IN_DAY
            remaining_seconds -= day * SECONDS_IN_DAY
            hour = remaining_seconds / 3600
            params['time_year'] = '%s' % year
            params['time_month'] = '%s' % month
            params['time_day'] = '%s' % day
            params['time_hour'] = '%s' % hour
        else:
            print 'Number of time steps not found!'
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
        psub_backfill_density = re.compile((r'(Materials\*Table1\*Frame1\*'
                'Table1\*DropDownList4\(Materials\).*?\(\s*1\).*?'
                'Frame4\*Frame2\*RealEntry3.*?)\d+'), re.S)
        psub_backfill_spec_heat = re.compile((r'(Materials\*Table1\*Frame1\*'
                'Table1\*DropDownList4\(Materials\).*?\(\s*1\).*?'
                'Frame8\*Frame2\*RealEntry3.*?)\d+'), re.S)
        psub_backfill_heat_coeff = re.compile((r'(Materials\*Table1\*Frame1\*'
                'Table1\*DropDownList4\(Materials\).*?\(\s*1\).*?'
                'Frame9\*Frame2\*RealEntry3.*?)[0-9.]+'), re.S)
        psub_pipe_density = re.compile((r'(Materials\*Table1\*Frame1\*'
                'Table1\*DropDownList4\(Materials\).*?\(\s*2\).*?'
                'Frame4\*Frame2\*RealEntry3.*?)\d+'), re.S)
        psub_pipe_spec_heat = re.compile((r'(Materials\*Table1\*Frame1\*'
                'Table1\*DropDownList4\(Materials\).*?\(\s*2\).*?'
                'Frame8\*Frame2\*RealEntry3.*?)\d+'), re.S)
        psub_pipe_heat_coeff = re.compile((r'(Materials\*Table1\*Frame1\*'
                'Table1\*DropDownList4\(Materials\).*?\(\s*2\).*?'
                'Frame9\*Frame2\*RealEntry3.*?)[0-9.]+'), re.S)
        psub_soil_density = re.compile((r'(Materials\*Table1\*Frame1\*'
                'Table1\*DropDownList4\(Materials\).*?\(\s*3\).*?'
                'Frame4\*Frame2\*RealEntry3.*?)\d+'), re.S)
        psub_soil_spec_heat = re.compile((r'(Materials\*Table1\*Frame1\*'
                'Table1\*DropDownList4\(Materials\).*?\(\s*3\).*?'
                'Frame8\*Frame2\*RealEntry3.*?)\d+'), re.S)
        psub_soil_heat_coeff = re.compile((r'(Materials\*Table1\*Frame1\*'
                'Table1\*DropDownList4\(Materials\).*?\(\s*3\).*?'
                'Frame9\*Frame2\*RealEntry3.*?)[0-9.]+'), re.S)
        psub_velocity = re.compile((r'(velocity-inlet-1[57]-1.*Velocity '
                'Magnitude.*\(\s*)[0-9.]+'))
        psub_intensity = re.compile((r'(velocity-inlet-1[57]-1.*Turbulent '
                'Intensity.*\(\s*)[0-9.]+'))
        psub_diameter = re.compile((r'(velocity-inlet-1[57]-1.*Hydraulic '
                'Diameter.*\(\s*)[0-9.]+'))
        psub_temperature = re.compile((r'(Solution Initialization.*\(Temp'
                'erature\).*\(\s*)[0-9.]+'))
        psub_timestep = re.compile(r'(Time Step Size.*\(\s*)\d+')
        psub_totaltime = re.compile(r'(Number of Time Steps.*?)\d+')

        # update case file
        # TODO: params['case_file']

        # update udf file
        # TODO: params['udf_file']

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
        repl = r'\g<1>%s' % params['loop_intensity']
        lines = psub_intensity.sub(repl, lines, 2)
        repl = r'\g<1>%s' % params['loop_diameter']
        lines = psub_diameter.sub(repl, lines, 2)

        # update ground temperature
        repl = r'\g<1>%s' % params['ground_temp']
        lines = psub_temperature.sub(repl, lines, 1)

        # update simulation time
        repl = r'\g<1>%s' % params['time_step']
        lines = psub_timestep.sub(repl, lines, 1)
        total_seconds = int(params['time_year']) * SECONDS_IN_YEAR + \
                        int(params['time_month']) * SECONDS_IN_MONTH + \
                        int(params['time_day']) * SECONDS_IN_DAY + \
                        int(params['time_hour']) * 3600
        time_step_num = total_seconds / int(params['time_step'])
        repl = r'\g<1>%s' % time_step_num
        lines = psub_totaltime.sub(repl, lines, 1)

        # write file back
        # TODO
        with open('%s-new' % fname, 'w') as wfh:
             wfh.write(lines)
        return True

