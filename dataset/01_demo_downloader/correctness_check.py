from demo_downloader import metadata_df, demo_dir
from collections import defaultdict


issues = defaultdict(lambda: [])

if __name__ == '__main__':    

    for d in demo_dir.iterdir():
        
        files = list(d.iterdir())
        
        if 'issue.txt' in [f.name for f in files]:
            print(f'Probably extraction error for {d}, issue.txt present.')
            continue

        if not all([f.suffix == '.dem' for f in files]):
            print(f'Not only .dem files in {d}.')
            continue

        maps = metadata_df.loc[d.name]['maps']
        if len(maps) != len(files):
            print(f'Inconsistent number of .dem files with respect to maps in metada for {d}.')
            print('maps:', maps)
            print('files:', files)

            continue

        # get constistent renaming
        map_match = {
            map: file 
            for map in maps 
            for file in files 
            if any([
                map.lower() in file.name.lower(),
                map.lower() == 'cobblestone' and 'cbble' in file.name.lower(),
            ])
        }

        if len(map_match) != len(maps):
            print(f'Couldn’t create consistant mapping from maps to files for renaming for {d}.')
            continue
        else:
            for i, map in enumerate(maps):
                map_match[map].rename(f'{d}/map-{i+1}_{d.name}_{map.lower()}.dem')