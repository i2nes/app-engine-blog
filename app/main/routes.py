from . import app
from flask import render_template


@app.route('/')
def home():

    context = {
        'title': 'Clean Blog - Start Bootstrap Theme'
    }

    return render_template('main/home_page.html', context=context)


@app.route('about/')
def about():

    context = {
        'title': 'About Page'
    }

    return render_template('main/about_page.html', context=context)


@app.route('contact/')
def contact():

    context = {
        'title': 'Contact Page'
    }

    return render_template('main/contact_page.html', context=context)


@app.route('post/')
def post():

    context = {
        'title': 'Post Page'
    }

    return render_template('main/post_page.html', context=context)


@app.app_errorhandler(404)
def page_not_found(e):

    context = {
        'title': 'Page Not Found'
    }

    return render_template('main/404.html', context=context), 404


@app.app_errorhandler(500)
def page_not_found(e):

    context = {
        'title': 'Server Error'
    }

    return render_template('main/500.html', context=context), 500
