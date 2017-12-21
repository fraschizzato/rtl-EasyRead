#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/fraschi/gr-urmetEasyRead/python
export PATH=/home/fraschi/gr-urmetEasyRead/build/python:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export PYTHONPATH=/home/fraschi/gr-urmetEasyRead/build/swig:$PYTHONPATH
/usr/bin/python2 /home/fraschi/gr-urmetEasyRead/python/qa_urmetEasyRead.py 
