# ranking_script_sql
for sql database\

private project

## Requirements - 
Python 3\
Dependencies - flask,mysql-connector-python,pandas  

### Check python version is 3
python --version


### In terminal
pip install flask\
pip install mysql-connector-python\
pip install pandas

### Also
Download python_code folder\
cd into the python_code folder

in terminal run - \
python rank_serv.py
### Then
this will open flask server at localhost:5000

The url for ranking is localhost:5000/rank\
On ranking this will return a string - 'ranked' with response code 200 for success.

