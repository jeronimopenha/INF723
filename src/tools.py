from mailbox import NotEmptyError


class Tool:
    def __init__(self, name: str, publication: str, link: str, year: int, citations: int, qualis: str, impact: int):
        self.name = name
        self.publication = publication
        self.link = link
        self.year = year
        self.citations = citations
        self.qualis = qualis
        self.impact = impact
