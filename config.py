# 情绪识别系统配置文件

# 应用设置
APP_NAME = "实时情绪识别系统"
VERSION = "1.0.0"
DEBUG = True
HOST = "0.0.0.0"
PORT = 5000

# 摄像头设置
CAMERA_INDEX = 0  # 默认摄像头索引
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30

# 情绪检测设置
EMOTION_CONFIDENCE_THRESHOLD = 0.3  # 情绪检测置信度阈值
MAX_HISTORY_RECORDS = 100  # 最大历史记录数

# 支持的情绪类型
EMOTIONS = {
    'angry': {
        'zh': '愤怒',
        'color': (0, 0, 255),  # BGR格式
        'icon': 'fa-angry'
    },
    'disgust': {
        'zh': '厌恶', 
        'color': (0, 128, 0),
        'icon': 'fa-grimace'
    },
    'fear': {
        'zh': '恐惧',
        'color': (128, 0, 128),
        'icon': 'fa-scared'
    },
    'happy': {
        'zh': '开心',
        'color': (0, 255, 255),
        'icon': 'fa-smile'
    },
    'sad': {
        'zh': '悲伤',
        'color': (255, 0, 0),
        'icon': 'fa-sad-tear'
    },
    'surprise': {
        'zh': '惊讶',
        'color': (255, 165, 0),
        'icon': 'fa-surprise'
    },
    'neutral': {
        'zh': '平静',
        'color': (128, 128, 128),
        'icon': 'fa-meh'
    }
}

# UI设置
UI_UPDATE_INTERVAL = 1000  # 毫秒
CHART_MAX_POINTS = 50  # 图表最大数据点数
