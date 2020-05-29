1) Go to the folder named 'flask_app':

cd flask_app

2) Create a venv folder:

python3 -m venv venv

3) Active the environment:

. venv/bin/activate

4) Within the activated environment, use the following command to install Flask:

pip install Flask

5) Notice that within the activated environment you can use pip to install other packages too.

6) To initialize the database:

flask init-db

7) To run the app in development mode:

export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

