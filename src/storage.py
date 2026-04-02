import fsspec
import logging
import pandas as pd

logger = logging.getLogger("Storage")

class Storage:
    """
    Stores the data as a csv in desired storage
    """

    def store_csv(self, df: pd.DataFrame, file_path: str) -> None:
        """

        :param df:
        :param file_path:
        :return:
        """

        logger.info("Storing CSV to: %s", file_path)

        with fsspec.open(file_path, "w", newline="") as f:
            df.to_csv(f, index=False)

        logger.info("Saved successfully")