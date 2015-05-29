from __future__ import unicode_literals

import unittest

from subprocess import Popen, PIPE

from openscad_dxf.inkutils import find_inkscape_path
from openscad_dxf.openscad_dxf import OpenSCADDXFEffect


class TestInkscapeOpenSCADDXFSave(unittest.TestCase):
    def setUp(self):
        """ Get the inkscape version so we can know which dxfs to compare """
        inkscape = find_inkscape_path()
        out, _ = Popen([inkscape, '--version'], stdout=PIPE).communicate()
        self.inkscape_version = '.'.join(out.split(' ')[1].split('.')[:2])

    def test_files(self):
        """ Test saving all the test SVG files as DXF """
        for name in ['circle', 'combo']:
            effect = OpenSCADDXFEffect()
            effect.affect(['tests/files/%s.svg' % name])
            dxf_path = 'tests/files/%s%s.dxf' % (name, self.inkscape_version)
            with open(dxf_path, 'r') as dxf_file:
                dxf_read = dxf_file.read()
                self.assertEqual(effect.dxf, dxf_read.rstrip())
