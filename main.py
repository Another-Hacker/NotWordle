from pprint import pprint
from random import choice
from string import ascii_lowercase
import datetime


with open('wordlist.txt','r') as f:
    words=f.read().split()
    target=choice(words)

#overwrite target to set word for debugging
# target = 'evoke'
letters = ' '.join(ascii_lowercase)

guess = input("Guess a five letter word: ")

while True:

#player debug
    if guess.lower() == "debug all":
        del words
        name = f"debug-{datetime.datetime.now().strftime('%Y%m%d-%H-%M-%S')}.txt"
        with open(name,'w') as d:
            pprint(vars(),d)
        print(f"debug file created at {name}")
        with open('wordlist.txt','r') as f:
            words=f.read().split()

#player escape
    if guess.lower() == 'i give up':
        print(f"The word was {target}")
        if input("Do you want to play again? (y/n): ").lower() == 'n': break
        else: 
            target = choice(words)
            letters = ' '.join(ascii_lowercase)
            guess = input("Guess a five letter word: ")
            continue

    #lower guess
    guess = guess.lower()
#check for valid input. are there other cases to watch for?
    if guess.isdigit() or guess.isspace() or guess == '' or len(guess) != 5 or not guess.isalpha():
        guess = input("Not a valid guess. Guess again: ")
        continue
    if guess not in words:
        guess = input(f"\"{guess}\" is not a real word. Guess again: ")
        continue
    
    

#check for correct guess
    if guess == target:
        print(f"You got it! The word was {target.upper()}")
        if input("Do you want to play again? (y/n): ").lower() == 'n': break
        else: 
            target = choice(words)
            letters = ' '.join(ascii_lowercase)
            with open('debug','a') as d:
                d.write(f"{target}\n")
            guess = input("Guess a five letter word: ")
            continue

#evaluate guess to create hint
    #set intermediate vars
    previousGuess=guess
    testList=[]
    clueStr=''

    #create guess,target array
    for i in range(5):
        testList.append([guess[i],target[i]])
    

    for currentLetters in testList:
        guessLetter=currentLetters[0]
        targetLetter=currentLetters[1]

        countTarget = target.count(guessLetter)
        countOutStr = clueStr.lower().count(guessLetter)
        countGuess = guess.count(guessLetter)

        if countTarget == countOutStr and countTarget != 0:
            clueStr += '*'
            continue

        if guessLetter==targetLetter:
            clueStr+=guessLetter.upper()
            letters = letters.replace(guessLetter,guessLetter.upper())
            continue

        exists=False
        for chrPair in testList:
            if guessLetter == chrPair[1]:
                exists=True
                break
        
        if exists: clueStr+=guessLetter 
        else: 
            clueStr+='*'
            letters = letters.replace(guessLetter,'-')

    print(clueStr)
    print(guess)
    print(letters)
    guess = input("Incorrect. Guess again: ")

