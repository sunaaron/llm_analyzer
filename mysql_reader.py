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

def read_wxc_posts_by_category(category):
    """
    Read posts from wxc_posts table filtered by category only.
    
    Args:
        category (str): The category to filter by
    
    Returns:
        list: List of posts matching the category, or empty list if none found
    """
    connection = create_connection()
    if connection is None:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Query to select posts by category only
        select_query = """
        SELECT * FROM wxc_posts 
        WHERE category = %s
        """
        
        cursor.execute(select_query, (category,))
        results = cursor.fetchall()
        
        print(f"Found {len(results)} posts matching category '{category}'")
        return results
        
    except Error as e:
        print(f"Error reading from wxc_posts table: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def read_all_wxc_posts():
    """
    Read all posts from wxc_posts table.
    
    Returns:
        list: All posts in the table, or empty list if none found
    """
    connection = create_connection()
    if connection is None:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Query to select all posts
        select_query = "SELECT * FROM wxc_posts"
        
        cursor.execute(select_query)
        results = cursor.fetchall()
        
        print(f"Found {len(results)} total posts in wxc_posts table")
        return results
        
    except Error as e:
        print(f"Error reading from wxc_posts table: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

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

def test_database_connection():
    """Test if we can connect to the database."""
    connection = create_connection()
    if connection:
        print("Successfully connected to MySQL database")
        connection.close()
        return True
    else:
        print("Failed to connect to MySQL database")
        return False

# Example usage
if __name__ == "__main__":
    # Test the database connection
    print("Testing MySQL connection...")
    test_database_connection()
    
    # Example queries
    print("\n--- Reading posts by category and date ---")
    posts = read_wxc_posts_by_category_and_date("znjy", "02212025")
    
    print("\n--- Reading posts by category only ---")
    posts = read_wxc_posts_by_category("znjy")
    
    print("\n--- Reading all posts ---")
    posts = read_all_wxc_posts()