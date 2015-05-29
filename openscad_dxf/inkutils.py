import os
import sys


class InkscapeEnvironmentError(EnvironmentError):
    pass


def find_inkscape_path(path_type='bin'):
    """
    Find the path of the Inkscape executable on the system
    """
    # Linux or Mac OS X
    pathlist = sys.path
    for path in [
            "/usr/%s/inkscape" % path_type, "/usr/local/%s/inkscape" % path_type,
            "/Applications/Inkscape.app/Contents/Resources/%s/inkscape" % path_type]:
        if os.path.exists(path):
            return path
    # Windows
    for p in pathlist:
        p = p.lower().replace("\\", "/")
        if "/python/lib" in p:
            return os.path.join(p.split("/python/lib")[0], "inkscape")
    raise InkscapeEnvironmentError(
        "Can't find the path of the Inkscape executable.")
