from __future__ import division
import roslib
roslib.load_manifest('fly_bowls')
import rospy
import copy
import numpy

import cad.finite_solid_objects as fso
import cad.csg_objects as csg
import cad.pattern_objects as po
import cad_library.screw_holes as screw_holes
# import cad.cad_export.bom as bom


PARAMETERS = {
    'x' : 12.0,
    'y' : 12.0,
    'z' : 0.25,
    'bowl_cutout_diameter' : 6,
    'threaded_hole_size' : '10',
    'threaded_hole_type' : 'fine',
    'threaded_hole_percent' : '75%',
    'threaded_hole_x' : [[-2.75,2.75],[-5.5,5.5],[-5.5,5.5]],
    'threaded_hole_y' : [[-4.5,4.5],[-4.5,4.5],[-2.25,2.25]],
    'mounting_hole_size' : '1/2',
    'mounting_hole_x' : [-5.5,5.5],
    'mounting_hole_y' : [-5.5,5.5],
    'color' : [0.3,0.3,0.3,1.0],
    'name' : 'FLYBOWL_SUPPORT_PLATE',
    'description' : '',
    'vendor' : '',
    'part number' : '',
    'cost' : 0.00,
    }


class FlyBowlSupportPlate(csg.Difference):
    def __init__(self):
        super(FlyBowlSupportPlate, self).__init__()
        self.parameters = PARAMETERS
        self.__make_plate()
        self.__make_bowl_cutout()
        self.__make_threaded_holes()
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

    def __make_bowl_cutout(self):
        bowl_cutout_diameter = self.parameters['bowl_cutout_diameter']
        bowl_cutout_l = self.parameters['z']*2
        bowl_cutout = fso.Cylinder(l=bowl_cutout_l,r=bowl_cutout_diameter/2)
        self.add_obj(bowl_cutout)

    def __make_threaded_holes(self):
        threaded_hole_size = self.parameters['threaded_hole_size']
        threaded_hole_type = self.parameters['threaded_hole_type']
        threaded_hole_percent = self.parameters['threaded_hole_percent']
        threaded_hole_depth = self.parameters['z']*2
        threaded_hole = screw_holes.TapHole(size=threaded_hole_size,type=threaded_hole_type,percent=threaded_hole_percent,depth=threaded_hole_depth)
        z_offset = self.parameters['z']/2
        threaded_hole.translate([0,0,z_offset])


        threaded_hole_x = self.parameters['threaded_hole_x']
        threaded_hole_y = self.parameters['threaded_hole_y']
        threaded_holes = po.LinearArraySet(threaded_hole,x=threaded_hole_x,y=threaded_hole_y)
        self.add_obj(threaded_holes)

    def __make_mounting_holes(self):
        mounting_hole_size = self.parameters['mounting_hole_size']
        hole_depth = self.parameters['z']*2
        mounting_hole = screw_holes.ClearanceHole(size=mounting_hole_size,depth=hole_depth,fit='free')
        z_offset = self.parameters['z']/2
        mounting_hole.translate([0,0,z_offset])

        mounting_hole_x = self.parameters['mounting_hole_x']
        mounting_hole_y = self.parameters['mounting_hole_y']
        mounting_holes = po.LinearArray(mounting_hole,x=mounting_hole_x,y=mounting_hole_y)
        self.add_obj(mounting_holes)


# ---------------------------------------------------------------------
if __name__ == '__main__':
    fly_bowl_support_plate = FlyBowlSupportPlate()
    fly_bowl_support_plate.export()
