from flask import Flask, render_template

app = Flask(__name__)

# Root route
@app.route('/')
def index():
    return render_template('create-account-names.html')

if __name__ == '__main__':
    app.run(debug=True)
