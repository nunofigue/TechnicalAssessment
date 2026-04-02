from downloader import Downloader
from transformer import Transformer
from storage import Storage
import xml.etree.ElementTree as ET
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

url = ("https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:"
       "[2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z]&wt=xml&indent=true&start=0&rows=100")

downloader = Downloader()
xml_with_links = downloader.download_xml(url)
zip_url = downloader.extract_link(xml_with_links)
zip_bytes = downloader.download_zip(zip_url)
xml_content = downloader.extract_xml_from_zip(zip_bytes)

transformer = Transformer(xml_content)

df = transformer.parse_to_dataframe()
print("Raw DataFrame:")
print(df.head(10))

df = transformer.add_new_columns(df)
print("New DataFrame:")
print(df.head(10))

transformer.save_to_csv(df.head(100), "data/sample_output.csv")

storage = Storage()
storage.store_csv(df.head(100),"data/sample_output_2.csv")

#to store in a aws s3 bucket
storage.store_csv(df, "s3://my-bucket/sample_output.csv")
