import requests, click, json
import random
from PyInquirer import prompt
API_KEY = 'b972c7ca44dda72a5b482052b1f5e13470e01477f3fb97c85d5313b3c112627073481104fec2fb1a0cc9d84c2212474c0cbe7d8e59d7b95c7cb32a1133f778abd1857bf934ba06647fda4f59e878d164'
query_params = {
    'api_key': API_KEY
}
category = ['defn', 'syn', 'anton'];


def get_defn(word):
    url_format = 'https://fourtytwowords.herokuapp.com/word/{}/definitions'

    response = requests.get(url_format.format(word), params=query_params)
    if response:
        for elem in response.json():
            click.echo('\n>>' + elem['text'])
    else:
        click.echo('\n >> Invalid word')


# Api to get the Synonyms for the user enetered word.
def get_syn(word):
    url_format = 'https://fourtytwowords.herokuapp.com/word/{}/relatedWords'

    response = requests.get(url_format.format(word), params=query_params)
    if response:
        for elem in response.json():
            if elem['relationshipType'] == 'synonym':
                for words in elem['words']:
                    click.echo('\n>>' + words)
    else:
        click.echo('\n >> Invalid word')

# Api to get the Antonyms for the user enetered word.

def get_ant(word):
    found = False
    url_format = 'https://fourtytwowords.herokuapp.com/word/{}/relatedWords'
    response = requests.get(url_format.format(word), params=query_params)
    if response:
        for elem in response.json():
            if elem['relationshipType'] == 'antonym':
                found = True
                for words in elem['words']:
                    click.echo('\n>>' + words)
    else:
        click.echo('\n >> Invalid word')
    if not found:
        click.echo('\n >> No antonym for the word is found in dictionary')

    # click.echo(response.json())

#  Api to get the Examples for the user enetered word.

def get_examples(word):
    url_format = 'https://fourtytwowords.herokuapp.com/word/{}/examples'
    response = requests.get(url_format.format(word), params=query_params)
    ex_array = response.json()['examples']
    for exampl in ex_array:
        click.echo('\n>>'+exampl['text'])


# Api for complete dictionary for the user entered word.

def get_full_dict(word):
    get_defn(word)
    get_syn(word)
    get_ant(word)
    get_examples(word)


# Api to get a random word from the dictionary.
def get_random_word():
    url_format = 'https://fourtytwowords.herokuapp.com/words/randomWord'
    response = requests.get(url_format, params=query_params)
    rand_word = response.json()['word']
    get_full_dict(rand_word)
    click.echo(rand_word)


##
##
##

def play():
    word = None
    synWord = []
    antWord = []
    defWord = []

    cat = random.choice(category)
    click.echo("The category is : "+ cat)
    # To get a random word
    url_format = 'https://fourtytwowords.herokuapp.com/words/randomWord'
    rand_response = requests.get(url_format, params=query_params)
    word = rand_response.json()['word']
    click.echo(word)

    # for getting definitions
    url_format = 'https://fourtytwowords.herokuapp.com/word/{}/definitions'

    def_response = requests.get(url_format.format(word), params=query_params)
    defWord = def_response.json()
    click.echo(defWord)

    ##### syn
    url_format = 'https://fourtytwowords.herokuapp.com/word/{}/relatedWords'

    syn_response = requests.get(url_format.format(word), params=query_params)
    for elem in syn_response.json():
        if elem['relationshipType'] == 'synonym':
            synWord = elem['words']
        if elem['relationshipType'] == 'antonym':
            antWord = elem['words']

    # If the category is antonym and if there is no antonym for that word, we generate a new word.
    if cat == 'anton' and antWord == []:
        play()
    # calling gameLogic function
    gameLogic(word, synWord, antWord, defWord, cat, None);


def gameLogic(newWord, newSynWord, newAntWord, newDefWord, cat, oldMessageChoice):
    word = newWord;
    synWord = newSynWord;
    antWord = newAntWord;
    defWord = newDefWord;
    newCat = cat;
    messageChoice = oldMessageChoice;

    if newCat == 'syn':
        messageChoice = '\nPlease guess the correct word for the below synonym\n\n '.join(synWord[0])

    if newCat == 'ant' and antWord != []:
        messageChoice = '\nPlease guess the correct word for the below antonym\n\n '.join(antWord[0])

    if newCat == 'defn':
        messageChoice = '\nPlease guess the correct word for the below definition\n\n '.join(defWord[0])

    guess_answer = prompt([{
        'type': 'input',
        'name': 'guess',
        'message': messageChoice,
    }])

    if guess_answer['guess'] in synWord and guess_answer['guess'] != synWord[0]:
        click.echo('\n *** You have guessed it correct. Congrats!!!  ***')
  #  else:
    # Need to implement from here.
        # question = [{
        #     'type': 'list',
        #     'name': 'wrongAnswer',
        #     'message': '\nWrong Answer::Select One option',
        #     'choices': ['Try Again', 'Hint', 'Quit']
        # }]
        # answers = prompt(question)
        # click.echo(answers)
        #
        # if answers['wrongAnswer'] == 'Try Again':
        #     gameLogic(word, synWord, antWord, defWord, newCat, messageChoice)
        #
        # if answers['wrongAnswer'] == 'Quit':
        #     click.echo('The correct word is : ' + word)
        #     click.echo('The synonyms are :\n' + synWord)
        #     if antWord:
        #         click.echo('The antonyyms are :\n' + antWord)
        #     click.echo('The definitions are :\n')
        #     for w in defWord:
        #         click.echo('>> ' + w)
