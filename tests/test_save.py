from __future__ import unicode_literals

import os
import sys
import unittest

from subprocess import Popen, PIPE

sys.path.append('..')  # Allow importing from parent dir
from inkutils import find_inkscape_path
# Add inkscape extensions to path
sys.path.append(os.path.join(
    find_inkscape_path(sys.path, path_type='share'), 'extensions'
))
from openscad_dxf import OpenSCADDXFEffect


class TestInkscapeOpenSCADDXFSave(unittest.TestCase):
    def setUp(self):
        inkscape = find_inkscape_path(sys.path)
        out, _ = Popen([inkscape, '--version'], stdout=PIPE).communicate()
        self.inkscape_version = '.'.join(out.split(' ')[1].split('.')[:2])

    def test_files(self):
        """ Test saving all the test SVG files as DXF """
        for name in ['circle', 'combo']:
            openscad_dxf = OpenSCADDXFEffect()
            openscad_dxf.affect(['tests/files/%s.svg' % name])
            dxf_path = 'tests/files/%s%s.dxf' % (name, self.inkscape_version)
            with open(dxf_path, 'r') as dxf_file:
                dxf_read = dxf_file.read()
                self.assertEqual(openscad_dxf.dxf, dxf_read.rstrip())