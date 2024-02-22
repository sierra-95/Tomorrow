sudo apt install python3-pip 
pip install flask
pip install Flask-Mail
pip install Flask-Bcrypt
pip install mysql-connector-python

#Running
set FLASK_APP=app.py
set FLASK_ENV=development
flask run

#nohup
nohup flask run --host=0.0.0.0 --port=8000 &

