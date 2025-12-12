import random
import linecache

def rec(a):
    d = '/'.join(__file__.split('\\')[:-1])
    with open(d + "/data/record.txt", "r+") as r:
        if  int(r.read()) < a:
            r.truncate()
            r.seek(0)
            r.write(str(a))
            print(f"новый рекорд (слов угадано): {a}")

def get_random_word(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f)
    used_lines = set()
    while len(used_lines) < total_lines:
        random_line_num = random.randint(1, total_lines)
        if random_line_num in used_lines:
            continue
        used_lines.add(random_line_num)
        word = linecache.getline(filename, random_line_num)
        yield word.strip()
    linecache.clearcache()


