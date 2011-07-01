from __future__ import division
import roslib
roslib.load_manifest('fly_bowls')
import rospy

import cad.csg_objects as csg

import fly_bowl
import fly_bowl_support_plate


class FlyBowlAssembly(csg.Union):
    def __init__(self):
        super(FlyBowlAssembly, self).__init__()
        self.__make_fly_bowl()
        self.__make_fly_bowl_support_plate()
        # self.__set_bom()

    def __set_bom(self):
        BOM = bom.BOMObject()
        BOM.set_parameter('name',self.parameters['name'])
        BOM.set_parameter('description',self.parameters['description'])
        # BOM.set_parameter('dimensions',('slide travel: ' + str(self.parameters['bearing_slide_travel'])))
        BOM.set_parameter('vendor',self.parameters['vendor'])
        BOM.set_parameter('part number',self.parameters['part number'])
        BOM.set_parameter('cost',self.parameters['cost'])
        self.set_object_parameter('bom',BOM)

    def __make_fly_bowl(self):
        fly_bowl_ = fly_bowl.FlyBowl()
        self.fly_bowl_parameters = fly_bowl_.get_parameters()
        z_offset = self.fly_bowl_parameters['z'] * self.fly_bowl_parameters['scale'][2]
        fly_bowl_.translate([0,0,z_offset])
        self.add_obj(fly_bowl_)

    def __make_fly_bowl_support_plate(self):
        fly_bowl_support_plate_ = fly_bowl_support_plate.FlyBowlSupportPlate()
        self.fly_bowl_support_plate_parameters = fly_bowl_support_plate_.get_parameters()
        z_offset = -self.fly_bowl_support_plate_parameters['z'] * self.fly_bowl_parameters['scale'][2]
        fly_bowl_support_plate_.translate([0,0,z_offset])
        self.add_obj(fly_bowl_support_plate_)


# ---------------------------------------------------------------------
if __name__ == '__main__':
    fly_bowl_assembly = FlyBowlAssembly()
    fly_bowl_assembly.export()
