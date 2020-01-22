import pandas as pd
import os
import sys
from pathlib import Path
from tqdm import tqdm
import subprocess

data_dir = Path('data')
demo_dir = data_dir / 'demos'
metadata = data_dir / 'metadata.json'

if not metadata.is_file():
    raise FileNotFoundError(f"{metadata} not found. You probably need to run the demo_scraper (run 'scrapy crawl hltv')")

metadata_df = pd.read_json(metadata).set_index('dir_name')

if __name__ == '__main__':

    faulty = []

    for dir_name, r in tqdm(metadata_df.iterrows()):
        
        demo_url = r['demo_url']

        path = demo_dir / dir_name

        try:
            os.makedirs(path)
            print(f"Download start: {demo_url}")

            r = subprocess.call(["wget", "-P", str(path), demo_url])
            if r != 0:
                print(f"Download issue with {demo_url}")
                faulty += [demo_url]
                continue
        
            print(f"Download done: {demo_url} to {path}")

        except FileExistsError:
            print(f"Skipping {dir_name}, already exists")
        except:
            print(f'Download canceled, cleaning unfinished {path}...')
            subprocess.call(['rm', '-r', str(path)])
            sys.exit()


    print(f"Download finished.")

    if len(faulty) > 0:
        print('Issues with:')
        for f in faulty:
            print(f)
