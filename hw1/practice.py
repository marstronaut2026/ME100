import random as r

#function for guessing
def guessr(): 
    while True:
        guess = int(input('Guess a number between 1 and 10:\n')) #guess input
        if (guess < 1 or guess > 10): #make sure guess is valid
            print('That is not a valid guess')
            print('\nGuess again.\n')
            continue
        else:
            break #end loop when guess is valid
    return guess

number = r.randint(1, 10) #random number generator
x = 0 #counter variable initialization


#print(number) #for testing
while True:
    x += 1 #increase counter every guess
    guess = guessr() 
    if (guess < number):
        print('\nGuess is too low.')
        print('Guess again.')
    elif (guess > number): 
        print('\nGuess is too high')
        print('Guess again.')
    else:  
        break #end loop if number is guessed correctly
if (x == 1):
    print('You cheated!') #obviously found my testing code
else:
    print('Nice guess!')
    print('You guessed the number in %i tries' %x)

