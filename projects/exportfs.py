# -*- python -*-
# ex: set filetype=python:

c["projects"].append(
    util.Project(name="exports CI", slug="Upstream exportfs Continuous Integration")
)

kdevops_fstests_builder("exportfs", "fs-current")

c["schedulers"].append(
    schedulers.Nightly(
        name="nightly-exportfs",
        change_filter=util.ChangeFilter(
            repository="https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git",
            branch="fs-current",
        ),
        hour=5,
        minute=31,
        builderNames=["fs-current-exportfs-fstests"],
    )
)
c["schedulers"].append(
    schedulers.ForceScheduler(
        name="force-fs-current-exportfs-fstests",
        builderNames=["fs-current-exportfs-fstests"],
        buttonName="Start fs-current-exportfs-fstests",
    )
)
