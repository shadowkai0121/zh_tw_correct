
import argparse
from glob import glob
import regex as re
import requests


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dict_url", help="category url")
    parser.add_argument("--correct_url", "-c",  help="correct_url", required=False)
    
    args = parser.parse_args()

    if args.dict_url.startswith("http://") or args.dict_url.startswith("https://"):
        response = requests.get(args.dict_url)
        response.raise_for_status()
        DICTIONARY = response.text.splitlines()
    else:
        with open(args.dict_url, "r", encoding="utf-8") as f:
            DICTIONARY = f.readlines()

    DICTIONARY = [x.split(' ') for x in DICTIONARY if x]

    if args.correct_url:
        with open(args.correct_url, "r", encoding="utf-8") as f:
            CORRECT = f.read()
            CORRECT = CORRECT.split('\n')
            CORRECT = [x.split(",") for x in CORRECT if x]
            CORRECT = {x[0]: x[1].split(" ") for x in CORRECT}
    else:
        CORRECT = []

    for file in glob("./**/*.md"):
        with open(file, "r", encoding="utf8") as f:
            txt = f.read()
            for word in DICTIONARY:
                if len(word) < 2:
                    continue
                txt, count = re.subn(
                    word[0].strip()+ r'\b', word[1].strip(), txt)
                if count > 0:
                    print(f'Replaced {word[0].strip()} with {word[1].strip()} x {count}')

            if len(CORRECT) == 0:
                continue
            for correct, words in CORRECT.items():
                correct = correct.strip()
                for word in words:
                    w = word.strip()
                    if not w:
                        continue

                    pat = re.compile(re.escape(w) + r'\b')
                    txt, n = pat.subn(correct, txt)
                    if n:
                        print(f"Replaced {word} with {correct} x {n}")
        with open(file, "w", encoding="utf8", newline='\n') as f:
            f.write(txt)