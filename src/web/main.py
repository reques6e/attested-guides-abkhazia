import os
from flask import Flask, render_template

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'template'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<user_id>')
def user(user_id):
    return render_template('user.html', user_id=user_id)

@app.route('/docs')
def docs():
    return render_template('docs.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
