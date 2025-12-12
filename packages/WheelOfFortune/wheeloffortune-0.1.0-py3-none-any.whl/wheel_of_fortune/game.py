import sys
import os
sys.path.append(os.path.dirname(__file__))
try:
    from wheel_of_fortune.file_handler import *
    from wheel_of_fortune.decorators import *
except:
    from file_handler import *
    from decorators import *

@timer
@log_error
def game():
    print('=== Поле Чудес ===')
    print('выберите сложность:')
    print('легко  (введите 1)')
    print('средне (введите 2)')
    print('сложно (введите 3)')
    lives = int(input())
    lives = [2 * (4 - lives) + 1]
    result = 0
    words = get_random_word('/'.join(__file__.split('\\')[:-1])+ "/data/words.txt")
    while lives[0] > 0:
        word = next(words)
        if gameround(word, lives):
            result += 1
            print('\n==победа в раунде!==\n')
    print(word, ": слово не угаданно!")
    rec(result)
    return result

def gameround(word, lives):
    guesses = []
    while 1:
        if lives[0] == 0:
            return False
        if all(i in guesses for i in word):
            return True
        print(''.join(i if i in guesses else '■' for i in word), '\n Введите букву: ')
        guess(word, lives, guesses)

@log_error
def guess(word, lives, guesses):
    g = input().lower()
    if g == "!":
        raise Exception("!")
    if not g.isalpha():
        raise ValueError("Введена не буква")
    if not len(g) == 1:
        if g.lower() == word:
            print("Слово угаданно!")
            guesses.extend(i for i in g)
            return
        else:
            lives[0] = 0
            raise Exception(f"не угадали слово, догадка: {g}")
    if not g in word or g in guesses:
        lives[0] -= 1
        print('неверно\n Осталось жизней: ', lives[0])
        raise Exception(f"неудачная попытка, буква: {g}")
    else:
        guesses.append(g)
        print('верно')