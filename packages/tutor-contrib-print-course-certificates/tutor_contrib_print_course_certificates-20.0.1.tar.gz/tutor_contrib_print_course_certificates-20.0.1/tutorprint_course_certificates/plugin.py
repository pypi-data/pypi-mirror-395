from __future__ import annotations

import os
from glob import glob

import shutil
import importlib_resources
from tutor import hooks, config as tutor_config

from .__about__ import __version__

########################################
# CONFIGURATION
########################################

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        # Add your new settings that have default values here.
        # Each new setting is a pair: (setting_name, default_value).
        # Prefix your setting names with 'PRINT_COURSE_CERTIFICATES_'.
        ("PRINT_COURSE_CERTIFICATES_VERSION", __version__),
        ("RUN_PRINT_COURSE_CERTIFICATE", True),
        (
            "PRINT_COURSE_CERTIFICATES_DOCKER_IMAGE",
            "docker.io/nauedu/nau-course-certificate:master",
        ),
        ("PRINT_COURSE_CERTIFICATES_UWSGI_WORKERS", 2),
        ("PRINT_COURSE_CERTIFICATES_HOST", "course-certificate.{{ LMS_HOST }}"),
        ("PRINT_COURSE_CERTIFICATES_PORT", 5000),
        ("PRINT_COURSE_CERTIFICATES_CERTIFICATE_P12_PATH", None),
        ("PRINT_COURSE_CERTIFICATES_CONFIG", {"some": "value"}),
    ]
)

hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        # Add settings that don't have a reasonable default for all users here.
        # For instance: passwords, secret keys, etc.
        # Each new setting is a pair: (setting_name, unique_generated_value).
        # Prefix your setting names with 'PRINT_COURSE_CERTIFICATES_'.
        # For example:
        ### ("PRINT_COURSE_CERTIFICATES_SECRET_KEY", "{{ 24|random_string }}"),
    ]
)

hooks.Filters.CONFIG_OVERRIDES.add_items(
    [
        # Danger zone!
        # Add values to override settings from Tutor core or other plugins here.
        # Each override is a pair: (setting_name, new_value). For example:
        ### ("PLATFORM_NAME", "My platform"),
    ]
)


########################################
# INITIALIZATION TASKS
########################################

# To add a custom initialization task, create a bash script template under:
# tutorprint_course_certificates/templates/print-course-certificates/tasks/
# and then add it to the MY_INIT_TASKS list. Each task is in the format:
# ("<service>", ("<path>", "<to>", "<script>", "<template>"))
MY_INIT_TASKS: list[tuple[str, tuple[str, ...]]] = [
    # For example, to add LMS initialization steps, you could add the script template at:
    # tutorprint_course_certificates/templates/print-course-certificates/tasks/lms/init.sh
    # And then add the line:
    ### ("lms", ("print-course-certificates", "tasks", "lms", "init.sh")),
]


# For each task added to MY_INIT_TASKS, we load the task template
# and add it to the CLI_DO_INIT_TASKS filter, which tells Tutor to
# run it as part of the `init` job.
for service, template_path in MY_INIT_TASKS:
    full_path: str = str(
        importlib_resources.files("tutorprint_course_certificates")
        / os.path.join("templates", *template_path)
    )
    with open(full_path, encoding="utf-8") as init_task_file:
        init_task: str = init_task_file.read()
    hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, init_task))


########################################
# DOCKER IMAGE MANAGEMENT
########################################


# Images to be built by `tutor images build`.
# Each item is a quadruple in the form:
#     ("<tutor_image_name>", ("path", "to", "build", "dir"), "<docker_image_tag>", "<build_args>")
hooks.Filters.IMAGES_BUILD.add_items(
    [
        # To build `myimage` with `tutor images build myimage`,
        # you would add a Dockerfile to templates/print-course-certificates/build/myimage,
        # and then write:
        ### (
        ###     "myimage",
        ###     ("plugins", "print-course-certificates", "build", "myimage"),
        ###     "docker.io/myimage:{{ PRINT_COURSE_CERTIFICATES_VERSION }}",
        ###     (),
        ### ),
    ]
)


