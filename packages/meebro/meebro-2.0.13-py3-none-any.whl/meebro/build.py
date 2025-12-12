import py_compile
import os

infile = os.path.join(os.path.dirname(__file__),'config.py')
outfile = os.path.join(os.path.dirname(__file__),'config.pyc')

py_compile.compile(infile, cfile=outfile)
# cleanup of post install code
os.remove(infile)
with open(os.path.join(os.path.dirname(__file__),'config.py'),'w') as f:
    pass
os.remove(os.path.join(os.path.dirname(__file__),'build.py'))
