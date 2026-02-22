#!/usr/bin/env python3
import asyncio
from fileinput import filename
import edge_tts
import argparse
from mysql_utils import read_wxc_post_summaries_by_category_date_and_is_useful
from datetime import datetime, timedelta
from constants import TTS_VOICE_NAME        

def remove_asterisk_sign(text):
    """
    Remove all asterisk signs (*) from a string.
    
    Args:
        text (str): The input string to process
        
    Returns:
        str: The string with all asterisk signs removed
    """
    return text.replace('*', '')

async def generate_tts(category, date_str):
    """Main function to fetch posts by category and date.
    
    Args:
        category (str): The category to filter by. Defaults to 'znjy'.
        date_str (str): The date string in mmddyyyy format. Defaults to today's date minus 3 days.
    """
    # If no date_str provided, calculate it as today's date minus 3 days
    if not date_str:
        # Get current date and subtract 3 days
        current_date = datetime.now()
        three_days_ago = current_date - timedelta(days=3)
        # Format as mmddyyyy
        date_str = three_days_ago.strftime("%m%d%Y")
    
    print(f"Fetching posts for category '{category}' with date '{date_str}'...")
    
    # Fetch all useful posts of the specified category and date_str
    posts = read_wxc_post_summaries_by_category_date_and_is_useful(category, date_str)
    
    if posts:
        print(f"Successfully fetched {len(posts)} posts:")
        
        # Process each post
        for i, post in enumerate(posts, 1):
            print(f"\nProcessing Post {i}...")
            
            # Wrap each post as a dictionary with the required structure
            post_data = {
                'id': post.get('id', ''),
                'post_url': post.get('post_url', ''),
                'llm_summary': post.get('llm_summary', ''),
            }
            text = post_data['llm_summary']
            # Remove asterisk signs from the text
            cleaned_text = remove_asterisk_sign(text)
            filename = f"{post_data['id']}.mp3"
            communicate = edge_tts.Communicate(cleaned_text, TTS_VOICE_NAME)
            await communicate.save(filename)
            print(f"Saved: {filename}")
            break
            
    else:
        print("No posts found matching the criteria.")

if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate TTS for WXC posts')
    parser.add_argument('--category', default='znjy', help='Category to filter by (default: znjy)')
    parser.add_argument('--date_str', default='', help='Date string in mmddyyyy format (default: 3 days ago)')
    
    args = parser.parse_args()
    
    # Call generate_tts function with parsed arguments
    asyncio.run(generate_tts(args.category, args.date_str))
