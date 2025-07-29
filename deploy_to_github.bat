@echo off
echo 正在部署情绪识别系统到GitHub...
echo.

echo 第一步：检查Git状态
git status
echo.

echo 第二步：添加所有文件
git add .
echo.

echo 第三步：提交更改
set /p commit_msg="请输入提交信息 (直接回车使用默认): "
if "%commit_msg%"=="" set commit_msg=更新情绪识别系统

git commit -m "%commit_msg%"
echo.

echo 第四步：请先在GitHub上创建仓库
echo 1. 访问 https://github.com/new
echo 2. 仓库名称: emotion-detection-system
echo 3. 选择 Public
echo 4. 点击 Create repository
echo.
pause

echo 第五步：请输入您的GitHub用户名
set /p username="GitHub用户名: "

echo.
echo 第六步：连接到GitHub仓库
git remote add origin https://github.com/%username%/emotion-detection-system.git
git branch -M main
git push -u origin main

echo.
echo 🎉 部署完成！
echo.
echo 📱 接下来的步骤：
echo 1. GitHub Pages: 在仓库设置中启用 Pages (Source: GitHub Actions)
echo 2. 云端部署: 可选择 Heroku、Railway 或 Render
echo.
echo 🌐 访问地址:
echo - GitHub Pages: https://%username%.github.io/emotion-detection-system
echo - 源码仓库: https://github.com/%username%/emotion-detection-system
echo.
pause
