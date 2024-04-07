import pygame 
import random  


class WordBank: 

    def __init__(self, level):

        self.level = level
        self.words = self.load_words()
        self.current_word, self.curren_description = self.get_new_word()
        self.letter_bank = self.create_letter_bank()

    #Will Load Words and Descriptions based on Grade Level 
    def load_words(self):
        grade_4_words = {
            'MEDICINE': 'Something a person takes when they are feeling sick or ill',
            'CLIMATE': 'The average weather conditions in an area over a long period',
            'FRAGMENT': 'A small part broken off or separated from something',
            'CIRCUIT': 'A path for an electrical current to flow around',
            'POLLUTION': 'The presence harmful substances into the environment '
        }

        grade_5_words = {
            'EXAMINATION': 'A formal test of a person’s knowledge or proficiency in a subject or skill',
            'TECHNIQUE': 'A way of carrying out a particular task, especially the execution or procedure',
            'SUFFICIENT': 'Enough or adequate',
            'ENVIRONMENT': 'The surroundings or conditions in which a person, animal, or plant lives or operates',
            'CONSEQUENCE': 'A result or effect of an action or condition'
        }

        if self.level == 4:
            return grade_4_words
        elif self.level == 5:
            return grade_5_words
        else:
            return {}
    #Select random word and description based on available options   
    def get_new_word(self):
        if self.words:
            word, description = random.choice(list(self.words.items()))
            return word, description
        else:
            return None, None
        
    #Creating the letter bank for the girs 
    def create_letter_bank(self):
        current_word, _ = self.get_new_word()
        unique_letters = set(current_word)


        num_random_letters = 30 - len(unique_letters)
        all_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        # Create a list of random letters, making sure not to duplicate any in the word
        random_letters = [letter for letter in all_letters if letter not in unique_letters]
        random.shuffle(random_letters)
        
        letter_bank = list(unique_letters) + random_letters[:num_random_letters]
        random.shuffle(letter_bank)

        return letter_bank
    
    # Return all the words in the word bank
    def get_all_words(self):
        return list(self.words.keys())