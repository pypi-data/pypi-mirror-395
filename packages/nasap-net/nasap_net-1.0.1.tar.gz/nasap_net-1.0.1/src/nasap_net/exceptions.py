class NasapNetError(Exception):
    pass


class IDNotSetError(NasapNetError):
    pass


class DuplicateIDError(NasapNetError):
    pass
