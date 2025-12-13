import abc
import datetime as dt
from pathlib import Path
from typing import Literal

import polars as pl
from pydantic import BaseModel

from bayesline.api._src._utils import docstrings_from_sync
from bayesline.api._src.tasks import AsyncTask, Task
from bayesline.api._src.types import DNFFilterExpressions


class UploadParserResult(BaseModel, frozen=True, extra="forbid"):
    """Result of a parser operation.

    Parameters
    ----------
    parser : str | None
        The name of the parser that was used.
    success : bool
        Whether the parsing was successful.
    messages : list[str]
        List of messages from the parsing operation.
    """

    parser: str | None = None  # TODO remove None
    success: bool
    messages: list[str]


class MultiParserResult(BaseModel, frozen=True, extra="forbid"):
    """Result of multiple parser operations.

    Parameters
    ----------
    results : list[UploadParserResult]
        List of parser results.
    """

    results: list[UploadParserResult]

    @property
    def success(self) -> bool:
        """Check if any parser was successful."""
        return any(result.success for result in self.results)

    @property
    def success_parser(self) -> UploadParserResult | None:
        """Get the first successful parser result."""
        return next((result for result in self.results if result.success), None)


class UploadStagingResult(BaseModel, frozen=True, extra="forbid"):
    """Result of a staging operation.

    Parameters
    ----------
    name : str
        The name of the staged item.
    timestamp : dt.datetime
        When the staging occurred.
    success : bool
        Whether the staging was successful.
    results : list[UploadParserResult]
        Results from the parsing operation.
    """

    name: str
    timestamp: dt.datetime
    success: bool
    results: list[UploadParserResult]

    @property
    def success_parser(self) -> UploadParserResult | None:
        """Get the first successful parser result."""
        return next((result for result in self.results if result.success), None)


class UploadCommitResult(BaseModel, frozen=True, extra="forbid"):
    """Result of a commit operation.

    Parameters
    ----------
    version : int
        The version number of the committed data.
    committed_names : list[str]
        Names of the committed items.
    """

    version: int
    committed_names: list[str]


class UploadParserApi(abc.ABC):
    """Abstract base class for upload parsers."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Get the name of the parser.

        Returns
        -------
        str
            The name of the parser.
        """
        ...

    @abc.abstractmethod
    def output_schema(self) -> dict[str, pl.DataType]:
        """Get the output schema that this parser produces.

        Returns
        -------
        dict[str, pl.DataType]
            The schema that this parser produces.
        """
        ...

    @abc.abstractmethod
    def get_examples(self) -> list[pl.DataFrame]:
        """Get example dataframes for testing the parser.

        Returns
        -------
        list[pl.DataFrame]
            A list of example portfolios that can be used to test the parser.
        """
        ...

    @abc.abstractmethod
    def can_handle(
        self, raw_df: pl.DataFrame, *, name: str | None = None
    ) -> UploadParserResult:
        """Check if this parser can handle the given dataframe.

        Parameters
        ----------
        raw_df : pl.DataFrame
            The dataframe to check if the parser can handle.
        name : str | None, default=None
            The name of the dataframe (which could be the filename).
            Some parsers might extract information (such as a date) from the name.

        Returns
        -------
        UploadParserResult
            Result indicating whether the parser can handle the dataframe.
        """
        ...

    @abc.abstractmethod
    def parse(
        self, raw_df: pl.DataFrame, *, name: str | None = None
    ) -> tuple[pl.DataFrame, UploadParserResult]:
        """Parse the given dataframe.

        Parameters
        ----------
        raw_df : pl.DataFrame
            The dataframe to parse.
        name : str | None, default=None
            The name of the dataframe (which could be the filename).
            Some parsers might extract information (such as a date) from the name.

        Returns
        -------
        tuple[pl.DataFrame, UploadParserResult]
            A tuple of the parsed pl.DataFrame and a UploadParserResult.
            If the parser was unsuccessful the parsed dataframe will instead be
            a (possibly empty) error dataframe.
        """
        ...


