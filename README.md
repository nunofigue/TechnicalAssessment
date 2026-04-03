Technical Assessment

- downloader.py includes requirements 1 to 3 from downloading the xml from the url to downloading the url from the zip. 
- transformer.py includes requirements 4 to 6 : converting to csv and adding the new columns. It also includes a standard save_to_csv that generates the file in data/sample_output.csv
- storage.py uses 'fsspec' to allow storing the csv locally or in a S3 bucket depending on the file path provided

Also included main.py to show how the methods are being used. It has an example of how storing to an AWS S3 bucket would be done with the store_csv() method.

There is a tests folder that includes three tests using pytest for:

- converting XML to dataframe
- adding new columns 'a_count' and 'contains_a'
- saving the csv using 'fsspec'

There is a data folder with 2 examples containing the first 100 rows of the dataset exported using the 2 different methods. 'sample_output.csv' corresponds to the standard save_to_csv() and 'sample_output_2.csv' corresponds used the store_csv() method that uses 'fsspec'.

Note: Decided not to incorporate dependency management or linters, as i have almost no experience using them and had not enough time to explore it properly.