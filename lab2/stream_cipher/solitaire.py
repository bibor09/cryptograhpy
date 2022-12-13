import random
import sys

def swap_white(k, n, white):
    try:
        i = k.index(white)
    except:
        sys.exit(0)

    if i == n - 1:
        k[2:n] = k[1:n-1]
        k[1] = white
    else:
        k[i] = k[i+1]
        k[i+1] = white

def swap_black(k, n, black):
    try:
        i = k.index(black)
    except:
        sys.exit(0)

    if i == n - 1:
        k[3:n] = k[2:n-1]
        k[2] = black
    elif i == n - 2:
        k[2:n-1] = k[1:n-2]
        k[1] = black
    else:
        k[i] = k[i+2]
        k[i+2] = black

def divide_and_swap(k, n, black, white):
    i = k.index(white) 
    j = k.index(black)
    if j < i:
        l = i
        i = j
        j = l
            
    first = k[0:i]
    last = k[j+1:n]
    middle = k[i:j+1]

    k[0:len(last)] = last
    k[n-len(first):n] = first
    k[len(last):n-len(first)] = middle

def count_and_swap(k, n, black, white):
    c = k[n-1] if k[n-1] != black else white
    first = k[0:c]
    last = k[c:n-1]

    k[0:n-c] = last
    k[n-c-1:n-2] = first

def solitaire(seed):
    k = seed[:]
    WHITE = 53
    BLACK = 54
    c = WHITE
    n = len(k)
    
    while c == WHITE or c == BLACK:
        # Swap white joker with card after, or with 2nd if joker is last
        swap_white(k, n, WHITE)

        # Swap black joker with card after with 2 distance, or count from the beginning
        swap_black(k, n, BLACK)

        # Divide in 3, middle is limited by the jokers, and swap outer parts
        divide_and_swap(k, n, BLACK, WHITE)

        # Count down from beginning the value of the last card and swap
        count_and_swap(k, n, BLACK, WHITE)

        # Count down from beginning the value of the first card and return value
        c = k[0]
    
    key = k[c] if k[c] != BLACK else WHITE
    return k, key

def generate_seed_solitaire():
    seed = [i+1 for i in range(54)]
    random.shuffle(seed)
    return seed

def generate_key_with_solitaire(n, seed):
    k = seed[:]
    key_stream = []
    for _ in range(n):
        # Generate two numbers and multiply them
        k, key_1 = solitaire(k)
        k, key_2 = solitaire(k)
        key = (key_1 * key_2) % 256
        key_stream.append(key)
    return key_stream
