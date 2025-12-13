import os
from typing import Optional

import pytest
from greener_reporter import Reporter, TestcaseStatus

REPORTER_PLUGIN_NAME = "greener_reporter"


def pytest_addoption(parser):
    group = parser.getgroup("greener", "Greener Reporter options")
    group.addoption(
        "--greener",
        dest="greener",
        action="store_true",
        help="Enable Greener Reporter",
    )


def pytest_configure(config):
    if not config.getoption("greener"):
        return

    reporter = GreenerReporter()
    config.pluginmanager.register(reporter, REPORTER_PLUGIN_NAME)


def pytest_unconfigure(config):
    if not config.pluginmanager.hasplugin(REPORTER_PLUGIN_NAME):
        return

    reporter = config.pluginmanager.getplugin(REPORTER_PLUGIN_NAME)
    reporter.stop()


class ReportOutcome:
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class ReportWhen:
    SETUP = "setup"
    CALL = "call"
    TEARDOWN = "teardown"


class GreenerReporter:
    def __init__(self) -> None:
        ingress_endpoint = os.environ.get("GREENER_INGRESS_ENDPOINT")
        if ingress_endpoint is None:
            raise ValueError("GREENER_INGRESS_ENDPOINT is not set")
        
        ingress_api_key = os.environ.get("GREENER_INGRESS_API_KEY")
        if ingress_api_key is None:
            raise ValueError("GREENER_INGRESS_API_KEY is not set")

        self.reporter = Reporter(ingress_endpoint, ingress_api_key)

        self._session_id = None
        self._testsuite = None

    def stop(self) -> None:
        self.reporter.shutdown()

    @pytest.hookimpl(tryfirst=True)
    def pytest_configure(self, config):
        self._testsuite = config.getini("junit_suite_name")

    @pytest.hookimpl(wrapper=True)
    def pytest_sessionstart(self, session):
        session_id = os.environ.get("GREENER_SESSION_ID")
        description = os.environ.get("GREENER_SESSION_DESCRIPTION")
        baggage = os.environ.get("GREENER_SESSION_BAGGAGE")
        labels = os.environ.get("GREENER_SESSION_LABELS")

        greener_session = self.reporter.create_session(
            session_id,
            description,
            baggage,
            labels,
        )

        self._session_id = greener_session.id
        yield

    @pytest.hookimpl(wrapper=True)
    def pytest_runtest_logreport(self, report):
        status = None
        if report.outcome == ReportOutcome.FAILED and report.when == ReportWhen.SETUP:
            status = TestcaseStatus.ERR
        elif (
                report.outcome == ReportOutcome.SKIPPED and report.when == ReportWhen.SETUP
        ) or report.when == ReportWhen.CALL:
            status = {
                ReportOutcome.PASSED: TestcaseStatus.PASS,
                ReportOutcome.FAILED: TestcaseStatus.FAIL,
                ReportOutcome.SKIPPED: TestcaseStatus.SKIP,
            }[report.outcome]

        if status:
            tc_file, tc_classname, tc_name = _parse_nodeid(report.nodeid)
            self.reporter.create_testcase(
                self._session_id,
                tc_name,
                tc_classname,
                tc_file,
                self._testsuite,
                status,
                report.longreprtext,
                None,
            )

        yield


def _parse_nodeid(address: str) -> tuple[str, Optional[str], str]:
    path, possible_open_bracket, params = address.partition("[")
    names = path.split("::")

    tc_file = names[0]
    tc_classname = '.'.join(names[1:-1]) if names[1:-1] else None
    tc_name = names[-1] + possible_open_bracket + params

    return tc_file, tc_classname, tc_name
