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

import bpy
from bpy.types import Operator, bpy_prop_collection
from .. import function as fn


class RH_OT_clean_invalid_drivers(Operator):
    """Loop over all ID types in the data of the blend and remove any driver whose path does not resolve and all duplicates drivers"""

    # credit : @batFINGER https://blender.stackexchange.com/questions/212450/invalid-drivers-arent-shown-and-cant-be-deleted

    # credit : @Yokomizo https://blender.stackexchange.com/questions/278917/can-i-delete-all-duplicated-drivers-of-armature

    # credit : refresh all drivers taken from rigify utility

    bl_idname = "objects.clean_invalid_drivers"
    bl_label = "Clean Drivers"

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == "ARMATURE"
        )

    def execute(self, context):
        fn.refresh_all_drivers()
        fn.remove_invalid_drivers()
        fn.refresh_all_drivers()
        fn.remove_duplicate_drivers()
        fn.refresh_all_drivers()

        self.report({"INFO"}, "Invalid and Duplicate Drivers cleaned successfully!")

        return {"FINISHED"}


registry = [
    RH_OT_clean_invalid_drivers,
]
