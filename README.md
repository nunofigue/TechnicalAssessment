Technical Assessment

- downloader.py includes requirements 1 to 3 from downloading the xml from the url to downloading the url from the zip. 
- transformer.py includes requirements 4 to 6 : converting to csv and adding the new columns. It also includes a standard save_to_csv that generates the file in data/sample_output.csv
- storage.py uses 'fsspec' to allow storing the csv locally or in a S3 bucket depending on the file path provided

I decided to include main.py to show how the methods are being used.

There is a tests folder that includes three tests using pytest for:

- converting XML to dataframe
- adding new columns 'a_count' and 'contains_a'
- saving the csv using 'fsspec'

Note: I didn't incorporate dependency management or linters, as i have almost no experience using them and had not enough time to explore it properly.