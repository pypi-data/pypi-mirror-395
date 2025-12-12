#!/usr/bin/env python3

import sysconfig
import sys
import shutil
import os

output_dir = sys.argv[1]
syspath = sysconfig.get_paths()

lib_filename = 'python{}{}.lib'.format(
    sys.version_info.major, sys.version_info.minor)

os.makedirs(output_dir, exist_ok=True)
shutil.copytree(syspath['include'], output_dir, dirs_exist_ok=True)

found_lib = False
lib_paths = []
for k, v in sysconfig.get_config_vars().items():
    if not isinstance(v, str):
        continue
    vf = os.path.join(v, lib_filename)
    if os.path.exists(vf):
        try:
            shutil.copyfile(vf, os.path.join(output_dir, 'python.lib'))
            found_lib = True
            break
        except:
            lib_paths += vf
    else:
        lib_paths += vf

    vfl = os.path.join(v, 'libs', lib_filename)
    if os.path.exists(vfl):
        try:
            shutil.copyfile(vfl, os.path.join(output_dir, 'python.lib'))
            found_lib = True
            break
        except:
            lib_paths += vfl
    else:
        lib_paths += vfl

if sys.platform == 'windows' and not found_lib:
    print("Warning: Did not find", lib_filename, "in:", file=sys.stderr)
    print(lib_paths, file=sys.stderr)

python_h = os.path.join(output_dir, 'Python.h')
if not os.path.isfile(python_h):
    raise Exception("Python.h missing! syspath include: {}\n output: {}".format(syspath['include'], output_dir))

with open(os.path.join(output_dir, 'Zig_Python_With_Hexver.h'), 'w') as fd:
    fd.write('''
#ifndef PY_SSIZE_T_CLEAN
#define PY_SSIZE_T_CLEAN
#endif

#ifndef PYHEXVER
#define PYHEXVER {}
#endif

#include "Python.h"
'''.format(sys.hexversion))
    print('OK:', os.path.join(output_dir, 'Zig_Python_With_Hexver.h'))
