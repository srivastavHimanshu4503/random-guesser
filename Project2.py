# Guess the random number
import random

def game():
    """The game function returns the score of number of scores a user takes to guess a random number between 1 to 100."""
    random_number = random.randint(1, 100)
    number_of_attempts = 0
    while True:
        user_guess = int(input("Enter number between from 1 to 100: "))
        number_of_attempts += 1
        if (user_guess == random_number):
            return number_of_attempts
        elif (user_guess > random_number):
            print("Lower the number.")
        else:
            print("Increase the number.")

if __name__ == "__main__":
    print(f"You took {game()} attempts to guess the random number.")