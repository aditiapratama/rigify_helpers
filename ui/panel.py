# Copyright (C) 2024 Aditia A. Pratama | aditia.ap@gmail.com
#
# This file is part of rigify_helpers.
#
# rigify_helpers is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rigify_helpers is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rigify_helpers.  If not, see <https://www.gnu.org/licenses/>.

from bpy.types import Panel
from .. import utils as ut


class RH_PT_panel:
    """
    Panel in 3D Viewport Sidebar
    """

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"


class RH_PT_tools(RH_PT_panel, Panel):
    bl_label = "Rigify Helpers"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon="OUTLINER_OB_ARMATURE")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        indent = 0.2
        separator_fac = 0.25

        col = layout.column(align=True)
        box = col.box()
        row = ut._indent_row(box, indent, True, icon="DRIVER")
        row.operator(
            "objects.clean_invalid_drivers",
        )
        col.separator(factor=separator_fac)
        box = col.box()
        row = ut._indent_row(box, indent, True, icon="ACTION")
        row.operator(
            "objects.clean_unused_keyframes",
        )
        col.separator(factor=separator_fac)
        box = col.box()
        row = ut._indent_row(box, indent, True, icon="MESH_DATA")
        row.operator(
            "objects.clean_widgets",
        )


registry = [RH_PT_tools]
