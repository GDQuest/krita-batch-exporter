import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Dependencies')))
from .GDquestArtTools import registerDocker  # noqa

registerDocker()

