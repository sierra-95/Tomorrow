sudo apt-get install tmux

#start tmux session
tmux
#run app
flask run --host=0.0.0.0 --port=8000
#detach from session
Ctrl+b d
#attach to session
tmux attach