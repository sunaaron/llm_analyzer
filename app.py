#!/usr/bin/env python3
"""
Flask web service to display wxc_posts table data.
"""

from flask import Flask, render_template, jsonify
from mysql_reader import read_all_wxc_posts, update_wxc_post_is_useful
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
                'post_url': post.get('post_url', ''),
                'post_title': post.get('post_title', ''),
                'post_body': post.get('post_body', '')[:200] + '...' if len(post.get('post_body', '')) > 200 else post.get('post_body', ''),
                'llm_summary': llm_summary,
                'is_useful': post.get('is_useful', 0) == 1
            })
    
    return render_template('index.html', posts=display_data)

@app.route('/update_is_useful/<int:post_id>/<int:value>')
def update_is_useful(post_id, value):
    """Endpoint to update the is_useful field of a post."""
    success = update_wxc_post_is_useful(post_id, bool(value))
    return jsonify({'success': success})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)