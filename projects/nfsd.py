# -*- python -*-
# ex: set filetype=python:

c["projects"].append(
    util.Project(name="NFSD CI", slug="Upstream NFSD Continuous Integration")
)


for sched_name in kdevopsSchedulerNames:
    kdevops_fstests_builder("nfsd", sched_name)
    kdevops_builder("nfsd", sched_name, "gitr")
    kdevops_builder("nfsd", sched_name, "ltp")
    kdevops_builder("nfsd", sched_name, "nfstest")
    kdevops_builder("nfsd", sched_name, "pynfs")


def kdevops_branch_scheduler(sched_name, watched_repo, watched_branch):
    c["schedulers"].append(
        schedulers.SingleBranchScheduler(
            name=f"branch-{sched_name}",
            change_filter=util.ChangeFilter(
                repository=watched_repo, branch=watched_branch
            ),
            treeStableTimer=300,
            builderNames=[
                f"{sched_name}-nfsd-{workflow}" for workflow in kdevopsWorkflowNames
            ],
        )
    )


def kdevops_nightly_scheduler(sched_name, watched_repo, watched_branch, hour, minute):
    c["schedulers"].append(
        schedulers.Nightly(
            name=f"nightly-{sched_name}",
            change_filter=util.ChangeFilter(
                repository=watched_repo, branch=watched_branch
            ),
            hour=hour,
            minute=minute,
            builderNames=[
                f"{sched_name}-nfsd-{workflow}" for workflow in kdevopsWorkflowNames
            ],
        )
    )


def kdevops_force_schedulers(sched_name):
    """Add one 'Force' scheduler"""
    for workflow in kdevopsWorkflowNames:
        c["schedulers"].append(
            schedulers.ForceScheduler(
                name=f"force-{sched_name}-nfsd-{workflow}",
                builderNames=[f"{sched_name}-nfsd-{workflow}"],
                buttonName=f"Start {sched_name}-nfsd-{workflow}",
            )
        )


kdevops_force_schedulers(sched_name="nfsd-next")

kdevops_force_schedulers(sched_name="nfsd-fixes")

kdevops_force_schedulers(sched_name="nfsd-testing")

kdevops_force_schedulers(sched_name="nfsd-6-13-y")

kdevops_force_schedulers(sched_name="nfsd-6-12-y")

kdevops_force_schedulers(sched_name="nfsd-6-6-y")

kdevops_force_schedulers(sched_name="nfsd-6-1-y")

kdevops_force_schedulers(sched_name="nfsd-5-15-y")

kdevops_force_schedulers(sched_name="nfsd-5-10-y")

kdevops_force_schedulers(sched_name="nfsd-5-4-y")

kdevops_nightly_scheduler(
    sched_name="queue-6-13",
    watched_repo="https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable-rc.git",
    watched_branch="queue/6.13",
    hour=19,
    minute=1,
)
kdevops_force_schedulers(sched_name="queue-6-13")

kdevops_nightly_scheduler(
    sched_name="queue-6-12",
    watched_repo="https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable-rc.git",
    watched_branch="queue/6.12",
    hour=19,
    minute=1,
)
kdevops_force_schedulers(sched_name="queue-6-12")

kdevops_nightly_scheduler(
    sched_name="queue-6-6",
    watched_repo="https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable-rc.git",
    watched_branch="queue/6.6",
    hour=20,
    minute=31,
)
kdevops_force_schedulers(sched_name="queue-6-6")

kdevops_nightly_scheduler(
    sched_name="queue-6-1",
    watched_repo="https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable-rc.git",
    watched_branch="queue/6.1",
    hour=22,
    minute=1,
)
kdevops_force_schedulers(sched_name="queue-6-1")

kdevops_nightly_scheduler(
    sched_name="queue-5-15",
    watched_repo="https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable-rc.git",
    watched_branch="queue/5.15",
    hour=23,
    minute=31,
)
kdevops_force_schedulers(sched_name="queue-5-15")

kdevops_nightly_scheduler(
    sched_name="queue-5-10",
    watched_repo="https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable-rc.git",
    watched_branch="queue/5.10",
    hour=1,
    minute=1,
)
kdevops_force_schedulers(sched_name="queue-5-10")

kdevops_nightly_scheduler(
    sched_name="queue-5-4",
    watched_repo="https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable-rc.git",
    watched_branch="queue/5.4",
    hour=2,
    minute=31,
)
kdevops_force_schedulers(sched_name="queue-5-4")

kdevops_nightly_scheduler(
    sched_name="fs-next",
    watched_repo="https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git",
    watched_branch="fs-next",
    hour=4,
    minute=1,
)
kdevops_force_schedulers(sched_name="fs-next")

kdevops_nightly_scheduler(
    sched_name="fs-current",
    watched_repo="https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git",
    watched_branch="fs-current",
    hour=5,
    minute=31,
)
kdevops_force_schedulers(sched_name="fs-current")
