from solitaire import *
from blum_blum_shub import *

def create_file():
    print("Create file, enter mode:")
    mode = input()

    with open("algorithm_&_seed", 'w') as f:
        if mode == 'solitaire':
            f.write("Solitaire\n")
            seed = generate_seed_solitaire()
            for s in seed:
                f.write(f'{s} ')
        elif mode == 'blumblumshub':
            f.write('BlumBlumShub\n')
            n = generate_n_for_seed_blumblum()
            seed = generate_seed_blumblum(n)
            f.write(f'{n}\n{seed}')

def read_from_file():
    with open("algorithm_&_seed", "r") as f:
        mode = f.readline().split()[0]
        if mode == "Solitaire":
            seed = f.read().split()
            return generate_key_with_solitaire, [int(s) for s in seed]
        if mode == "BlumBlumShub":
            n = int(f.readline())
            seed = int(f.readline())
            return generate_key_with_bbs, (n, seed)

# create_file()
