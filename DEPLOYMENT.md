# 部署指南

本指南将帮助您将情绪识别系统部署到GitHub和云平台上。

## 📋 部署清单

✅ 已创建的文件：
- `.gitignore` - Git忽略文件
- `.github/workflows/deploy.yml` - GitHub Actions自动部署
- `Procfile` - Heroku部署配置
- `runtime.txt` - Python版本说明
- `app.py` - 云端演示版本
- `templates/demo.html` - 演示页面

## 🚀 GitHub部署步骤

### 1. 创建GitHub仓库

1. 打开 [GitHub](https://github.com)
2. 点击 "New repository"
3. 仓库名称：`emotion-detection-system`
4. 选择 "Public"
5. 点击 "Create repository"

### 2. 上传代码到GitHub

在项目目录中运行以下命令：

```bash
# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "Initial commit: 情绪识别系统"

# 连接到GitHub仓库（替换为您的用户名）
git remote add origin https://github.com/您的用户名/emotion-detection-system.git

# 推送代码
git push -u origin main
```

### 3. 启用GitHub Pages

1. 在GitHub仓库页面，点击 "Settings"
2. 滚动到 "Pages" 部分
3. 在 "Source" 下选择 "GitHub Actions"
4. 等待自动部署完成

🌐 **GitHub Pages地址**: `https://您的用户名.github.io/emotion-detection-system`

## ☁️ 云平台部署选项

### 选项1: Heroku部署

1. 注册 [Heroku](https://heroku.com) 账号
2. 安装 Heroku CLI
3. 在项目目录运行：

```bash
# 登录Heroku
heroku login

# 创建应用
heroku create 您的应用名称

# 推送到Heroku
git push heroku main

# 打开应用
heroku open
```

### 选项2: Railway部署

1. 访问 [Railway](https://railway.app)
2. 使用GitHub账号登录
3. 点击 "New Project" → "Deploy from GitHub repo"
4. 选择您的仓库
5. 自动部署完成

### 选项3: Render部署

1. 访问 [Render](https://render.com)
2. 连接GitHub账号
3. 选择您的仓库
4. 选择 "Web Service"
5. 构建命令：`pip install -r requirements.txt`
6. 启动命令：`python app.py`

## 📱 部署版本说明

### 本地完整版
- 文件：`simple_emotion_detector.py`
- 功能：摄像头实时检测
- 适用：本地开发测试

### 云端演示版
- 文件：`app.py`
- 功能：模拟数据演示
- 适用：云端部署展示

## 🔧 部署后配置

### 1. 更新README.md

在GitHub仓库中更新README.md，添加在线演示链接：

```markdown
## 🌐 在线演示

- **GitHub Pages**: https://您的用户名.github.io/emotion-detection-system
- **云端应用**: https://您的应用.herokuapp.com (如果使用Heroku)
```

### 2. 自定义域名（可选）

如果您有自己的域名：

1. 在GitHub Pages设置中添加自定义域名
2. 在DNS提供商处添加CNAME记录

## 📊 部署验证

部署完成后，请验证以下功能：

- ✅ 页面正常加载
- ✅ 演示数据正常更新
- ✅ 响应式设计在移动设备上正常工作
- ✅ 所有按钮和链接正常工作

## 🆘 常见问题

### Q: GitHub Actions部署失败
A: 检查workflows文件语法，确保权限设置正确

### Q: Heroku部署超时
A: 检查requirements.txt中的依赖包，移除不必要的包

### Q: 页面显示空白
A: 检查浏览器开发者工具的控制台错误信息

## 🔄 持续更新

要更新部署的应用：

```bash
# 修改代码后
git add .
git commit -m "更新功能"
git push origin main

# GitHub Pages会自动重新部署
# 其他平台也会自动检测更新
```

## 📞 技术支持

如果在部署过程中遇到问题，可以：

1. 检查GitHub Actions的构建日志
2. 查看云平台的应用日志
3. 确认所有依赖包都在requirements.txt中

---

🎉 **恭喜！您的情绪识别系统现在已经部署到互联网上了！**
