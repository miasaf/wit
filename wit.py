# Upload 170
import os
import sys


def init(path):
    current_dir = os.path.join(path, '.wit')
    sub_folders = ('images', 'staging_area')
    if not os.path.exists(current_dir):
        os.mkdir(current_dir)
        for folder in sub_folders:
            os.mkdir(os.path.join(current_dir, folder))


if len(sys.argv) > 1 and sys.argv[1] == 'init':
    init(os.getcwd())
# Reupload