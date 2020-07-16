#!/usr/bin/env python
# vim: shiftwidth=4 tabstop=4 softtabstop wrapmargin=79 textwidth=72

import os
from distutils.core import setup
from os.path import exists, isdir, join
import shutil

import py2exe

from semvertest import appname as APPNAME, applongname as APPLONGNAME, appversion as VERSION, copyright as COPYRIGHT

dist_dir = 'dist.win32'

if dist_dir and len(dist_dir)>1 and isdir(dist_dir):
    shutil.rmtree(dist_dir)

# Windows paths
WIXPATH = r'C:\Program Files (x86)\WiX Toolset v3.11\bin'
SDKPATH = r'C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\x86'

APP = 'semvertest.py'
OPTIONS = {
    'py2exe': {
        'dist_dir': dist_dir,
        'optimize': 2,
     }
}
DATA_FILES = [
    ('', [
        'WinSparkle.dll',
        'WinSparkle.pdb', # For debugging - don't include in package
    ]),
]

setup(
    name = APPLONGNAME,
    version = VERSION,
#    app = [APP],
    console = [{
        'dest_base': APPNAME,
        'script': APP,
        'company_name': 'EDCD',
        'product_name': APPNAME,
        'version': VERSION,
        'copyright': COPYRIGHT,
    }],
    data_files = DATA_FILES,
    options = OPTIONS,
#    setup_requires = ['py2exe'],
)

PKG = None
os.system(r'"%s\candle.exe" -out %s\ %s.wxs' % (WIXPATH, dist_dir, APPNAME))
if not exists('%s/%s.wixobj' % (dist_dir, APPNAME)):
    raise AssertionError('No %s/%s.wixobj: candle.exe failed?' % (dist_dir, APPNAME))

PKG = '%s_win_%s.msi' % (APPNAME, VERSION)
import subprocess
os.system(r'"%s\light.exe" -sacl -spdb -sw1076 %s\%s.wixobj -out %s' % (WIXPATH, dist_dir, APPNAME, PKG))
if not exists(PKG):
    raise AssertionError('light.exe failed, no %s' % (PKG))


