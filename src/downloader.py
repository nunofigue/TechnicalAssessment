import logging
import requests
import xml.etree.ElementTree as ET

logger = logging.getLogger("Downloader")

class Downloader:
    """
    Downloads and extracts XML and ZIP files.
    """

    def download_xml(self, url: str) -> str:
        """
        Downloads XML content from a given URl.
        :param url: The url to fetch the XML from.
        :return: The XML content as a string.
        """

        logger.info("Downloading XML from %s", url)

        response = requests.get(url)
        response.raise_for_status()

        logger.info("Successfully downloaded XML")

        return response.text

    def extract_link(self, xml_content: str) -> str:
        """
        Extract the second download link whose file_type is DLTINS.
        :param xml_content: The XML content as a string.
        :return: The url of the second DLTINS file.
        """

        logger.info("Parsing XML to find desired link.")

        root = ET.fromstring(xml_content)
        dltins_links = []

        for doc in root.findall(".//doc"):
            file_type = None
            download_link = None
            for field in doc.findall("str"):
                if field.attrib.get("name") == "file_type":
                    file_type = field.text
                elif field.attrib.get("name") == "download_link":
                    download_link = field.text
            if file_type == "DLTINS" and download_link:
                dltins_links.append(download_link)

        if len(dltins_links) < 2:
            raise ValueError("XML has less than 2 DLTINS links")

        desired_link = dltins_links[1]
        logger.info("Second DLTINS link found: %s", desired_link)

        return desired_link


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    url = ("https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2021-01"
           "-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100")
    downloader = Downloader()
    xml_content = downloader.download_xml(url)

    zip_url = downloader.extract_link(xml_content)
    print(zip_url)