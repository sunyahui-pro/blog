from flask import Blueprint, render_template
from app.models import Post
from datetime import datetime, date
import calendar
import random

main = Blueprint('main', __name__)

# 科技名言库
TECH_QUOTES = [
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Code is like humor. When you have to explain it, it's bad.", "Cory House"),
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("Any fool can write code that a computer can understand.", "Martin Fowler"),
    ("Simplicity is the soul of efficiency.", "Austin Freeman"),
    ("Make it work, make it right, make it fast.", "Kent Beck"),
    ("The best error message is the one that never shows up.", "Thomas Fuchs"),
    ("Deleted code is debugged code.", "Jeff Sickel"),
    ("It's not a bug, it's a feature.", "Anonymous"),
]

# 风水宜忌数据
FENGSHUI_DATA = {
    'yi': ['编程', '写博客', '学习新技术', '重构代码', '部署上线'],
    'ji': ['改需求', '删库', '硬编码', '复制粘贴', '通宵加班']
}

def generate_calendar(year=None, month=None, selected_date=None):
    """生成交互式日历HTML"""
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month
    
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)
    month_names = ['', '一月', '二月', '三月', '四月', '五月', '六月', 
                   '七月', '八月', '九月', '十月', '十一月', '十二月']
    
    html = f'''
    <div class="calendar" id="calendar" data-year="{year}" data-month="{month}">
        <div class="calendar-header">
            <button type="button" onclick="changeMonth({year}, {month}, -1)">◀</button>
            <span>{year}年 {month_names[month]}</span>
            <button type="button" onclick="changeMonth({year}, {month}, 1)">▶</button>
        </div>
        <table class="calendar-table">
            <tr>
                <th>日</th><th>一</th><th>二</th><th>三</th><th>四</th><th>五</th><th>六</th>
            </tr>
    '''
    
    today = date.today()
    for week in month_days:
        html += '<tr>'
        for day in week:
            if day == 0:
                html += '<td></td>'
            else:
                classes = []
                if year == today.year and month == today.month and day == today.day:
                    classes.append('today')
                if selected_date and date(year, month, day) == selected_date:
                    classes.append('selected')
                
                html += f'''<td class="{' '.join(classes)}" onclick="selectDate({year}, {month}, {day})" data-date="{year}-{month:02d}-{day:02d}">
                    <div class="day-num">{day}</div>
                </td>'''
        html += '</tr>'
    
    html += '''</table></div>'''
    return html

@main.route('/')
def index():
    # 获取所有文章
    posts = Post.query.order_by(Post.created_at.desc()).all()
    all_posts = posts
    recent_posts = posts[:5]
    
    # 统计数据
    from sqlalchemy import func
    from app import db
    total = Post.query.count()
    
    # 本周文章数
    from datetime import timedelta
    week_start = datetime.now() - timedelta(days=datetime.now().weekday())
    week_count = Post.query.filter(Post.created_at >= week_start).count()
    
    # 本月文章数
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0)
    month_count = Post.query.filter(Post.created_at >= month_start).count()
    
    stats = {'total': total, 'week': week_count, 'month': month_count}
    
    # 随机名言和风水
    quote = random.choice(TECH_QUOTES)
    fengshui = {
        'yi': random.sample(FENGSHUI_DATA['yi'], 3),
        'ji': random.sample(FENGSHUI_DATA['ji'], 2)
    }
    
    # 日历
    cal_html = generate_calendar()
    
    return render_template('index.html', 
                         posts=posts, 
                         all_posts=all_posts, 
                         recent_posts=recent_posts,
                         stats=stats,
                         quote=quote,
                         fengshui=fengshui,
                         calendar=cal_html)

@main.route('/calendar')
def calendar_page():
    cal_html = generate_calendar()
    return render_template('calendar.html', calendar=cal_html)
