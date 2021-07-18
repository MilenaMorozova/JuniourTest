class PageTagsException(Exception):
    def __init__(self, status_code):
        self.status_code = status_code


class IncorrectUrlException(PageTagsException):
    def __init__(self):
        super().__init__(400)


class UnableToParseException(PageTagsException):
    def __init__(self):
        super().__init__(409)


class PageDoesNotExistException(PageTagsException):
    def __init__(self):
        super().__init__(404)
