#This runs the app.py on the backgorund  to serve the web pages.
pip install --upgrade gunicorn
nohup gunicorn -b 0.0.0.0:8000 -w 4 wsgi:app &
