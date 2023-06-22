Python Script to extract employee count for the Company names provided in a csv file

We are using company_data.csv file for the company names which are read by the script and then the linkedin Url for these companies is generated. Though the current algorithm is not 100% perfect and can miss out some edge cases, but this approach seemed to me much better, because other that I came through required either to have a linkedin account and use it to login or have the linkedin company search api access.

Then the generated links are stored in the company_links.csv file which is then used for the next part of the script which scrapes the employee count of these companies using playwright. Also to have the correct information about the employee count we are using regex to check the comma seperated values for the employee count i.e 122,232 and etc.

Further we again use the company_data.csv file to store these employee count scraped.

** NOTE: There are several things that can be improved in the program like using OOPS to manage the logic so that we can write the employee count for every employer because in case the program fails in between we will make sure to write the other data to the csv file. Currently we do it with the try block. which ignores the issue.


INSTALLATION

Clone the repo and get in the directory

```python3 -m venv .venv  # Create the virtual environment
source .venv/bin/activate # activate the environment
pip install -r requirements.txt # install the dependencies
python3 idea.py  #Run the script
```