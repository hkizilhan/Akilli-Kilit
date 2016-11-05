from cx_Freeze import setup, Executable

import sys

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [],
                    excludes = [],
                    optimize = 0,
                    include_files = [],
                    include_msvcr = True,
                    build_exe = "build_Locker"
                    )

base = 'Win32GUI'

executables = [
    Executable('Locker.py', base=base)
]

setup(name='Locker',
      version = '0.10',
      description = 'Locker',
      options = dict(build_exe = buildOptions),
      executables = executables)
