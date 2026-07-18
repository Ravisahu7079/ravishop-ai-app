import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))  # noqa: E402

from flask import Flask, jsonify, request, Response  # noqa: E402
from flask_cors import CORS  # noqa: E402
from dotenv import load_dotenv  # noqa: E402
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST  # noqa: E402
from ai_agent import (  # noqa: E402
    ai_agent,
    tool_debug_error,
    tool_infra_status,
    tool_deploy_advice,
    tool_cost_optimize,
    tool_security_scan,
    tool_check_logs
)
from anomaly_detector import detect_anomaly, auto_heal  # noqa: E402

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

REQUEST_COUNT = Counter(
    'ravishop_request_total',
    'Total request count',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'ravishop_request_latency_seconds',
    'Request latency in seconds',
    ['endpoint']
)


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
            'logs': '/logs/check',
            'metrics': '/metrics',
            'anomaly_detect': '/anomaly/detect',
            'anomaly_heal': '/anomaly/heal'
        }
    })


@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get('query', '')
    if not query:
        REQUEST_COUNT.labels('POST', '/ask', '400').inc()
        return jsonify({'error': 'Query required'}), 400
    result = ai_agent(query)
    REQUEST_COUNT.labels('POST', '/ask', '200').inc()
    return jsonify({'response': result})


@app.route('/debug', methods=['POST'])
def debug_route():
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


@app.route('/metrics', methods=['GET'])
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route('/anomaly/detect', methods=['GET'])
def anomaly_detect():
    result = detect_anomaly()
    return jsonify({'anomaly_report': result})


@app.route('/anomaly/heal', methods=['POST'])
def anomaly_heal():
    data = request.get_json()
    issue = data.get('issue', '')
    if not issue:
        return jsonify({'error': 'Issue required'}), 400
    result = auto_heal(issue)
    return jsonify({'heal_plan': result})


if __name__ == '__main__':
    port = int(os.getenv('APP_PORT', 5000))
    flag = os.getenv('DEBUG', 'False').lower() == 'true'
    print(f"🚀 RaviShop AI starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=flag)
