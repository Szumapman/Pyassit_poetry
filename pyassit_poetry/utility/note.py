from datetime import datetime

from utility.title import Title
from utility.content import Content


class Note:
    """class for note object"""

    def __init__(self, title: Title, content: Content, tags: set):
        self._title = title
        self._content = content
        self.__create_time = datetime.now()
        self.__modified_time = None
        self._tags = tags

    def __repr__(self):
        creation_time_str = self.__create_time.strftime("%Y-%m-%d %H:%M:%S")
        modified_time_str = (
            f'Last Modified Time: {self.__modified_time.strftime("%Y-%m-%d %H:%M:%S")}\n'
            if self.__modified_time
            else ""
        )
        tags_str = ", ".join(self._tags) if self._tags else "note has no tag"
        return (
            f"Title: {self.title}\n"
            f"Content: {self.content}\n"
            f"Creation Time: {creation_time_str}\n"
            f"{modified_time_str}"
            f"Tags: {tags_str}"
        )

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title: Title):
        self._title = title
        self.__modified_time = datetime.now()

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content: Content):
        self._content = content
        self.__modified_time = datetime.now()

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, tags):
        return self._tags

    def add_tag(self, tag):
        self._tags.add(tag)
        self.__modified_time = datetime.now()

    def delete_tag(self, tag):
        self._tags.discard(tag)
        self.__modified_time = datetime.now()
