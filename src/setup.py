# A setup script showing advanced features.
#

from distutils.core import setup
import py2exe
import sys
import glob
import os
import zlib
import shutil

distname = "../bin"

# If run without args, build executables, in quiet mode.
if len(sys.argv) == 1:
	sys.argv.append("py2exe")
	sys.argv.append("-q")

# remove the build folder
shutil.rmtree("build", ignore_errors=True)
# remove the dist folder
shutil.rmtree(distname, ignore_errors=True)

class Target(object):
	def __init__(self, **kw):
		self.__dict__.update(kw)
		# for the versioninfo resources


# define data files, excludes and dll excludes
data_files = []
includes   = ['sip']
excludes   = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 
			     'pywin.debugger', 'pywin.debugger.dbgcon', 
			     'pywin.dialogs', 'tcl', 'Tkconstants', 'Tkinter']

packages = []
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 
				    'tcl84.dll', 'tk84.dll']
icon_resources = [(1, "./images/fluentsim-32.ico")]
bitmap_resources = []
other_resources = []

baseFolder, progFolder = os.path.split(os.getcwd())

# copy the MSVC run time DLLs
py26MSdll = glob.glob( r"D:\Development\PyQt\Microsoft.VC90.CRT\*.*" )

data_files += [ ('Microsoft.VC90.CRT', py26MSdll),
				('lib\Microsoft.VC90.CRT', py26MSdll),
			  ]

# add ico
#icons = glob.glob( r"./*.ico" )
#data_files += [('icon', icons)]

# Ok, now we are going to build our target class.
# I chose this building strategy as it works perfectly for me :-D
GUI2Exe_Target_1 = Target( 
			# what to build
			script = "fluentsim.py",
			icon_resources = icon_resources,
			bitmap_resources = bitmap_resources,
			other_resources = other_resources,
			dest_base = "FluentSim",
			version = "1.1.0",
			description = "Fluent simulator",
			company_name = "China Building Design Consultants Company",
			copyright = "China Building Design Consultants Company, All Rights Reserved",
			name = "FluentSim, v1.1.0",
		)

# That's serious now: we have all (or almost all) the options py2exe
# supports. I put them all even if some of them are usually defaulted
# and not used. Some of them I didn't even know about.
setup(
	data_files = data_files,
	
	options = {"py2exe": {"compressed"  : 2,
						  "optimize"    : 2,
						  "includes"    : includes,
						  "excludes"    : excludes,
						  "packages"    : packages,
						  "dll_excludes": dll_excludes,
						  "bundle_files": 3,
						  "dist_dir"    : distname,
						  "xref"        : False,
						  "skip_archive": False,
						  "ascii"       : False,
						  "custom_boot_script": '',
						  }
			},
	
	zipfile = "lib\shared.zip",
	console = [],
	windows = [GUI2Exe_Target_1]
	)

# end
print "\n$$$ Generate exe file successfully\n\n"
