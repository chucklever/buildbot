# -*- python -*-
# ex: set filetype=python:

c["projects"].append(
    util.Project(name="tmpfs CI", slug="Upstream tmpfs Continuous Integration")
)


kdevops_fstests_builder("tmpfs", "fs-current")
kdevops_builder("tmpfs", "fs-current", "gitr")
kdevops_fstests_builder("tmpfs", "fs-next")
kdevops_builder("tmpfs", "fs-next", "gitr")


TmpfsWorkflowNames = ["fstests", "gitr", ]


def kdevops_tmpfs_nightly_scheduler(sched_name, watched_repo, watched_branch, hour, minute):
    c["schedulers"].append(
        schedulers.Nightly(
            name=f"nightly-{sched_name}-tmpfs",
            change_filter=util.ChangeFilter(
                repository=watched_repo, branch=watched_branch
            ),
            hour=hour,
            minute=minute,
            builderNames=[
                f"{sched_name}-tmpfs-{workflow}" for workflow in TmpfsWorkflowNames
            ],
        )
    )


def kdevops_tmpfs_force_schedulers(sched_name):
    """Add one 'Force' scheduler"""
    for workflow in TmpfsWorkflowNames:
        c["schedulers"].append(
            schedulers.ForceScheduler(
                name=f"force-{sched_name}-tmpfs-{workflow}",
                builderNames=[f"{sched_name}-tmpfs-{workflow}"],
                buttonName=f"Start {sched_name}-tmpfs-{workflow}",
            )
        )


kdevops_tmpfs_nightly_scheduler(
    sched_name="fs-current",
    watched_repo="https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git",
    watched_branch="fs-current",
    hour=5,
    minute=31,
)
kdevops_tmpfs_force_schedulers(
    sched_name="fs-current",
)

kdevops_tmpfs_nightly_scheduler(
    sched_name="fs-next",
    watched_repo="https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git",
    watched_branch="fs-next",
    hour=7,
    minute=1,
)
kdevops_tmpfs_force_schedulers(
    sched_name="fs-next",
)
