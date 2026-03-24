from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Post, PostUpdate
from app import db
from datetime import datetime

bp = Blueprint('post', __name__)


@bp.route('/post/<int:id>')
def post_detail(id):
    """文章详情页"""
    post = Post.query.get_or_404(id)
    updates = PostUpdate.query.filter_by(post_id=id).order_by(PostUpdate.created_at.desc()).all()
    return render_template('post.html', post=post, updates=updates)


@bp.route('/new', methods=['GET', 'POST'])
def new_post():
    """新建文章"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        author = request.form.get('author', '主人').strip()

        if not title or not content:
            flash('标题和内容不能为空', 'error')
            return render_template('new.html')

        post = Post(
            title=title,
            content=content,
            author=author or '主人',
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.session.add(post)
        db.session.commit()

        flash('文章发布成功', 'success')
        return redirect(url_for('post.post_detail', id=post.id))

    return render_template('new.html')


@bp.route('/delete/<int:id>', methods=['POST'])
def delete_post(id):
    """删除文章"""
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('文章已删除', 'success')
    return redirect(url_for('main.index'))


@bp.route('/append/<int:id>', methods=['GET', 'POST'])
def append_update(id):
    """追加更新文章"""
    post = Post.query.get_or_404(id)

    if request.method == 'POST':
        content = request.form.get('content', '').strip()

        if not content:
            flash('更新内容不能为空', 'error')
            return render_template('append.html', post=post)

        update = PostUpdate(
            post_id=id,
            content=content,
            created_at=datetime.now()
        )
        db.session.add(update)

        post.updated_at = datetime.now()
        db.session.commit()

        flash('更新已添加', 'success')
        return redirect(url_for('post.post_detail', id=id))

    return render_template('append.html', post=post)


@bp.route('/search')
def search():
    """搜索文章"""
    query = request.args.get('q', '').strip()
    if not query:
        return render_template('search.html', posts=[], query='')

    posts = Post.query.filter(
        db.or_(
            Post.title.contains(query),
            Post.content.contains(query)
        )
    ).order_by(Post.created_at.desc()).all()

    return render_template('search.html', posts=posts, query=query)
