"""
Useful functions for SPAGHETTI
"""

import os


def find_checkpoint(dir: str):
    """
    Find the latest checkpoint in the directory
    args:
        dir: str, the directory to search for the checkpoint for Pytorch Lightning
    return:
        str or None. The str of the path to the latest checkpoint that ends with .ckpt
        If no checkpoint is found, return None
    """
    files = []
    for path, _, file in os.walk(dir):
        for f in file:
            if f.endswith(".ckpt"):
                files.append(os.path.join(path, f))
    if len(files) == 0:
        return None
    else:
        return max(files, key=os.path.getctime)
