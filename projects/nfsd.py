# -*- python -*-
# ex: set filetype=python:

c["projects"].append(
    util.Project(name="NFSD CI", slug="Upstream NFSD Continuous Integration")
)

c["workers"].append(
    worker.Worker("kdevops-small", util.Secret("worker-kdevops-small"), max_builds=1)
)
c["workers"].append(
    worker.Worker("kdevops-large", util.Secret("worker-kdevops-large"), max_builds=1),
)


def kdevops_factory(testBranch, workflow):
    all_steps = [
        steps.Git(
            name="download kdevops",
            description="downloading",
            descriptionDone="download",
            repourl="https://github.com/chucklever/kdevops.git",
            branch=testBranch,
            mode="full",
            method="clobber",
            alwaysUseLatest=True,
            progress=False,
            shallow=True,
        ),
        steps.ShellCommand(
            name="configure kdevops",
            description="configuring",
            descriptionDone="configure",
            command=["make", f"defconfig-nfsd-{workflow}"],
            workdir="build/",
            haltOnFailure=True,
        ),
        steps.ShellCommand(
            name="prepare ansible",
            description="preparing",
            descriptionDone="prepare",
            command=["make"],
            workdir="build/",
            haltOnFailure=True,
        ),
        steps.ShellCommand(
            name="bring up test nodes",
            description="launching",
            descriptionDone="bring-up",
            command=["make", "bringup"],
            workdir="build/",
            haltOnFailure=True,
        ),
        steps.ShellCommand(
            name="build linux",
            description="building",
            descriptionDone="build",
            command=["make", "linux"],
            workdir="build/",
            timeout=None,
            haltOnFailure=True,
        ),
        steps.ShellCommand(
            name="build tests",
            description="building",
            descriptionDone="build",
            command=["make", workflow],
            workdir="build/",
            timeout=None,
            haltOnFailure=True,
        ),
        steps.ShellCommand(
            name="run tests",
            description="testing",
            descriptionDone="test",
            command=["make", f"{workflow}-baseline"],
            workdir="build/",
            timeout=5 * 3600,
            haltOnFailure=True,
        ),
        steps.ShellCommand(
            name="clean up",
            description="quiescing",
            descriptionDone="quiescing",
            command=["make", "destroy"],
            workdir="build/",
            alwaysRun=True,
        ),
    ]
    factory = util.BuildFactory(all_steps)
    factory.useProgress = False
    return factory


def kdevops_builder(branch, workflow, workerList):
    return util.BuilderConfig(
        name=f"{branch}-{workflow}",
        workernames=workerList,
        collapseRequests=True,
        tags=["nfsd", "kdevops", f"{branch}", f"{workflow}"],
        factory=kdevops_factory(branch, workflow),
    )


kdevopsSchedulerNames = [
    "fs-next",
    "fs-current",
    "nfsd-next",
    "nfsd-fixes",
    "nfsd-testing",
    "queue-6-9",
    "queue-6-6",
]

kdevopsLtsSchedulerNames = [
    "nfsd-6-9-y",
    "nfsd-6-6-y",
    "nfsd-6-1-y",
    "nfsd-5-15-y",
    "nfsd-5-10-y",
    "nfsd-5-4-y",
    "queue-6-1",
    "queue-5-15",
    "queue-5-10",
    "queue-5-4",
]

# Builders that build the test kernel on the control node
for sched_name in kdevopsSchedulerNames:
    c["builders"].append(
        kdevops_builder(
            sched_name,
            "fstests",
            [
                "kdevops-large",
            ],
        )
    )
    c["builders"].append(
        kdevops_builder(
            sched_name,
            "gitr",
            [
                "kdevops-large",
                "kdevops-small",
            ],
        )
    )
    c["builders"].append(
        kdevops_builder(
            sched_name,
            "ltp",
            [
                "kdevops-large",
                "kdevops-small",
            ],
        )
    )
    c["builders"].append(
        kdevops_builder(
            sched_name,
            "nfstest",
            [
                "kdevops-large",
                "kdevops-small",
            ],
        )
    )
    c["builders"].append(
        kdevops_builder(
            sched_name,
            "pynfs",
            [
                "kdevops-small",
                "kdevops-large",
            ],
        )
    )

