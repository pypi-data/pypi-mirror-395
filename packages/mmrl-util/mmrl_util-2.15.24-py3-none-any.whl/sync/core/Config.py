import os
import magic

from pathlib import Path

from ..error import ConfigError
from ..model import ConfigJson, JsonIO
from ..utils import Log, StrUtils


class Config(ConfigJson):
    def __init__(self, root_folder):
        self._log = Log("Config", enable_log=True)
        self._root_folder = root_folder
        self._mime = magic.Magic(mime=True)

        json_file = self.json_folder.joinpath(ConfigJson.filename())
        if not json_file.exists():
            raise FileNotFoundError(json_file.as_posix())

        obj = JsonIO.load(json_file)
        super().__init__(obj)

        self._check_values()

        self._log = Log("Config", enable_log=self.enable_log, log_dir=self.log_dir)
        for key in ConfigJson.expected_fields().keys():
            self._log.d(f"{key} = {self.get(key)}")

    def _check_values(self):
        default = self.default()

        name = self.get("name", default.name)
        if name == default.name:
            self._log.w("_check_values: 'name' is undefined")

        base_url = self.get("base_url", default.base_url)
        if base_url == default.base_url:
            raise ConfigError("'base_url' is undefined")
        elif not StrUtils.is_with(base_url, "https", "/"):
            raise ConfigError("'base_url' must start with 'https' and end with '/'")

        max_num = self.get("max_num", default.max_num)
        enable_log = self.get("enable_log", default.enable_log)

        repoId = StrUtils.extract_parts(base_url)
        website = self.get("website", default.website)
        support = self.get("support", default.support)
        donate = self.get("donate", default.donate)
        submission = self.get("submission", default.submission)
        description = self.get("description", default.description)

        log_dir = self.get("log_dir", default.log_dir)
        if log_dir != default.log_dir:
            log_dir = Path(log_dir)

            if not log_dir.is_absolute():
                log_dir = self._root_folder.joinpath(log_dir)

        self.update(
            id=repoId,
            name=name,
            website=website,
            support=support,
            donate=donate,
            submission=submission,
            description=description,
            cover=self.get_cover,
            base_url=base_url,
            max_num=max_num,
            enable_log=enable_log,
            log_dir=log_dir
        )


    @property
    def get_cover(self):
        cover_file = self.assets_folder.joinpath("cover.webp")
        cover = None

        if cover_file.exists() and cover_file.suffix.lower() == '.webp':
            cover_mime_type = self._mime.from_file(cover_file)

            if cover_mime_type.lower() == 'image/webp':
                cover = f"{self.base_url}assets/cover.webp"
            else:
                self._log.warning(f"get_cover: '{cover_file.name}' is not a valid WebP image.")
        else:
            self._log.info(f"get_cover: '{cover_file.name}' does not exist or is not a WebP file.")

        return cover

    @property
    def json_folder(self):
        return self.get_json_folder(self._root_folder)

    @property
    def assets_folder(self):
        return self.get_assets_folder(self._root_folder)

    @property
    def modules_folder(self):
        return self.get_modules_folder(self._root_folder)

    @property
    def local_folder(self):
        return self.get_local_folder(self._root_folder)

    @classmethod
    def get_json_folder(cls, root_folder):
        return root_folder.joinpath("json")

    @classmethod
    def get_assets_folder(cls, root_folder):
        return root_folder.joinpath("assets")

    @classmethod
    def get_modules_folder(cls, root_folder):
        return root_folder.joinpath("modules")

    @classmethod
    def get_local_folder(cls, root_folder):
        return root_folder.joinpath("local")
