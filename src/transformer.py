import pandas as pd
import logging
import xml.etree.ElementTree as ET

logger = logging.getLogger("Transformer")

class Transformer:
    """
    Converts XML to CSV and adds additional columns.
    """

    def __init__(self, xml_content: str):
        """
        Initializes the transformer with the XML content.
        :param xml_content: The XML content as a string.
        """
        self.xml_content = xml_content

    def parse_to_dataframe(self) -> pd.DataFrame:
        """
        Parses the XML into a Pandas Dataframe with the required columns.

        Columns:
            - FinInstrmGnlAttrbts.Id
            - FinInstrmGnlAttrbts.FullNm
            - FinInstrmGnlAttrbts.ClssfctnTp
            - FinInstrmGnlAttrbts.CmmdtyDerivInd
            - FinInstrmGnlAttrbts.NtnlCcy
            - Issr

        :return: Pandas Dataframe with raw columns.
        """

        logger.info("Parsing XML to Dataframe")

        root = ET.fromstring(self.xml_content)
        ns = {"ns": "urn:iso:std:iso:20022:tech:xsd:auth.036.001.02"}

        records = []
        for fin_instrm in root.findall(".//ns:FinInstrm", ns):

            mod_record = fin_instrm.find("ns:ModfdRcrd", ns)
            if mod_record is None:
                continue

            gnl_attr = mod_record.find(".//ns:FinInstrmGnlAttrbts", ns)
            if gnl_attr is None:
                continue

            issuer = mod_record.findtext("ns:Issr", default="", namespaces=ns)

            record = {
                "FinInstrmGnlAttrbts.Id": gnl_attr.findtext("ns:Id", default="", namespaces=ns),
                "FinInstrmGnlAttrbts.FullNm": gnl_attr.findtext("ns:FullNm", default="", namespaces=ns),
                "FinInstrmGnlAttrbts.ClssfctnTp": gnl_attr.findtext("ns:ClssfctnTp", default="", namespaces=ns),
                "FinInstrmGnlAttrbts.CmmdtyDerivInd": gnl_attr.findtext("ns:CmmdtyDerivInd", default="", namespaces=ns),
                "FinInstrmGnlAttrbts.NtnlCcy": gnl_attr.findtext("ns:NtnlCcy", default="", namespaces=ns),
                "Issr": issuer
            }
            records.append(record)

        df = pd.DataFrame(records)
        logger.info("Parsed %d records from XML", len(df))
        return df

    def add_new_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds columns 'a_count' and 'contains_a' to the Dataframe.
        :param df: Raw Dataframe
        :return: DataFrame with new columns
        """

        logger.info("Adding 'a_count' and 'contains_a columns")

        df["a_count"] = df["FinInstrmGnlAttrbts.FullNm"].apply(lambda x: x.count("a") if x else 0)
        df["contains_a"] = df["a_count"].apply(lambda x: "YES" if x>0 else "NO")

        logger.info("Columns added successfully")
        return df

    def save_to_csv(self, df: pd.DataFrame, file_path: str) -> None:
        """
        Saves the DataFrame with the added columns to a CSV file.
        :param df: DataFrame with new columns
        :param file_path: Path to save the CSV file
        """

        logger.info("Saving DataFrame to CSV: %s", file_path)
        df.to_csv(file_path, index=False)
        logger.info("CSV saved successfully")