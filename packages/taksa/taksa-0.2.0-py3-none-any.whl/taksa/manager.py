from .dependency import Dependency
from .configuration import BuildType

class DependecyManager:
    def __init__(self):
        self._dependencies = []
    
    def download_all(self):
        for d in self._dependencies:
            d.download()

    def make_all(self, build_type: BuildType):
        for d in self._dependencies:
            d.make(build_type)

    def add_dependency(self, dependency):
        self._dependencies.append(dependency)
        return self
