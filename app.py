"""Flask 应用入口"""

from flask import Flask
from routes import  ticket_bp

# 创建 Flask 应用实例
app = Flask(__name__)

# 注册蓝图
app.register_blueprint(ticket_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
