"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """Render homepage."""

    return render_template('homepage.html')

@app.route('/movies')
def all_movies():
    """View all movies."""

    movies = crud.get_movies()

    return render_template('all_movies.html', jinja_movies=movies) # we changed movies_jinja from movies (in solution)

@app.route('/movies/<movie_id>')  #route with a variable URL
def show_movie(movie_id):
    """Show details on a particular movie."""

    movie = crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', jinja_movie=movie) # we changed movies_jinja from movies (in solution)

@app.route('/users')
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template('all_users.html', jinja_users=users) # we changed movies_jinja from movies (in solution)

@app.route('/users', methods=['POST'])
def register_user():
    """Create a new user."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash('Cannot create an account with that email. Try again.')
    else:
        crud.create_user(email, password)
        flash('Account created! Please log in.')

    return redirect('/')


@app.route('/users/<user_id>')  #route with a variable URL
def show_user(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', jinja_user=user)


@app.route('/handle-form-session')
def login():
    """ Handle session from users who created account already."""

    email = request.args.get('email')
    password = request.args.get('password')

    # print(f'email is {email} and password is {password}')

    user = crud.get_user_by_email(email)
    # if  user != None:
    #     print(f'DB email is {user.email} and password is {user.password}')

    if  user == None or password != user.password:
        flash("Email and password did not match our records. Please try again.")
    else:
        flash('Successfully logged in!')
        session['user_id'] = user.user_id
        print(f"HERE THIS THE SESSION{session['user_id']}")


    return redirect('/')



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
