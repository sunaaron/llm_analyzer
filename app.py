#!/usr/bin/env python3
"""
Flask web service to display wxc_posts table data.
"""

from flask import Flask, render_template, jsonify, request
from mysql_utils import read_all_wxc_posts, update_wxc_post_is_useful, update_wxc_post_llm_summary, delete_wxc_post
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Main page to display wxc_posts table data."""
    # Get filter parameter from query string, default to 'both'
    filter_param = request.args.get('filter', 'both')
    
    posts = read_all_wxc_posts()
    
    # Prepare data for display - only show posts with non-empty LLM summaries
    display_data = []
    for post in posts:
        llm_summary = post.get('llm_summary', '')
        if llm_summary and llm_summary.strip():  # Check if LLM summary exists and is not empty
            # Apply filter logic
            is_useful = post.get('is_useful', 0) == 1
            
            # Filter posts based on the filter parameter
            if filter_param == 'both':
                # Show all posts
                show_post = True
            elif filter_param == 'useful_only':
                # Show only useful posts
                show_post = is_useful
            elif filter_param == 'useless_only':
                # Show only useless posts
                show_post = not is_useful
            else:
                # Default to showing all posts
                show_post = True
            
            if show_post:
                display_data.append({
                    'id': post.get('id', ''),
                    'post_url': post.get('post_url', ''),
                    'post_title': post.get('post_title', ''),
                    'post_body': post.get('post_body', '')[:200] + '...' if len(post.get('post_body', '')) > 200 else post.get('post_body', ''),
                    'llm_summary': llm_summary,
                    'is_useful': is_useful
                })
    
    return render_template('index.html', posts=display_data, filter=filter_param)

@app.route('/update_is_useful/<int:post_id>/<int:value>')
def update_is_useful(post_id, value):
    """Endpoint to update the is_useful field of a post."""
    success = update_wxc_post_is_useful(post_id, bool(value))
    return jsonify({'success': success})

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    """Endpoint to delete a post from the database."""
    success = delete_wxc_post(post_id)
    return jsonify({'success': success})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)