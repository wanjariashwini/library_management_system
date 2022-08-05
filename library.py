from flask import *
from library_service import *

app = Flask(__name__)
app.secret_key = 'abc'


@app.route('/')
def login():
    return render_template('home.html')


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['email'] or not request.form['id'] or not request.form['password']:
            flash('Please enter all the fields', 'error')
            return "enter correct details"
        else:
            LibraryService.student_registration_details(request.form['name'], request.form['email'],
                                                        request.form['id'], request.form['password'])
            # flash('Student details successfully added')
            return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/library', methods=['POST'])
def library():
    if request.method == 'POST':
        if not request.form['student_id'] or not request.form['password']:
            flash('Please enter details', 'error')
        else:
            status = LibraryService.check_authority(request.form['student_id'], request.form['password'])
            print(status)
            print(request.form['student_id'])
            if status == "True":
                flash('Student login successfully')
                return render_template('library.html')
            else:
                flash('Enter correct details')
                return redirect(url_for('welcome'))


@app.route('/addBookDetails', methods=['POST'])
def add_book():
    if request.method == 'POST':
        if request.form:
            book_id = request.form.get('book_id')
            title = request.form.get('title')
            author = request.form.get('author')
            quantity = request.form.get('quantity')
            status = request.form.get('status')
            message = LibraryService.register_book(book_id, title, author, quantity, status)
        else:
            message = 'Please enter book details'

        return render_template('book_registration.html', message=message)


@app.route('/BookList', methods=['GET', 'POST'])
def book_list():
    books_list = LibraryService.registered_book_details()
    return render_template('books_list.html', books_list=books_list)


@app.route('/deleteBook', methods=['POST'])
def delete_book():
    if request.method == 'POST':
        if request.form:
            book_id = request.form.get('book_id')
            message = LibraryService.remove_book(book_id)
        else:
            message = 'Please enter book details to delete'

        return render_template('delete_book.html', message=message)


@app.route('/issueBook', methods=['POST'])
def issue_book():
    if request.method == 'POST':
        if request.form:
            book_id = request.form.get('book_id')
            student_name = request.form.get('student_name')
            message = LibraryService.get_book(book_id, student_name)
        else:
            message = 'Please enter valid book ID'

        return render_template('issue_book.html', message=message)


@app.route('/returnBook', methods=['POST'])
def return_book(book_id):
    if request.method == 'POST':
        if request.form:
            book_id = request.form.get(book_id)
            message = LibraryService.return_books(book_id)
        else:
            message = 'Please enter valid book ID'

        return render_template('return_book.html', message=message)


if __name__ == '__main__':
    app.run(host="localhost", port="5004", debug=True)
