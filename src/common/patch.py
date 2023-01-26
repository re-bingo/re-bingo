from tortoise import Model


def auto_get_item_fields(cls: type):
    def __init__(self, item: Model):
        self.item = item

    cls.__init__ = __init__
    cls.__getattr__ = lambda self, field: getattr(self.item, field)

    return cls
