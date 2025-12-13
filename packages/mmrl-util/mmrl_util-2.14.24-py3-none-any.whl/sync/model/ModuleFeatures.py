from .AttrDict import AttrDict

class ModuleFeatures(AttrDict):
    service: bool
    post_fs_data: bool
    # system.prop
    resetprop: bool
    sepolicy: bool
    zygisk: bool
    apks: bool
    
    # KernelSU
    webroot: bool
    post_mount: bool
    boot_completed: bool
    
    # MMRL
    webui_plugins: bool
    
    @classmethod
    def expected_fields(cls, __type=True):
        if __type:
            return cls.__annotations__

        return {k: v.__name__ for k, v in cls.__annotations__.items()}