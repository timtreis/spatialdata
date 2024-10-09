from pathlib import Path
from typing import Union

import pandas as pd
import zarr


def _read_global_metadata(
    store: Union[str, Path], name: str = "metadata.csv", metadata_group: str = "metadata", **kwargs
) -> pd.DataFrame:
    """
    Read a pandas DataFrame from a CSV file within a Zarr container.

    Parameters
    ----------
    - store (str or Path): The path to the Zarr store.
    - name (str): The name of the CSV file. Defaults to "metadata.csv".
    - metadata_group (str): The group within the Zarr container where metadata is stored. Defaults to "metadata".
    - **kwargs: Additional keyword arguments passed to `read_csv`.

    Returns
    -------
    - pd.DataFrame: The reconstructed DataFrame.
    """
    store_path = Path(store)
    metadata_file = store_path / metadata_group / name

    if not metadata_file.exists():
        raise FileNotFoundError(f"Metadata file {metadata_file} does not exist.")

    metadata = pd.read_csv(metadata_file, **kwargs)
    return metadata


def write_global_metadata(
    metadata: pd.DataFrame,
    group: zarr.Group,
    name: str = "metadata",
    **kwargs,
) -> None:
    """
    Write a pandas DataFrame to a CSV file within a Zarr container.

    Parameters
    ----------
    - metadata (pd.DataFrame): The DataFrame to write.
    - store (str or Path): The path to the Zarr store.
    - name (str): The name of the CSV file. Defaults to "metadata.csv".
    - group (str): The group within the Zarr container to store metadata. Defaults to "metadata".
    - **kwargs: Additional keyword arguments passed to `to_csv`.
    """
    path = Path(group._store.path) / "metadata" / name

    metadata.to_csv(
        f"{str(path)}.csv", index=False, **kwargs
    )  # because Pathlib crops the extension and I'm too lazy to fix it
