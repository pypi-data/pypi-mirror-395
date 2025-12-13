import abc

import polars as pl

from bayesline.api._src._utils import docstrings_from_sync


class AssetIdApi:
    """Abstract base class for asset ID API operations."""

    @abc.abstractmethod
    def lookup_ids(self, ids: list[str], top_n: int = 0) -> pl.DataFrame:
        """
        Look up asset IDs and return matching records.

        Parameters
        ----------
        ids : list[str]
            The ids to lookup.
        top_n : int, default=0
            The number of results to return, where `0` denotes all records.

        Returns
        -------
        pl.DataFrame
            A dataframe with all identifiers that could be matched, sorted by
            `id` and `start_date`.
        """
        ...


@docstrings_from_sync
class AsyncAssetIdApi:

    @abc.abstractmethod
    async def lookup_ids(  # noqa: D102
        self, ids: list[str], top_n: int = 0
    ) -> pl.DataFrame: ...