@docstrings_from_sync
class AsyncUploadParserApi(abc.ABC):

    @property
    @abc.abstractmethod
    def name(self) -> str: ...  # noqa: D102

    @abc.abstractmethod
    async def output_schema(self) -> dict[str, pl.DataType]: ...  # noqa: D102

    @abc.abstractmethod
    async def get_examples(self) -> list[pl.DataFrame]: ...  # noqa: D102

    @abc.abstractmethod
    async def can_handle(  # noqa: D102
        self, raw_df: pl.DataFrame, *, name: str | None = None
    ) -> UploadParserResult: ...

    @abc.abstractmethod
    async def parse(  # noqa: D102
        self, raw_df: pl.DataFrame, *, name: str | None = None
    ) -> tuple[pl.DataFrame, UploadParserResult]: ...


class UploadError(Exception):
    """Exception raised for upload-related errors."""

    pass


class UploaderApi(abc.ABC):
    """Provide functionality to parse, stage and upload data to a versioned storage.

    Parsing:
    This uploader contains a set of parsers that can be used to parse raw dataframes
    into their standardized format.

    Staging:
    The staging functionality allows to stage multiple dataframes for upload.
    This is done by providing a name and a dataframe for each staged dataframe
    and is not affecting the 'committed' data until the staged dataframes are committed.
    The staging area is unversioned.

    Commit:
    Allows to commit the staged dataframes to the versioned storage. All committed
    dataframes will be removed from the staging area. At commit time all staged
    dataframes will be concatenated. The committed data is one consolidated dataframe.

    Versioning:
    Committed data is versioned. At commit time a 'commit mode' can be provided to
    determine how the committed data is merged with the already committed data
    (e.g. overwrite, append, upsert, etc.).
    """

    @abc.abstractmethod
    def get_schema(
        self, which: Literal["data", "staging"] = "data"
    ) -> dict[str, pl.DataType]:
        """Get the schema for the specified data type.

        Parameters
        ----------
        which : Literal["data", "staging"], default="data"
            The type of schema to get.
            If "data" will get the schema for the committed data.
            If "staging" will get the schema for the staged data.

        Returns
        -------
        dict[str, pl.DataType]
            The schema of the uploaded files.
        """
        ...

    @abc.abstractmethod
    def get_summary_schema(
        self, which: Literal["data", "staging"] = "data"
    ) -> dict[str, pl.DataType]:
        """Get the summary schema for the specified data type.

        Parameters
        ----------
        which : Literal["data", "staging"], default="data"
            The type of summary statistics to get the schema for.
            If "data" will get the schema for the committed data.
            If "staging" will get the schema for the staged data.

        Returns
        -------
        dict[str, pl.DataType]
            The schema of the summary statistics.
        """
        ...

    @abc.abstractmethod
    def get_detail_summary_schema(
        self, which: Literal["data", "staging"] = "data"
    ) -> dict[str, pl.DataType]:
        """Get the detail summary schema for the specified data type.

        Parameters
        ----------
        which : Literal["data", "staging"], default="data"
            The type of detail summary statistics to get the schema for.
            If "data" will get the schema for the committed data.
            If "staging" will get the schema for the staged data.

        Returns
        -------
        dict[str, pl.DataType]
            The schema of the detail summary statistics.
        """
        ...

    @abc.abstractmethod
    def get_commit_modes(self) -> dict[str, str]:
        """Get the available commit modes and their descriptions.

        Returns
        -------
        dict[str, str]
            Available modes (keys) that can be passed to the commit function
            and their descriptions (values).
        """
        ...

    @abc.abstractmethod
    def get_parser_names(self) -> list[str]:
        """Get the list of available parser names.

        Returns
        -------
        list[str]
            The list of available parsers that can be used to parse files with
            this uploader.
        """
        ...

    @abc.abstractmethod
    def get_parser(self, parser: str) -> UploadParserApi:
        """Get a specific parser by name.

        Parameters
        ----------
        parser : str
            The parser to obtain.

        Returns
        -------
        UploadParserApi
            The parser.
        """
        ...

    @abc.abstractmethod
    def can_handle(
        self, df: pl.DataFrame, *, parser: str | None = None, name: str | None = None
    ) -> MultiParserResult:
        """Check if the uploader can handle the given dataframe.

        Parameters
        ----------
        df : pl.DataFrame
            The dataframe to check if the parser can handle.
        parser : str | None, default=None
            The parser to use. If None will check all parsers and choose the first
            parser that can handle the dataframe.
        name : str | None, default=None
            The name of the dataframe (which could be the filename).
            Some parsers might extract information (such as a date) from the name.

        Returns
        -------
        MultiParserResult
            The result of the parser check.
        """
        ...

    @abc.abstractmethod
    def stage_df(
        self,
        name: str,
        df: pl.DataFrame,
        parser: str | None = None,
        replace: bool = False,
    ) -> UploadStagingResult:
        """Stage a dataframe for upload under the given name.

        Parameters
        ----------
        name : str
            The name of the dataframe to stage.
        df : pl.DataFrame
            The dataframe to stage.
        parser : str | None, default=None
            The parser to use. If None will check all parsers.
        replace : bool, default=False
            If True will replace a possible existing staging with the same name.
            If False a name clash will result in a failed staging result.

        Raises
        ------
        UploadError
            If the given name already exists.

        Returns
        -------
        UploadStagingResult
            The result of the staging operation.
        """
        ...

    @abc.abstractmethod
    def stage_df_as_task(  # noqa: D102
        self,
        name: str,
        df: pl.DataFrame,
        parser: str | None = None,
        replace: bool = False,
    ) -> Task[UploadStagingResult]: ...

    @abc.abstractmethod
    def stage_file(
        self,
        path: Path,
        name: str | None = None,
        parser: str | None = None,
        replace: bool = False,
    ) -> UploadStagingResult:
        """Stage a file for upload under the given name.

        Parameters
        ----------
        path : Path
            File path for the file to stage.
        name : str | None, default=None
            The name of the dataframe to stage. If None will use the file name.
        parser : str | None, default=None
            The parser to use. If None will check all parsers.
        replace : bool, default=False
            If True will replace a possible existing staging with the same name.
            If False a name clash will result in a failed staging result.

        Raises
        ------
        UploadError
            If the file could not be staged.

        Returns
        -------
        UploadStagingResult
            The result of the staging operation.
        """
        ...

    @abc.abstractmethod
    def stage_file_as_task(  # noqa: D102
        self,
        path: Path,
        name: str | None = None,
        parser: str | None = None,
        replace: bool = False,
    ) -> Task[UploadStagingResult]: ...

    @abc.abstractmethod
    def get_staging_results(
        self, names: list[str] | None = None
    ) -> dict[str, UploadStagingResult]:
        """Get the staging results for the optional list of names.

        Parameters
        ----------
        names : list[str] | None, default=None
            The names of the staging results to get.
            If None will get all staging results.
            Missing names will be ignored and won't be part of the result.

        Returns
        -------
        dict[str, UploadStagingResult]
            A dictionary of staging results.
        """
        ...

    @abc.abstractmethod
    def wipe_staging(
        self,
        names: list[str] | None = None,
    ) -> dict[str, UploadStagingResult]:
        """Wipe the staging results for the optional list of names.

        Parameters
        ----------
        names : list[str] | None, default=None
            The names of the staging results to wipe.
            If None will wipe all staging results.
            Names that do not exist will be ignored.

        Returns
        -------
        dict[str, UploadStagingResult]
            A dictionary of staging results that were wiped.
        """
        ...

    @abc.abstractmethod
    def get_staging_data(
        self,
        names: list[str] | None = None,
        *,
        columns: list[str] | None = None,
        unique: bool = False,
    ) -> pl.LazyFrame:
        """Get the staging data for the optional list of names.

        Parameters
        ----------
        names : list[str] | None, default=None
            The names of the staging data to get.
            If None will get all staging data.
            Names that do not exist will be ignored.
        columns : list[str] | None, default=None
            The columns to get. If None will get all columns.
        unique : bool, default=False
            If True will return a unique set of rows.
            If False will return all rows.

        Returns
        -------
        pl.LazyFrame
            The staging data with an additional column `_name` that contains
            the staging name.
        """
        ...

    @abc.abstractmethod
    def get_staging_data_as_task(  # noqa: D102
        self,
        names: list[str] | None = None,
        *,
        columns: list[str] | None = None,
        unique: bool = False,
    ) -> Task[pl.LazyFrame]: ...

    @abc.abstractmethod
    def get_staging_data_summary(self, names: list[str] | None = None) -> pl.DataFrame:
        """Get the staging summary statistics for the optional list of names.

        Parameters
        ----------
        names : list[str] | None, default=None
            The names for which to get the staging summary statistics.
            If None will get all staging data.
            Names that do not exist will be ignored.

        Returns
        -------
        pl.DataFrame
            The staging summary statistics data which will contain one row
            per staged file.
            The schema matches `get_summary_schema` with an additional column
            `_name` (at the beginning) of type str which contains the name of the
            staged file.
        """
        ...

    @abc.abstractmethod
    def get_staging_data_summary_as_task(  # noqa: D102
        self, names: list[str] | None = None
    ) -> Task[pl.DataFrame]: ...

    @abc.abstractmethod
    def get_staging_data_detail_summary(
        self, names: list[str] | None = None
    ) -> pl.DataFrame:
        """Get the detail staging summary statistics for the optional list of names.

        Parameters
        ----------
        names : list[str] | None, default=None
            The names for which to get the detail staging summary statistics.
            If None will get all staging data.
            Names that do not exist will be ignored.

        Returns
        -------
        pl.DataFrame
            The detail staging summary statistics data which will contain multiple rows
            per staged file.
            The schema matches `get_detail_summary_schema` with an additional column
            `_name` (at the beginning) of type str which contains the name of the
            staged file.
        """
        ...

    @abc.abstractmethod
    def get_staging_data_detail_summary_as_task(  # noqa: D102
        self, names: list[str] | None = None
    ) -> Task[pl.DataFrame]: ...

    @abc.abstractmethod
    def validate_staging_data(
        self, names: list[str] | None = None, short: bool = False
    ) -> dict[str, pl.DataFrame]:
        """Validate the staging data for the optional list of names, and return errors.

        The errors are returned as a dict of error dataframes keyed by the name of the
        validation test.

        Parameters
        ----------
        names : list[str] | None, default=None
            The names for which to carry out the validation.
            If None will use all staging data.
            Names that do not exist will be ignored.
        short : bool, default=False
            If True will return a shorter dataframes which only contain a column `_name`
            to indicate the name of the staging file which has validation errors with
            other staging files.
            If False will return a dataframe with the `_name` (as above) and other
            columns to indicate the validation errors.

        Returns
        -------
        dict[str, pl.DataFrame]
            Error dataframes for different validation checks. The dataframes will
            contain a column `_name`. If `short` is False then the `_name` column
            contains a comma separated list of staging names that are the cause of the
            respective validation error.
            If `short` is True then the `_name` column will be the only column and
            each row contains a staging file name that has validation errors.
        """
        ...

    @abc.abstractmethod
    def validate_staging_data_as_task(  # noqa: D102
        self, names: list[str] | None = None, short: bool = False
    ) -> Task[dict[str, pl.DataFrame]]: ...

    @abc.abstractmethod
    def commit(self, mode: str, names: list[str] | None = None) -> UploadCommitResult:
        """Commit and clear all staged files identified by given names.

        Parameters
        ----------
        mode : str
            Commit mode, one of `commit_modes`.
        names : list[str] | None, default=None
            The names of the staging results to commit.
            If None will commit all staging results.
            Names that do not exist will be ignored.

        Raises
        ------
        ValueError
            If the given commit mode does not exist.
        UploadError
            If the staged data fails validation (as tested by `validate_staging_data`).

        Returns
        -------
        UploadCommitResult
            The result of the commit operation.
        """
        ...

    @abc.abstractmethod
    def commit_as_task(  # noqa: D102
        self, mode: str, names: list[str] | None = None
    ) -> Task[UploadCommitResult]: ...

    @abc.abstractmethod
    def fast_commit(
        self, df: pl.DataFrame | Path, mode: str, parser: str | None = None
    ) -> UploadCommitResult:
        """Directly commit the given dataframe without staging.

        Parameters
        ----------
        df : pl.DataFrame | Path
            The dataframe to commit.
        mode : str
            Commit mode, one of `commit_modes`.
        parser : str | None, default=None
            The parser to use. If None will check all parsers.

        Raises
        ------
        ValueError
            If the given commit mode does not exist.
        UploadError
            If the staged data fails validation (as tested by `validate_staging_data`).

        Returns
        -------
        UploadCommitResult
            The result of the commit operation.
        """
        ...

    @abc.abstractmethod
    def fast_commit_as_task(  # noqa: D102
        self, df: pl.DataFrame | Path, mode: str, parser: str | None = None
    ) -> Task[UploadCommitResult]: ...

    @abc.abstractmethod
    def get_data(
        self,
        columns: list[str] | None = None,
        *,
        filters: DNFFilterExpressions | None = None,
        unique: bool = False,
        head: int | None = None,
        version: int | dt.datetime | None = None,
        download_to: Path | str | None = None,
        download_filename: str = "data-{i}.parquet",
    ) -> pl.LazyFrame:
        """Get the committed data at the given version.

        Parameters
        ----------
        columns : list[str] | None, default=None
            The columns to get. If None will get all columns.
        filters : DNFFilterExpressions | None, default=None
            The filters to apply to the data. If None will get all data.
            Follow the pyarrow filter syntax.
            https://arrow.apache.org/docs/python/generated/pyarrow.parquet.ParquetDataset.html
        unique : bool, default=False
            If True will return a unique set of rows.
            If False will return all rows.
        head : int | None, default=None
            If given will return the first `head` rows.
            If None will return all rows.
        version : int | dt.datetime | None, default=None
            The version of the underlying data, latest if not given.
            By definition version 0 is the empty dataframe with correct schema.
        download_to : Path | str | None, default=None
            If given will download the data to the given path and then return
            a LazyFrame against that downloaded path. The path must point to a
            an existing directory. If a string is given then a Path object will be
            created from it using `Path(download_to)`.
            If None will consume the data in memory and return a lazy frame.
        download_filename : str, default="data-{i}.parquet"
            The filename to use for the downloaded data which must contain the
            placeholder `{i}` which will be replaced with the index of the file.
            Only used if `download_to` is given.
            If `download_to/download_filename` already exists then an exception
            will be raised.

        Raises
        ------
        KeyError
            If the given version does not exist.
        FileExistsError
            If `download_to/download_filename` already exists.
        FileNotFoundError
            If `download_to` is given and does not exist.

        Returns
        -------
        pl.LazyFrame
            The committed data at the given version.
        """
        ...

    @abc.abstractmethod
    def get_data_as_task(  # noqa: D102
        self,
        columns: list[str] | None = None,
        *,
        filters: DNFFilterExpressions | None = None,
        unique: bool = False,
        head: int | None = None,
        version: int | dt.datetime | None = None,
        download_to: Path | str | None = None,
        download_filename: str = "data-{i}.parquet",
    ) -> Task[pl.LazyFrame]: ...

    @abc.abstractmethod
    def get_data_summary(
        self, version: int | dt.datetime | None = None
    ) -> pl.DataFrame:
        """Get the data summary statistics (single row) at the given version.

        Parameters
        ----------
        version : int | dt.datetime | None, default=None
            The version of the underlying data, latest if not given.

        Returns
        -------
        pl.DataFrame
            The summary statistics data (single row) for the data at the given
            version.
        """
        ...

    @abc.abstractmethod
    def get_data_summary_as_task(  # noqa: D102
        self, version: int | dt.datetime | None = None
    ) -> Task[pl.DataFrame]: ...

    @abc.abstractmethod
    def get_data_detail_summary(
        self, version: int | dt.datetime | None = None
    ) -> pl.DataFrame:
        """Get the detail data summary statistics (multi row) at the given version.

        Parameters
        ----------
        version : int | dt.datetime | None, default=None
            The version of the underlying data, latest if not given.

        Returns
        -------
        pl.DataFrame
            The summary statistics data (multi row) for the data at the given
            version.
        """
        ...

    @abc.abstractmethod
    def get_data_detail_summary_as_task(  # noqa: D102
        self, version: int | dt.datetime | None = None
    ) -> Task[pl.DataFrame]: ...

    @abc.abstractmethod
    def destroy(self) -> None:
        """Irreversibly delete the entire dataset.

        This includes the entire version history of uploads and staged files. Cannot be
        undone.
        """
        ...

    @abc.abstractmethod
    def version_history(self) -> dict[int, dt.datetime]:
        """Get the version history of the dataset.

        Returns
        -------
        dict[int, dt.datetime]
            A dictionary of version numbers and the corresponding timestamps.
        """
        ...


