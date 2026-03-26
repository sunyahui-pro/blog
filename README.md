# NEURAL.LOG - 技术备忘录博客

一个 Flask 构建的个人技术博客系统，支持 Markdown 富文本编辑、文章追加更新、代码高亮等功能。

## 功能特性

### 文章管理
- ✍️ **写文章** - 支持富文本编辑器（Quill），可粘贴图片、代码高亮
- 📝 **追加更新** - 文章支持多次追加更新，记录迭代过程
- 🗑️ **删除文章** - 支持删除文章及其所有更新
- 🔍 **搜索文章** - 支持按标题和内容搜索

### 首页展示
- 📚 **文章目录** - 侧边栏展示所有文章，支持展开/收起
- 🔄 **最近更新** - 展示最近更新的 3 篇文章
- 📊 **数据统计** - 显示总文章数、本周、本月文章数
- 📅 **系统日历** - 交互式日历，支持农历显示
- 💬 **每日名言** - 随机展示科技名人名言
- ☯️ **今日宜忌** - 程序员专属宜忌提示

### 特色功能
- 🌧️ **代码雨特效** - 发布文章后显示黑客帝国风格代码雨动画
- 🎨 **科技霓虹风格** - 暗色主题配合霓虹色点缀
- 📱 **响应式设计** - 适配桌面和移动端

## 运行环境

- Python 3.8+
- Flask 3.x
- SQLite 3

## 安装运行

### 1. 克隆项目
```bash
git clone https://github.com/sunyahui-pro/blog.git
cd blog
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 运行方式

#### 方式一：直接运行（开发环境）
```bash
python3 run.py
```
访问 http://127.0.0.1:5000

#### 方式二：守护进程运行（生产环境）
```bash
bash run.sh
```
守护进程会自动重启崩溃的服务。

#### 方式三：使用 Gunicorn（推荐生产环境）
```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

## 项目结构

```
blog/
├── app/                    # 应用主目录
│   ├── __init__.py        # 应用工厂
│   ├── models.py          # 数据模型
│   ├── routes/            # 路由模块
│   │   ├── main.py        # 首页、日历等
│   │   ├── post.py        # 文章相关
│   │   └── auth.py        # 登录认证
│   ├── templates/         # HTML 模板
│   │   ├── base.html      # 基础模板
│   │   ├── index.html     # 首页
│   │   ├── new.html       # 写文章
│   │   ├── append.html    # 追加更新
│   │   └── post.html      # 文章详情
│   └── static/            # 静态文件
│       ├── css/
│       ├── js/
│       └── uploads/       # 图片上传目录
├── config.py              # 配置文件
├── run.py                 # 启动入口
├── run.sh                 # 守护进程脚本
├── requirements.txt       # 依赖列表
└── blog.db               # SQLite 数据库
```

## 配置说明

编辑 `config.py` 可修改以下配置：

```python
# 管理员账号
ADMIN_USERNAME = 'feizi'
ADMIN_PASSWORD = 'feizi'

# 上传文件配置
UPLOAD_FOLDER = 'app/static/uploads'
MAX_CONTENT_LENGTH = 16MB
```

## Nginx 反向代理配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 技术栈

- **后端**: Flask + Flask-SQLAlchemy + Flask-Login
- **数据库**: SQLite
- **前端**: Bootstrap 5 + Quill Editor + Highlight.js
- **字体**: Orbitron + Rajdhani

## 登录信息

- 用户名: `feizi`
- 密码: `feizi`

## 更新日志

### 2026-03-26
- 重构项目结构，使用 Blueprint 模块化
- 添加代码雨发布特效
- 实现文章分页加载（每次 7 篇）
- 修复富文本编辑器，支持图片粘贴上传
- 添加守护进程自动重启

## License

MIT License
