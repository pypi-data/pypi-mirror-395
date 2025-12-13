from .AttrDict import AttrDict

class RootSolutions(AttrDict):
    magisk: str
    kernelsu: str
    apatch: str
    
    @classmethod
    def expected_fields(cls, __type=True):
        if __type:
            return cls.__annotations__

        return {k: v.__name__ for k, v in cls.__annotations__.items()}