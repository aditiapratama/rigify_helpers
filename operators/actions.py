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


class RH_OT_clean_unused_keyframes(Operator):
    """Clean all Fcurves in all actions keyframe if only hold single key point"""

    bl_idname = "objects.clean_unused_keyframes"
    bl_label = "Clean Keyframes"

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == "ARMATURE"
        )

    def execute(self, context):
        fn.remove_unused_fcurves()
        fn.remove_nla_tracks()

        self.report({"INFO"}, "Keyframes and NLA Tracks cleaned successfully!")
        return {"FINISHED"}


registry = [
    RH_OT_clean_unused_keyframes,
]
