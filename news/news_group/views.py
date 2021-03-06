from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from news import db
from news.models import News, Comment, Likes
from news.news_group.forms import NewsForm, CommentForm, LikesForm, DislikesForm, SearchForm
from news.picture_handlers import add_news_pic

news_group = Blueprint('news_group', __name__)


# create news manually
@news_group.route('/create', methods=['GET', 'POST'])
@login_required
def create_news():
    form = NewsForm()

    if form.validate_on_submit():
        new_news = News(title=form.title_news.data,
                        text=form.text_news.data, user_id=current_user.id,
                        picture_link=form.picture_link.data, link=form.link.data)

        db.session.add(new_news)
        db.session.commit()
        flash('News Created')
        return redirect(url_for('core.index'))

    return render_template('create_news.html', form=form)

# view news
@news_group.route('/news/<int:news_id>', methods=['GET', 'POST'])
def news_view(news_id):
    form_comment = CommentForm()
    form_likes = LikesForm()
    form_dislikes = DislikesForm()
    news_view = News.query.get_or_404(news_id)
    like = Likes.query.filter_by(
        user_id=current_user.id, news_id=news_id).first()

    if form_comment.submit_comment.data and form_comment.validate():

        comment = Comment(text=form_comment.text.data, news_id=news_id,
                          user_name=current_user.username)

        db.session.add(comment)
        db.session.commit()
        flash('Comment Added')
        return redirect(url_for('news_group.news_view', news_id=news_id))

    if form_likes.submit_like.data and form_likes.validate():
        new_like = Likes(user_id=current_user.id, news_id=news_id)
        news_view.likes += 1
        db.session.add(new_like)
        db.session.commit()
        return redirect(url_for('news_group.news_view', news_id=news_id))

    if form_dislikes.submit_dislike.data and form_dislikes.validate():
        news_view.likes -= 1
        db.session.delete(like)
        db.session.commit()
        return redirect(url_for('news_group.news_view', news_id=news_id))

    comments = Comment.query.order_by(
        Comment.date.desc()).filter_by(news_id=news_id)

    return render_template('view_news.html', title=news_view.title, date=news_view.date, news=news_view, form_comment=form_comment, form_likes=form_likes, form_dislikes=form_dislikes, comments=comments, news_id=news_id, like=like)


# update news
@news_group.route("/<int:news_id>/update", methods=['GET', 'POST'])
@login_required
def update(news_id):
    new_news = News.query.get_or_404(news_id)
    if new_news.author != current_user:

        abort(403)

    form = NewsForm()
    if form.validate_on_submit():
        new_news.title = form.title_news.data
        new_news.text = form.text_news.data
        new_news.picture_link = form.picture_link.data
        db.session.commit()
        flash('News Updated')
        return redirect(url_for('news_group.news_view', news_id=new_news.id))

    elif request.method == 'GET':
        form.title_news.data = new_news.title
        form.text_news.data = new_news.text
        form.picture_link.data = new_news.picture_link
        form.link.data = new_news.link
    return render_template('create_news.html', title='Update', form=form)

# delete news
@news_group.route('/<int:news_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_news(news_id):
    news = News.query.get_or_404(news_id)

    if news.author != current_user:
        abort(403)

    db.session.delete(news)
    db.session.commit()
    flash('News Deleted')
    return redirect(url_for('core.index'))


@news_group.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    search_word = request.args['search_word']
    found_news = News.query.filter(News.title.like(
        '%' + search_word + '%'))

    return render_template('search.html', found_news=found_news)
