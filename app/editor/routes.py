from . import app
from flask import render_template, url_for, redirect
from config import blog_config
from forms import CreateArticleLoginForm
from app.models import Article


@app.route('/create', methods=['GET', 'POST'])
def create_article():

    context = {}

    form = CreateArticleLoginForm()
    if form.validate_on_submit():

        new_article = Article()

        new_article.title1 = form.title1.data
        new_article.title2 = form.title2.data
        new_article.slug = form.slug.data
        new_article.content = form.content.data
        new_article.published = True if form.status.data == 'published' else False
        new_article.isPost = True if form.page_type.data == 'post' else False

        new_article.put()

        return redirect(url_for('main.home'))

    else:
        pass

    return render_template('editor/create_article_page.html', context=context, form=form, blog_config=blog_config)
