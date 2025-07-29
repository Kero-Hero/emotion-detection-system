import os
from flask import Flask, render_template, jsonify
import json
from datetime import datetime
import random
import time

class DemoEmotionDetector:
    """演示版情绪检测器，用于云端部署展示"""
    
    def __init__(self):
        # 当前检测到的情绪数据
        self.current_emotions = {}
        self.emotion_history = []
        
        # 情绪标签中文映射
        self.emotion_labels_zh = {
            'happy': '开心',
            'sad': '悲伤',
            'angry': '愤怒',
            'surprise': '惊讶',
            'fear': '恐惧',
            'disgust': '厌恶',
            'neutral': '平静'
        }
        
        # 模拟情绪数据
        self.demo_emotions = ['happy', 'sad', 'angry', 'surprise', 'fear', 'disgust', 'neutral']
        self.start_demo()
    
    def start_demo(self):
        """启动演示模式"""
        self.is_demo_running = True
        self.generate_demo_data()
    
    def generate_demo_data(self):
        """生成演示数据"""
        # 生成模拟的情绪数据
        emotions = {}
        for emotion in self.demo_emotions:
            emotions[emotion] = random.uniform(0.0, 1.0)
        
        # 归一化概率
        total = sum(emotions.values())
        emotions = {k: v/total for k, v in emotions.items()}
        
        self.current_emotions = emotions
        self.emotion_history.append({
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'emotions': emotions.copy()
        })
        
        # 保持历史记录在合理范围内
        if len(self.emotion_history) > 100:
            self.emotion_history.pop(0)

    def get_emotion_data(self):
        """获取当前情绪数据"""
        # 每次请求时生成新的模拟数据
        self.generate_demo_data()
        
        return {
            'current_emotions': self.current_emotions,
            'emotion_history': self.emotion_history[-10:],  # 返回最近10条记录
            'emotion_labels': self.emotion_labels_zh,
            'demo_mode': True
        }

# 创建全局检测器实例
detector = DemoEmotionDetector()

# 创建Flask应用
app = Flask(__name__)

@app.route('/')
def index():
    """主页面"""
    return render_template('demo.html')

@app.route('/emotion_data')
def emotion_data():
    """获取情绪数据"""
    return jsonify(detector.get_emotion_data())

@app.route('/health')
def health():
    """健康检查端点"""
    return jsonify({'status': 'healthy', 'mode': 'demo'})

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5000))
        print("正在启动演示版情绪识别系统...")
        if os.environ.get('PORT'):
            print(f"部署模式，端口: {port}")
            app.run(host='0.0.0.0', port=port, threaded=True)
        else:
            print("请打开浏览器访问: http://localhost:5000")
            app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
    except Exception as e:
        print(f"系统启动失败: {e}")
