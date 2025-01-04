import random

#print(dir(random))

rando = random.choice(['Rock', 'Paper', 'Scissors'])
print("Hi user, I hope you are doing well\nPlease choose between Rock, Paper or Scissors\nChoose wisely")

Valid = True

while Valid:
    user_Choice = input("Choice: ")
    print ("Computer choice: ", rando)
    if user_Choice == 'Rock':
        Valid = False
        if rando == 'Rock':
            print("You Tie!")
        elif rando == "Paper":
            print("You Lose!")
        elif rando == 'Scissors':
            print("You Win!")
    elif user_Choice == 'Paper':
        Valid = False
        if rando == 'Rock':
            print("You Win!")
        elif rando == "paper":
            print("You Tie!")
        elif rando == 'Scissors':
            print("You Lose!")
    elif user_Choice == 'Scissors':
        Valid = False
        if rando == 'Rock':
            print("You Lose!")
        elif rando == "paper":
            print("You Win!")
        elif rando == 'Scissors':
            print("You Tie!")
    else:
        print ("Not valid choice")
        Valid = True

