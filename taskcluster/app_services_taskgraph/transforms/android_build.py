# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function, unicode_literals

from taskgraph.transforms.base import TransformSequence

from taskcluster.app_services_taskgraph.build_config import script_to_bash_command
from ..build_config import get_components

transforms = TransformSequence()


@transforms.add
def add_megazord_checks(config, tasks):
    components = get_components()
    megazord_names = [component["name"] for component in components if component["name"].endswith("-megazord")]
    megazord_commands = ["./automation/check_megazord.sh {}".format(name[0:-9].replace("-", "_")) for name in megazord_names]
    for task in tasks:
        if task.get("attributes", {}).get("add-megazord-checks", False):
            task["worker"]["script"] += "\n" + "\n".join(megazord_commands)
        yield task


@transforms.add
def build_task(config, tasks):
    for task in tasks:
        script = task["worker"].pop("script")
        task["run"]["command"] = script_to_bash_command(script)

        yield task

