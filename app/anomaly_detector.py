import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Bedrock Mantle Client
client = OpenAI(
    base_url="https://bedrock-mantle.ap-south-1.api.aws/v1",
    api_key=os.getenv("BEDROCK_API_KEY"),
    default_headers={"OpenAI-Project": "default"},
)

MODEL = "openai.gpt-oss-120b"

PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")


def get_metrics(query):
    """Prometheus se metrics fetch karo"""
    try:
        response = requests.get(
            f"{PROMETHEUS_URL}/api/v1/query",
            params={"query": query},
            timeout=10
        )
        data = response.json()
        if data["status"] == "success":
            return data["data"]["result"]
        return []
    except Exception as e:
        return f"Metrics fetch error: {str(e)}"


def detect_anomaly():
    """AI se anomaly detect karo"""
    try:
        # Metrics fetch karo
        error_rate = get_metrics("sum(ravishop_request_total{status='400'})")
        cpu_usage = get_metrics("rate(container_cpu_usage_seconds_total[5m])")
        latency = get_metrics(
            "histogram_quantile(0.95, rate(ravishop_request_latency_seconds_bucket[5m]))"
        )

        # AI se analyze karo
        metrics_summary = f"""
        Current Metrics:
        - Error Rate: {error_rate}
        - CPU Usage: {cpu_usage}
        - P95 Latency: {latency}
        """

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """You are an AIOps expert.
                    Analyze metrics and detect anomalies.
                    If anomaly found, suggest immediate fix.
                    Response format:
                    STATUS: [NORMAL/WARNING/CRITICAL]
                    ANOMALY: [description or None]
                    FIX: [fix steps or None]"""
                },
                {
                    "role": "user",
                    "content": f"Analyze these metrics: {metrics_summary}"
                }
            ],
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Anomaly detection error: {str(e)}"


def auto_heal(issue):
    """AI se auto heal suggestion lo"""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """You are a self-healing system expert.
                    Given an issue, provide kubectl/AWS CLI commands to fix it.
                    Be specific and actionable."""
                },
                {
                    "role": "user",
                    "content": f"Auto-heal this issue: {issue}"
                }
            ],
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Auto heal error: {str(e)}"