@docstrings_from_sync
class AsyncUploaderApi(abc.ABC):

    @abc.abstractmethod
    async def get_schema(  # noqa: D102
        self, which: Literal["data", "staging"] = "data"
    ) -> dict[str, pl.DataType]: ...

    @abc.abstractmethod
    async def get_summary_schema(  # noqa: D102
        self, which: Literal["data", "staging"] = "data"
    ) -> dict[str, pl.DataType]: ...

    @abc.abstractmethod
    async def get_detail_summary_schema(  # noqa: D102
        self, which: Literal["data", "staging"] = "data"
    ) -> dict[str, pl.DataType]: ...

    @abc.abstractmethod
    async def get_commit_modes(self) -> dict[str, str]: ...  # noqa: D102

    @abc.abstractmethod
    async def get_parser_names(self) -> list[str]: ...  # noqa: D102

    @abc.abstractmethod
    async def get_parser(self, parser: str) -> AsyncUploadParserApi: ...  # noqa: D102

    @abc.abstractmethod
    async def can_handle(  # noqa: D102
        self, df: pl.DataFrame, *, parser: str | None = None, name: str | None = None
    ) -> MultiParserResult: ...

    @abc.abstractmethod
    async def stage_df(  # noqa: D102
        self,
        name: str,
        df: pl.DataFrame,
        parser: str | None = None,
        replace: bool = False,
    ) -> UploadStagingResult: ...

    @abc.abstractmethod
    async def stage_df_as_task(  # noqa: D102
        self,
        name: str,
        df: pl.DataFrame,
        parser: str | None = None,
        replace: bool = False,
    ) -> AsyncTask[UploadStagingResult]: ...

    @abc.abstractmethod
    async def stage_file(  # noqa: D102
        self,
        path: Path,
        name: str | None = None,
        parser: str | None = None,
        replace: bool = False,
    ) -> UploadStagingResult: ...

    @abc.abstractmethod
    async def stage_file_as_task(  # noqa: D102
        self,
        path: Path,
        name: str | None = None,
        parser: str | None = None,
        replace: bool = False,
    ) -> AsyncTask[UploadStagingResult]: ...

    @abc.abstractmethod
    async def get_staging_results(  # noqa: D102
        self, names: list[str] | None = None
    ) -> dict[str, UploadStagingResult]: ...

    @abc.abstractmethod
    async def wipe_staging(  # noqa: D102
        self,
        names: list[str] | None = None,
    ) -> dict[str, UploadStagingResult]: ...

    @abc.abstractmethod
    async def get_staging_data(  # noqa: D102
        self,
        names: list[str] | None = None,
        *,
        columns: list[str] | None = None,
        unique: bool = False,
    ) -> pl.LazyFrame: ...

    @abc.abstractmethod
    async def get_staging_data_as_task(  # noqa: D102
        self,
        names: list[str] | None = None,
        *,
        columns: list[str] | None = None,
        unique: bool = False,
    ) -> AsyncTask[pl.LazyFrame]: ...

    @abc.abstractmethod
    async def get_staging_data_summary(  # noqa: D102
        self, names: list[str] | None = None
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def get_staging_data_summary_as_task(  # noqa: D102
        self, names: list[str] | None = None
    ) -> AsyncTask[pl.DataFrame]: ...

    @abc.abstractmethod
    async def get_staging_data_detail_summary(  # noqa: D102
        self, names: list[str] | None = None
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def get_staging_data_detail_summary_as_task(  # noqa: D102
        self, names: list[str] | None = None
    ) -> AsyncTask[pl.DataFrame]: ...

    @abc.abstractmethod
    async def validate_staging_data(  # noqa: D102
        self, names: list[str] | None = None, short: bool = False
    ) -> dict[str, pl.DataFrame]: ...

    @abc.abstractmethod
    async def validate_staging_data_as_task(  # noqa: D102
        self, names: list[str] | None = None, short: bool = False
    ) -> AsyncTask[dict[str, pl.DataFrame]]: ...

    @abc.abstractmethod
    async def commit(  # noqa: D102
        self, mode: str, names: list[str] | None = None
    ) -> UploadCommitResult: ...

    @abc.abstractmethod
    async def commit_as_task(  # noqa: D102
        self, mode: str, names: list[str] | None = None
    ) -> AsyncTask[UploadCommitResult]: ...

    @abc.abstractmethod
    async def fast_commit(  # noqa: D102
        self, df: pl.DataFrame | Path, mode: str, parser: str | None = None
    ) -> UploadCommitResult: ...

    @abc.abstractmethod
    async def fast_commit_as_task(  # noqa: D102
        self, df: pl.DataFrame | Path, mode: str, parser: str | None = None
    ) -> AsyncTask[UploadCommitResult]: ...

    @abc.abstractmethod
    async def get_data(  # noqa: D102
        self,
        columns: list[str] | None = None,
        *,
        filters: DNFFilterExpressions | None = None,
        unique: bool = False,
        head: int | None = None,
        version: int | dt.datetime | None = None,
        download_to: Path | str | None = None,
        download_filename: str = "data-{i}.parquet",
    ) -> pl.LazyFrame: ...

    @abc.abstractmethod
    async def get_data_as_task(  # noqa: D102
        self,
        columns: list[str] | None = None,
        *,
        filters: DNFFilterExpressions | None = None,
        unique: bool = False,
        head: int | None = None,
        version: int | dt.datetime | None = None,
        download_to: Path | str | None = None,
        download_filename: str = "data-{i}.parquet",
    ) -> AsyncTask[pl.LazyFrame]: ...

    @abc.abstractmethod
    async def get_data_summary(  # noqa: D102
        self, version: int | dt.datetime | None = None
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def get_data_summary_as_task(  # noqa: D102
        self, version: int | dt.datetime | None = None
    ) -> AsyncTask[pl.DataFrame]: ...

    @abc.abstractmethod
    async def get_data_detail_summary(  # noqa: D102
        self, version: int | dt.datetime | None = None
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def get_data_detail_summary_as_task(  # noqa: D102
        self, version: int | dt.datetime | None = None
    ) -> AsyncTask[pl.DataFrame]: ...

    @abc.abstractmethod
    async def destroy(self) -> None: ...  # noqa: D102

    @abc.abstractmethod
    async def version_history(self) -> dict[int, dt.datetime]: ...  # noqa: D102


class DataTypeUploaderApi(abc.ABC):
    """Expose different datasets of an uploader.

    Datasets are completely isolated spaces to upload data of the same type.
    """

    @abc.abstractmethod
    def get_datasets(self) -> list[str]:
        """Get the list of available datasets.

        Returns
        -------
        list[str]
            A sorted list of available datasets.
        """
        ...

    @abc.abstractmethod
    def get_dataset(self, dataset: str) -> UploaderApi:
        """Get a specific dataset uploader.

        Parameters
        ----------
        dataset : str
            The dataset of the uploader to obtain.
            Must be one of the datasets returned by `get_datasets`.

        Raises
        ------
        KeyError
            If the given dataset does not exist.

        Returns
        -------
        UploaderApi
            The uploader for the specified dataset.
        """
        ...

    @abc.abstractmethod
    def create_dataset(self, dataset: str) -> UploaderApi:
        """Create a new dataset.

        Parameters
        ----------
        dataset : str
            The dataset to create.

        Raises
        ------
        ValueError
            If the given dataset already exists.

        Returns
        -------
        UploaderApi
            The uploader for the new dataset.
        """
        ...

    def get_or_create_dataset(self, dataset: str) -> UploaderApi:
        """Get the dataset if it exists, otherwise create it.

        Parameters
        ----------
        dataset : str
            The dataset to get or create.

        Returns
        -------
        UploaderApi
            The uploader for the dataset.
        """
        if dataset in self.get_datasets():
            return self.get_dataset(dataset)
        else:
            return self.create_dataset(dataset)

    def create_or_replace_dataset(self, dataset: str) -> UploaderApi:
        """Create a new dataset and delete the old one if it exists.

        Parameters
        ----------
        dataset : str
            The dataset to create.

        Returns
        -------
        UploaderApi
            The uploader for the dataset.
        """
        if dataset in self.get_datasets():
            self.get_dataset(dataset).destroy()

        return self.create_dataset(dataset)


@docstrings_from_sync
class AsyncDataTypeUploaderApi(abc.ABC):

    @abc.abstractmethod
    async def get_datasets(self) -> list[str]: ...  # noqa: D102

    @abc.abstractmethod
    async def get_dataset(self, dataset: str) -> AsyncUploaderApi: ...  # noqa: D102

    @abc.abstractmethod
    async def create_dataset(self, dataset: str) -> AsyncUploaderApi: ...  # noqa: D102

    async def get_or_create_dataset(  # noqa: D102
        self, dataset: str
    ) -> AsyncUploaderApi:
        if dataset in await self.get_datasets():
            return await self.get_dataset(dataset)
        else:
            return await self.create_dataset(dataset)

    async def create_or_replace_dataset(  # noqa: D102
        self, dataset: str
    ) -> AsyncUploaderApi:
        if dataset in await self.get_datasets():
            await (await self.get_dataset(dataset)).destroy()

        return await self.create_dataset(dataset)


class UploadersApi(abc.ABC):
    """Expose uploaders for different data types, e.g. exposures, portfolios, etc."""

    @abc.abstractmethod
    def get_data_types(self) -> list[str]:
        """Get the list of available data types.

        Returns
        -------
        list[str]
            A sorted list of available upload data types,
            e.g. "exposures", "portfolios", etc.
        """
        ...

    @abc.abstractmethod
    def get_data_type(self, data_type: str) -> DataTypeUploaderApi:
        """Get a specific data type uploader.

        Parameters
        ----------
        data_type : str
            The data type of the uploader to obtain.
            One of the data types returned by `get_data_types`.

        Raises
        ------
        KeyError
            If the given data type does not exist.

        Returns
        -------
        DataTypeUploaderApi
            The uploader for the given data type.
        """
        ...


@docstrings_from_sync
class AsyncUploadersApi(abc.ABC):

    @abc.abstractmethod
    async def get_data_types(self) -> list[str]: ...  # noqa: D102

    @abc.abstractmethod
    async def get_data_type(  # noqa: D102
        self, data_type: str
    ) -> AsyncDataTypeUploaderApi: ...
