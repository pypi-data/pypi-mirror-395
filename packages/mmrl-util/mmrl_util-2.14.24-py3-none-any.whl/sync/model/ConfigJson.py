import re, os

from .AttrDict import AttrDict
from .JsonIO import JsonIO


class ConfigJson(AttrDict, JsonIO):
    name: str
    base_url: str
    max_num: int
    enable_log: bool
    log_dir: str

    def write(self, file):
        new = AttrDict()
        for key in self.expected_fields().keys():
            value = self.get(key)
            if value is not None:
                new[key] = value

        JsonIO.write(new, file)

    @classmethod
    def load(cls, file):
        obj = JsonIO.load(file)
        return ConfigJson(obj)

    @classmethod
    def default(cls):
        return ConfigJson(
            name="Unknown",
            base_url="",
            max_num=3,
            enable_log=True,
            log_dir=None
        )

    @classmethod
    def filename(cls, json_folder=None):
        return "config.json"
        # pattern = r"^config\.(json|y(a)?ml)$"
        # files = os.listdir(json_folder)
        # for file in files:
        #     if re.match(pattern, file):
        #         return file
        # raise FileNotFoundError("No matching file found in the folder. Supported file types are config.json, config.yml or config.yaml")

    @classmethod
    def expected_fields(cls, __type=True):
        if __type:
            return cls.__annotations__

        return {k: v.__name__ for k, v in cls.__annotations__.items()}
