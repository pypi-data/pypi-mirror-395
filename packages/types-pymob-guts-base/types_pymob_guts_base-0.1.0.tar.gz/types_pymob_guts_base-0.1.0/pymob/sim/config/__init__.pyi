# This stub file expands Pymob's config class with a section guts_base defined
# in the config module of this case study. 
# Note that the stub of pymob.sim.config.base is NOT changed. init import and submodule
# import CANT be changed at the same time. It simply does not work.
# This is however a nice solution. The inline definitions are done in 
# the pymob.sim.config.base.py file which should NOT be used for importing in the case study
# This way, the exposed Config file via the __init__.py can be updated with additional
# type hints
# in pymob.simulation.py it is ensured that also the Config is used from __init__ 

from pymob.sim.config.casestudy_registry import *
from pymob.sim.config.sections import *
from pymob.sim.config.parameters import *
from pymob.sim.config.base import * # type: ignore

# reimport under a different name, so it can be used for subclassing
from pymob.sim.config.base import Config as ConfigBase
from guts_base.sim.config import GutsBaseConfig


class Config(ConfigBase):
    guts_base: GutsBaseConfig = ...

