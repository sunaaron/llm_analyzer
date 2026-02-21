#!/usr/bin/env python3
"""
Flask web service to display wxc_posts table data.
"""

from flask import Flask, render_template, jsonify
from mysql_reader import read_all_wxc_posts
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Main page to display wxc_posts table data."""
    posts = read_all_wxc_posts()
    
    # Prepare data for display - only show posts with non-empty LLM summaries
    display_data = []
    for post in posts:
        llm_summary = post.get('llm_summary', '')
        if llm_summary and llm_summary.strip():  # Check if LLM summary exists and is not empty
            display_data.append({
                'id': post.get('id', ''),
                'post_url': post.get('url', ''),
                'post_title': post.get('title', ''),
                'post_body': post.get('content', '')[:200] + '...' if len(post.get('content', '')) > 200 else post.get('content', ''),
                'llm_summary': llm_summary
            })
    
    return render_template('index.html', posts=display_data)

@app.route('/api/posts')
def api_posts():
    """API endpoint to get all posts in JSON format."""
    posts = read_all_wxc_posts()
    
    # Prepare data for API response - only show posts with non-empty LLM summaries
    api_data = []
    for post in posts:
        llm_summary = post.get('llm_summary', '')
        if llm_summary and llm_summary.strip():  # Check if LLM summary exists and is not empty
            api_data.append({
                'id': post.get('id', ''),
                'post_url': post.get('url', ''),
                'post_title': post.get('title', ''),
                'post_body': post.get('content', ''),
                'llm_summary': llm_summary
            })
    
    return jsonify(api_data)

@app.route('/api/posts/<int:post_id>')
def api_post(post_id):
    """API endpoint to get a specific post by ID."""
    # For simplicity, we'll fetch all posts and filter
    posts = read_all_wxc_posts()
    
    for post in posts:
        if post.get('id') == post_id:
            llm_summary = post.get('llm_summary', '')
            if llm_summary and llm_summary.strip():  # Check if LLM summary exists and is not empty
                return jsonify({
                    'id': post.get('id', ''),
                    'post_url': post.get('url', ''),
                    'post_title': post.get('title', ''),
                    'post_body': post.get('content', ''),
                    'llm_summary': llm_summary
                })
    
    return jsonify({'error': 'Post not found or no summary available'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)