# 技术博客系统需求文档

## 1. 项目概述

### 1.1 项目目标
构建一个现代化的个人技术博客系统，支持文章管理、日历展示、数据统计等功能，采用前后端分离架构，支持Markdown编辑和富文本编辑双模式。

### 1.2 目标用户
- 个人技术博主
- 后端开发者
- 需要记录技术笔记的程序员

---

## 2. 功能需求

### 2.1 核心功能模块

#### 2.1.1 文章管理模块
| 功能点 | 详细描述 | 优先级 |
|--------|----------|--------|
| 文章列表 | 首页分页展示，支持按时间/分类排序 | P0 |
| 文章详情 | 独立页面，支持Markdown渲染、代码高亮 | P0 |
| 新建文章 | 双编辑器模式（Markdown/富文本），实时预览 | P0 |
| 编辑文章 | 支持修改已有文章内容和标题 | P0 |
| 删除文章 | 软删除机制，保留数据可恢复 | P0 |
| 文章分类 | 支持标签/分类管理 | P1 |
| 文章搜索 | 全文搜索，支持标题/内容/标签 | P0 |
| 文章草稿 | 自动保存草稿，支持手动保存 | P1 |

#### 2.1.2 更新记录模块
| 功能点 | 详细描述 | 优先级 |
|--------|----------|--------|
| 追加更新 | 为文章添加更新记录，独立显示 | P0 |
| 更新历史 | 按时间线展示所有更新 | P0 |
| 版本对比 | 查看文章历史版本差异 | P2 |

#### 2.1.3 日历模块
| 功能点 | 详细描述 | 优先级 |
|--------|----------|--------|
| 月历展示 | 交互式日历，显示当前月份 | P0 |
| 月份切换 | 支持上一月/下一月切换 | P0 |
| 日期标记 | 有文章的日期高亮显示 | P1 |
| 农历显示 | 显示农历日期和传统节日 | P1 |
| 日期筛选 | 点击日期筛选当天文章 | P2 |

#### 2.1.4 数据统计模块
| 功能点 | 详细描述 | 优先级 |
|--------|----------|--------|
| 总文章数 | 统计所有文章数量 | P0 |
| 本周新增 | 本周发布文章统计 | P0 |
| 本月新增 | 本月发布文章统计 | P0 |
| 年度统计 | 按年份统计文章分布 | P1 |
| 分类统计 | 按分类统计文章数量 | P1 |

#### 2.1.5 趣味功能模块
| 功能点 | 详细描述 | 优先级 |
|--------|----------|--------|
| 每日名言 | 随机展示科技名言 | P0 |
| 今日宜忌 | 随机生成宜做/忌做的事 | P0 |
| 程序员黄历 | 基于日期的趣味提示 | P1 |

#### 2.1.6 用户认证模块
| 功能点 | 详细描述 | 优先级 |
|--------|----------|--------|
| 登录 | 单用户系统，JWT Token认证 | P0 |
| 登出 | 清除登录状态 | P0 |
| 权限控制 | 文章管理需登录，列表可公开访问 | P0 |
| 密码修改 | 支持修改登录密码 | P2 |

---

## 3. 技术栈选型

### 3.1 方案对比

| 方案 | 前端 | 后端 | 数据库 | 优点 | 缺点 |
|------|------|------|--------|------|------|
| **方案A：现代化全栈** | Next.js 14 + React Server Components | Next.js API Routes / 独立后端 | PostgreSQL + Redis | SSR性能好，SEO友好，现代化架构 | 学习成本高，部署复杂 |
| **方案B：前后端分离** | Vue 3 + Vite | FastAPI / Django | MySQL 8.0 | 开发效率高，生态丰富 | 需要维护两套代码 |
| **方案C：精简版（当前）** | Jinja2模板 + Bootstrap | Flask | MySQL | 简单快速，易于维护 | 前端交互受限，SEO一般 |
| **方案D：静态站点** | Astro / Hugo | 无（静态生成） | Markdown文件 | 性能极佳，部署简单 | 动态功能受限 |

### 3.2 推荐方案：方案B（前后端分离）

**推荐理由：**
- 适合个人博客，开发效率高
- 前后端可独立部署和扩展
- 生态丰富，文档完善
- 肥子熟悉这套技术栈

---

## 4. 详细技术架构

### 4.1 前端技术栈

```
框架：Vue 3.4 + TypeScript
构建工具：Vite 5
UI框架：Element Plus / Ant Design Vue
状态管理：Pinia
路由：Vue Router 4
HTTP客户端：Axios
编辑器：
  - Markdown: Milkdown / Toast UI Editor
  - 富文本: Editor.js / Quill (保留)
代码高亮：Shiki / Prism.js
图表：ECharts（数据统计）
日历组件：FullCalendar / 自定义
CSS：Tailwind CSS + UnoCSS
图标：Iconify
```

### 4.2 后端技术栈

```
框架：FastAPI 0.110 (Python 3.11+)
ORM：SQLAlchemy 2.0 + Alembic（迁移）
数据库：
  - 主库：MySQL 8.0
  - 缓存：Redis 7
任务队列：Celery + Redis
搜索：Meilisearch / MySQL全文搜索
文件存储：本地 / MinIO / 阿里云OSS
认证：JWT (python-jose) + Passlib
API文档：自动生成 OpenAPI/Swagger
测试：Pytest + HTTPX
```

