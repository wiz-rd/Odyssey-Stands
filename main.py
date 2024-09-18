bl_info = {
    "name": "Show Mario Stand",
    "blender": (2, 80, 0),
    "category": "Object",
}

from math import degrees

import bpy
import bmesh
from mathutils import Vector


class ShowStandableGround(bpy.types.Operator):
    """Show Standable Ground"""
    bl_idname = "object.show_standable_ground"
    bl_label = "Show Standable Ground"
    bl_options = {"REGISTER", "UNDO"}


    # create a material to assign to the faces
    # thank you:
    # https://blender.stackexchange.com/a/240875
    def create_material(self, mat_name, diffuse_color=(1,1,1,1)):
        mat = bpy.data.materials.new(name=mat_name)
        mat.diffuse_color = diffuse_color
        return mat

    def execute(self, context):
        # max steepness of slope in degrees
        # when compared to global z
        # global rotation is counted,
        # so faces "facing" downwards are
        # considered "too steep"
        MAX_STEEPNESS = 45

        # the global z vector. Maybe Blender
        # has one by default but it's not hard to add
        # and I can't find any reference to one online
        GLOBAL_Z = Vector((0, 0, 1))

        # store original object to hide later
        # (because we can't hide it and it still be selected)
        original_obj = context.active_object
        or_name = original_obj.name

        # duplicate original/selected object
        bpy.ops.object.duplicate(linked=0,mode='TRANSLATION')

        # hide original object
        original_obj.hide_set(True)

        # store the new object in a variable
        new_obj = context.active_object
        new_obj.name = f"Stand_{or_name}"

        green_mat = self.create_material(f"StandableGreen_{or_name}", (0, 1, 0, 1))
        red_mat = self.create_material(f"NonstandableRed_{or_name}", (1, 0, 0, 1))
        # blue_mat = self.create_material(f"ProblematicBlue_{or_name}", (0, 0, 1, 1))

        # if materials already exist (on the DUPICATE
        # OBJECT - this is non-destructive)
        # then delete them
        if len(new_obj.data.materials) > 0:
            new_obj.data.materials.clear()

        new_obj.data.materials.append(green_mat)
        new_obj.data.materials.append(red_mat)
        # new_obj.data.materials.append(blue_mat)

        # get the data for that object
        new_obj_mesh = new_obj.to_mesh(preserve_all_data_layers=True)

        # "globalize" the data. Not sure if this is necessary anymore
        # as I removed manual calculation of face normals
        new_obj_mesh.transform(new_obj.matrix_world)

        # create a new mesh object (not in the editor)
        # to give us access to additional
        # data and data types
        bm = bmesh.new()
        bm.from_mesh(new_obj_mesh)
        bm.faces.ensure_lookup_table()

        print()
        standable_faces = set()
        not_standable_faces = set()

        # get normal vectors of each face
        # and compare them to the global z
        for face in bm.faces:
            # append to the great vertex list
            # the index and coordinates of each vertices
            # of each face
            too_steep = False
            normal = face.normal
            angle_difference_to_z = normal.angle(GLOBAL_Z)
            angle_to_z_deg = degrees(angle_difference_to_z)

            if angle_to_z_deg > MAX_STEEPNESS:
                too_steep = True

            if not too_steep:
                # appending the face to the list to be highlighted
                standable_faces.add(face.index)
            else:
                # similar to above
                not_standable_faces.add(face.index)

        print(f"{len(standable_faces)} faces found standable.")
        print(f"{len(not_standable_faces)} faces found non-standable.")

        for face in standable_faces:
            # setting face colors to green
            new_obj.data.polygons[face].material_index = 0

        for face in not_standable_faces:
            # setting face colors to red
            new_obj.data.polygons[face].material_index = 1

        # for face in standable_faces U not_standable_faces:
        #     print(f"We have a problem. Face {face} is in both sets.")
        #     new_obj.data.polygons[face].material_index = 2

        return {"FINISHED"}


def menu_func(self, context):
    self.layout.operator(ShowStandableGround.bl_idname)

def register():
    bpy.utils.register_class(ShowStandableGround)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():
    bpy.utils.unregister_class(ShowStandableGround)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
