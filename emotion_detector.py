import cv2
import numpy as np
from fer import FER
from flask import Flask, render_template, Response, jsonify
import threading
import time
import json
from datetime import datetime

class EmotionDetector:
    def __init__(self):
        """初始化情绪检测器"""
        # 初始化FER情绪检测器
        self.emotion_detector = FER(mtcnn=True)
        
        # 初始化OpenCV人脸检测器（备用）
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # 摄像头
        self.camera = None
        self.is_running = False
        
        # 当前检测到的情绪数据
        self.current_emotions = {}
        self.emotion_history = []
        
        # 情绪颜色映射
        self.emotion_colors = {
            'angry': (0, 0, 255),      # 红色
            'disgust': (0, 128, 0),    # 深绿色
            'fear': (128, 0, 128),     # 紫色
            'happy': (0, 255, 255),    # 黄色
            'sad': (255, 0, 0),        # 蓝色
            'surprise': (255, 165, 0), # 橙色
            'neutral': (128, 128, 128) # 灰色
        }
        
        # 中文情绪标签
        self.emotion_labels_zh = {
            'angry': '愤怒',
            'disgust': '厌恶',
            'fear': '恐惧',
            'happy': '开心',
            'sad': '悲伤',
            'surprise': '惊讶',
            'neutral': '平静'
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

    def detect_emotions(self, frame):
        """检测图像中的情绪"""
        try:
            # 使用FER进行情绪检测
            result = self.emotion_detector.detect_emotions(frame)
            
            emotions_data = []
            for face in result:
                # 获取人脸边界框
                x, y, w, h = face['box']
                
                # 获取情绪概率
                emotions = face['emotions']
                
                # 找到最可能的情绪
                dominant_emotion = max(emotions, key=emotions.get)
                confidence = emotions[dominant_emotion]
                
                emotions_data.append({
                    'box': (x, y, w, h),
                    'emotions': emotions,
                    'dominant_emotion': dominant_emotion,
                    'confidence': confidence
                })
            
            return emotions_data
            
        except Exception as e:
            print(f"情绪检测错误: {e}")
            return []

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
            
            # 绘制情绪条形图
            bar_y = y + h + 10
            bar_height = 15
            bar_width = w
            
            for i, (emotion, score) in enumerate(emotions.items()):
                # 计算条形的宽度
                bar_length = int(bar_width * score)
                bar_color = self.emotion_colors.get(emotion, (255, 255, 255))
                
                # 绘制条形背景
                cv2.rectangle(frame, (x, bar_y + i * (bar_height + 2)), 
                             (x + bar_width, bar_y + i * (bar_height + 2) + bar_height), 
                             (50, 50, 50), -1)
                
                # 绘制条形
                if bar_length > 0:
                    cv2.rectangle(frame, (x, bar_y + i * (bar_height + 2)), 
                                 (x + bar_length, bar_y + i * (bar_height + 2) + bar_height), 
                                 bar_color, -1)
                
                # 绘制情绪标签
                emotion_label = f"{self.emotion_labels_zh[emotion]}: {score:.2f}"
                cv2.putText(frame, emotion_label, 
                           (x + bar_width + 5, bar_y + i * (bar_height + 2) + bar_height - 2), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
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
            
            # 检测情绪
            emotions_data = self.detect_emotions(frame)
            
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
detector = EmotionDetector()

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
        print("正在启动情绪识别系统...")
        print("请打开浏览器访问: http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
    except KeyboardInterrupt:
        print("\n正在关闭系统...")
        detector.stop_camera()
    except Exception as e:
        print(f"系统启动失败: {e}")
    finally:
        detector.stop_camera()
