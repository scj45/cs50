from cs50 import get_string
import string

text = get_string("Insert text here: ")  # prompt for text input


def count_letters(text):
    letters = 0
    for i in range(len(text)):
        if text[i].isalpha():
            letters += 1
    return letters


def count_words(text):
    words = 1
    for i in range(len(text)):
        if text[i].isspace():
            words += 1
    return words


def count_sentences(text):
    sentences = 0
    for i in range(len(text)):
        if text[i] == '.' or text[i] == '!' or text[i] == '?':
            sentences += 1
    return sentences


letters = count_letters(text)  # count letters

words = count_words(text)  # count words

sentences = count_sentences(text)  # count sentences

L = (letters/words)*100
S = (sentences/words)*100
index = round(0.0588 * L - 0.296 * S - 15.8)  # Coleman-Liau index

if 1 <= index and index < 16:
    print("Grade " + str(index))
elif index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
