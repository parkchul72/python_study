import os

# Each website you want to crawl is a seperate project(folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print("Creating Project " + directory)
        os.makedirs(directory)

# Create queue and crawled files(if not created)
def crate_data_files(project_name, base_url):