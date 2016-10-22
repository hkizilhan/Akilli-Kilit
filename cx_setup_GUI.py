from cx_Freeze import setup, Executable

import sys

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [],
                    excludes = [],
                    optimize = 0,
                    include_files = [],
                    include_msvcr = True,
                    )

base = 'Win32GUI'

executables = [
    Executable('GUI.py', base=base)
]

setup(name='Locker Key Generator',
      version = '0.08',
      description = 'Locker Key Generator',
      options = dict(build_exe = buildOptions),
      executables = executables)
