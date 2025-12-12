"""Library exceptions"""


class MissingOptionalDependencyError(ImportError):
    """An optional library is missing in env"""

    def __init__(self, package_name: str) -> None:
        super().__init__(f"Missing dependency {package_name}.", name=package_name)
