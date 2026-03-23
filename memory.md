# 博客项目 - 肥子的记忆

## 项目概述
- **名称**: 个人博客系统
- **位置**: `/home/admin/.openclaw/workspace/blog/`
- **入口**: `app.py`
- **访问地址**: http://47.85.8.85/

## 技术栈
- **后端**: Flask (Python)
- **数据库**: SQLite
- **前端**: Bootstrap 5
- **编辑器**: Quill 富文本编辑器
- **代码高亮**: Highlight.js

## 部署架构
```
用户 → 47.85.8.85:80 → nginx → 127.0.0.1:5000 (Flask)
```

**nginx 配置**: `/etc/nginx/conf.d/blog.conf`
```nginx
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 核心功能

### 1. 文章管理
- 文章列表展示
- 文章详情页（支持 Markdown）
- 代码高亮显示

### 2. 追加更新功能
- 使用 Quill 富文本编辑器
- 支持在文章末尾追加内容
- 自动保存到数据库

**修复历史**:
- 2026-03-20: 修复两次，解决 Quill 异步加载导致的按钮无响应问题
- 改用 `form.onsubmit` 绑定事件，添加库加载检测

### 3. 导航栏设计
- 科技霓虹风格（Neon Style）
- 青色发光效果 + 悬停动画
- 特殊符号图标（◈ 首页、✦ 写入）

## 数据库结构
- **文件**: `blog.db`
- **表**: `posts` (id, title, content, created_at, updated_at)

## 重要文件
| 文件 | 说明 |
|-----|------|
| `app.py` | Flask 主程序 |
| `blog.db` | SQLite 数据库 |
| `templates/` | HTML 模板 |
| `static/` | CSS/JS 静态文件 |

## 已知问题
- ✅ 追加功能已修复，目前正常
- ✅ 导航栏样式已完成

## 待办事项
- [ ] 文章编辑功能
- [ ] 文章删除功能
- [ ] 搜索功能
- [ ] 分类/标签

## 修改历史

### 2026-03-20
- 修复追加更新功能（第二轮修复）
- 导航栏改成科技霓虹风格
- 服务重启验证通过

### 2026-03-21
- 确认公网访问正常 (http://47.85.8.85/)
