"""
系统测试脚本
用于验证所有组件是否正常工作
"""

import sys
import importlib
import subprocess

def test_imports():
    """测试依赖包导入"""
    print("=" * 50)
    print("测试依赖包导入...")
    print("=" * 50)
    
    required_packages = [
        ('cv2', 'OpenCV'),
        ('numpy', 'NumPy'),
        ('flask', 'Flask'),
        ('PIL', 'Pillow')
    ]
    
    failed_packages = []
    
    for package, name in required_packages:
        try:
            importlib.import_module(package)
            print(f"✓ {name} 导入成功")
        except ImportError:
            print(f"✗ {name} 导入失败")
            failed_packages.append(name)
    
    # 测试可选包
    try:
        importlib.import_module('fer')
        print("✓ FER (高级情绪识别) 导入成功")
        advanced_available = True
    except ImportError:
        print("⚠ FER (高级情绪识别) 导入失败，将使用简化版本")
        advanced_available = False
    
    try:
        importlib.import_module('tensorflow')
        print("✓ TensorFlow 导入成功")
    except ImportError:
        print("⚠ TensorFlow 导入失败")
    
    return len(failed_packages) == 0, advanced_available

def test_camera():
    """测试摄像头访问"""
    print("\n" + "=" * 50)
    print("测试摄像头访问...")
    print("=" * 50)
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print("✓ 摄像头访问成功")
                print(f"  分辨率: {frame.shape[1]}x{frame.shape[0]}")
                camera_ok = True
            else:
                print("✗ 摄像头无法读取图像")
                camera_ok = False
            cap.release()
        else:
            print("✗ 无法打开摄像头")
            camera_ok = False
    except Exception as e:
        print(f"✗ 摄像头测试失败: {e}")
        camera_ok = False
    
    return camera_ok

def test_face_detection():
    """测试人脸检测功能"""
    print("\n" + "=" * 50)
    print("测试人脸检测功能...")
    print("=" * 50)
    
    try:
        import cv2
        import numpy as np
        
        # 加载人脸检测器
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        if face_cascade.empty():
            print("✗ 人脸检测器加载失败")
            return False
        
        print("✓ 人脸检测器加载成功")
        
        # 创建测试图像
        test_image = np.zeros((400, 400, 3), dtype=np.uint8)
        gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        
        # 测试检测功能
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        print("✓ 人脸检测功能正常")
        
        return True
    except Exception as e:
        print(f"✗ 人脸检测测试失败: {e}")
        return False

def test_flask_app():
    """测试Flask应用启动"""
    print("\n" + "=" * 50)
    print("测试Flask应用...")
    print("=" * 50)
    
    try:
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/')
        def test():
            return "测试成功"
        
        print("✓ Flask应用创建成功")
        return True
    except Exception as e:
        print(f"✗ Flask应用测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("情绪识别系统 - 环境测试")
    print("Python版本:", sys.version)
    print()
    
    # 测试导入
    imports_ok, advanced_available = test_imports()
    
    # 测试摄像头
    camera_ok = test_camera()
    
    # 测试人脸检测
    face_detection_ok = test_face_detection()
    
    # 测试Flask
    flask_ok = test_flask_app()
    
    # 总结
    print("\n" + "=" * 50)
    print("测试结果总结")
    print("=" * 50)
    
    if imports_ok and camera_ok and face_detection_ok and flask_ok:
        print("🎉 所有测试通过！系统准备就绪。")
        if advanced_available:
            print("📋 推荐使用: emotion_detector.py (高级版)")
        else:
            print("📋 推荐使用: simple_emotion_detector.py (简化版)")
        
        print("\n启动步骤:")
        print("1. 运行: python emotion_detector.py 或 python simple_emotion_detector.py")
        print("2. 打开浏览器访问: http://localhost:5000")
    else:
        print("❌ 部分测试失败，请检查以下问题:")
        if not imports_ok:
            print("  - 安装缺失的依赖包: pip install -r requirements.txt")
        if not camera_ok:
            print("  - 检查摄像头连接和权限")
        if not face_detection_ok:
            print("  - 重新安装OpenCV: pip install --upgrade opencv-python")
        if not flask_ok:
            print("  - 重新安装Flask: pip install --upgrade flask")
    
    print("\n按任意键退出...")
    input()

if __name__ == "__main__":
    main()
