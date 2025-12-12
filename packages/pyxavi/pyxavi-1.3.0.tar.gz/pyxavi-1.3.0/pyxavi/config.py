from pyxavi import Dictionary, Storage
import os


class Config(Storage):
    """Class to handle a config file

    It inherits from the Storage class but denying all
    writes. It is a read-only class.

    :Authors:
        Xavier Arnaus <xavi@arnaus.net>

    """

    _avoid_load_data_from_file: bool = False

    def __init__(self, filename: str = None, params: dict = None) -> None:

        if filename is None and params is None:
            raise RuntimeError("Both [filename] and [params] parameters can't be None")

        # If we receive a filename we let the Storage class load the parameters
        if filename is not None:
            self._avoid_load_data_from_file = False
        else:
            self._avoid_load_data_from_file = True
            filename = "FAKE.yaml"

        # Now we're ready to initialise by the parent class.
        #   read_file() will be called!
        super().__init__(filename=filename)

        # If we receive a dict with params we merge it over whatever we have already load
        if params is not None:
            # pre-initialise the content in case it's None
            self.merge_from_dict(parameters=params)

    def read_file(self) -> None:
        if self._avoid_load_data_from_file:
            self._content = {}
            return

        if os.path.exists(self._filename):
            self._content = super()._load_file_contents(self._filename)
        else:
            raise RuntimeError(f"Config file [{self._filename}] not found")

    def merge_from_dict(self, parameters: dict) -> None:
        self.merge(Dictionary(parameters))

    def merge_from_file(self, filename: str) -> None:
        if os.path.exists(filename):
            self.merge_from_dict(parameters=super()._load_file_contents(filename))
        else:
            raise RuntimeError(f"Config file [{filename}] not found")

    def write_file(self) -> None:
        raise RuntimeError("Config class does not allow writting")

    def set(self, param_name: str, value: any = None, dictionary=None):
        raise RuntimeError("Config class does not allow writting")

    def set_hashed(self, param_name: str, value: any = None):
        raise RuntimeError("Config class does not allow writting")
