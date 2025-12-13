class ModelKind:
    def __init__(self, kind: str):
        self.kind = kind


class Inferable(ModelKind):
    def __init__(self):
        super().__init__("all")


class Trainable(ModelKind):
    def __init__(self):
        super().__init__("trainable")
