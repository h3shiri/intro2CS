__author__ = 'S.H'
from hangman_helper import *

#Global constant set of valid lower case letters
alpha_init_index = 97
alpha_ending_index = 123
VALID_LETTERS = set([chr(i) for i in range(alpha_init_index,alpha_ending_index)])
ONE_GUESS = 1

#Updating the pattern using a letter guess
def update_word_pattern(word,pattern,letter):
    #iterating on the word one char at a time
    for i in range(len(word)):
        if word[i] == letter:
            #changing the pattern
            pattern = replace_letter(pattern,i,letter)
    return pattern

#assisting function that replaces a letter in the pattern
def replace_letter(pattern,n,letter):
    lst = [i for i in pattern]
    lst[n] = letter
    result = "".join(lst)
    return result

#assisting creating an empty pattern string according to the word
def create_empty_pattern(word):
    lst =["_"]*len(word)
    result = "".join(lst)
    return result

#creating the previously selected letters list
def previously_selected_letters(pattern,wrong_guess_list):
    result = set(pattern)
    result = result.union(wrong_guess_list)
    #result.remove("_") , it is possible to move redundant "_"
    return list(result)

#creating a function that checks if the game is over
def game_status(wrong_guess_lst,error_count,word,pattern,msg,game_is_on):
    #Too many wrong guesses
    if error_count >= MAX_ERRORS:
        msg = LOSS_MSG
        result = False
    #Player won the game
    elif word == pattern:
        msg = WIN_MSG
        result = False
    else:
        result = True
    return (result,msg)


#running a single game using the word list
def run_single_game(word_list):
    #Setting the game with a random word and empty pattern.
    word = get_random_word(word_list)
    pattern = create_empty_pattern(word)
    msg = DEFAULT_MSG

    #runing the game plus initial conditions
    game_is_on = True
    error_count = 0
    previously_selected = []
    wrong_guess_lst = []
    while game_is_on:
        #checking the game has not ended
        check = game_status(wrong_guess_lst,error_count,word,pattern,msg,game_is_on)
        game_is_on = check[0]
        msg = check[1]
        if (game_is_on == False):
            break

        #displaying the state and asking for input
        display_state(pattern,error_count,wrong_guess_lst,msg)
        user_input = get_input()

        #checking the user input type
        if (user_input[0] == LETTER):
            #checking it is a valid letter
            letter = user_input[1]
            previously_selected = previously_selected_letters(pattern,wrong_guess_lst)
            if letter not in VALID_LETTERS:
                msg = NON_VALID_MSG
            #if the user has chosen a previously selcted letter
            elif letter in set(previously_selected):
                msg = ALREADY_CHOSEN_MSG
            #if the user chose correctly
            elif letter in set(word):
                pattern = update_word_pattern(word,pattern,letter)
                msg = DEFAULT_MSG
            else:
                wrong_guess_lst.append(letter)
                error_count += ONE_GUESS
                msg = DEFAULT_MSG
        elif (user_input[0] == HINT):
            #giving a hint by filtering the words and finding the most common letter
            relevant = filter_words_list(word_list,pattern,wrong_guess_lst)
            HINT_MSG = choose_letter(relevant,pattern)
            msg = HINT_MSG

    display_state(pattern,error_count,wrong_guess_lst,msg,ask_play=True)

#filtering the relevant words for the hint
def filter_words_list(words, pattern, wrong_guess_lst):
    result =[]

    #const for counters
    step = 1
    #words with equal length
    words_with_equal_lengh = [i for i in words if len(i) == len(pattern)]
    relevant_words =[]
    #sorting out relevant words with the matching letters
    for i in words_with_equal_lengh:
        counter = 0
        for j in range(len(pattern)):
            if ((pattern[j] != i[j]) and (pattern[j] != "_")):
                break
            else:
                counter += step
        if counter == len(pattern):
            relevant_words.append(i)
    #sorting out from the relevant words
    for i in relevant_words:
        success_counter = 0
        #checking one letter at a time if it was previously disqualified
        for j in range(len(i)):
            if i[j] in set(wrong_guess_lst):
                break
            else:
                success_counter += step
        #working candidates
        if success_counter == len(pattern):
            result.append(i)

    return result

def choose_letter(words,pattern):
    #running on all the letters then on the list word by word
    letters = [chr(i) for i in range(alpha_init_index,alpha_ending_index)]
    counters = [0]*(len(letters))
    #TODO: check if they meant how much in each individual word or just 1
    step = 1
    under_low_frequency = -1
    for i in range(len(letters)):
        for j in words:
            #for each word we check the frequency of the letter
            for k in range(len(j)):
                if letters[i] == j[k]:
                    counters[i] += step

    #finding a valid hint with maximal frequency
    pattern_valid_letters = set(pattern)
    maximal_frequency = under_low_frequency
    #going on the indexes for valid letters and increasing frequencies
    for i in range(len(letters)):
        if (letters[i] not in pattern) and (counters[i] >=maximal_frequency) :
            index = i
            maximal_frequency = counters[i]
    result = letters[index]
    #TODO: test this function extensively
    return result

#TODO: test gui interface in the aquarium
#Main function
def main():
    word_list = load_words('word.txt')
    run_single_game(word_list)
    user_input = get_input()
    #Running the game again if the user selected play_again
    while (user_input[0] == PLAY_AGAIN):
        run_single_game(word_list)
        user_input = get_input()



#Running the programme
if __name__ == "__main__":
    start_gui_and_call_main(main)
    close_gui()
