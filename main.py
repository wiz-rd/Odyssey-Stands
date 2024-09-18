bl_info = {
    "name": "Show Mario Stand",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import bmesh
import numpy as np


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
        MAX_STEEPNESS = 0.5
        # store original object to hide later
        # (because we can't hide it and it still be selected)
        original_obj = context.active_object
        # duplicate original/selected object
        bpy.ops.object.duplicate(linked=0,mode='TRANSLATION')
        # hide original object
        original_obj.hide_set(True)
        # store the new object in a variable
        new_obj = context.active_object
        new_obj.name = "StandableGround"

        green_mat = self.create_material("StandableGreen", (0, 1, 0, 1))
        red_mat = self.create_material("NonstandableRed", (1, 0, 0, 1))

        # if no materials exist, add them
        if len(new_obj.materials) == 0:
            new_obj.data.materials.append(green_mat)
        # if only green exists, add red
        if len(new_obj.materials) == 1:
            new_obj.data.materials.append(red_mat)

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

        # get all vertices of each face
        for face in bm.faces:
            # append to the great vertex list
            # the index and coordinates of each vertices
            # of each face
            too_steep = False

            print(face.normal.z)
            print(f"is too steep: {face.normal.z > MAX_STEEPNESS}")

            if not too_steep:
                print(f"Appended {face} to highlight list.")
                # appending the face to the list to be highlighted
                standable_faces.add(face.index)
            else:
                not_standable_faces.add(face.index)

        for face in standable_faces:
            # setting face colors to green
            new_obj.data.polygons[face].material_index = 1

        for face in not_standable_faces:
            # setting face colors to red
            new_obj.data.polygons[face].material_index = 2

        # bmesh.ops.delete(bm, geom=selected_faces, context="FACES")
        # bm.to_mesh(new_obj_mesh)
        # new_obj.update_from_editmode()

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
