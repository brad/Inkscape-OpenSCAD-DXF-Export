import os
import sys

from openscad_dxf.inkutils import find_inkscape_path


# Add inkscape extensions to path
sys.path.append(os.path.join(
    find_inkscape_path(path_type='share'), 'extensions'
))
