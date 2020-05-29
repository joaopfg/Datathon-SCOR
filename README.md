# Datathon-SCOR
Web app and data treatment for datathon organized by SCOR

### Using the script get_data.py to get all the data from NHANES website
It's necessary to have the following python libraries installed on your machine: os, re and BeautifulSoup. If you don't have some of them you can install it through pip.
Then just run it as a common python program:
```
python3 get_data.py
```
It will automatically create adequate folders and install the corresponding files in each folder.

### Merging the data using the R scripts which are inside the "Merging" folder
You need to create a "Member Data" inside the "Merging folder" with the NHANES data you want to use for your analyses. The format of the files and folders inside it are given as example for a particular subset of NHANES dataset.
The installation of the needed libraries are commented in the code. If you don't have some of them installed on your machine, just uncomment the corresponding part.
Firstly, run the script 1_Mortality_Data.R:
```
Rscript 1_Mortality_Data.R
```
This script will merge the mortality data from NCHS website.
Then, run the script 2_2_Member_Data.R:
```
Rscript 2_2_Member_Data.R
```
This script will download the description files from NHANES website, use them to code the variables located in "Member Data" folder and merge them. The "download" part is commented. If you are running the script for the first time, uncomment the lines which refer to downloads.
Finally, run the script 3_Merge_Member_Mortality.R:
```
3_Merge_Member_Mortality.R
```
This script will merge the NHANES data and the mortality data.
At each part, a .csv file is generated with the corresponding merged dataset. 

### About the app code
The app has python backend (using Flask framework) and HTML/CSS frontend (using Jinja templates).
The backend calls the compressed machine learning models via python's pickle module and a SQL database is used to store user data and transfer it to the other views in the app.

### Creating an environment
Create a project folder and a venv folder within:

```mkdir myproject
cd myproject
python3 -m venv venv
```

On Windows:

```py -3 -m venv venv```

If you needed to install virtualenv because you are using Python 2, use the following command instead:

```python2 -m virtualenv venv```

On Windows:

```\Python27\Scripts\virtualenv.exe venv```

### Activating the environment
Before you run the app, activate the corresponding environment:

```. venv/bin/activate```

On Windows:

```venv\Scripts\activate```

Your shell prompt will change to show the name of the activated environment.

### Running the app

You can run the application using the flask command. From the terminal, tell Flask where to find the application, then run it in development mode. Remember, you should still be in the top-level directory, not the flaskr package.

Development mode shows an interactive debugger whenever a page raises an exception, and restarts the server whenever you make changes to the code. You can leave it running and just reload the browser page as you do changes in the code.

For Linux and Mac:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

For Windows cmd, use set instead of export:

```bash
> set FLASK_APP=flaskr
> set FLASK_ENV=development
> flask run
```

For Windows PowerShell, use $env: instead of export:

```bash
> $env:FLASK_APP = "flaskr"
> $env:FLASK_ENV = "development"
> flask run
```

You’ll see output similar to this:

```bash
* Serving Flask app "flaskr"
* Environment: development
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 855-212-761
```

### Initializing the database
The application uses a SQLite database to store the data provided by the user. Python comes with built-in support for SQLite in the *sqlite3* module.

To initialize the database, run the *init-db* command:

```bash
$ flask init-db
```

You should see the message *Initialized the database* on the terminal.

There will now be a *flaskr.sqlite* file in the instance folder in your project.
