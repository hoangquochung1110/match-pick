from lxml import html


class Component:
    def __init__(self, doc, path) -> None:
        self.doc = doc
        self.component: html.HtmlElement = doc.find_class(path)[0]
