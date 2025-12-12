class State:
    """
    Represents a reasoning module activation.
    """

    def __init__(self, module_name, content=None):
        self.module_name = module_name
        self.content = content

    def to_dict(self):
        return {
            "module": self.module_name,
            "content": self.content
        }
