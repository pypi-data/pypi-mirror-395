from contextlib import contextmanager
import os
from abc import ABC, abstractmethod
from typing import Callable

from aias_common.access.configuration import AnyStorageConfiguration, AccessType
from aias_common.access.file import File
from aias_common.access.logger import Logger

from aias_common.access.storages.path_helper import http_href_to_s3

LOGGER = Logger.logger


class AbstractStorage(ABC):
    cache_tt = 60 * 5
    cache_size = 2048
    DO_NOT_PROTECT_METHODS = ["get_authorized_pathes", "is_path_authorized", "get_configuration", "get_storage_parameters", "to_string", "supports", "get_full_href", "get_gdal_stream_options"]

    def __init__(self, storage_configuration: AnyStorageConfiguration):
        self.storage_configuration = storage_configuration

    def _check_read_write_wrapper(self, fct: Callable, index: int, action: AccessType):
        """Checks whether the action is permitted on the specified path before calling the function.

        Args:
            storage (AbstractStorage): Storage to use to check permissions
            attr (_type_): function to call
            index (int): index of the href in the function's parameters
            action (AccessType): Action to check permission for, on the specified path
        """
        def wrapper(*args, **kwargs):
            if len(kwargs) > 0:
                LOGGER.warning("Dangerous call: positional arguments only should be used on {}, found: {}".format(self.__class__.__name__, kwargs))
            href = args[index]
            if self.is_path_authorized(href, action):
                return fct(*args, **kwargs)
            LOGGER.error("{} on {} is not permitted on {}".format(action.value, self.to_string(), href))
            raise PermissionError("{} access on {} is not permitted on {}".format(action.value, href, self.to_string()))
        return wrapper

    def __getattribute__(self, name: str):
        """Intercepts calls to public methods to check read/write permissions before executing them.

        Args:
            name (str): Name of the method being called

        Raises:
            Exception: If a public method is not protected for read/write permission check

        Returns:
            _type_: The method being accessed
        """
        fct = object.__getattribute__(self, name)
        if callable(fct) and not name.startswith("_"):
            match name:
                case "get_matching_s3_objects" | "is_dir" | "is_file" | "exists" | "listdir" | "get_file_size" | "get_rasterio_session" | "get_last_modification_time" | "get_creation_time" | "dirname" | "gdal_transform_href_vsi" | "get_gdal_src" | "get_gdal_info" | "stream":
                    return self._check_read_write_wrapper(fct, 0, AccessType.READ)
                case "makedir" | "clean":
                    return self._check_read_write_wrapper(fct, 0, AccessType.WRITE)
                case "pull":
                    return self._check_read_write_wrapper(fct, 0, AccessType.READ)  # TODO need to solve circular import: and self._check_read_write_wrapper(AccessManager.get_local_storage(), attr, 1, AccessType.WRITE)
                case "push":
                    return self._check_read_write_wrapper(fct, 1, AccessType.WRITE)  # TODO need to solve circular import: and self._check_read_write_wrapper(AccessManager.get_local_storage(), attr, 0, AccessType.READ)
                case "async_push_file_obj":
                    return self._check_read_write_wrapper(fct, 1, AccessType.WRITE)  # TODO need to solve circular import: and self._check_read_write_wrapper(AccessManager.get_local_storage(), attr, 0, AccessType.READ)
                case _:
                    if name not in AbstractStorage.DO_NOT_PROTECT_METHODS:
                        raise Exception("Invalid implementation {} of AbstractStorage: method {} is public and not protected for READ/WRITE permission check.".format(self.__class__.__name__, name))
        return fct

    def get_authorized_pathes(self, href: str, action: AccessType) -> list[str]:
        """ Returns the list of authorized pathes for the specified action, if the href is supported by the storage.

        Args:
            href (str): Href of the resource to consult
            action (AccessType): Action to check permission for, on the specified path

        Raises:
            PermissionError: If the href is not supported by the storage

        Returns:
            list[str]: The list of authorized pathes for the specified action
        """
        if action == AccessType.WRITE:
            return self.get_configuration().writable_paths
        else:
            return list([*self.get_configuration().readable_paths, *self.get_configuration().writable_paths])

    @abstractmethod
    def to_string(self) -> str:
        """Returns the storage to_string description

        Returns:
            str: a description that can be displayed
        """
        ...

    @abstractmethod
    def get_configuration(self) -> AnyStorageConfiguration:
        """Returns the storage configuration

        Returns:
            AnyStorageConfiguration: storage configuration
        """
        ...

    @abstractmethod
    def get_storage_parameters(self) -> dict:
        """Based on the type of storage and its characteristics, gives storage-specific parameters to use to access data
        """
        ...

    @abstractmethod
    def is_path_authorized(self, href: str, action: AccessType) -> bool:
        """Check whether a given action is permitted on the specified path.

        Args:
            href (str): Href of the file to consult
            action (AccessType): Action to check permission for, on the specified path

        Returns:
            bool: True if the action is authorized, False otherwise
        """

    @abstractmethod
    def supports(self, href: str) -> bool:
        """Return whether the provided href can be handled by the storage.

        Args:
            href (str): Href of the file to consult

        Returns:
            bool: True if the storage can handle href, False otherwise
        """
        ...

    @abstractmethod
    def exists(self, href: str) -> bool:
        """Return whether the file given exists in the storage

        Args:
            href (str): Href of the file to consult

        Returns:
            bool: True if the file exists, False otherwise
        """
        ...

    @abstractmethod
    def get_rasterio_session(self, href: str) -> dict:
        """Return a rasterio Session and potential variables to access data remotely

        Args:
            href (str): Href od the file to stream

        Returns:
            dict
        """
        ...

    @abstractmethod
    def pull(self, href: str, dst: str):
        """Copy/Download the desired file from the file system to write it locally

        Args:
            href (str): File to fetch
            dst (str): Destination of the file
        """
        ...

    @abstractmethod
    def push(self, href: str, dst: str, content_type: str | None = None):
        """Copy/upload the desired file from local to write it on the file system

        Args:
            href (str): File to upload
            dst (str): Destination of the file
        """
        ...

    @abstractmethod
    def is_file(self, href: str) -> bool:
        """Returns whether the specified href is a file

        Args:
            href(str): The href to test

        Returns:
            bool: Whether the input is a file
        """
        ...

    @abstractmethod
    def is_dir(self, href: str) -> bool:
        """Returns whether the specified href is a directory

        Args:
            href(str): The href to test

        Returns:
            bool: Whether the input is a directory
        """
        ...

    @abstractmethod
    def get_file_size(self, href: str) -> int | None:
        """Returns the size of the specified href

        Args:
            href(str): The href to examine
        """
        ...

    @abstractmethod
    def listdir(self, href: str) -> list[File]:
        """Returns the list of files and folders in the specified directory

        Args:
            href(str): The directory to examine
        """
        ...

    @abstractmethod
    def get_last_modification_time(self, href: str) -> float | None:
        """Returns the last modification time of the specified href

        Args:
            href(str): The href to examine

        Returns:
            float: the timestamp in seconds of last modification time
        """
        ...

    @abstractmethod
    def get_creation_time(self, href: str) -> float | None:
        """Returns the creation time of the specified href

        Args:
            href(str): The href to examine

        Returns:
            float: the timestamp in seconds of creation time
        """
        ...

    @abstractmethod
    def makedir(self, href: str, strict=False):
        """Create if needed (and possible) the specified dir

        Args:
            href(str): The href to the dir to create
            strict(bool): Whether to force the creation
        """
        ...

    def dirname(self, href: str):
        """Return the name of the directory containing the specified href

        Args:
            href(str): The href to examine
        """
        return os.path.dirname(href)

    @abstractmethod
    def clean(self, href: str):
        """If authorized, remove the given file

        Args:
            href(str): The href to delete
        """
        ...

    @abstractmethod
    def get_gdal_stream_options(self) -> dict:
        """Return the options to use to stream a GDAL file through its virtual file systems
        """
        ...

    @abstractmethod
    def gdal_transform_href_vsi(self, href: str) -> str:
        """Transform the archive's href into a format manageable by GDAL's virtual file systems

        Args:
            href(str): The href to examine
        """
        ...

    def get_gdal_src(self, href: str):
        """Return the archive's dataset through GDAL's virtual file systems

        Args:
            href(str): The href to examine
        """
        from osgeo import gdal
        from osgeo.gdalconst import GA_ReadOnly

        with gdal.config_options(self.get_gdal_stream_options()):
            src_ds = gdal.Open(self.gdal_transform_href_vsi(href), GA_ReadOnly)
        return src_ds

    def get_gdal_info(self, href: str, gdal_options):
        """Return the archive's info through GDAL's virtual file systems

        Args:
            href(str): The href to examine
        """
        from osgeo import gdal

        with gdal.config_options(self.get_gdal_stream_options()):
            return gdal.Info(self.gdal_transform_href_vsi(href), options=gdal_options)

    @contextmanager
    def stream(self, href: str):
        import smart_open
        params = self.get_storage_parameters()
        if self.get_configuration().type.lower() == "s3":
            href = http_href_to_s3(href)
        with smart_open.open(href, "rb", transport_params=params) as f:
            yield f
