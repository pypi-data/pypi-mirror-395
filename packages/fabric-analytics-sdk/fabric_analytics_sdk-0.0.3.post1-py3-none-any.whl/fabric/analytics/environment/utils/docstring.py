def inherit_docs(cls):
    for name, method in cls.__dict__.items():
        if method and not method.__doc__:
            for parent in cls.__bases__:
                if hasattr(parent, name):
                    method.__doc__ = getattr(parent, name).__doc__
    return cls
