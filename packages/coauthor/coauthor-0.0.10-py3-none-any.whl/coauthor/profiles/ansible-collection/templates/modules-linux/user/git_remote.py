#!/usr/bin/python
#
# Example Code for Linux module `git_remote.py`
#

from __future__ import annotations
import os
from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            dest=dict(type="path", required=True),
            name=dict(type="str", required=True),
            url=dict(type="str", required=True),
            state=dict(
                type="str",
                required=False,
                choices=["present", "absent"],
                default="present",
            ),
        ),
        supports_check_mode=True,
    )

    dest = module.params["dest"]
    remote_name = module.params["name"]
    remote_url = module.params["url"]
    state = module.params["state"]

    result = dict(changed=False)

    git_cmd = "git -C {}".format(dest)

    if state == "present":
        # Check if remote already exists
        check_remote_command = f"{git_cmd} remote get-url {remote_name}"
        rc, stdout, stderr = module.run_command(check_remote_command)

        if rc != 0:
            # Remote does not exist, add it
            add_remote_command = f"{git_cmd} remote add {remote_name} {remote_url}"
            if module.check_mode:
                result["changed"] = True
            else:
                module.run_command(add_remote_command)
                result["changed"] = True
        else:
            # Remote exists, check url
            existing_url = stdout.strip()
            if existing_url != remote_url:
                update_remote_command = f"{git_cmd} remote set-url {remote_name} {remote_url}"
                if module.check_mode:
                    result["changed"] = True
                else:
                    module.run_command(update_remote_command)
                    result["changed"] = True

    elif state == "absent":
        # Check if remote exists
        check_remote_command = f"{git_cmd} remote get-url {remote_name}"
        rc, stdout, stderr = module.run_command(check_remote_command)

        if rc == 0:
            # Remote exists, remove it
            remove_remote_command = f"{git_cmd} remote remove {remote_name}"
            if module.check_mode:
                result["changed"] = True
            else:
                module.run_command(remove_remote_command)
                result["changed"] = True

    module.exit_json(**result)


if __name__ == "__main__":
    main()
