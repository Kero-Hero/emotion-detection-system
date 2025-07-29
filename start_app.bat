@echo off
echo ============================================
echo 启动情绪识别系统
echo ============================================
echo.

echo 正在启动服务器...
echo 请在浏览器中打开: http://localhost:5000
echo.
echo 按 Ctrl+C 停止服务器
echo.

python emotion_detector.py

pause
