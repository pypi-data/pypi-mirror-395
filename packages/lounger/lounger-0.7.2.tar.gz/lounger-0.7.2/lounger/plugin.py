from datetime import datetime, timezone
from io import StringIO
from typing import Any

import pytest
from pytest_req.log import log_cfg

from lounger.pytest_extend import screenshot_base64

LOG_STREAM = StringIO()

html_title = "Lounger Test Report"


@pytest.fixture(scope="session", autouse=True)
def setup_log():
    """
    setup log
    """
    # setting log format
    log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</> |<level> {level} | {message}</level>"
    log_cfg.set_level(format=log_format)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    global html_title
    # Here we fetch the command-line argument using config object
    title = config.getoption("--html-title")
    if title:
        html_title = title
    # add env markers
    config.addinivalue_line(
        "markers", "env(name): mark test to run only on named environment"
    )


def pytest_runtest_setup(item: Any) -> None:
    """
    Called to perform the setup phase for a test item.
    """
    env_names = [mark.args[0] for mark in item.iter_markers(name="env")]
    if env_names:
        if item.config.getoption("--env") not in env_names:
            pytest.skip(f"test requires env in {env_names}")


def pytest_xhtml_report_title(report):
    """
    Configures the pytest-xhtml report title based on command-line options.
    :param report:
    :return:
    """
    global html_title
    report.title = html_title


def pytest_xhtml_results_table_header(cells):
    cells.insert(2, "<th>Description</th>")
    cells.insert(3, '<th class="sortable time" data-column-type="time">Time</th>')


def pytest_xhtml_results_table_row(report, cells):
    if hasattr(report, "description"):
        cells.insert(2, f"<td>{report.description}</td>")
    else:
        cells.insert(2, "<td>No description</td>")
    cells.insert(3, f'<td class="col-time">{datetime.now(timezone.utc)}</td>')


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    pytest_html = item.config.pluginmanager.getplugin('html')
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    extra = getattr(report, 'extra', [])
    if report.when == 'call':
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            page = item.funcargs.get('page')
            if page is not None:
                # add screenshot to HTML report.
                image = screenshot_base64(page)
                if pytest_html:
                    extra.append(pytest_html.extras.image(image, mime_type='image/png'))

        # Empty memory stream
        LOG_STREAM.truncate(0)
        LOG_STREAM.seek(0)

    report.extras = extra


def pytest_addoption(parser: Any) -> None:
    """
    Add pytest option
    """
    group = parser.getgroup("lounger", "Lounger")
    group.addoption(
        "--html-title",
        action="store",
        default=[],
        help="Specifies the title of the pytest-xhtml test report",
    ),
    group.addoption(
        "--env",
        action="store",
        default=[],
        help="only run tests matching the environment {name}.",
    )
