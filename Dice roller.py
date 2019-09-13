import random

'''
The question being answered is:
"What is the probability of rolling at least requiredSixes '6's in diceGiven rolls?"
'''

winCounter = 0 ## every successful set of rolls adds one to this

def roll(diceGiven, requiredSixes): ## conducts one set of rolls using a diceGiven number of dice
    global winCounter
    sixesCounter = 0
    for i in range(diceGiven):
        if random.randint(1, 6) == 6: ## upon a successful roll, sixesCounter increments
            sixesCounter += 1
        if sixesCounter >= requiredSixes: ## checks whether requiredSixes have been reached
            winCounter += 1
            break

def sixrolls(gamesPlayed, diceGiven, requiredSixes): ## calls rolls() a gamesPlayed number of times to get a large number of test rolls
    for i in range(gamesPlayed):
        roll(diceGiven, requiredSixes)
    print("Dice given per trial: " + str(diceGiven))
    print("Number of sixes required to pass: " + str(requiredSixes))
    print("Number of trials performed: " + str(gamesPlayed))
    print("Win rate: " + str(winCounter/gamesPlayed))

print("Number of sixes required:")
requiredSixes = int(input())
print("Number of dice given:")
diceGiven = int(input())
print("Number of games played:")
gamesPlayed = int(input())

sixrolls(gamesPlayed, diceGiven, requiredSixes)


        
