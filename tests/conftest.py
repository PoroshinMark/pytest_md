import os
import sys

# add project root so pytest_md package can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

pytest_plugins = ["pytest_md"]