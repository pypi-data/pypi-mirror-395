class TestAopClass:
    def __init__(self, v):
        self.v = v
        pass

    def cls_func_to_wrap(self):
        return self.v
