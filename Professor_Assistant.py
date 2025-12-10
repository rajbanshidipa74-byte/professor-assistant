import random
import os

def load_question_bank(path):
    pairs = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = [ln.strip() for ln in f.readlines()]
    i = 0
    while i < len(lines):
        if lines[i] == "":
            i += 1
            continue
        q = lines[i]
        j = i + 1
        while j < len(lines) and lines[j] == "":
            j += 1
        if j < len(lines):
            a = lines[j]
            pairs.append((q, a))
            i = j + 1
        else:
            break
    return pairs

def select_pairs_with_randint(pairs, k):
    n = len(pairs)
    if k >= n:
        indices = list(range(n))
        random.shuffle(indices)
        return [pairs[i] for i in indices]
    selected = set()
    result = []
    attempts = 0
    while len(selected) < k and attempts < k * 10 + 1000:
        idx = random.randint(0, n - 1)   # using randint as required
        if idx not in selected:
            selected.add(idx)
            result.append(pairs[idx])
        attempts += 1
    return result

def save_exam(pairs, output_path, title="Exam"):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"{title}\n\n")
        for i, (q, a) in enumerate(pairs, start=1):
            f.write(f"{i}. {q}\n\n")
        f.write("\nAnswer Key\n\n")
        for i, (q, a) in enumerate(pairs, start=1):
            f.write(f"{i}. {a}\n\n")

def interactive_program():
    print("Welcome to Professor Assistant version 1.0")
    name = input("Please Enter Your Name: ").strip()
    print(f"Hello Professor {name}, I am here to help you create exams from a question bank.")
    proceed = input("Do you want me to help you create an exam (Yes to proceed | No to quit the program)? ").strip().lower()
    if proceed not in ("yes", "y"):
        print(f"Program exits. Thank you Professor {name}. Have a good day!")
        return
    path = input("Please Enter The Path to the Question Bank file: ").strip()
    if not os.path.exists(path):
        print("The path you provided does not exist or file not found. Exiting.")
        return
    pairs = load_question_bank(path)
    if not pairs:
        print("No question-answer pairs were found in the provided file. Exiting.")
        return
    try:
        k = int(input("How many question-answer pairs do you want to include in your exam? ").strip())
    except ValueError:
        print("Invalid number. Exiting.")
        return
    outname = input("Where do you want to save your exam? (e.g. midterm.txt) ").strip()
    outpath = outname if os.path.isabs(outname) else os.path.join(os.getcwd(), outname)
    selected = select_pairs_with_randint(pairs, k)
    save_exam(selected, outpath, title=f"Exam created by Professor {name}")
    print(f"Congratulations Professor {name}. Your exam is created and saved in {outpath}.")
    again = input("Do you want me to help you create another exam (Yes to proceed | No to quit the program)? ").strip().lower()
    if again in ("yes", "y"):
        interactive_program()
    else:
        print(f"Thank you professor {name}. Have a good day!")

if __name__ == "__main__":
    interactive_program()
