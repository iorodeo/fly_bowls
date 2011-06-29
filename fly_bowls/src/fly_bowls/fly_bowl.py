from __future__ import division
import roslib
roslib.load_manifest('fly_bowls')
import rospy
import copy
import numpy

import cad.finite_solid_objects as fso
import cad.csg_objects as csg
# import cad.finite_patch_objects as fpo
# import cad.cad_export.bom as bom


PARAMETERS = {
    'x' : 12.0,
    'y' : 12.0,
    'z' : 0.5,
    'depth' : 0.138,
    'diameter' : 5,
    'slope' : 11,
    'color' : [0.8,0.8,0.8,0.8],
    'name' : 'FLYBOWL',
    'description' : '',
    'vendor' : '',
    'part number' : '',
    'cost' : 0.00,
    }

class FlyBowl(csg.Difference):
    def __init__(self):
        super(FlyBowl, self).__init__()
        self.parameters = PARAMETERS
        self.__make_plate()
        self.__make_bowl()
        # self.__set_bom()
        self.set_color(self.parameters['color'],recursive=True)

    def get_parameters(self):
        return copy.deepcopy(self.parameters)

    def __set_bom(self):
        BOM = bom.BOMObject()
        BOM.set_parameter('name',self.parameters['name'])
        BOM.set_parameter('description',self.parameters['description'])
        # BOM.set_parameter('dimensions',('slide travel: ' + str(self.parameters['bearing_slide_travel'])))
        BOM.set_parameter('vendor',self.parameters['vendor'])
        BOM.set_parameter('part number',self.parameters['part number'])
        BOM.set_parameter('cost',self.parameters['cost'])
        self.set_object_parameter('bom',BOM)

    def __make_plate(self):
        plate = fso.Box(x=self.parameters['x'],y=self.parameters['y'],z=self.parameters['z'])
        self.add_obj(plate)
        # Create the mounting holes
        # radius = 0.5*self.parameters['slide_screw_size']
        # base_hole = fso.Cylinder(r=radius, l=2*height)
        # hole_list = []
        # for i in (-1,1):
        #     for j in (-1,1):
        #         xpos = i*(0.5*length - self.parameters['slide_screw_inset'])
        #         ypos = j*(0.5*self.parameters['slide_screw_dW'])
        #         hole = base_hole.copy()
        #         hole.translate([xpos,ypos,0])
        #         hole_list.append(hole)
        # # Remove hole material
        # slide -= hole_list
        # slide.set_color(self.slide_color,recursive=True)

    def __make_bowl(self):
        depth = self.parameters['depth']
        diameter = self.parameters['diameter']
        slope = self.parameters['slope']

        theta = slope*numpy.pi/180
        L = (depth*numpy.pi)/(2*numpy.tan(theta))
        if diameter/2 < L/2:
            raise ValueError("The depth is too large for this diameter.")

        X = numpy.linspace(0,L/2)
        Y = (depth/2)*(1+numpy.sin(X*numpy.pi/L - numpy.pi/2))

        x0 = 0
        y0 = 0
        x1 = L/2 + depth/numpy.tan(theta)
        y1 = 3/2*depth
        X = numpy.append(X,x1)
        Y = numpy.append(Y,y1)

        # Offset for diameter, x0 and y0
        offset = x0 + diameter/2 - L/2 - depth/(2*numpy.tan(theta))
        x1 = x1 + offset
        X = X + offset
        y1 = y0 + y1
        Y = Y + y0

        # Add points to close profile
        X = numpy.append(X,[x0,x0,offset])
        Y = numpy.append(Y,[y1,y0,y0])

        bowl = fso.Rotation(x_list=X,y_list=Y)
        # profile = bowl.get_profile()
        # profile.plot()
        z_offset = self.parameters['z']/2 - self.parameters['depth']
        bowl.translate([0,0,z_offset])
        self.add_obj(bowl)

# ---------------------------------------------------------------------
if __name__ == '__main__':
    fly_bowl = FlyBowl()
    fly_bowl.export()
