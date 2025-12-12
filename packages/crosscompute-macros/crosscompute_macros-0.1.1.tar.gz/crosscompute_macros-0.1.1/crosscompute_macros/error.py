from .log import redact_path


class MacroError(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.__dict__.update(kwargs)

    def __str__(self):
        texts = [super().__str__()]
        if hasattr(self, 'path'):
            texts.append(f'path="{redact_path(self.path)}"')
        return '; '.join(texts)


class DiskError(MacroError):
    pass


class PackageError(MacroError):
    pass


class SecurityError(MacroError):
    pass


class WebError(MacroError):
    pass


class WebConnectionError(WebError):
    pass


class WebRequestError(WebError):
    pass


class ParsingError(MacroError):
    pass


class FormattingError(MacroError):
    pass
