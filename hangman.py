# Josh Klaus
# CS131A
# Python

# Implementation of the game Hangman as modified from code adopted from these sources:
# ActivateState Code Recipes : thelivingpearl.com
# This game pulls a random 4 or 5 letter word and allows the user 5 chances to guess a 
# a letter in the word.  The game ends when either all the letters have been guessed (the user wins), 
# or the user has made five incorrect guesses (the user loses).  

import random
import re

# class that holds the game functionality
class Hangman:

    # initialize the game
    def __init__(self,word):
        self.word = word
        self.wrong = []
        self.correct = []
    
    # function for guessing letters 
    def guess(self,letter):
        if letter in self.word and letter not in self.correct:
            self.correct.append(letter)
        elif letter not in self.word and letter not in self.wrong:
            self.wrong.append(letter)
    
    # determines if game is won or lost    
    def game_over(self):
        return self.game_won() or (len(self.wrong) == 5)
    
    # determines if player is a winner    
    def game_won(self):
        if '_' not in self.hide_word():
            return True
        return False
    
    # function for concealing the word while guessing    
    def hide_word(self):
        hidden_word = ''
        for letter in self.word:
            if letter not in self.correct:
                hidden_word += '_'
            else:
                hidden_word += letter + ''
        return hidden_word

    # function for updating the status of word, incorrect, and correct letters    
    def print_game_status(self):
        print('Word: ' + self.hide_word())
        print( 'Incorrect Letters: ') 
        print(', '.join(self.wrong))        # print list as a string
        print( 'Correct Letters: ')
        print(', '.join(self.correct))      # print list as a string

# function for selecting a collection of random words to pull from
# for the user to play the game with.
def random_word():

    # Pattern of 4 letter words:
    # where 1st letter is one of [r,s,t,n,l,h]; 
    # next two letters are a vowel followed by a consonant; 
    # ending with one random letter
    pattern_a = r'^[rstnlh][aeiou][^aeiou].$'
    four_letter_words = []

    # Pattern of 5 letter words:
    # where 1st letter is one of [r,s,t,n,l,h]; 
    # next two letters are a vowel followed by a consonant; 
    # next letter is a vowel;
    # ending with one random letter
    pattern_b = r'^[rstnlh][aeiou][^aeiou][aeiou].$'
    five_letter_words = []

    # Pattern of 6 letter words where:
    # 1st letter is a consonant but not a s, z or x; 
    # next two letters are vowels;
    # and there are 3 letters that are not a q, x or z;
    # ending with one random letter
    pattern_c = r'^[^A-Zqxz][aeiou]{2}[^qxz]{2}.$'
    six_letter_words = []

    for line in open('/usr/share/dict/words'):
        if re.search ( pattern_a, line) :
            four_letter_words.append (line.strip())
        if re.search ( pattern_b, line) :
            five_letter_words.append (line.strip())
        if re.search ( pattern_c, line):
            six_letter_words.append (line.strip())

    # Chose to only add 4 and 5 letter words to bank for simplification
    # Optionally could add 6 letter words by add ( + six_letter_words )to next line
    all_words = four_letter_words + five_letter_words

    return all_words[random.randint(0,len(all_words))]

# function for running the game
def main():
    
    answer = 'yes'
    
    while answer != 'no':
        game = Hangman(random_word())
        while not game.game_over():
            game.print_game_status()
            user_input = input('\nEnter a letter: ').lower()    # Converts caps to lowercase
            if len(user_input) >= 2:
                while True:
                    print( "\nYou must enter only one letter!\n")
                    try_again = input('Try again: ').lower()    # Converts caps to lowercase
                    if len(try_again) == 1:
                        game.guess(try_again)
                        break
                    else:
                        continue
            else:
                game.guess(user_input.lower())

        game.print_game_status()    
        if game.game_won():
            print( '\nCongratulations! You are the winner of Hangman!')
        else:
            print( '\nSorry, you have lost in the game of Hangman...')
            print( 'The word was ' + game.word)
        
        # Allows user to repeat game
        answer = input('Do you want to play again? Yes/No? ').lower()   # Converts caps to lowercase 
        
    print( '\nGoodbye!\n')
        
if __name__ == "__main__":
    main()
    