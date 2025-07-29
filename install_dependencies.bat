@echo off
echo ============================================
echo 情绪识别系统 - 环境配置脚本
echo ============================================
echo.

echo [1/4] 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo.
echo [2/4] 升级pip...
python -m pip install --upgrade pip

echo.
echo [3/4] 安装依赖包...
echo 正在安装OpenCV...
pip install opencv-python==4.8.1.78

echo 正在安装TensorFlow...
pip install tensorflow==2.13.0

echo 正在安装Flask...
pip install flask==2.3.3

echo 正在安装其他依赖...
pip install numpy==1.24.3
pip install pillow==10.0.1
pip install fer==22.4.0

echo.
echo [4/4] 验证安装...
python -c "import cv2; print('OpenCV版本:', cv2.__version__)"
python -c "import tensorflow as tf; print('TensorFlow版本:', tf.__version__)"
python -c "import flask; print('Flask版本:', flask.__version__)"
python -c "import fer; print('FER情绪检测库安装成功')"

echo.
echo ============================================
echo 安装完成！
echo ============================================
echo.
echo 运行方式:
echo 1. 双击运行 start_app.bat
echo 2. 或者在命令行运行: python emotion_detector.py
echo 3. 然后在浏览器打开: http://localhost:5000
echo.
echo 注意事项:
echo - 请确保摄像头已连接并可正常使用
echo - 首次运行可能需要下载模型文件，请保持网络连接
echo - 建议在光线充足的环境下使用以获得更好的检测效果
echo.
pause
