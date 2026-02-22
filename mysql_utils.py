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

def update_wxc_post_is_useful(post_id, is_useful):
    """
    Update a post in wxc_posts table with the is_useful value.
    
    Args:
        post_id (int): The ID of the post to update
        is_useful (bool): The is_useful value to store (True/False)
    
    Returns:
        bool: True if update was successful, False otherwise
    """
    connection = create_connection()
    if connection is None:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Convert boolean to integer (0 or 1) for storage in MySQL
        is_useful_int = 1 if is_useful else 0
        
        # Query to update the post with is_useful value
        update_query = """
        UPDATE wxc_posts 
        SET is_useful = %s 
        WHERE id = %s
        """
        
        cursor.execute(update_query, (is_useful_int, post_id))
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"Successfully updated is_useful for post with ID {post_id}")
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

def delete_wxc_post(post_id):
    """
    Delete a post from wxc_posts table.
    
    Args:
        post_id (int): The ID of the post to delete
    
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    connection = create_connection()
    if connection is None:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Query to delete the post
        delete_query = """
        DELETE FROM wxc_posts 
        WHERE id = %s
        """
        
        cursor.execute(delete_query, (post_id,))
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"Successfully deleted post with ID {post_id}")
            return True
        else:
            print(f"No post found with ID {post_id} to delete")
            return False
            
    except Error as e:
        print(f"Error deleting from wxc_posts table: {e}")
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
        date_str (str): The date string in mmddyyyy format to filter by
    
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