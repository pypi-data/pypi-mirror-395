"""
Configuration loading utilities.
"""
import os
import json
import sys
from argparse import Namespace
from typing import Dict
from pathlib import Path


def load_config(config_path: str = 'config.json') -> Dict:
    """
    Load configuration from environment variables or JSON file.
    Priority: Environment variables > JSON file
    
    Args:
        config_path (str): Path to the configuration file (fallback)
        
    Returns:
        dict: Configuration dictionary
    """
    # Priority 1: Try to load from environment variables
    env_config = {
        'base_url': os.getenv('BASE_URL'),
        'cookie': os.getenv('COOKIE'),
        'max_workers': os.getenv('MAX_WORKERS', '4'),
        'max_retries': os.getenv('MAX_RETRIES', '3'),
        'DEFAULT_CONNECT_TIMEOUT': os.getenv('DEFAULT_CONNECT_TIMEOUT', '10'),
        'DEFAULT_READ_TIMEOUT': os.getenv('DEFAULT_READ_TIMEOUT', '300'),
        'DEFAULT_RETRY_DELAY': os.getenv('DEFAULT_RETRY_DELAY', '2'),
        'DEFAULT_BATCH_SIZE': os.getenv('DEFAULT_BATCH_SIZE', '10')
    }
    
    # If required environment variables are set, use env config
    # base_url and orthanc_base_url are both required
    if env_config['base_url'] and env_config['orthanc_base_url'] and env_config['cookie']:
        # Convert string numbers to integers
        for key in ['max_workers', 'max_retries', 'DEFAULT_CONNECT_TIMEOUT', 
                    'DEFAULT_READ_TIMEOUT', 'DEFAULT_RETRY_DELAY', 'DEFAULT_BATCH_SIZE']:
            env_config[key] = int(env_config[key])
        return env_config
    else:
        print("未找到环境变量，将使用配置文件")
   

def create_upload_config(config: Dict) -> Namespace:
    """
    Create upload configuration namespace from config dictionary.
    
    Args:
        config (dict): Configuration dictionary
        
    Returns:
        Namespace: Upload configuration namespace
    """
    return Namespace(
        base_url=config['base_url'],
        cookie=config['cookie'],
        max_workers=config['max_workers'],
        max_retries=config['max_retries'],
        DEFAULT_CONNECT_TIMEOUT=config['DEFAULT_CONNECT_TIMEOUT'],
        DEFAULT_READ_TIMEOUT=config['DEFAULT_READ_TIMEOUT'],
        DEFAULT_RETRY_DELAY=config['DEFAULT_RETRY_DELAY'],
        DEFAULT_BATCH_SIZE=config['DEFAULT_BATCH_SIZE']
    )
