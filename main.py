import requests
from bs4 import BeautifulSoup
import os
import webbrowser

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

def removeWhiteSpace(a):
    a = a.replace('듣기]', ']')
    return " ".join(a.split())

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main():
    clearConsole()
    print("⚓ KR - EN | Quick Dictionary Lookup\n")
    search = input("Enter korean word: ")
    print("Connecting with krdict.korean.go.kr ...\n")
    html = requests.get(f'https://krdict.korean.go.kr/m/eng/searchResult?nationCode=6&nation=eng&displayNum=100&mainSearchWord={search}').text
    clearConsole()
    print("KR - EN | Quick Dictionary Lookup\n")

    soup = BeautifulSoup(html, 'lxml')
    results = soup.find_all('dl')

    if not results:
        print(f"Not entries for {search} in National Institute of Korean Language's Dictionary")
        return False

    for result in results:
        i = 0
        english_descriptions = []
        english_words = []
        kr_words = []
        kr_similar = []
        kr_description = []
        hanja = []
        pronounciation = []

        # Looks for english descriptions and extracts them
        for dd in result.find_all("dd", class_="manyLang6 ml20"):
            english_descriptions.append(removeWhiteSpace(dd.text))
            dd.decompose()

        # Stores an instance of a single Korean Main Word
        kr_word = result.find('span', class_= 'word_type1_17')
        # Stores an instance of all translations of the word
        en_words_unformatted = result.find_all('dd', class_="manyLang6")
        # TRYING TO SAVE NO-CLASS NO-TRANSLATION
        no_translated = result.find_all('dd', class_="")
        # Hanja
        if result.find_all('span', class_=""):
            hanja_raw = result.find_all('span', class_="")
        # Pronounciation
        if result.find('span', class_= 'search_sub'):
            pron_raw = result.find('span', class_= 'search_sub')
            formated = removeWhiteSpace(pron_raw.text)
            pronounciation.append(formated)
        # Korean Description
        if result.find('dd', class_ = 'ml20 mt10'):
            desc_raw = result.find_all('dd', class_ = 'ml20 mt10')
        
        # Formats and appends word translations
        for word in en_words_unformatted:
            formated = removeWhiteSpace(word.text)
            english_words.append(formated)
        
        # Formats and appends Korean Main Word
        for word in kr_word:
            formated = removeWhiteSpace(word.text)
            kr_words.append(formated)

        for translation in no_translated:
            formated = removeWhiteSpace(translation.text)
            kr_similar.append(formated)
        
        for word in hanja_raw:
            formated = removeWhiteSpace(word.text)
            hanja.append(formated)
        
        for word in desc_raw:
            formated = removeWhiteSpace(word.text)
            kr_description.append(formated)

        
        print(f'{bcolors.WARNING}❱❱❱ {kr_words[i]}{bcolors.ENDC} {hanja[i]} {pronounciation[i]}')
        if kr_similar:
            print(f'{bcolors.BOLD}{kr_similar[i]}{bcolors.ENDC}\n')
        while i < len(english_words):
            print(f'{bcolors.BOLD}{english_words[i]}{bcolors.ENDC}')
            print(f'{bcolors.OKCYAN}{kr_description[i]}{bcolors.ENDC}')
            print(f'{english_descriptions[i]}\n')
            i += 1


    webbrowser.open(f'https://en.dict.naver.com/#/search?range=example&query={search}')
    print("Naver dictionary has been opened")
    input("Press enter for Anki formatted results...")
    print("-"*50)


    # ----------------------------QUICK ANKI FLASH CARD SECTION -------------------------------
    soup = BeautifulSoup(html, 'lxml')
    results = soup.find_all('dl')

    for result in results:
        en_words = []
        english_descriptions = []
        # Looks for english descriptions and extracts them
        for dd in result.find_all("dd", class_="manyLang6 ml20"):
            english_descriptions.append(removeWhiteSpace(dd.text))
            dd.decompose()

        en_words_unformatted = result.find_all('dd', class_="manyLang6")

        for word in en_words_unformatted:
            formated = removeWhiteSpace(word.text)
            en_words.append(formated)

        # Stores an instance of a single Korean Main Word
        kr_word = result.find('span', class_= 'word_type1_17').text

        # Stores an instance of all translations of the word
        en_words_unformatted = result.find_all('dd', class_="manyLang6")

        # TRYING TO SAVE NO-CLASS NO-TRANSLATION
        #no_translated = result.find_all('dd', class_="")

        # Korean Description
        if result.find('dd', class_ = 'ml20 mt10'):
            desc_raw = result.find_all('dd', class_ = 'ml20 mt10')
        
        print(removeWhiteSpace(kr_word))
        for description in desc_raw:
            print(f'{bcolors.OKCYAN}{removeWhiteSpace(description.text)}{bcolors.ENDC}')
        i = 0

        while i < len(english_descriptions):
            print(f'> {en_words[i]}')
            print(f'{english_descriptions[i]}')
            i += 1
        print(" ")

main()