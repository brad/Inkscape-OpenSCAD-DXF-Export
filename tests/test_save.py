from __future__ import unicode_literals

import os
import sys
import unittest

sys.path.append('..')  # Allow importing from parent dir
from inkutils import find_inkscape_path
# Add inkscape extensions to path
sys.path.append(os.path.join(
    find_inkscape_path(sys.path, path_type='share'), 'extensions'
))
from openscad_dxf import OpenSCADDXFEffect


class TestInkscapeOpenSCADDXFSave(unittest.TestCase):
    def test_files(self):
        """ Test saving all the test SVG files as DXF """
        args = ['tests/files/circle.svg']
        openscad_dxf = OpenSCADDXFEffect()
        openscad_dxf.affect(args)
        with open('tests/files/circle.dxf', 'r') as dxf_file:
            dxf_read = dxf_file.read()
            self.assertEqual(openscad_dxf.dxf, dxf_read.rstrip())