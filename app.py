from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))
from ai_agent import (
    ai_agent,
    tool_debug_error,
    tool_infra_status,
    tool_deploy_advice,
    tool_cost_optimize,
    tool_security_scan,
    tool_check_logs
)

# .env file load karo
load_dotenv()

# Flask app banao
app = Flask(__name__)
CORS(app)

# App config
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'app': os.getenv('APP_NAME'),
        'version': '1.0.0',
        'environment': os.getenv('APP_ENV')
    })


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Welcome to RaviShop AI 2026!',
        'endpoints': {
            'health': '/health',
            'ask': '/ask',
            'debug': '/debug',
            'infra': '/infra/status',
            'deploy': '/deploy/advice',
            'cost': '/cost/optimize',
            'security': '/security/scan',
            'logs': '/logs/check'
        }
    })


@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get('query', '')
    if not query:
        return jsonify({'error': 'Query required'}), 400
    result = ai_agent(query)
    return jsonify({'response': result})


@app.route('/debug', methods=['POST'])
def debug():
    data = request.get_json()
    error = data.get('error', '')
    if not error:
        return jsonify({'error': 'Error message required'}), 400
    result = tool_debug_error(error)
    return jsonify({'fix': result})


@app.route('/infra/status', methods=['GET'])
def infra_status():
    result = tool_infra_status()
    return jsonify({'status': result})


@app.route('/deploy/advice', methods=['POST'])
def deploy_advice():
    data = request.get_json()
    issue = data.get('issue', '')
    if not issue:
        return jsonify({'error': 'Issue required'}), 400
    result = tool_deploy_advice(issue)
    return jsonify({'advice': result})


@app.route('/cost/optimize', methods=['GET'])
def cost_optimize():
    result = tool_cost_optimize()
    return jsonify({'suggestions': result})


@app.route('/security/scan', methods=['POST'])
def security_scan():
    data = request.get_json()
    code = data.get('code', '')
    if not code:
        return jsonify({'error': 'Code required'}), 400
    result = tool_security_scan(code)
    return jsonify({'issues': result})


@app.route('/logs/check', methods=['GET'])
def check_logs():
    result = tool_check_logs()
    return jsonify({'logs': result})


if __name__ == '__main__':
    port = int(os.getenv('APP_PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    print(f" RaviShop AI starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
