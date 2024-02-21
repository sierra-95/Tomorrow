#This runs the app.py on the backgorund  to serve the web pages.
sudo apt install gunicorn
pip install --upgrade gunicorn
nohup gunicorn -b 0.0.0.0:8000 -w 4 wsgi:app &
##run on terminal
nohup gunicorn -b 0.0.0.0:8000 -w 4 wsgi:app

##fore debug
gunicorn -b 0.0.0.0:8000 -w 4 --log-level=debug wsgi:app

#pkill
pkill -9 -f gunicorn

