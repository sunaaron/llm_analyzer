#!/usr/bin/env python3
import asyncio
from fileinput import filename
import edge_tts
import argparse
from mysql_utils import read_wxc_post_summaries_by_category_and_is_useful_and_has_not_tts, update_has_tts_by_id
from datetime import datetime, timedelta
from constants import TTS_VOICE_NAMES, TTS_OUTPUT_DIR 
import os
import re

def remove_special_chars(text):
    """
    Remove * and # from a string.
    
    Args:
        text (str): The input string to process

    """
    return text.replace('*', '').replace('#', '').replace('<br>', ' ').replace('-', '')

def remove_url(text):
    """
    Remove URLs from text using regex.
    
    Args:
        text (str): The input string to process

    Returns:
        str: The text with URLs removed
    """
    # Pattern to match URLs (http, https, ftp, etc.)
    url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/!])*(?:\?(?:[\w.])=(?:[\w.])?)?(?:#(?:[\w.])?)?)?'
    
    # Remove URLs from text
    return re.sub(url_pattern, '', text)

async def generate_tts_audio(id, category, text, filename):
    """
    Generate TTS audio from text and save to file.
    
    Args:
        text (str): The text to convert to speech
        filename (str): The output filename
    """
    try:
        cleaned_text = remove_special_chars(text)
        cleaned_text = remove_url(cleaned_text)
        index = id % len(TTS_VOICE_NAMES)
        communicate = edge_tts.Communicate(cleaned_text, TTS_VOICE_NAMES[index])
        output_path = os.path.join(TTS_OUTPUT_DIR, category, filename)
        await communicate.save(output_path)
        print(f"Saved: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error generating TTS for {filename}: {str(e)}")
        return None

async def generate_tts(category):
    """Main function to fetch posts by category.
    
    Args:
        category (str): The category to filter by. Defaults to 'znjy'.
    """
    print(f"Fetching posts for category '{category}'...")
    
    # Fetch all useful posts of the specified category that do not have TTS generated and is_useful
    posts = read_wxc_post_summaries_by_category_and_is_useful_and_has_not_tts(category)

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
            id = post_data['id']
            text = post_data['llm_summary']
            post_id = post_data['post_url'].split('/')[-1].split('.')[0]  # Extract post ID from URL
            filename = f"{category}_{post_data['id']}_{post_id}.mp3"
            
            # Generate TTS audio
            output_path = await generate_tts_audio(id, category, text, filename)
            
            # Update has_tts flag if TTS was successfully generated
            if output_path:
                update_has_tts_by_id(id, 1)
                print(f"Updated has_tts flag for post ID {id}")
            
    else:
        print("No posts found matching the criteria.")

if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate TTS for WXC posts')
    parser.add_argument('--category', default='znjy', help='Category to filter by (default: znjy)')
    
    args = parser.parse_args()
    
    # Call generate_tts function with parsed arguments
    asyncio.run(generate_tts(args.category))
