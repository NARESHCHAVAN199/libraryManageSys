from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulate a basic database with dictionaries
users_db = {}  # Dictionary to store users: {username: password}
books_db = {}  # Dictionary to store books: {book_id: {details}}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users_db and users_db[username] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users_db:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            users_db[username] = password
            flash(f'Account created successfully for {username}.', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', books=books_db)

@app.route('/add_book', methods=['POST'])
def add_book():
    if 'username' not in session:
        return redirect(url_for('login'))

    book_id = request.form['book_id']
    title = request.form['title']
    author = request.form['author']
    year = request.form['year']

    if book_id in books_db:
        flash(f'Book ID {book_id} already exists. Please use a unique ID.', 'danger')
    else:
        books_db[book_id] = {'Title': title, 'Author': author, 'Year': year}
        flash(f"Book '{title}' added successfully.", 'success')

    return redirect(url_for('dashboard'))

@app.route('/remove_book/<book_id>', methods=['GET'])
def remove_book(book_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    if book_id in books_db:
        removed_book = books_db.pop(book_id)
        flash(f"Book '{removed_book['Title']}' removed successfully.", 'success')
    else:
        flash(f"Book with ID {book_id} not found.", 'danger')

    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
