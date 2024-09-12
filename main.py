bl_info = {
    "name": "Show Mario Stand",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import bmesh


class ShowStandableGround(bpy.types.Operator):
    """Show Standable Ground"""
    bl_idname = "object.show_standable_ground"
    bl_label = "Show Standable Ground"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        MAX_STEEPNESS = 10
        obj = context.active_object

        # create a new mesh object (not in the editor)
        # to give us access to additional
        # data and data types
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bm.faces.ensure_lookup_table()

        # TODO: add additional logic here
        # to detect the baremost part that Mario
        # can stand on

        standable_faces = []

        # get all vertices of each face
        for face in bm.faces:
            # append to the great vertex list
            # the index and coordinates of each vertices
            # of each face
            too_steep = False

            for i in range(0, 2):
                # if the absolute value of the current vertex's
                # z coordinate MINUS the z coordinate
                # of the previous vertex is greater than
                # the threshhold, mark it as too steep
                if abs(face.verts[i].co[3] - face.verts[i - 1].co[3]) > MAX_STEEPNESS:
                    too_steep = True
                    break

                # values of i - 1 should be -1, 0, 1
                # so that way the last one is compared to
                # the first vertex, the second to the first,
                # and the third to the second

            if not too_steep:
                standable_faces.append(face)

        bm.to_mesh(standable_faces)

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


