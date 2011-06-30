from __future__ import division
import roslib
roslib.load_manifest('fly_bowls')
import rospy
import copy
import numpy

import cad.finite_solid_objects as fso
import cad.csg_objects as csg
import cad_library.screw_holes as screw_holes
# import cad.finite_patch_objects as fpo
# import cad.cad_export.bom as bom


PARAMETERS = {
    'x' : 12.0,
    'y' : 12.0,
    'z' : 0.5,
    'depth' : 0.138,
    'diameter' : 5,
    'slope' : 11,
    'counterbore_size' : '10',
    'mounting_hole_size' : '1/2',
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
        self.__make_counterbores()
        self.__make_mounting_holes()
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

    def __make_counterbores(self):
        counterbore_size = self.parameters['counterbore_size']
        screw_hole_depth = self.parameters['z']*2
        counterbore = screw_holes.Counterbore(size=counterbore_size,depth=screw_hole_depth,fit='free')
        z_offset = self.parameters['z']/2
        counterbore.translate([0,0,z_offset])

        counterbore_set = []
        # Make counterbore set 1
        for x in [-2.75,2.75]:
            for y in [-4.5,4.5]:
                counterbore_copy = counterbore.copy()
                counterbore_copy.translate([x,y,0])
                counterbore_set.append(counterbore_copy)

        # Make counterbore set 2
        for x in [-5.5,5.5]:
            for y in [-4.5,4.5]:
                counterbore_copy = counterbore.copy()
                counterbore_copy.translate([x,y,0])
                counterbore_set.append(counterbore_copy)

        # Make counterbore set 3
        for x in [-5.5,5.5]:
            for y in [-2.25,2.25]:
                counterbore_copy = counterbore.copy()
                counterbore_copy.translate([x,y,0])
                counterbore_set.append(counterbore_copy)

        self.add_obj(counterbore_set)

    def __make_mounting_holes(self):
        mounting_hole_size = self.parameters['mounting_hole_size']
        hole_depth = self.parameters['z']*2
        mounting_hole = screw_holes.ClearanceHole(size=mounting_hole_size,depth=hole_depth,fit='free')
        z_offset = self.parameters['z']/2
        mounting_hole.translate([0,0,z_offset])

        mounting_hole_set = []
        for x in [-5.5,5.5]:
            for y in [-5.5,5.5]:
                mounting_hole_copy = mounting_hole.copy()
                mounting_hole_copy.translate([x,y,0])
                mounting_hole_set.append(mounting_hole_copy)

        self.add_obj(mounting_hole_set)


# ---------------------------------------------------------------------
if __name__ == '__main__':
    fly_bowl = FlyBowl()
    fly_bowl.export()
