from .AttrDict import AttrDict

class ModuleManagerSolution(AttrDict):
    min: int
    devices: list[str]
    arch: list[str]
    require: list[str]
    
    @classmethod
    def expected_fields(cls, __type=True):
        if __type:
            return cls.__annotations__

        return {k: v.__name__ for k, v in cls.__annotations__.items() if v is not None and v is not False}

class ModuleManager(AttrDict):
    magisk: ModuleManagerSolution
    kernelsu: ModuleManagerSolution
    ksunext: ModuleManagerSolution
    apatch: ModuleManagerSolution
    
    @classmethod
    def expected_fields(cls, __type=True):
        if __type:
            return cls.__annotations__

        return {k: v.__name__ for k, v in cls.__annotations__.items() if v is not None and v is not False}
    