# Builders that build the test kernel on the target nodes
for sched_name in kdevopsLtsSchedulerNames:
    c["builders"].append(
        kdevops_builder(
            sched_name,
            "fstests",
            [
                "kdevops-large",
            ],
        )
    )
    c["builders"].append(
        kdevops_builder(
            sched_name,
            "gitr",
            [
                "kdevops-large",
            ],
        )
    )
    c["builders"].append(
        kdevops_builder(
            sched_name,
            "ltp",
            [
                "kdevops-large",
            ],
        )
    )
    c["builders"].append(
        kdevops_builder(
            sched_name,
            "nfstest",
            [
                "kdevops-large",
            ],
        )
    )
    c["builders"].append(
        kdevops_builder(
            sched_name,
            "pynfs",
            [
                "kdevops-small",
            ],
        )
    )


kdevopsWorkflowNames = ["fstests", "gitr", "ltp", "nfstest", "pynfs"]


def kdevops_branch_scheduler(sched_name, watched_repo, watched_branch):
    c["schedulers"].append(
        schedulers.SingleBranchScheduler(
            name=f"branch-{sched_name}",
            change_filter=util.ChangeFilter(
                repository=watched_repo, branch=watched_branch
            ),
            treeStableTimer=300,
            builderNames=[
                f"{sched_name}-{workflow}" for workflow in kdevopsWorkflowNames
            ],
        )
    )


def kdevops_nightly_scheduler(sched_name, watched_repo, watched_branch, hour):
    c["schedulers"].append(
        schedulers.Nightly(
            name=f"nightly-{sched_name}",
            change_filter=util.ChangeFilter(
                repository=watched_repo, branch=watched_branch
            ),
            hour=hour,
            minute=31,
            builderNames=[
                f"{sched_name}-{workflow}" for workflow in kdevopsWorkflowNames
            ],
        )
    )


def kdevops_force_schedulers(sched_name):
    """Add one 'Force' scheduler"""
    for workflow in kdevopsWorkflowNames:
        c["schedulers"].append(
            schedulers.ForceScheduler(
                name=f"force-{sched_name}-{workflow}",
                builderNames=[f"{sched_name}-{workflow}"],
                buttonName=f"Start {sched_name}-{workflow}",
            )
        )


kdevops_nightly_scheduler(
    sched_name="fs-next",
    watched_repo="https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git",
    watched_branch="fs-next",
    hour=7,
)
kdevops_force_schedulers(sched_name="fs-next")

kdevops_nightly_scheduler(
    sched_name="fs-current",
    watched_repo="https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git",
    watched_branch="fs-current",
    hour=9,
)
kdevops_force_schedulers(sched_name="fs-current")

kdevops_force_schedulers(sched_name="nfsd-next")

kdevops_force_schedulers(sched_name="nfsd-fixes")

kdevops_force_schedulers(sched_name="nfsd-testing")

kdevops_force_schedulers(sched_name="nfsd-6-9-y")

kdevops_force_schedulers(sched_name="nfsd-6-6-y")

kdevops_force_schedulers(sched_name="nfsd-6-1-y")

kdevops_force_schedulers(sched_name="nfsd-5-15-y")

kdevops_force_schedulers(sched_name="nfsd-5-10-y")

kdevops_force_schedulers(sched_name="nfsd-5-4-y")

kdevops_nightly_scheduler(
    sched_name="queue-6-9",
    watched_repo="https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable-rc.git",
    watched_branch="queue/6.9",
    hour=19,
)
kdevops_force_schedulers(sched_name="queue-6-9")

kdevops_nightly_scheduler(
    sched_name="queue-6-6",
    watched_repo="https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable-rc.git",
    watched_branch="queue/6.6",
    hour=21,
)
kdevops_force_schedulers(sched_name="queue-6-6")

kdevops_nightly_scheduler(
    sched_name="queue-6-1",
    watched_repo="https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable-rc.git",
    watched_branch="queue/6.1",
    hour=23,
)
kdevops_force_schedulers(sched_name="queue-6-1")

kdevops_nightly_scheduler(
    sched_name="queue-5-15",
    watched_repo="https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable-rc.git",
    watched_branch="queue/5.15",
    hour=1,
)
kdevops_force_schedulers(sched_name="queue-5-15")

kdevops_nightly_scheduler(
    sched_name="queue-5-10",
    watched_repo="https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable-rc.git",
    watched_branch="queue/5.10",
    hour=3,
)
kdevops_force_schedulers(sched_name="queue-5-10")

kdevops_nightly_scheduler(
    sched_name="queue-5-4",
    watched_repo="https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable-rc.git",
    watched_branch="queue/5.4",
    hour=5,
)
kdevops_force_schedulers(sched_name="queue-5-4")
