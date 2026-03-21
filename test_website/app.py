import os
import sqlite3
import requests
from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = 'demo-super-secret-key'

DB_FILE = 'hiring.db'

# NOTE: Replace this with an actual API key generated from HashDocs dashboard
HASHDOCS_API_KEY = 'hd_9f9aaa459edf1529c283ad1884aa0dcf487b9bf3'
HASHDOCS_API_URL = 'http://127.0.0.1:8000/api/v1/verify/'


def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT NOT NULL,
                cert_hash TEXT NOT NULL,
                status TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        role = request.form.get('role', '').strip()
        cert_hash = request.form.get('cert_hash', '').strip()

        if not all([name, email, role, cert_hash]):
            flash('All fields are required.', 'error')
            return redirect('/')

        # Verify Certificate using HashDocs API
        try:
            response = requests.post(
                HASHDOCS_API_URL,
                headers={'X-API-Key': HASHDOCS_API_KEY},
                json={
                    'cert_hash': cert_hash,
                    'fields': {
                        'name': name,
                        'email': email
                    }
                },
                timeout=5
            )
            data = response.json()
            is_valid = data.get('valid', False)
            reason = data.get('reason', '')
            
            if is_valid:
                status = 'Hired! ✅ (Verified)'
                flash(f'Certificate Verified via HashDocs! {name} has been hired.', 'success')
            else:
                status = 'Rejected ❌ (Fake/Mismatched Cert)'
                flash(f'Certificate Verification Failed: {reason}', 'error')

        except Exception as e:
            status = 'Error ⚠️ (API Connection)'
            flash(f'Could not connect to verification server: {str(e)}', 'error')

        # Save to DB
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute(
                'INSERT INTO candidates (name, email, role, cert_hash, status) VALUES (?, ?, ?, ?, ?)',
                (name, email, role, cert_hash, status)
            )
        
        return redirect('/')

    # GET Request - show form and current candidates
    init_db()
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        candidates = conn.execute('SELECT * FROM candidates ORDER BY timestamp DESC LIMIT 10').fetchall()

    return render_template('index.html', candidates=candidates)


if __name__ == '__main__':
    print(f"Starting Demo Hiring Portal...")
    print(f"Using API Key: {HASHDOCS_API_KEY[:10]}***")
    print(f"Targeting HashDocs at: {HASHDOCS_API_URL}")
    app.run(port=5000, debug=True)
