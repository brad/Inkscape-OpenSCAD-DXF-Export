#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
Copyright (C) 2005,2007 Aaron Spike, aaron@ekips.org
- template dxf_outlines.dxf added Feb 2008 by Alvin Penner, penner@vaxxine.com
- layers, transformation, flattening added April 2008 by Bob Cook, bob@bobcookdev.com
- bug fix for xpath() calls added February 2009 by Bob Cook, bob@bobcookdev.com
- colors, finer detail, layer name correction, September 2010 by Simon Arthur simon@bigbluesaw.com
- max value of 10 on path flattening, August 2011 by Bob Cook, bob@bobcookdev.com
- converted to OpenSCAD export supporting objects, October 2011 by Brad Pitcher, bradpitcher@gmail.com

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import inkex, object2path, pathmodifier, simplepath, simplestyle, simpletransform, cspsubdiv, cubicsuperpath, dxf_templates, dxf_color, re

class OpenSCADDXFEffect(object2path.ObjectToPath):
    def __init__(self):
        object2path.ObjectToPath.__init__(self)
        self.dxf = ''
        self.global_dims = {
            'minX':None,
            'minY':None,
            'maxX':None,
            'maxY':None
        }
        self.layer_dims = {}
        self.handle = 255
        self.flatness = 0.1
        self.dxf_color = dxf_color.DxfColor()
        
    def output(self):
        print self.dxf

    def dxf_add_codes(self, codes):
        lines = ''
        for code in codes:
            lines += code[0] + '\n' + code[1] + '\n'
        return lines
        
    def dxf_path_to_lines(self, layer, p, color=None):
        f = self.flatness
        is_flat = 0
        while is_flat < 1:
            try:
                cspsubdiv.cspsubdiv(p, f)
                is_flat = 1
            except IndexError:
                break
            except:
                f += 0.1
                if f>2:
                    #something has gone very wrong.
                    break
        
        lines = ''
        for sub in p:
            lines += self.dxf_add_codes([
	        ('0', 'LWPOLYLINE'),
	        ('100', 'AcDbPolyline'),
                ('8', layer),
	        ('90', '%i' % (len(sub))),
	        ('70', '0')
            ])
            for i in range(len(sub)):
                self.handle += 1
                x = sub[i][1][0]
                y = sub[i][1][1]
		# Compare global maxes and mins
                dims = self.global_dims
                if dims['minX'] is None or x < dims['minX']:
                    self.global_dims['minX'] = x
                elif dims['maxX'] is None or x > dims['maxX']:
                    self.global_dims['maxX'] = x
                if dims['minY'] is None or y < dims['minY']:
                    self.global_dims['minY'] = y
                elif dims['maxY'] is None or y > dims['maxY']:
                    self.global_dims['maxY'] = y
                # Compare layer maxes and mins
                dims = self.layer_dims[layer]
		if dims['minX'] is None or x < dims['minX']:
                    self.layer_dims[layer]['minX'] = x
		elif dims['maxX'] is None or x > dims['maxX']:
                    self.layer_dims[layer]['maxX'] = x
		if dims['minY'] is None or y < dims['minY']:
                    self.layer_dims[layer]['minY'] = y
		elif dims['maxY'] is None or y > dims['maxY']:
                    self.layer_dims[layer]['maxY'] = y
                lines += self.dxf_add_codes([
                    ('10', '%f' % x),
                    ('20', '%f' % y),
                    ('30', '0.0')
                ]);
        return lines

    def dxf_add_dimension(self, name, x = None, y = None, layer = None):
        codes = [('0', 'DIMENSION')]
	if layer is not None:
            codes.append(('8', layer))
        codes += [
            ('5', '83'),
            ('100', 'AcDbEntity'),
            ('62', '256'),
            ('370', '-1'),
            ('6', 'ByLayer'),
            ('1', name),
            ('3', 'Standard'),
            ('70', '0'),
            ('71', '5'),
            ('72', '1'),
            ('41', '1.0'),
            ('100', 'AcDbAlignedDimension'),
            ('13', '%f' % (x[0] if x is not None else 0.0)),
            ('23', '%f' % (y[0] if y is not None else 0.0)),
            ('33', '0.0'),
            ('14', '%f' % (x[1] if x is not None else 0.0)),
            ('24', '%f' % (y[1] if y is not None else 0.0)),
            ('34', '0.0'),
            ('50', '%f' % (90.0 if y is not None else 0.0)),
            ('100', 'AcDbRotatedDimension')
        ]
        return self.dxf_add_codes(codes)
        
    def effect(self):
        object2path.ObjectToPath.effect(self)
        self.dxf += self.dxf_add_codes([('999', 'Inkscape export via OpenSCAD DXF Export')])
        self.dxf += dxf_templates.r14_header
        
        scale = 25.4/90.0
        h = inkex.unittouu(self.document.getroot().xpath('@height',namespaces=inkex.NSS)[0])

        path = '//svg:path'
        pm = pathmodifier.PathModifier()
        layers = []
        dxf_body = ''
        for node in self.document.getroot().xpath(path,namespaces=inkex.NSS):
            pm.objectToPath(node, True)
            layer = node.getparent().get(inkex.addNS('label', 'inkscape'))
            if layer == None:
                layer = 'Layer 1'
            layer = layer.replace(' ', '_')

            if layer not in layers:
                layers.append(layer)
                self.layer_dims[layer] = {
                    'minX':None,
                    'minY':None,
                    'maxX':None,
                    'maxY':None
                }

            d = node.get('d')
            color = (0,0,0)
            style = node.get('style')
            if style:
                style = simplestyle.parseStyle(style)
                if style.has_key('stroke'):
                    if style['stroke'] and style['stroke'] != 'none':
                        color = simplestyle.parseColor(style['stroke'])

            p = cubicsuperpath.parsePath(d)
            
            t = node.get('transform')
            if t != None:
                m = simpletransform.parseTransform(t)
                simpletransform.applyTransformToPath(m,p)
            
            m = [[scale,0,0],[0,-scale,h*scale]]
            simpletransform.applyTransformToPath(m,p)

            dxf_body += self.dxf_path_to_lines(layer, p, color)

        self.dxf += self.dxf_add_codes([
            ('0', 'TABLE'),
            ('2', 'LAYER'),
            ('5', '2'),
            ('330', '0'),
            ('100', 'AcDbSymbolTable'),
            # group code 70 tells a reader how many table records to expect (e.g. pre-allocate memory for).
            # It must be greater or equal to the actual number of records
            ('70', str(len(layers)))
        ])

        # Add dimensions for total width and height
        dxf_dims = self.dxf_add_dimension('total_width', 
            [self.global_dims['minX'], self.global_dims['maxX']])
        dxf_dims += self.dxf_add_dimension('total_height', 
            None, [self.global_dims['minY'], self.global_dims['maxY']])
        for layer in layers:
            self.dxf += self.dxf_add_codes([
                ('0', 'LAYER'),
                ('5', '10'),
                ('330', '2'),
                ('100', 'AcDbSymbolTableRecord'),
                ('100', 'AcDbLayerTableRecord'),
                ('2', layer),
                ('70', '0'),
                ('62', '7'),
                ('6', 'CONTINUOUS')
            ])
            # Add dimensions for layer width and height
            dxf_dims += self.dxf_add_dimension(layer + '_width', 
                [self.layer_dims[layer]['minX'], self.layer_dims[layer]['maxX']], None, layer)
            dxf_dims += self.dxf_add_dimension(layer + '_height', 
                None, [self.layer_dims[layer]['minY'], self.layer_dims[layer]['maxY']], layer)

        self.dxf += self.dxf_add_codes([
            ('0', 'ENDTAB'),
            ('0', 'ENDSEC')
        ])

        self.dxf += dxf_templates.r14_style
        self.dxf += dxf_dims
        self.dxf += dxf_body

        self.dxf += dxf_templates.r14_footer

if __name__ == '__main__': OpenSCADDXFEffect().affect()
