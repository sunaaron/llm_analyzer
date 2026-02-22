#!/usr/bin/env python3
"""
Main entry point for the wxc_reader application.
"""
import json
import argparse
from mysql_utils import read_wxc_posts_by_category_date_and_unsummarized, update_wxc_post_llm_summary
from post_analyzer import analyze_with_llm
from constants import LLM_IRRELEVANT_RESPONSE
from datetime import datetime, timedelta

def summarize(category, date_str):
    """Main function to fetch posts by category and date.
    
    Args:
        category (str): The category to filter by. Defaults to 'znjy'.
        date_str (str): The date string in yyyymmdd format. Defaults to today's date minus 3 days.
    """
    # If no date_str provided, calculate it as today's date minus 3 days
    if not date_str:
        # Get current date and subtract 3 days
        current_date = datetime.now()
        three_days_ago = current_date - timedelta(days=3)
        # Format as yyyymmdd
        date_str = three_days_ago.strftime("%Y%m%d")
    
    print(f"Fetching posts for category '{category}' with date '{date_str}'...")
    
    # Fetch all posts of the specified category and date_str
    posts = read_wxc_posts_by_category_date_and_unsummarized(category, date_str)
    
    if posts:
        print(f"Successfully fetched {len(posts)} posts:")
        
        # Process each post
        for i, post in enumerate(posts, 1):
            print(f"\nProcessing Post {i}...")
            
            # Wrap each post as a dictionary with the required structure
            post_data = {
                'post_title': post.get('post_title', ''),
                'post_content': post.get('post_body', ''),
                'comments': json.loads(post.get('comments', '[]'))
            }
            
            # Analyze with LLM and get the result
            analysis_result = analyze_with_llm(post_data, category)
                        
            # Update the database with the LLM summary (only if not irrelevant)
            post_id = post.get('id')
            if post_id and analysis_result != LLM_IRRELEVANT_RESPONSE:
                print(f"Updating database record with ID {post_id}...")
                update_wxc_post_llm_summary(post_id, analysis_result)
            elif post_id:
                print(f"Skipping database update for ID {post_id} - result is irrelevant")
            else:
                print("Warning: Could not find post ID to update database")
            
    else:
        print("No posts found matching the criteria.")

if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Summarize WXC posts')
    parser.add_argument('--category', default='znjy', help='Category to filter by (default: znjy)')
    parser.add_argument('--date_str', default='', help='Date string in yyyymmdd format (default: 3 days ago)')
    
    args = parser.parse_args()
    
    # Call summarize function with parsed arguments
    summarize(args.category, args.date_str)
