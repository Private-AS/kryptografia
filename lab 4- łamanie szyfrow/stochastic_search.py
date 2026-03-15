# python
#!/usr/bin/env python3
import random
import math
from collections import Counter
from multiprocessing import Pool, cpu_count

TARGET = "cryptography"
COMMON_WORDS = ["the", "and", "that", "have", "for", "with", "not", "this", "but", "from", TARGET]
LETTER_FREQ_SCORE = {
    'e': 12.0, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7,
    's': 6.3, 'r': 6.0, 'h': 6.1, 'l': 4.0, 'd': 4.3, 'c': 2.8,
    'u': 2.8, 'm': 2.4, 'w': 2.4, 'f': 2.2, 'g': 2.0, 'y': 2.0,
    'p': 1.9, 'b': 1.5, 'v': 1.0, 'k': 0.8, 'x': 0.2, 'q': 0.1, 'j': 0.15, 'z': 0.07
}

def make_columns(cypher, width, height):
    return [cypher[i*height:(i+1)*height] for i in range(width)]

def reconstruct(columns, order):
    height = len(columns[0])
    width = len(order)
    rows = []
    for r in range(height):
        row_chars = [columns[order[c]][r] for c in range(width)]
        rows.append("".join(row_chars))
    return "".join(rows)

def score_text(text):
    t = text.lower()
    score = 0.0
    # huge bonus if target appears so the search strongly prefers it
    if TARGET in t:
        score += 1e7
    for w in COMMON_WORDS:
        count = t.count(w)
        if count:
            score += 50.0 * count
    counts = Counter([c for c in t if c.isalpha()])
    total = sum(counts.values()) or 1
    for ch, freq in LETTER_FREQ_SCORE.items():
        score += freq * (counts.get(ch, 0) / total) * 2.0
    score += t.count(" ") * 3.0
    return score

def random_neighbor(order):
    a = random.randrange(len(order))
    b = random.randrange(len(order))
    if a == b:
        b = (a + 1) % len(order)
    new = list(order)
    new[a], new[b] = new[b], new[a]
    return new

def search_worker(args):
    columns, iterations, start_temp, seed, target = args
    random.seed(seed)
    n = len(columns)
    current = list(range(n))
    random.shuffle(current)
    current_text = reconstruct(columns, current)
    current_score = score_text(current_text)
    # if starting configuration already contains target, return immediately
    if target in current_text.lower():
        return (current_score, current_text, list(current), True)
    best = (current_score, current_text, list(current))
    temp = start_temp
    for i in range(iterations):
        neighbor = random_neighbor(current)
        neighbor_text = reconstruct(columns, neighbor)
        neighbor_score = score_text(neighbor_text)
        # if neighbor contains target, return immediately
        if target in neighbor_text.lower():
            return (neighbor_score, neighbor_text, list(neighbor), True)
        delta = neighbor_score - current_score
        if delta > 0 or math.exp(delta / max(1e-6, temp)) > random.random():
            current, current_text, current_score = neighbor, neighbor_text, neighbor_score
            if current_score > best[0]:
                best = (current_score, current_text, list(current))
        temp *= 0.9995
    return (best[0], best[1], best[2], False)

def solve_heurstic(cypher, width, height, restarts=8, iterations=20000):
    columns = make_columns(cypher, width, height)
    args = []
    workers = min(restarts, max(1, cpu_count()))
    for i in range(restarts):
        args.append((columns, iterations, 5.0, random.randrange(1 << 30), TARGET))
    with Pool(workers) as p:
        results = p.map(search_worker, args)
    # sort by score
    results.sort(reverse=True, key=lambda x: x[0])
    best_score, best_text, best_order, found_flag = results[0]
    # if any worker found the target, mark it
    contains = any(r[3] for r in results)
    return {
        "score": best_score,
        "text": best_text,
        "order": best_order,
        "contains_target": contains,
        "all_results": results
    }

if __name__ == "__main__":
    SIZES = [(12, 15)]
    CYPHER = "ssyl ipiewiepst yplucts hvdt oseg  enc eeoncdsdraof wentk rry ipr ehsyhedeeamowekoaoltfoeeetrfoy ca  r uamaraely l rsynssoch pnisoeyemle c hbrhbepuri tn ytuccin  caybmtos i tia isr"

    for width, height in SIZES:
        if width * height != len(CYPHER):
            print(f"Skipping {width}x{height}: size mismatch")
            continue
        print(f"Trying {width}x{height} ...")
        res = solve_heurstic(CYPHER, width, height, restarts=cpu_count()*4, iterations=40000)
        print("Best score:", res["score"])
        print("Contains 'cryptography':", res["contains_target"])
        print("Candidate text (first 300 chars):")
        print(res["text"][:300])
        print("-" * 60)