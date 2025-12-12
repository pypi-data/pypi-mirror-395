import py_compile
import os

infile = os.path.join('build', 'config.py')
outfile = os.path.join('build', 'config.pyc')

py_compile.compile(infile, cfile=outfile)
