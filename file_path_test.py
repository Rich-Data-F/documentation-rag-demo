import os
import sys
from python-dotenv import load_dotenv, find_dotenv


try:
    # Locate the .env file
    dotenv_path = find_dotenv()
    if not dotenv_path:
        raise FileNotFoundError("No .env file found.")
    # Load the .env file
    load_dotenv(dotenv_path)
    # Print the path of the .env file
    print(f"The .env file being used is: {dotenv_path}")
    # Retrieve a sample environment variable to verify loading
    knowledge_base_dir = os.getenv("KNOWLEDGE_BASE_DIR")
    print(f"KNOWLEDGE_BASE_DIR: {knowledge_base_dir}")
except Exception as e:
    print(f"An error occurred: {e}")

# Check Operating System
os_details = f"""
Operating System: {os.name}
Platform: {os.sys.platform}
OS Details: {os.uname() if hasattr(os, 'uname') else 'N/A'}
"""

# Check Python Version
python_version = f"""
Python Version: {sys.version}
Python Version Info: {sys.version_info}
"""

# Check for Virtual Environment
is_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
virtual_env = os.getenv('VIRTUAL_ENV')
venv_status = f"""
Running in Virtual Environment: {is_venv}
Virtual Environment Path: {virtual_env if virtual_env else 'Not in a virtual environment'}
"""

# Print environment details
print(f"{os_details}\n{python_version}\n{venv_status}")

# Additional checks for WSL
if 'WSL_DISTRO_NAME' in os.environ:
    print("Running in WSL")

print("\nrépertoire de départ " + os.getcwd())

if os.path.exists(os.path.join(os.path.dirname(__file__),'TDAH')):
    print(os.getcwd()+ "was well recognised")
else: 
    print("path of the os.path.join(os.path.dirname(__file__) not understood")

# if knowledge_base_dir is None:
#     raise ValueError("KNOWLEDGE_BASE_DIR environment variable not set")
paths_list=[
    '/g/My Drive/Pdfs/Sample_for_Rag',
    '/mnt/g/My Drive/Pdfs/Sample_for_Rag',
    'g\My Drive\Pdfs\Sample_for_Rag',
    'g\My Drive\Pdfs\Sample_for_Rag',
    'g:\My Drive\Pdfs\Sample_for_Rag',
    "/mnt/g/My Drive/Pdfs/Sample_for_Rag",
    "./mnt//g://My Drive//Pdfs//Sample_for_Rag",
    "./mnt//g://My Drive//Pdfs//Sample_for_Rag",
    "./mnt/g/My Drive/Pdfs/Sample_for_Rag"
]

for path in paths_list:
    if os.path.exists(path):
        print(path+" is recognised")
    else:
        print(path+" was not understood")


load_dotenv()

knowledge_base_dir = os.getenv("KNOWLEDGE_BASE_DIR")
print(knowledge_base_dir)
print(os.path.exists(knowledge_base_dir))