
from logging import Logger

from src.dependencymanager import DependencyManager


# should create the logger
def test_should_create_logger():
  assert isinstance (DependencyManager().logger, Logger)


