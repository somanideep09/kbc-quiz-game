import requests
import random
import html

# get 10 questions from API
url = "https://opentdb.com/api.php"

params = {
    "amount": 10,
    "type": "multiple"
}

# wrapped in try/except so a bad connection doesn't just crash the whole script
try:
    response = requests.get(url, params=params, timeout=10)
except requests.exceptions.RequestException as e:
    print(f"Error while connecting to the trivia API: {e}")
    exit()

if response.status_code != 200:
    print("Error while getting questions")
    exit()

# sometimes the API sends back junk instead of real JSON, catching that too
try:
    data = response.json()
except ValueError:
    print("Error: the API returned invalid (non-JSON) data")
    exit()

if data["response_code"] != 0:  # 0 = success, anything else = something went wrong
    print("Could not get questions")
    exit()

questions = data["results"]  # contains all 10 que with their correct ans and incorrect ans from API's  

random.shuffle(questions)  # so it's not the same question order every time

prizes = [
    100000,
    320000,
    400000,
    450000,
    500000,
    1000000,
    2000000,
    3000000,
    4000000,
    5000000
]

i = 0
lifeline_used = False  # only get ONE 50-50 for the whole game

for question in questions:

    # html,unesacpe makes question and options clean 
    question_text = html.unescape(question["question"])
    correct_answer = html.unescape(question["correct_answer"])
    wrong_answers = [
        html.unescape(answer)                           # list comprehension method 
        for answer in question["incorrect_answers"]
    ]

    options = wrong_answers + [correct_answer]
    random.shuffle(options)

    print("\n" + question_text)

    for j in range(len(options)):
        print(f"{j + 1}. {options[j]}")

    if not lifeline_used:
        use_lifeline = input("Use your 50-50 lifeline? (y/n): ").strip().lower()

        if use_lifeline == "y":
            lifeline_used = True

            # grab the wrong ones, randomly kill 2 of them
            wrong_options_left = [opt for opt in options if opt != correct_answer]
            options_to_remove = random.sample(wrong_options_left, 2)

            for opt in options_to_remove:
                options.remove(opt)

            print("\n50-50 used! Two wrong answers removed.\n")
            print(question_text)

            for j in range(len(options)):
                print(f"{j + 1}. {options[j]}")

    while True:

        try:
            answer = int(input(f"Enter your answer (1-{len(options)}): "))

            if 1 <= answer <= len(options):
                break
            else:
                print(f"Please enter a number between 1 and {len(options)}.")

        except ValueError:
            print("Invalid input! Enter a number.")

    selected_answer = options[answer - 1]

    if selected_answer == correct_answer:

        print("Correct Answer! 🎉")
        print(f"You won ₹{prizes[i]}")

        i += 1

    else:
        correct_index = options.index(correct_answer) + 1

        print("Wrong Answer!")
        print(f"Correct answer was option {correct_index}: {correct_answer}")
        print("Better luck next time!")
        break

else:
    # only hits if we never broke out, meaning every question was right
    print(f"\n🏆 Congratulations! You answered all questions and won ₹{prizes[i - 1]}!")