class OBJ:
    def __init__(self, _internal=False):
        if not _internal:
            raise RuntimeError("Use OBJ.create(...) to instantiate this class.")
        self.width_mm = None
        self.height_mm = None

    @classmethod
    def create(cls, width, height):
        obj = cls(_internal=True)
        obj.width_mm = width
        obj.height_mm = height
        return obj

    def image(self):
        pass
