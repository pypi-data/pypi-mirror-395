from lounger import __version__
from lounger.log import log

logo = rf"""
    __                                 
   / /___  __  ______  ____ ____  _____
  / / __ \/ / / / __ \/ __ `/ _ \/ ___/
 / / /_/ / /_/ / / / / /_/ /  __/ /    
/_/\____/\__,_/_/ /_/\__, /\___/_/     
                    /____/             V{__version__}
"""


def pytest_configure(config):
    log.info(logo)


def pytest_xhtml_report_title(report):
    report.title = "Lounger Test Report"
