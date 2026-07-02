from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# .env file load karo
load_dotenv()

# Flask app banao
app = Flask(__name__)
CORS(app)

# App config
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'app': os.getenv('APP_NAME'),
        'version': '1.0.0',
        'environment': os.getenv('APP_ENV')
    })


# Home endpoint
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Welcome to RaviShop AI 2026!',
        'endpoints': {
            'health': '/health',
            'products': '/products',
            'orders': '/orders',
            'ai': '/ask'
        }
    })


if __name__ == '__main__':
    port = int(os.getenv('APP_PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    print(f"🚀 RaviShop AI starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
