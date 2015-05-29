.. image:: https://travis-ci.org/brad/Inkscape-OpenSCAD-DXF-Export.svg?branch=master
    :target: https://travis-ci.org/brad/Inkscape-OpenSCAD-DXF-Export
.. image:: https://coveralls.io/repos/brad/Inkscape-OpenSCAD-DXF-Export/badge.svg?branch=master
    :target: https://coveralls.io/r/brad/Inkscape-OpenSCAD-DXF-Export?branch=master
.. image:: https://www.versioneye.com/user/projects/5562cdd13664660019180100/badge.svg?style=flat
    :target: https://www.versioneye.com/user/projects/5562cdd13664660019180100

See http://www.thingiverse.com/thing:14221

Installation
============

Simply copy the appropriate files (``openscad_dxf.inx`` and the ``openscad_dxf`` folder)
to the installation directory. Install to your Inkscape global installation's ``extensions``
directory or to your local user's inkscape extensions directory. The per platform
installation directories can be found below. If you have ``pip`` and want to try an
even easier (but experimental) installation method you can try using
``pip install --target=<installation_dir> inkscape-openscad-dxf``. If you do use
this method, do not use a ``~`` to refer to your home directory. Some versions of
``pip`` will misinterpret it and create a directory called ``~`` in the current
directory.

Windows
-------
 * *Global* - ``C:\Program Files\Inkscape\share\extensions``
 * *Local* - ``C:\Documents and Settings\User\Application Data\Inkscape\extensions``

Linux
-----
  * *Global* - ``/usr/share/inkscape/extensions``
  * *Local* - ``$HOME/.config/inkscape/extensions``

OS X
-----
  * *Global* - ``/Applications/Inkscape.app/Contents/Resources/extensions``
  * *Local* - ``$HOME/.config/inkscape/extensions``
