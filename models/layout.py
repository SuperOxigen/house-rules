class Footer(object):
    def __init__(self):
        pass

    def copy(self):
        return Footer()

    def dictify(self) -> dict:
        return {}

class Header(object):
    def __init__(self):
        self._links = list()

    def copy(self):
        newHeader = Header()
        for link in self.links:
            newHeader.links.append(link.copy())

        return newHeader

    @property
    def links(self) -> list:
        return self._links

    def dictify(self) -> dict:
        return {
            "links": self.links
        }

class Link(object):
    def __init__(self, uri: str, name: str, active: bool=False):
        self._uri = uri
        self._name = name
        self._active = active

    def copy(self):
        return Link(uri=self.uri,
                    name=self.name)

    @property
    def uri(self) -> str:
        return self._uri

    @property
    def name(self) -> str:
        return self._name

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool):
        self._active = bool(value)
