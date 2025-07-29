import cv2
import numpy as np
from flask import Flask, render_template, Response, jsonify
import threading
import time
import json
from datetime import datetime

class SimpleEmotionDetector:
    """简化版情绪检测器，基于OpenCV人脸检测和简单的面部特征分析"""
    
    def __init__(self):
        # 加载人脸检测器
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
        
        # 摄像头
        self.camera = None
        self.is_running = False
        
        # 当前检测到的情绪数据
        self.current_emotions = {}
        self.emotion_history = []
        
        # 情绪颜色映射
        self.emotion_colors = {
            'happy': (0, 255, 255),    # 黄色
            'neutral': (128, 128, 128), # 灰色
            'sad': (255, 0, 0),        # 蓝色
        }
        
        # 中文情绪标签
        self.emotion_labels_zh = {
            'happy': '开心',
            'neutral': '平静',
            'sad': '悲伤',
        }

    def start_camera(self):
        """启动摄像头"""
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                raise Exception("无法打开摄像头")
            
            # 设置摄像头参数
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            self.is_running = True
            print("摄像头启动成功")
            return True
        except Exception as e:
            print(f"摄像头启动失败: {e}")
            return False

    def stop_camera(self):
        """停止摄像头"""
        self.is_running = False
        if self.camera:
            self.camera.release()
            self.camera = None
        print("摄像头已停止")

    def detect_simple_emotions(self, frame, faces):
        """基于简单特征的情绪检测"""
        emotions_data = []
        
        for (x, y, w, h) in faces:
            face_roi = frame[y:y+h, x:x+w]
            gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
            
            # 检测眼部
            eyes = self.eye_cascade.detectMultiScale(gray_face, 1.1, 5)
            
            # 检测微笑
            smiles = self.smile_cascade.detectMultiScale(gray_face, 1.8, 20)
            
            # 简单的情绪判断逻辑
            emotions = {'happy': 0.0, 'neutral': 0.0, 'sad': 0.0}
            
            if len(smiles) > 0:
                # 检测到微笑
                emotions['happy'] = 0.8
                emotions['neutral'] = 0.15
                emotions['sad'] = 0.05
                dominant_emotion = 'happy'
            elif len(eyes) < 2:
                # 眼部检测异常，可能是悲伤或其他情绪
                emotions['sad'] = 0.6
                emotions['neutral'] = 0.3
                emotions['happy'] = 0.1
                dominant_emotion = 'sad'
            else:
                # 中性表情
                emotions['neutral'] = 0.7
                emotions['happy'] = 0.2
                emotions['sad'] = 0.1
                dominant_emotion = 'neutral'
            
            confidence = emotions[dominant_emotion]
            
            emotions_data.append({
                'box': (x, y, w, h),
                'emotions': emotions,
                'dominant_emotion': dominant_emotion,
                'confidence': confidence
            })
        
        return emotions_data

    def draw_emotions(self, frame, emotions_data):
        """在图像上绘制情绪检测结果"""
        for emotion_data in emotions_data:
            x, y, w, h = emotion_data['box']
            dominant_emotion = emotion_data['dominant_emotion']
            confidence = emotion_data['confidence']
            emotions = emotion_data['emotions']
            
            # 绘制人脸边界框
            color = self.emotion_colors.get(dominant_emotion, (255, 255, 255))
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            
            # 绘制主要情绪标签
            label = f"{self.emotion_labels_zh[dominant_emotion]}: {confidence:.2f}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            
            # 绘制标签背景
            cv2.rectangle(frame, (x, y - label_size[1] - 10), 
                         (x + label_size[0], y), color, -1)
            
            # 绘制标签文字
            cv2.putText(frame, label, (x, y - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame

    def generate_frames(self):
        """生成视频帧流"""
        while self.is_running:
            if self.camera is None:
                break
                
            success, frame = self.camera.read()
            if not success:
                break
            
            # 水平翻转图像（镜像效果）
            frame = cv2.flip(frame, 1)
            
            # 转换为灰度图像进行人脸检测
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # 检测人脸
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            # 检测情绪
            emotions_data = self.detect_simple_emotions(frame, faces)
            
            # 更新当前情绪数据
            if emotions_data:
                self.current_emotions = emotions_data[0]['emotions']
                self.emotion_history.append({
                    'timestamp': datetime.now().strftime('%H:%M:%S'),
                    'emotions': self.current_emotions.copy()
                })
                
                # 保持历史记录在合理范围内
                if len(self.emotion_history) > 100:
                    self.emotion_history.pop(0)
            
            # 在图像上绘制情绪信息
            frame = self.draw_emotions(frame, emotions_data)
            
            # 编码图像
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
            # 控制帧率
            time.sleep(0.03)  # 约30 FPS

    def get_emotion_data(self):
        """获取当前情绪数据"""
        return {
            'current_emotions': self.current_emotions,
            'emotion_history': self.emotion_history[-10:],  # 返回最近10条记录
            'emotion_labels': self.emotion_labels_zh
        }

# 创建全局检测器实例
detector = SimpleEmotionDetector()

# 创建Flask应用
app = Flask(__name__)

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """视频流端点"""
    return Response(detector.generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_camera')
def start_camera():
    """启动摄像头"""
    success = detector.start_camera()
    return jsonify({'success': success})

@app.route('/stop_camera')
def stop_camera():
    """停止摄像头"""
    detector.stop_camera()
    return jsonify({'success': True})

@app.route('/emotion_data')
def emotion_data():
    """获取情绪数据"""
    return jsonify(detector.get_emotion_data())

if __name__ == '__main__':
    try:
        print("正在启动简化版情绪识别系统...")
        print("请打开浏览器访问: http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
    except KeyboardInterrupt:
        print("\n正在关闭系统...")
        detector.stop_camera()
    except Exception as e:
        print(f"系统启动失败: {e}")
    finally:
        detector.stop_camera()
