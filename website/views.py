from flask import Blueprint, render_template, session
from flask import request
from .api import get_manga_by_name, get_manga_by_id


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/mylist')
def mylist():
    return render_template('mylist.html')

@views.route('/search', methods=('GET', 'POST'))
def search():
    results=False
    data=False
    if request.method == 'POST':
        data = request.form.get('search-input')
        # follow = false
        results = get_manga_by_name(data)
        
    return render_template('search.html', results=results)

@views.route('/search/<id>', methods=('GET', 'POST'))
def search_manga(id):
    results = get_manga_by_id(id)
    return render_template('manga.html', result=results)

@views.route('/follow/<id>', methods=('GET', 'POST'))
def follow(id):
    results = get_manga_by_name(id)
    return render_template('search.html', results=results)