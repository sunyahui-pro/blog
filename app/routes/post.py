from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.models import Post, PostUpdate
from app import db
from datetime import datetime
import os
import re
import base64
from werkzeug.utils import secure_filename
from flask import current_app

bp = Blueprint('post', __name__)


@bp.route('/post/<int:id>')
def post_detail(id):
    """文章详情页"""
    post = Post.query.get_or_404(id)
    updates = PostUpdate.query.filter_by(post_id=id).order_by(PostUpdate.created_at.asc()).all()
    return render_template('post.html', post=post, updates=updates)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
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

        # 返回代码雨特效页面
        success_js = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UPLOAD COMPLETE - NEURAL.LOG</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; overflow: hidden; background: #000; }
    </style>
</head>
<body>
<div id="matrix-rain" style="position:fixed;top:0;left:0;width:100%;height:100%;background:#000;z-index:9999;display:flex;flex-direction:column;justify-content:center;align-items:center;font-family:'Orbitron',monospace;">
    <canvas id="matrix-canvas" style="position:absolute;top:0;left:0;"></canvas>
    <div id="upload-text" style="color:#0f0;font-size:2rem;z-index:10000;opacity:0;text-shadow:0 0 20px #0f0;letter-spacing:3px;">UPLOAD COMPLETE</div>
</div>
<script>
(function(){
    var canvas = document.getElementById('matrix-canvas');
    var ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    var chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
    var drops = [];
    var fontSize = 14;
    var columns = canvas.width / fontSize;
    for(var i = 0; i < columns; i++) drops[i] = Math.random() * -100;

    function draw() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#0f0';
        ctx.font = fontSize + 'px monospace';
        for(var i = 0; i < drops.length; i++) {
            var text = chars[Math.floor(Math.random() * chars.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            if(drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
    }

    var interval = setInterval(draw, 35);

    setTimeout(function() {
        document.getElementById('upload-text').style.transition = 'opacity 0.5s';
        document.getElementById('upload-text').style.opacity = '1';
    }, 1500);

    setTimeout(function() {
        clearInterval(interval);
        window.location.href = '/post/''' + str(post.id) + '''';
    }, 3000);
})();
</script>
</body>
</html>
'''
        return success_js

    return render_template('new.html')


@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_post(id):
    """删除文章"""
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('文章已删除', 'success')
    return redirect(url_for('main.index'))


@bp.route('/append/<int:id>', methods=['GET', 'POST'])
@login_required
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


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/upload', methods=['POST'])
@login_required
def upload_image():
    """处理图片上传（包括粘贴的图片）"""
    # 处理 base64 粘贴的图片
    if request.json and 'image' in request.json:
        image_data = request.json['image']
        # data:image/png;base64,xxxxx
        match = re.match(r'data:image/(\w+);base64,(.+)', image_data)
        if match:
            ext = match.group(1)
            data = match.group(2)
            filename = f"paste_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            with open(filepath, 'wb') as f:
                f.write(base64.b64decode(data))
            return jsonify({'url': f'/static/uploads/{filename}'})

    # 处理文件上传
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return jsonify({'url': f'/static/uploads/{filename}'})

    return jsonify({'error': '上传失败'}), 400
