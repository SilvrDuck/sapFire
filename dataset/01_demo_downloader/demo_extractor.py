import pandas as pd
import os
import sys
from pathlib import Path
import subprocess
import tqdm as tqdm
from demo_downloader import demo_dir


issues = []

def extract_in_dir(path):
        print(f'Extraction start: {path}')

        for f in path.iterdir():
            if f.suffix != '.dem':
                r = subprocess.call(["unzip", "-o", str(f), "-d", str(path)])
                if r != 0:
                    r = subprocess.call(["unrar", "x", "-y", str(f), str(path)])
                if r != 0:
                    print(f'Extraction issue with {f}')                
                    issues += [f]
                else:
                    # clean extracted files
                    subprocess.call(["rm", str(f)])

        print(f'Extraction done: {path}')


if __name__ == '__main__':
    for d in demo_dir.iterdir():
        extract_in_dir(d)
        
    if len(issues) > 0:
        print('Issues with:')
        for f in issues:
            print(f)
    