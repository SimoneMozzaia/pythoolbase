# Python toolbox

Small Python toolbox containing various functionalities.

## Introduction
Tired of coding the same chunks of code or copying and pasting existing ones, I've decided 
to share some of my most used functions while refactoring some.

## Tech Stack
The project is written in Python

## Installation
Just the clone repo and use the functions that interest you

# Usage 
```
Clone the repository

Copy the requirements.txt inside your python package folder
Copy the folder "external_files" inside your python package folder

Install the package and the requirements in your virtualenv with pip 
    pip install C:\custom_apps\programming_languages\repositories\pytoolbase
    pip install -r requirements.txt

Import the package and its functions
```
Example

```python
from pytoolbase.database_connection import Database
def main():
    db = Database()
    connection = db.connect_to_database("env","country")
    # Do something
    connection.close()
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to add or change.

## Notes
As of now, it's just a boilerplate of different things. WORK IN PROGRESS....

## License
[GPL 3.0](https://choosealicense.com/licenses/gpl-3.0/)
