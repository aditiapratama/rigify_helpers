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
from typing import Optional
from bpy.types import (
    bpy_prop_collection,
    Material,
    AnimData,
)


def remove_unused_fcurves():
    for action in bpy.data.actions:
        fcus = [fcu for fcu in action.fcurves if not len(fcu.keyframe_points) > 1]
        for fcu in fcus:
            action.fcurves.remove(fcu)


def remove_nla_tracks():
    for attr in dir(bpy.data):
        coll = getattr(bpy.data, attr, None)

        if isinstance(coll, bpy_prop_collection):
            for item in coll:
                anim_data = getattr(item, "animation_data", None)
                if anim_data:
                    for i, track in enumerate(anim_data.nla_tracks):
                        anim_data.nla_tracks.remove(track)


def remove_duplicate_drivers():
    driver_list = list()

    for attr in dir(bpy.data):
        coll = getattr(bpy.data, attr, None)

        if isinstance(coll, bpy_prop_collection):
            for item in coll:
                anim_data = getattr(item, "animation_data", None)
                if anim_data:
                    for fcu in anim_data.drivers:
                        driver_id = (
                            "Object name = "
                            + item.name
                            + " Path = "
                            + fcu.data_path
                            + "["
                            + str(fcu.array_index)
                            + "]"
                            + " Driver expression = "
                            + fcu.driver.expression
                        )
                        if driver_id not in driver_list:
                            driver_list.append(driver_id)
                        else:
                            print(
                                "Deleting Unwanted Drivers",
                                driver_id,
                            )
                            item.driver_remove(fcu.data_path, fcu.array_index)


def remove_invalid_drivers():
    colls = [
        p
        for p in dir(bpy.data)
        if isinstance(getattr(bpy.data, p), bpy_prop_collection)
    ]
    for p in colls:
        for ob in getattr(bpy.data, p, []):
            ad = getattr(ob, "animation_data", None)
            if not ad:
                continue
            invalid_drivers = []
            for d in ad.drivers:
                try:
                    ob.path_resolve(d.data_path)
                except ValueError:
                    invalid_drivers.append(d)
            while invalid_drivers:
                ad.drivers.remove(invalid_drivers.pop())


def to_delete(widgets, custom_shape_objects) -> list:
    csobjs = [o[1] for o in custom_shape_objects]
    return [i for i in widgets if i not in csobjs]


def get_custom_shape_objects() -> list:
    return [
        [b, b.custom_shape]
        for o in bpy.data.objects
        if o.type == "ARMATURE"
        for b in o.pose.bones
        if b.custom_shape
    ]


def get_widget_objects() -> list:
    return [o for o in bpy.data.objects if o.name.lower().startswith("wgt-")]


def get_custom_shape_colls(custom_shape_objects, wgt_coll_name):
    colls = []
    for o in custom_shape_objects:
        for coll in o[1].users_collection:
            if coll.name != wgt_coll_name:
                colls.append(coll)

    return set(colls)


def set_custom_shape_colls(custom_shape_objects):
    filename = bpy.path.clean_name(bpy.path.display_name(bpy.data.filepath))
    rig_names = list(set([o[0].id_data.name for o in custom_shape_objects]))

    for r in rig_names:
        wgt_coll_name = "WGTS_" + str(r)

        wgt_coll = (
            bpy.data.collections[wgt_coll_name]
            if bpy.data.collections.get(wgt_coll_name)
            else bpy.data.collections.new(wgt_coll_name)
        )
        wgt_coll.use_fake_user = True

        cs_objs_colls = get_custom_shape_colls(custom_shape_objects, wgt_coll_name)

        for c in cs_objs_colls:
            bpy.data.collections.remove(c)

    for obj in custom_shape_objects:
        obj[1].display_type = "WIRE"
        ob_name = f"WGT-{obj[0].id_data.name}_{obj[0].name}"
        me_name = ob_name + ".mesh"
        obj[1].name = ob_name
        obj[1].data.name = me_name
        mod = next((m for m in obj[1].modifiers), None)
        if mod:
            obj[1].modifiers.remove(mod)
        try:
            coll = bpy.data.collections.get(f"WGTS_{obj[0].id_data.name}")
            coll.objects.link(obj[1])

        except RuntimeError:
            pass


def clean_unused_widgets(wgts, cs_objs):
    objs_to_delete = to_delete(wgts, cs_objs)

    print(f"Total Unused Widgets : {len(objs_to_delete)}")

    for o in objs_to_delete:
        bpy.data.objects.remove(o)


def refresh_drivers(obj):
    """Cause all drivers belonging to the object to be re-evaluated, clearing any errors."""

    # Refresh object's own drivers if any
    anim_data: Optional[AnimData] = getattr(obj, "animation_data", None)

    if anim_data:
        for fcu in anim_data.drivers:
            # Make a fake change to the driver
            fcu.driver.type = fcu.driver.type

    # Material node trees aren't in any lists
    if isinstance(obj, Material):
        refresh_drivers(obj.node_tree)


def refresh_all_drivers():
    """Cause all drivers in the file to be re-evaluated, clearing any errors."""

    # Iterate over all data blocks in the file
    for attr in dir(bpy.data):
        coll = getattr(bpy.data, attr, None)

        if isinstance(coll, bpy_prop_collection):
            for item in coll:
                refresh_drivers(item)