### 4.3 部署架构

```
生产环境：
  - Web服务器：Nginx（反向代理 + 静态文件）
  - 应用服务器：Uvicorn (ASGI) + Gunicorn
  - 数据库：MySQL 8.0
  - 缓存：Redis
  - 容器化：Docker + Docker Compose

CI/CD：
  - GitHub Actions / GitLab CI
  - 自动测试 + 自动部署

监控：
  - 日志：Loki + Grafana
  - 指标：Prometheus + Grafana
  - 告警：AlertManager
```

---

## 5. 数据库设计

### 5.1 实体关系

```
User (用户)
  - id: PK
  - username: unique
  - password_hash
  - email
  - created_at
  - updated_at

Post (文章)
  - id: PK
  - title
  - content (HTML/Markdown)
  - content_type: enum ['markdown', 'html']
  - author_id: FK -> User
  - status: enum ['draft', 'published', 'archived']
  - view_count
  - created_at
  - updated_at
  - published_at

PostUpdate (文章更新)
  - id: PK
  - post_id: FK -> Post
  - content
  - created_at

Category (分类)
  - id: PK
  - name
  - slug
  - description
  - created_at

PostCategory (文章分类关联)
  - post_id: FK
  - category_id: FK

Tag (标签)
  - id: PK
  - name
  - slug

PostTag (文章标签关联)
  - post_id: FK
  - tag_id: FK

Media (媒体文件)
  - id: PK
  - filename
  - original_name
  - mime_type
  - size
  - url
  - created_at
```

---

## 6. API设计

### 6.1 RESTful API规范

```
GET    /api/v1/posts          # 文章列表
GET    /api/v1/posts/:id      # 文章详情
POST   /api/v1/posts          # 创建文章
PUT    /api/v1/posts/:id      # 更新文章
DELETE /api/v1/posts/:id      # 删除文章

GET    /api/v1/posts/:id/updates  # 文章更新记录
POST   /api/v1/posts/:id/updates  # 追加更新

GET    /api/v1/categories     # 分类列表
GET    /api/v1/tags           # 标签列表

GET    /api/v1/stats          # 统计数据
GET    /api/v1/calendar       # 日历数据

POST   /api/v1/auth/login     # 登录
POST   /api/v1/auth/logout    # 登出
POST   /api/v1/auth/refresh   # 刷新Token

POST   /api/v1/upload         # 文件上传
```

---

## 7. 界面设计

### 7.1 页面清单

| 页面 | 路径 | 说明 |
|------|------|------|
| 首页 | / | 文章列表 + 侧边栏 |
| 文章详情 | /post/:id | 文章内容 + 更新记录 |
| 新建文章 | /new | 编辑器页面 |
| 编辑文章 | /edit/:id | 编辑器页面 |
| 搜索 | /search?q= | 搜索结果页 |
| 分类 | /category/:slug | 分类文章列表 |
| 标签 | /tag/:slug | 标签文章列表 |
| 归档 | /archive | 按时间归档 |
| 登录 | /login | 登录页面 |
| 管理后台 | /admin | 文章管理、数据统计 |

### 7.2 主题设计

```
风格：科技霓虹 (Cyberpunk Tech)
主色调：
  - 青色: #00f0ff (霓虹主色)
  - 粉色: #ff00a0 (强调色)
  - 紫色: #b829dd (辅助色)
  - 深蓝: #0080ff
背景色：
  - 深色背景: #0a0a0f
  - 卡片背景: #12121a
字体：
  - 标题: Orbitron (科技感)
  - 正文: Rajdhani / Inter
特效：
  - 霓虹发光效果
  - 扫描线动画
  - 故障(Glitch)效果
  - 打字机效果
```

---

## 8. 非功能需求

### 8.1 性能要求
- 首屏加载 < 2s
- API响应 < 200ms (P95)
- 支持并发 100+ 用户

### 8.2 安全要求
- HTTPS强制
- SQL注入防护
- XSS防护
- CSRF防护
- 密码加密存储
- JWT Token安全

### 8.3 可维护性
- 代码注释覆盖率 > 80%
- 单元测试覆盖率 > 70%
- API文档自动生成
- 日志分级记录

---

## 9. 开发计划

### 阶段1：基础架构 (2周)
- [ ] 项目初始化
- [ ] 数据库设计
- [ ] 后端API开发
- [ ] 前端基础框架

### 阶段2：核心功能 (2周)
- [ ] 文章CRUD
- [ ] 用户认证
- [ ] 编辑器集成
- [ ] 基础UI

### 阶段3：高级功能 (1周)
- [ ] 日历功能
- [ ] 数据统计
- [ ] 搜索功能
- [ ] 文件上传

### 阶段4：优化部署 (1周)
- [ ] 性能优化
- [ ] 主题美化
- [ ] Docker部署
- [ ] 文档完善

---

## 10. 风险评估

| 风险 | 影响 | 应对措施 |
|------|------|----------|
| 编辑器兼容性 | 高 | 充分测试，准备备选方案 |
| 数据库迁移 | 中 | 使用Alembic，做好备份 |
| SEO效果 | 中 | 使用SSR或预渲染 |
| 部署复杂度 | 低 | 提供Docker Compose配置 |

---

**文档版本：** v1.0  
**编写日期：** 2026-03-24  
**编写者：** 肥子 🐷
