import logging
import requests

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


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    url = ("https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2021-01"
           "-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100")
    downloader = Downloader()
    xml_content = downloader.download_xml(url)

    #test download_xml
    print(xml_content[:500])