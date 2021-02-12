# ### BEGIN GPL LICENSE BLOCK ###
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ### END GPL LICENSE BLOCK ###

import bpy
from bpy.types import Operator
from mathutils import Color

bl_info = {
    "name": "Select Vertex Color",
    "author": "Smilex",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": " Found is select similar shift + G",
    "description": "Some tools for vertex colors that should already be in Blender.",
    "category": "Mesh"}




def vertex_color(context):

    threshold = .1
   
    if len(context.selected_objects) == 0:
        return
    obj = context.selected_objects[0]
    bpy.ops.object.mode_set(mode="OBJECT")

    colors = obj.data.vertex_colors.active.data
    #selected_polygons = list(filter(lambda p: p.select, obj.data.polygons))
    selected_polygons = [p for p in obj.data.polygons if p.select] 
    if len(selected_polygons):
        p = selected_polygons[0]
   
        r = g = b = 0
       
        for i in p.loop_indices:
            c = colors[i].color
            r += c[0]
            g += c[1]
            b += c[2]
        r /= p.loop_total
        g /= p.loop_total
        b /= p.loop_total
        target = Color((r, g, b))

        for p in obj.data.polygons:
            r = g = b = 0
            for i in p.loop_indices:
                c = colors[i].color
                r += c[0]
                g += c[1]
                b += c[2]
            r /= p.loop_total
            g /= p.loop_total
            b /= p.loop_total
            source = Color((r, g, b))

            print(target, source)

            if (abs(source.r - target.r) < threshold and
                abs(source.g - target.g) < threshold and
                abs(source.b - target.b) < threshold):

                p.select = True

    bpy.ops.object.mode_set(mode="EDIT")



class Vertexcolor(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.vertex_operator"
    bl_label = "Select by Vertex Color"

    def execute(self, context):
        vertex_color(context) #
        return {'FINISHED'}


def register():
    bpy.utils.register_class(Vertexcolor)
    bpy.types.VIEW3D_MT_edit_mesh_select_similar.append(add_menu_item)

def unregister():
    bpy.utils.unregister_class(Vertexcolor)
    bpy.types.VIEW3D_MT_edit_mesh_select_similar.remove(add_menu_item)

def add_menu_item(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("object.vertex_operator")

if __name__ == "__main__":
    register()

