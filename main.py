#!/usr/bin/env python3
"""
Main entry point for the wxc_reader application.
"""
import json
from mysql_reader import read_wxc_posts_by_category_date_and_unsummarized, update_wxc_post_llm_summary
from post_analyzer import analyze_with_llm
from constants import LLM_IRRELEVANT_RESPONSE

def main():
    """Main function to fetch posts by category and date."""
    print("Fetching posts for category 'znjy' with date '02182026'...")
    
    # Fetch all posts of category "znjy" and date_str = "02182026"
    posts = read_wxc_posts_by_category_date_and_unsummarized("znjy", "02182026")
    
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
            analysis_result = analyze_with_llm(post_data)
                        
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
    main()