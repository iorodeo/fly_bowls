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
# import cad.finite_patch_objects as fpo
# import cad.cad_export.bom as bom


PARAMETERS = {
    'x' : 12.0,
    'y' : 12.0,
    'z' : 0.5,
    'bowl_depth' : 0.138,
    'bowl_diameter' : 5,
    'bowl_slope' : 11,
    'counterbore_size' : '10',
    'counterbore_x' : [[-2.75,2.75],[-5.5,5.5],[-5.5,5.5]],
    'counterbore_y' : [[-4.5,4.5],[-4.5,4.5],[-2.25,2.25]],
    'mounting_hole_size' : '1/2',
    'mounting_hole_x' : [-5.5,5.5],
    'mounting_hole_y' : [-5.5,5.5],
    'food_dish_diameter' : 1.591,
    'food_dish_depth' : 0.244,
    'extraction_hole_diameter' : 0.3,
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
        self.__make_food_dish_hole()
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
        bowl_depth = self.parameters['bowl_depth']
        bowl_diameter = self.parameters['bowl_diameter']
        bowl_slope = self.parameters['bowl_slope']

        theta = bowl_slope*numpy.pi/180
        L = (bowl_depth*numpy.pi)/(2*numpy.tan(theta))
        if bowl_diameter/2 < L/2:
            raise ValueError("The bowl_depth is too large for this bowl_diameter.")

        X = numpy.linspace(0,L/2)
        Y = (bowl_depth/2)*(1+numpy.sin(X*numpy.pi/L - numpy.pi/2))

        x0 = 0
        y0 = 0
        x1 = L/2 + bowl_depth/numpy.tan(theta)
        y1 = 3/2*bowl_depth
        X = numpy.append(X,x1)
        Y = numpy.append(Y,y1)

        # Offset for bowl_diameter, x0 and y0
        offset = x0 + bowl_diameter/2 - L/2 - bowl_depth/(2*numpy.tan(theta))
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
        z_offset = self.parameters['z']/2 - self.parameters['bowl_depth']
        bowl.translate([0,0,z_offset])
        self.add_obj(bowl)

    def __make_counterbores(self):
        counterbore_size = self.parameters['counterbore_size']
        screw_hole_depth = self.parameters['z']*2
        counterbore = screw_holes.Counterbore(size=counterbore_size,depth=screw_hole_depth,fit='free')
        z_offset = self.parameters['z']/2
        counterbore.translate([0,0,z_offset])


        counterbore_x = self.parameters['counterbore_x']
        counterbore_y = self.parameters['counterbore_y']
        counterbores = po.LinearArraySet(counterbore,x=counterbore_x,y=counterbore_y)
        self.add_obj(counterbores)

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

    def __make_food_dish_hole(self):
        food_dish_diameter = self.parameters['food_dish_diameter']
        food_dish_depth = self.parameters['food_dish_depth']
        depth_padding = 0.25
        food_dish_hole_l = food_dish_depth + depth_padding
        food_dish_hole = fso.Cylinder(l=food_dish_hole_l,r=food_dish_diameter/2)
        z_offset = food_dish_hole_l/2 + self.parameters['z']/2 - self.parameters['bowl_depth'] - self.parameters['food_dish_depth']
        food_dish_hole.translate([0,0,z_offset])

        extraction_hole_diameter = self.parameters['extraction_hole_diameter']
        extraction_hole_depth = self.parameters['z']*2
        extraction_hole = fso.Cylinder(l=extraction_hole_depth,r=extraction_hole_diameter/2)

        food_dish_hole |= extraction_hole

        self.add_obj(food_dish_hole)


# ---------------------------------------------------------------------
if __name__ == '__main__':
    fly_bowl = FlyBowl()
    fly_bowl.export()
