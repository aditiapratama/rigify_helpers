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

from bpy.types import Operator
from .. import function as fn


class RH_OT_clean_widgets(Operator):
    """Clean unused widget objects, rename it and put it back to standard rigify structure."""

    bl_idname = "objects.clean_widgets"
    bl_label = "Clean Widgets"

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == "ARMATURE"
        )

    def execute(self, context):
        wgts = fn.get_widget_objects()
        csobjs = fn.get_custom_shape_objects()

        fn.set_custom_shape_colls(csobjs)
        fn.clean_unused_widgets(wgts, csobjs)

        self.report({"INFO"}, "Widgets Objects cleaned successfully!")
        return {"FINISHED"}


registry = [
    RH_OT_clean_widgets,
]
