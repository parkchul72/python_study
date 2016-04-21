import os

def create_project_dir(directory):
    if not os.path.exists(directory):
        print("Creating Project " + directory)
        os.makedirs(directory)
