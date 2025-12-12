import os
import shutil
from contextlib import contextmanager
from typing import Annotated, Union
from urllib.parse import urlparse

from pydantic import Field

from aias_common.access.configuration import AccessManagerSettings
from aias_common.access.file import File
from aias_common.access.logger import Logger
from aias_common.access.storages.file import AccessType, FileStorage
from aias_common.access.storages.gs import GoogleStorage
from aias_common.access.storages.http import HttpStorage
from aias_common.access.storages.https import HttpsStorage
from aias_common.access.storages.s3 import S3Storage

AnyStorage = Annotated[Union[FileStorage, GoogleStorage, HttpStorage, HttpsStorage, S3Storage], Field(discriminator="type")]

LOGGER = Logger.logger


class AccessManager:
    storages: list[AnyStorage]
    tmp_dir: str
    cache_ttl: int = 60 * 60 * 24
    cache_size = 1024

    @staticmethod
    def init(ams: AccessManagerSettings):
        LOGGER.info("Initializing storages Access Manager")
        AccessManager.storages = []
        for s in ams.storages:
            match s.type:
                case "file":
                    AccessManager.storages.append(FileStorage(s))
                case "gs":
                    AccessManager.storages.append(GoogleStorage(s))
                case "http":
                    AccessManager.storages.append(HttpStorage(s))
                case "https":
                    AccessManager.storages.append(HttpsStorage(s))
                case "s3":
                    AccessManager.storages.append(S3Storage(s))
                case _:
                    raise NotImplementedError(f"Specified storage {s.storage_configuration.type} is not implemented")

        tmp_dir = ams.tmp_dir
        is_tmp_dir_authorized = any(
            map(lambda s: s.is_path_authorized(tmp_dir, AccessType.WRITE),
                filter(lambda s: s.storage_configuration.type == "file", AccessManager.storages)))
        if not is_tmp_dir_authorized:
            raise PermissionError("The given tmp_dir is not part of any defined FileStorage with WRITE authorization")

        AccessManager.tmp_dir = tmp_dir

    @staticmethod
    def resolve_storage(href: str) -> AnyStorage:
        """
        Based on the defined storages, returns the one matching the input href
        """

        for s in AccessManager.storages:
            try:
                if s.supports(href):
                    return s
            except Exception:
                ...
        raise PermissionError(f"Storage for {href} is not configured")

    @staticmethod
    def get_local_storage() -> FileStorage:
        """
        Based on the defined storages, returns the one that is a file storage
        """

        for s in AccessManager.storages:
            if s.get_configuration().is_local:
                return s
        raise Exception("No local storage configured")

    @staticmethod
    def get_storage_parameters(href: str) -> dict:
        storage = AccessManager.resolve_storage(href)

        return storage.get_storage_parameters()

    @staticmethod
    def check_path_writable(href: str):
        """
        Checks that the path is a writable path for at least one of the file storages
        """
        if not AccessManager.resolve_storage(href=href).is_path_authorized(href, AccessType.WRITE):
            raise PermissionError(f"Path '{href}' is not writable")

    @staticmethod
    def check_path_readable(href: str):
        """
        Checks that the path is a readable path for at least one of the file storages
        """
        if not AccessManager.resolve_storage(href=href).is_path_authorized(href, AccessType.READ):
            raise PermissionError(f"Path '{href}' is not readable")

    @staticmethod
    def push(href: str, dst: str):
        """
        Push a file from a local storage to write it in a storage.
        If the destination storage is local, then it is a copy. Otherwise it is an upload.
        """
        # Check that href is local
        scheme = urlparse(href).scheme
        if scheme != "" and scheme != "file":
            raise ValueError("Source file to upload must be on the local filesystem")

        storage = AccessManager.resolve_storage(dst)
        storage.push(href, dst)

    @staticmethod
    def pull(href: str, dst: str):
        """
        Pulls a file from a storage to write it in the local storage.
        If the input storage is local, then it is a copy. Otherwise it is a download.
        """
        # Check that dst is local
        scheme = urlparse(dst).scheme
        if scheme != "" and scheme != "file":
            raise ValueError("Destination must be on the local filesystem")

        storage = AccessManager.resolve_storage(href)
        storage.pull(href, dst)

    @staticmethod
    @contextmanager
    def stream(href: str):
        """
        Reads the content of a file in a storage without downloading it.
        """
        with AccessManager.resolve_storage(href=href).stream(href) as f:
            yield f

    @staticmethod
    def get_rasterio_session(href: str):
        storage = AccessManager.resolve_storage(href)
        return storage.get_rasterio_session(href)

    @staticmethod
    def exists(href: str) -> bool:
        """
        Whether the file exists
        """
        storage = AccessManager.resolve_storage(href)
        return storage.exists(href)

    @staticmethod
    def is_download_required(href: str):
        storage = AccessManager.resolve_storage(href)

        return storage.storage_configuration.type in ["http", "https"] \
            and storage.get_configuration().force_download

    @staticmethod
    @contextmanager
    def make_local(href: str, dst: str | None = None):
        """Prepare the file to be processed locally. Once the file has been used, if it has been pulled, deletes it.

        Args:
            href (str): Href (local or not) of the file

        Returns:
            str: The local path at which the file can be found
        """
        storage = AccessManager.resolve_storage(href)

        # If the storage is not local, pull it
        if not storage.storage_configuration.is_local:
            if dst is None:
                dst = os.path.join(AccessManager.tmp_dir, os.path.basename(href))

            AccessManager.pull(href, dst)
            try:
                yield dst
            finally:
                AccessManager.clean(dst)  # !DELETE!
        else:
            yield href

    @staticmethod
    @contextmanager
    def make_local_list(href_list: list[str], dst_list: list[str | None] | None = None):
        """Prepare a list of files to make them available locally for further processing.
           Once used, the file is deleted if it has been pulled
        """
        # Check that the input lists match each other length
        if dst_list is not None and len(href_list) != len(dst_list):
            raise ValueError("Input href and dst must have the same length")
        if dst_list is None:
            dst_list = [None for _ in href_list]

        # For each of the input pair of (href, dst), check if the corresponding storage is local
        # If not, pull it, store dst and tag the iteration as pulled. Otherwise, store href and tag as not pulled.
        # Once all local, will yield the list of local paths
        # Cleanup will only remove the files that were pulled
        local_href_list: list[str] = []
        was_pulled = []
        try:
            for href, dst in zip(href_list, dst_list):
                storage = AccessManager.resolve_storage(href)

                if not storage.storage_configuration.is_local:
                    if dst is None:
                        dst = os.path.join(AccessManager.tmp_dir, os.path.basename(href))

                    AccessManager.pull(href, dst)
                    local_href_list.append(dst)
                    was_pulled.append(True)
                else:
                    local_href_list.append(href)
                    was_pulled.append(False)
            yield local_href_list
        finally:
            for pulled, local_href in zip(was_pulled, local_href_list):
                # Only pulled files (files downloaded by this process) are deleted, as a clean up procedure.
                if pulled:
                    AccessManager.clean(local_href)  # !DELETE!

    @staticmethod
    def clean(href: str):
        storage = AccessManager.resolve_storage(href)
        storage.clean(href)  # !DELETE!

    @staticmethod
    def zip(href: str, zip_path: str):
        with AccessManager.make_local(href) as local_href:
            # Get direct parent folder of href_file to zip
            dir_name = os.path.dirname(local_href)
            shutil.make_archive(zip_path, 'zip', dir_name)

    @staticmethod
    def is_file(href: str):
        storage = AccessManager.resolve_storage(href)

        return storage.is_file(href)

    @staticmethod
    def is_dir(href: str):
        storage = AccessManager.resolve_storage(href)

        return storage.is_dir(href)

    @staticmethod
    def get_size(href: str):
        storage = AccessManager.resolve_storage(href)
        if AccessManager.exists(href):
            if AccessManager.is_file(href):
                return storage.get_file_size(href)
            else:
                folder_size = 0
                for f in AccessManager.listdir(href):
                    folder_size += AccessManager.get_size(f.path)
                return folder_size
        raise FileNotFoundError(f"Given href does not exist: {href}")

    @staticmethod
    def listdir(href: str) -> list[File]:
        storage = AccessManager.resolve_storage(href)

        if not storage.is_dir(href):
            raise NotADirectoryError(f"Given href does not point to a directory: {href}")

        return storage.listdir(href)

    @staticmethod
    def get_last_modification_time(href: str) -> float | None:
        storage = AccessManager.resolve_storage(href)
        return storage.get_last_modification_time(href)

    @staticmethod
    def get_creation_time(href: str) -> float | None:
        storage = AccessManager.resolve_storage(href)
        return storage.get_creation_time(href)

    @staticmethod
    def makedir(href: str, strict=False):
        """
        Create if needed (and possible) the specified dir
        """
        storage = AccessManager.resolve_storage(href)
        return storage.makedir(href, strict)

    @staticmethod
    def dirname(href: str):
        """
        Wraps os.path.dirname to allow for absolute path to be determined if needed
        """
        storage = AccessManager.resolve_storage(href)
        return storage.dirname(href)

    @staticmethod
    def get_gdal_src(href: str):
        """
        Returns the dataset of an archive through GDAL without pulling the file
        """
        storage = AccessManager.resolve_storage(href)
        return storage.get_gdal_src(href)

    @staticmethod
    def get_gdal_md(href: str):
        """
        Returns the metadata of an archive through GDAL without pulling the file
        """
        return AccessManager.get_gdal_src(href).GetMetadata()

    @staticmethod
    def get_gdal_proj(href: str):
        """
        Returns the projection of an archive through GDAL without pulling the file
        """
        return AccessManager.get_gdal_src(href).GetProjection()

    @staticmethod
    def get_gdal_info(href: str, gdal_options):
        """
        Returns the info of an archive through GDAL without pulling the file
        """
        storage = AccessManager.resolve_storage(href)
        return storage.get_gdal_info(href, gdal_options)
