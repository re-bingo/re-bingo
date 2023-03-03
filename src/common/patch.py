from tortoise import Model


def auto_get_item_fields(cls: type):
    def __init__(self, item: Model):
        self.item = item

    def __getattr__(self, field):
        if "__" not in field:
            return getattr(self.item, field)
        raise AttributeError

    cls.__init__ = __init__
    cls.__getattr__ = __getattr__

    return cls