# Images to be pulled as part of `tutor images pull`.
# Each item is a pair in the form:
#     ("<tutor_image_name>", "<docker_image_tag>")
hooks.Filters.IMAGES_PULL.add_items(
    [
        # To pull `myimage` with `tutor images pull myimage`, you would write:
        ### (
        ###     "myimage",
        ###     "docker.io/myimage:{{ PRINT_COURSE_CERTIFICATES_VERSION }}",
        ### ),
    ]
)


# Images to be pushed as part of `tutor images push`.
# Each item is a pair in the form:
#     ("<tutor_image_name>", "<docker_image_tag>")
hooks.Filters.IMAGES_PUSH.add_items(
    [
        # To push `myimage` with `tutor images push myimage`, you would write:
        ### (
        ###     "myimage",
        ###     "docker.io/myimage:{{ PRINT_COURSE_CERTIFICATES_VERSION }}",
        ### ),
    ]
)


########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        str(importlib_resources.files("tutorprint_course_certificates") / "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``source_path/destination_path`` (relative to your Tutor environment).
    # For example, ``tutorprint_course_certificates/templates/print-course-certificates/build``
    # will be rendered to ``$(tutor config printroot)/env/plugins/print-course-certificates/build``.
    [
        ("print-course-certificates/build", "plugins"),
        ("print-course-certificates/apps", "plugins"),
    ],
)


########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutorprint_course_certificates/patches,
# apply a patch based on the file's name and contents.
for path in glob(
    str(importlib_resources.files("tutorprint_course_certificates") / "patches" / "*")
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))


########################################
# CUSTOM JOBS (a.k.a. "do-commands")
########################################

# A job is a set of tasks, each of which run inside a certain container.
# Jobs are invoked using the `do` command, for example: `tutor local do importdemocourse`.
# A few jobs are built in to Tutor, such as `init` and `createuser`.
# You can also add your own custom jobs:


# To add a custom job, define a Click command that returns a list of tasks,
# where each task is a pair in the form ("<service>", "<shell_command>").
# For example:
### @click.command()
### @click.option("-n", "--name", default="plugin developer")
### def say_hi(name: str) -> list[tuple[str, str]]:
###     """
###     An example job that just prints 'hello' from within both LMS and CMS.
###     """
###     return [
###         ("lms", f"echo 'Hello from LMS, {name}!'"),
###         ("cms", f"echo 'Hello from CMS, {name}!'"),
###     ]


# Then, add the command function to CLI_DO_COMMANDS:
## hooks.Filters.CLI_DO_COMMANDS.add_item(say_hi)

# Now, you can run your job like this:
#   $ tutor local do say-hi --name="Ivo Branco"


#######################################
# CUSTOM CLI COMMANDS
#######################################

# Your plugin can also add custom commands directly to the Tutor CLI.
# These commands are run directly on the user's host computer
# (unlike jobs, which are run in containers).

# To define a command group for your plugin, you would define a Click
# group and then add it to CLI_COMMANDS:


### @click.group()
### def print-course-certificates() -> None:
###     pass


### hooks.Filters.CLI_COMMANDS.add_item(print-course-certificates)


# Then, you would add subcommands directly to the Click group, for example:


### @print-course-certificates.command()
### def example_command() -> None:
###     """
###     This is helptext for an example command.
###     """
###     print("You've run an example command.")


# This would allow you to run:
#   $ tutor print-course-certificates example-command


@hooks.Actions.PLUGINS_LOADED.add()
def _copy_file_p12() -> None:
    config = tutor_config.get_user(os.environ["TUTOR_ROOT"])
    p12_path = config.get("PRINT_COURSE_CERTIFICATES_CERTIFICATE_P12_PATH")
    dest_fpath = "env/plugins/print-course-certificates/apps/file.p12"
    # create folder of p12_path on env
    os.makedirs(os.path.dirname(dest_fpath), exist_ok=True)
    # copy file p12 to env
    shutil.copyfile(str(p12_path), dest_fpath)
