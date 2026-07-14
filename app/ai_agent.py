from openai import OpenAI
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# Bedrock Mantle Client
client = OpenAI(
    base_url="https://bedrock-mantle.ap-south-1.api.aws/v1",
    api_key=os.getenv("BEDROCK_API_KEY"),
    default_headers={"OpenAI-Project": "default"},
)

MODEL = "openai.gpt-oss-120b"


# Tool 1 — CloudWatch Logs Check
def tool_check_logs(log_group="/ravishop-ai/app", minutes=30):
    """CloudWatch se logs fetch karke analyze karo"""
    try:
        logs_client = boto3.client('logs', region_name='ap-south-1')
        response = logs_client.describe_log_groups(
            logGroupNamePrefix=log_group
        )
        if response['logGroups']:
            return f"Log group found: {log_group} — logs available"
        return f"Log group {log_group} not found"
    except Exception as e:
        return f"Logs check error: {str(e)}"


# Tool 2 — Error Debug
def tool_debug_error(error_message):
    """Error message ko AI se analyze karke fix suggest karo"""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a DevOps expert. Analyze errors and suggest fixes."
                },
                {
                    "role": "user",
                    "content": f"Debug this error and suggest fix: {error_message}"
                }
            ],
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Debug error: {str(e)}"


# Tool 3 — Infra Status Check
def tool_infra_status():
    """EC2 aur RDS status check karo"""
    try:
        ec2 = boto3.client('ec2', region_name='ap-south-1')
        instances = ec2.describe_instances(
            Filters=[{'Name': 'tag:Name', 'Values': ['ravishop-ai-ec2']}]
        )
        reservations = instances['Reservations']
        if reservations:
            state = reservations[0]['Instances'][0]['State']['Name']
            return f"EC2 Status: {state}"
        return "EC2 instance not found"
    except Exception as e:
        return f"Infra status error: {str(e)}"


# Tool 4 — Deploy Advice
def tool_deploy_advice(issue):
    """Deployment issue ke liye AI advice lo"""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a DevOps expert specializing in deployments."
                },
                {
                    "role": "user",
                    "content": f"Deployment issue: {issue}. Give step by step solution."
                }
            ],
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Deploy advice error: {str(e)}"


# Tool 5 — Cost Optimize
def tool_cost_optimize():
    """AWS cost optimization suggestions lo"""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AWS cost optimization expert."
                },
                {
                    "role": "user",
                    "content": "Suggest top 5 AWS cost optimization tips for a Flask app on EC2 with RDS MySQL."
                }
            ],
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Cost optimize error: {str(e)}"


# Tool 6 — Security Scan
def tool_security_scan(code_snippet):
    """Code security issues detect karo"""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a security expert. Find vulnerabilities in code."
                },
                {
                    "role": "user",
                    "content": f"Find security issues in this code: {code_snippet}"
                }
            ],
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Security scan error: {str(e)}"


# Main AI Agent — Sab tools orchestrate karta hai
def ai_agent(user_query):
    """Main AI Agent — query samjho aur sahi tool use karo"""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """You are RaviShop AI DevOps Agent.
                    You help with:
                    - Debugging errors
                    - Infrastructure status
                    - Deployment advice
                    - Cost optimization
                    - Security scanning
                    Always respond in a helpful, concise manner."""
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ],
            max_tokens=1000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Agent error: {str(e)}"
