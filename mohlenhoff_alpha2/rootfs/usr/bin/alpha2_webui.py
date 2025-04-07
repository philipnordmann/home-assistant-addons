#!/usr/bin/env python3
import os
import json
import logging
import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('alpha2-webui')

app = Flask(__name__, 
            static_folder='/usr/share/alpha2/static',
            template_folder='/usr/share/alpha2/templates')

# Get ingress path
ingress_path = os.environ.get('INGRESS_URI', '')
logger.info(f"Ingress path: {ingress_path}")

# Create a simple index page
@app.route('/')
@app.route(f'{ingress_path}')
@app.route(f'{ingress_path}/')
def index():
    """Main dashboard page"""
    return f"""
    <html>
    <head>
        <title>Alpha 2 Manager</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .card {{ background: #f0f0f0; border-radius: 5px; padding: 15px; margin-bottom: 15px; }}
        </style>
    </head>
    <body>
        <h1>Möhlenhoff Alpha 2 Manager</h1>
        
        <div class="card">
            <h2>System Information</h2>
            <p>Ingress Path: {ingress_path}</p>
            <p>Current URL: {request.url}</p>
            <p>Base URL: {request.base_url}</p>
        </div>
        
        <div class="card">
            <h2>Environment Variables</h2>
            <pre>{json.dumps({k:v for k,v in os.environ.items() if k.startswith('INGRESS')}, indent=2)}</pre>
        </div>
        
        <div class="card">
            <h2>Available Routes</h2>
            <ul>
                <li><a href="{ingress_path}/config">View Configuration</a></li>
                <li><a href="{ingress_path}/test">Test Page</a></li>
            </ul>
        </div>
    </body>
    </html>
    """

# Add some additional test routes
@app.route(f'{ingress_path}/config')
def config():
    """Show configuration"""
    config_path = '/data/options.json'
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
    else:
        config = {"error": "Config file not found"}
    
    return f"""
    <html>
    <head>
        <title>Alpha 2 Configuration</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            pre {{ background: #f0f0f0; padding: 15px; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <h1>Current Configuration</h1>
        <pre>{json.dumps(config, indent=2)}</pre>
        <p><a href="{ingress_path}/">Back to Home</a></p>
    </body>
    </html>
    """

@app.route(f'{ingress_path}/test')
def test():
    """Test page"""
    return f"""
    <html>
    <head>
        <title>Alpha 2 Test Page</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
        </style>
    </head>
    <body>
        <h1>Test Page</h1>
        <p>This is a test page to verify routing is working correctly.</p>
        <p><a href="{ingress_path}/">Back to Home</a></p>
    </body>
    </html>
    """

# Catch-all route for debugging
@app.route('/<path:path>')
def catch_all(path):
    logger.info(f"Catch-all route called with path: {path}")
    return f"""
    <html>
    <head>
        <title>Debug Route</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            pre {{ background: #f0f0f0; padding: 15px; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <h1>Debug Information</h1>
        <p>You accessed path: <code>{path}</code></p>
        <p>Ingress path: <code>{ingress_path}</code></p>
        <p>Try visiting <a href="{ingress_path}/">the home page</a> instead.</p>
        
        <h2>Request Details</h2>
        <pre>
URL: {request.url}
Path: {request.path}
Base URL: {request.base_url}
URL Root: {request.url_root}
        </pre>
    </body>
    </html>
    """

if __name__ == '__main__':
    # Get ingress port from environment
    ingress_port = int(os.environ.get('INGRESS_PORT', 8099))
    
    # Debug information
    logger.info(f"Starting web UI on http://0.0.0.0:{ingress_port}")
    logger.info(f"Ingress path: {ingress_path}")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=ingress_port, debug=True)