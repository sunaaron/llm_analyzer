#!/usr/bin/env python3
"""
MySQL reader to read from wxc_posts table in the remote MySQL instance.
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime

def create_connection():
    """Create connection to MySQL database."""
    try:
        connection = mysql.connector.connect(
            host='192.168.86.55',
            port=3306,
            database='wxc_crawler',
            user='crawler_admin',
            password='123'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def update_wxc_post_llm_summary(post_id, llm_summary):
    """
    Update a post in wxc_posts table with the LLM summary.
    
    Args:
        post_id (int): The ID of the post to update
        llm_summary (str): The LLM-generated summary to store
    
    Returns:
        bool: True if update was successful, False otherwise
    """
    connection = create_connection()
    if connection is None:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Query to update the post with LLM summary
        update_query = """
        UPDATE wxc_posts 
        SET llm_summary = %s 
        WHERE id = %s
        """
        
        cursor.execute(update_query, (llm_summary, post_id))
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"Successfully updated post with ID {post_id}")
            return True
        else:
            print(f"No post found with ID {post_id} to update")
            return False
            
    except Error as e:
        print(f"Error updating wxc_posts table: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def read_wxc_posts_by_category_date_and_unsummarized(category, date_str):
    """
    Read posts from wxc_posts table filtered by category, date_str, 
    and ensure llm_summary is empty or null (posts that haven't been summarized yet).
    
    Args:
        category (str): The category to filter by
        date_str (str): The date string in yyyymmdd format to filter by
    
    Returns:
        list: List of posts matching the criteria, or empty list if none found
    """
    connection = create_connection()
    if connection is None:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Query to select posts by category and date_str, 
        # ensuring llm_summary is empty or null
        select_query = """
        SELECT * FROM wxc_posts 
        WHERE category = %s AND date_str = %s 
        AND (llm_summary IS NULL OR llm_summary = '' OR llm_summary = 'NULL')
        """
        
        cursor.execute(select_query, (category, date_str))
        results = cursor.fetchall()
        
        print(f"Found {len(results)} unsummarized posts matching category '{category}' and date '{date_str}'")
        return results
        
    except Error as e:
        print(f"Error reading from wxc_posts table: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def read_wxc_post_summaries_by_category_date_and_is_useful(category, date_str):
    """
    Read post LLM summaries from wxc_posts table filtered by category, date_str, 
    and is_useful = 1.
    
    Args:
        category (str): The category to filter by
        date_str (str): The date string in yyyymmdd format to filter by
    
    Returns:
        list: List of (id, llm_summary) matching the criteria, or empty list if none found
    """
    connection = create_connection()
    if connection is None:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Query to select posts by category and date_str, 
        # ensuring is_useful = 1
        select_query = """
        SELECT id, post_url, llm_summary FROM wxc_posts 
        WHERE category = %s AND date_str = %s AND is_useful = 1
        """
        
        cursor.execute(select_query, (category, date_str))
        results = cursor.fetchall()
        
        print(f"Found {len(results)} useful posts matching category '{category}' and date '{date_str}'")
        return results
        
    except Error as e:
        print(f"Error reading from wxc_posts table: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def read_wxc_posts_by_category_and_date(category, date_str):
    """
    Read posts from wxc_posts table filtered by category and date_str.
    
    Args:
        category (str): The category to filter by
        date_str (str): The date string in mmddyyyy format to filter by
    
    Returns:
        list: List of posts matching the criteria, or empty list if none found
    """
    connection = create_connection()
    if connection is None:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Query to select posts by category and date_str
        select_query = """
        SELECT * FROM wxc_posts 
        WHERE category = %s AND date_str = %s
        """
        
        cursor.execute(select_query, (category, date_str))
        results = cursor.fetchall()
        
        print(f"Found {len(results)} posts matching category '{category}' and date '{date_str}'")
        return results
        
    except Error as e:
        print(f"Error reading from wxc_posts table: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
