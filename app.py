import os
import sqlite3
import csv
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'super_secret_esports_key'
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__name__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            bgmi_id TEXT NOT NULL,
            in_game_name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            team_name TEXT NOT NULL,
            email TEXT NOT NULL,
            num_players INTEGER NOT NULL,
            payment_screenshot TEXT NOT NULL,
            p1_dept TEXT NOT NULL,
            p1_class TEXT NOT NULL,
            p2_name TEXT NOT NULL,
            p2_game_id TEXT NOT NULL,
            p2_dept TEXT NOT NULL,
            p2_class TEXT NOT NULL,
            p3_name TEXT NOT NULL,
            p3_game_id TEXT NOT NULL,
            p3_dept TEXT NOT NULL,
            p3_class TEXT NOT NULL,
            p4_name TEXT NOT NULL,
            p4_game_id TEXT NOT NULL,
            p4_dept TEXT NOT NULL,
            p4_class TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        player_name = request.form['player_name']
        bgmi_id = request.form['bgmi_id']
        in_game_name = request.form['in_game_name']
        phone_number = request.form['phone_number']
        team_name = request.form['team_name']
        email = request.form['email']
        num_players = request.form['num_players']
        p1_dept = request.form['p1_dept']
        p1_class = request.form['p1_class']
        p2_name = request.form['p2_name']
        p2_game_id = request.form['p2_game_id']
        p2_dept = request.form['p2_dept']
        p2_class = request.form['p2_class']
        p3_name = request.form['p3_name']
        p3_game_id = request.form['p3_game_id']
        p3_dept = request.form['p3_dept']
        p3_class = request.form['p3_class']
        p4_name = request.form['p4_name']
        p4_game_id = request.form['p4_game_id']
        p4_dept = request.form['p4_dept']
        p4_class = request.form['p4_class']
        
        # Check if the post request has the file part
        if 'payment_screenshot' not in request.files:
            flash('No payment screenshot provided.')
            return redirect(request.url)
        file = request.files['payment_screenshot']
        
        if file.filename == '':
            flash('No selected file.')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Save to database
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('''
                INSERT INTO registrations (
                    player_name, bgmi_id, in_game_name, phone_number, team_name, email, num_players, payment_screenshot,
                    p1_dept, p1_class, p2_name, p2_game_id, p2_dept, p2_class,
                    p3_name, p3_game_id, p3_dept, p3_class, p4_name, p4_game_id, p4_dept, p4_class
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                player_name, bgmi_id, in_game_name, phone_number, team_name, email, num_players, filename,
                p1_dept, p1_class, p2_name, p2_game_id, p2_dept, p2_class,
                p3_name, p3_game_id, p3_dept, p3_class, p4_name, p4_game_id, p4_dept, p4_class
            ))
            conn.commit()
            conn.close()
            
            flash('Registration successful!')
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/rules')
def rules():
    return render_template('rules.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Simulated contact form submission
        flash('Thank you for contacting us!')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'logged_in' in session:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM registrations')
        registrations = c.fetchall()
        conn.close()
        return render_template('admin.html', registrations=registrations, logs=True)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials')
            return render_template('admin.html', login=True)

    return render_template('admin.html', login=True)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin'))

@app.route('/delete/<int:id>')
def delete(id):
    if 'logged_in' in session:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('DELETE FROM registrations WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash('Entry deleted successfully.')
    return redirect(url_for('admin'))

@app.route('/download_csv')
def download_csv():
    if 'logged_in' in session:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM registrations')
        registrations = c.fetchall()
        column_names = [description[0] for description in c.description]
        conn.close()
        
        csv_file_path = os.path.join(app.root_path, 'registrations.csv')
        with open(csv_file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(column_names)
            writer.writerows(registrations)
            
        return send_file(csv_file_path, as_attachment=True)
    return redirect(url_for('admin'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
