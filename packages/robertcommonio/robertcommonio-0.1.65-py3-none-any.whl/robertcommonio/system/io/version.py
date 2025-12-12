from typing import Union, Optional


class Version:

    def __init__(self):
        self.versions = {}

    def add_version(self, version: str, content: Union[str, list]):
        if version not in self.versions.keys():
            self.versions[version] = []

        if isinstance(content, str):
            self.versions[version].append(content)
        elif isinstance(content, list):
            self.versions[version].extend(content)

    def get_version(self, version: Optional[str] = None) -> list:
        if version is None:
            version = sorted(list(self.versions.keys()))[-1]
        return self.versions.get(version, [])

    def get_versions(self):
        return self.versions
