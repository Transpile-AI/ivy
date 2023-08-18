# global
import os
import redis
from colorama import Fore
from hypothesis import settings, HealthCheck, Phase
from hypothesis.database import (
    MultiplexedDatabase,
    ReadOnlyDatabase,
    DirectoryBasedExampleDatabase,
)
from hypothesis.extra.redis import RedisExampleDatabase
from ivy_tests.test_ivy.helpers.pipeline_helper import (
    BackendHandler,
    BackendHandlerMode,
)


hypothesis_cache = os.getcwd() + "/.hypothesis/examples/"
redis_connect_dev = None
redis_connect_master = None
try:
    os.makedirs(hypothesis_cache)
except FileExistsError:
    pass


def is_db_available(master=False, credentials=None):
    global redis_connect_dev, redis_connect_master
    redis_connect_local = None
    if master:
        redis_connect_master = redis.Redis.from_url(
            url=credentials[0], password=credentials[1]
        )
        redis_connect_local = redis_connect_master
    else:
        redis_connect_dev = redis.Redis.from_url(
            url="redis://redis-17011.c259.us-central1-2.gce.cloud.redislabs.com:17011",
            username="general_use",
            password="Hypothesiscache@123",
            max_connections=2,
        )
        redis_connect_local = redis_connect_dev
    try:
        redis_connect_local.get("b")
    except redis.exceptions.ConnectionError:
        print("Fallback to DirectoryBasedExamples")
        return False
    return True


def pytest_terminal_summary(terminalreporter):
    session = terminalreporter._session

    if session.testscollected == 0:
        return

    passed_ratio = 1 - (session.testsfailed / session.testscollected)
    text = " {:.1%} of {} passed ".format(passed_ratio, session.testscollected)
    text = text.center(terminalreporter._screen_width, "=")
    terminalreporter.write(content=Fore.GREEN + text)


def pytest_addoption(parser):
    parser.addoption(
        "-N",
        "--num-examples",
        action="store",
        default=25,
        type=int,
        help="set max examples generated by Hypothesis",
    )
    parser.addoption(
        "--deadline",
        action="store",
        default=500000,
        type=int,
        help="set deadline for testing one example",
    )
    parser.addoption(
        "--ivy-tb",
        action="store",
        default="full",
        type=str,
        help="ivy traceback",
    )
    parser.addoption(
        "--reuse-only",
        default=False,
        action="store_true",
        help="Only reuse stored examples from database",
    )
    parser.addoption(
        "-R",
        "--robust",
        action="store_true",
        default=False,
        help=(
            "Disable Hypothesis Shrinking. Allow all Hypothesis HealthChecks."
            "Disabling the HealthChecks will most likely introduce new failures, "
            "this mode should be only used during development on the testing pipeline."
        ),
    )
    parser.addoption(
        "--set-backend",
        action="store_true",
        default=False,
        help="Force the testing pipeline to use ivy.set_backend for backend setting",
    )


def pytest_configure(config):
    profile_settings = {}
    getopt = config.getoption

    if getopt("--set-backend"):
        BackendHandler._update_context(BackendHandlerMode.SetBackend)

    max_examples = getopt("--num-examples")
    deadline = getopt("--deadline")
    if (
        os.getenv("REDIS_URL", default=False)
        and os.environ["REDIS_URL"]
        and is_db_available(
            master=True,
            credentials=(os.environ["REDIS_URL"], os.environ["REDIS_PASSWD"]),
        )
    ):
        print("Update Database with examples !")
        profile_settings["database"] = RedisExampleDatabase(
            redis_connect_master, key_prefix=b"hypothesis-example:"
        )

    elif not os.getenv("REDIS_URL") and is_db_available():
        print("Use Database in ReadOnly Mode with local caching !")
        shared = RedisExampleDatabase(
            redis_connect_dev, key_prefix=b"hypothesis-example:"
        )
        profile_settings["database"] = MultiplexedDatabase(
            DirectoryBasedExampleDatabase(path=hypothesis_cache),
            ReadOnlyDatabase(shared),
        )

    else:
        print("Database unavailable, local caching only !")
        profile_settings["database"] = DirectoryBasedExampleDatabase(
            path=hypothesis_cache
        )

    if max_examples:
        profile_settings["max_examples"] = max_examples
    if deadline:
        profile_settings["deadline"] = deadline

    if getopt("--reuse-only"):
        profile_settings["phases"] = [Phase.explicit, Phase.reuse]

    settings.register_profile(
        "ivy_profile",
        **profile_settings,
        suppress_health_check=(HealthCheck(3), HealthCheck(2), HealthCheck(1)),
        print_blob=True,
    )

    settings.register_profile(
        "robust",
        phases=[Phase.explicit, Phase.reuse, Phase.generate, Phase.target],
    )

    settings.register_profile(
        "diff",
        database=None,
        derandomize=True,
        max_examples=100,
        deadline=5000,
        phases=[Phase.generate],
        suppress_health_check=(HealthCheck(3), HealthCheck(2), HealthCheck(1)),
    )

    if getopt("robust"):
        settings.load_profile("robust")
    else:
        settings.load_profile("ivy_profile")
