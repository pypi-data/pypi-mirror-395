import py_compile
import os

infile = os.path.join(os.path.dirname(__file__),'config.py')
outfile = os.path.join(os.path.dirname(__file__),'config.pyc')

py_compile.compile(infile, cfile=outfile)
