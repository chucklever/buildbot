# -*- python -*-
# ex: set filetype=python:

c["projects"].append(
    util.Project(name="rds-tcp", slug="Port UEK's RDS-TCP to upstream Linux")
)

c["workers"].append(
    worker.LocalWorker("rds"),
)

rdsBuilderSteps = [
    steps.Git(
        name="clone rds-coverage",
        description="cloning",
        descriptionDone="clone",
        repourl="https://github.com/allisonhenderson/rds_work.git",
        branch="rds-coverage",
        mode="full",
        method="clobber",
        alwaysUseLatest=True,
        progress=False,
        shallow=True,
    ),
    steps.ShellCommand(
        name="configure kernel",
        description="configuring",
        descriptionDone="configure",
        command=["tools/testing/selftests/net/rds/config.sh"],
        workdir="build/",
        haltOnFailure=True,
    ),
    steps.ShellCommand(
        name="build kernel",
        description="building",
        descriptionDone="build",
        command=["make", "-s", "-j8"],
        workdir="build/",
        haltOnFailure=True,
    ),
    steps.ShellCommand(
        name="run tests",
        description="testing",
        descriptionDone="test",
        command=["tools/testing/selftests/net/rds/run.sh"],
        workdir="build/",
        haltOnFailure=True,
    ),
]

c["builders"].append(
    util.BuilderConfig(
        name="rdsBuilder",
        workernames=["rds"],
        tags=["rds"],
        factory=util.BuildFactory(rdsBuilderSteps),
    )
)

c["change_source"].append(
    changes.GitPoller(
        repourl="https://github.com/allisonhenderson/rds_work.git",
        branches=["rds-coverage"],
        pollInterval=7200,
        pollRandomDelayMin=30,
        pollRandomDelayMax=300,
        workdir="/usr/local/home/buildmaster/basedir/GitPoller/rds/",
    )
)

c["schedulers"].append(
    schedulers.SingleBranchScheduler(
        name="branch-rds-coverage",
        change_filter=util.ChangeFilter(
            repository="https://github.com/allisonhenderson/rds_work.git",
            branch="rds-coverage",
        ),
        treeStableTimer=300,
        builderNames=["rdsBuilder"],
    )
)
c["schedulers"].append(
    schedulers.ForceScheduler(
        name="force-rds-coverage",
        builderNames=["rdsBuilder"],
        buttonName="Start rds-coverage",
    )
)
