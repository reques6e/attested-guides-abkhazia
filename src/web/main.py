import os
import hmac

from hashlib import sha256
from flask import Flask, render_template, request, redirect, url_for, session, make_response

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'template'))
app.secret_key = 'supersecretkey'
app.config['SESSION_COOKIE_SECURE'] = True 
app.config['SESSION_COOKIE_HTTPONLY'] = True  
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  

SECRET_SALT = os.urandom(16)

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

############################################################################
#                               ADMIN PANEL
############################################################################
ADMIN_CREDENTIALS = {'username': 'admin', 'password': 'test'}

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_CREDENTIALS['username'] and password == ADMIN_CREDENTIALS['password']:
            session['logged_in'] = True
            
            user_hash = hmac.new(
                SECRET_SALT,
                f"{username}{password}".encode(),
                sha256
            ).hexdigest()
            
            return f"""
            <!DOCTYPE html>
            <html>
            <body>
                <script>
                    localStorage.setItem('auth_hash', '{user_hash}');
                    window.location.href = '{url_for('dashboard')}';
                </script>
            </body>
            </html>
            """
        else:
            return render_template('admin/login.html', error='Неверный логин или пароль')
    
    return render_template('admin/login.html')

@app.route('/admin/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('admin_login'))
    return render_template('admin/dashboard.html')

@app.route('/admin/docs', methods=['GET', 'POST'])
def admin_docs():
    if 'logged_in' in session:  
        return render_template('admin/docs.html', is_authenticated='logged_in' in session)
    
@app.route('/admin/logout')
def logout():
    session.clear()
    
    response = make_response(redirect(url_for('admin_login')))
    
    response.set_cookie('auth_hash', '', expires=0)  # Удаляем cookie auth_hash
    response.set_cookie('session', '', expires=0)    # Удаляем session cookie
    
    response.headers['Cache-Control'] = 'no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
