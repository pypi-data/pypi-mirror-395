import os
from dotenv import load_dotenv

def load_env():
    """
    Load environment variables from config/.env
    """
    # Get the directory of the current file (mcp_server)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Path to config/.env
    env_path = os.path.join(current_dir, "config", ".env")
    
    load_dotenv(env_path)
    
    return {
        "patent_appkey": os.getenv("PATENT_DB_APPKEY"),
        "patent_secret": os.getenv("PATENT_DB_SECRET"),
        "patent_baseurl": os.getenv("PATENT_DB_BASEURL"),
    }
