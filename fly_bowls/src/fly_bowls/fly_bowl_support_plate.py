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

import fly_bowl


PARAMETERS = {
    'z' : 0.25,
    'threaded_hole_type' : 'fine',
    'threaded_hole_percent' : '75%',
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
        self.fly_bowl_parameters = fly_bowl.PARAMETERS
        self.__make_plate()
        self.__make_bowl_cutout()
        self.__make_threaded_holes()
        self.__make_mounting_holes()
        # self.__set_bom()
        self.set_color(self.parameters['color'],recursive=True)

        # convert to mm
        scale = self.fly_bowl_parameters['scale']
        self.set_scale(scale)

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
        plate = fso.Box(x=self.fly_bowl_parameters['x'],y=self.fly_bowl_parameters['y'],z=self.parameters['z'])
        self.add_obj(plate)

    def __make_bowl_cutout(self):
        bowl_cutout_diameter = self.fly_bowl_parameters['bowl_diameter'] + 1
        bowl_cutout_l = self.parameters['z']*2
        bowl_cutout = fso.Cylinder(l=bowl_cutout_l,r=bowl_cutout_diameter/2)
        self.add_obj(bowl_cutout)

    def __make_threaded_holes(self):
        threaded_hole_size = self.fly_bowl_parameters['counterbore_size']
        threaded_hole_type = self.parameters['threaded_hole_type']
        threaded_hole_percent = self.parameters['threaded_hole_percent']
        threaded_hole_depth = self.parameters['z']*2
        threaded_hole = screw_holes.TapHole(size=threaded_hole_size,type=threaded_hole_type,percent=threaded_hole_percent,depth=threaded_hole_depth)
        z_offset = self.parameters['z']/2
        threaded_hole.translate([0,0,z_offset])


        counterbore_x_distances = self.fly_bowl_parameters['counterbore_x_distances']
        counterbore_y_distances = self.fly_bowl_parameters['counterbore_y_distances']
        cxd = list(set([abs(number) for number in counterbore_x_distances]))
        cxd.sort()
        cyd = list(set([abs(number) for number in counterbore_y_distances]))
        cyd.sort()

        threaded_hole_x = [[-cxd[0],cxd[0]],[-cxd[1],cxd[1]],[-cxd[1],cxd[1]]]
        threaded_hole_y = [[-cyd[1],cyd[1]],[-cyd[1],cyd[1]],[-cyd[0],cyd[0]]]
        threaded_holes = po.LinearArraySet(threaded_hole,x=threaded_hole_x,y=threaded_hole_y)
        self.add_obj(threaded_holes)

    def __make_mounting_holes(self):
        mounting_hole_size = self.fly_bowl_parameters['mounting_hole_size']
        hole_depth = self.parameters['z']*2
        mounting_hole = screw_holes.ClearanceHole(size=mounting_hole_size,depth=hole_depth,fit='free')
        z_offset = self.parameters['z']/2
        mounting_hole.translate([0,0,z_offset])

        mounting_hole_x = self.fly_bowl_parameters['mounting_hole_x']
        mounting_hole_y = self.fly_bowl_parameters['mounting_hole_y']
        mounting_holes = po.LinearArray(mounting_hole,x=mounting_hole_x,y=mounting_hole_y)
        self.add_obj(mounting_holes)


# ---------------------------------------------------------------------
if __name__ == '__main__':
    fly_bowl_support_plate = FlyBowlSupportPlate()
    fly_bowl_support_plate.export()
