import requests
import sys
import os
import csv

# Yandex Translate API key (from env)
key = os.environ['YANDEX_TRANSLATE_KEY']
ya_tr_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
# "from"-"to", for example en-ru, or only destination language, for example ru
lang = sys.argv[1]
text = sys.argv[2]
add = '-s' # show only
if len(sys.argv) >= 4: add = sys.argv[3]

url = ya_tr_url + 'key=' + key + '&text=' + text + '&lang=' + lang

response = requests.get(url)
data = response.json()
code = (data['code'])

file_name = 'yandex-translate-dictionary.csv'
if code == 200:
    translate = data['text'][0]
    print(text + ' | ' + translate)

    if (add == '-a'):
        # csv
        founded = False
        file_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(file_path, file_name), 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                if len(row) > 0 and ((text == row[2] and translate == row[3]) or (text == row[3] and translate == row[2])):
                    print('This word/phrase was translated already')
                    founded = True
                    break
        if (not founded) and (text != translate):
            with open(os.path.join(file_path, file_name), 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                if lang == 'en-ru':
                    csv_writer.writerow(
                            ['English'] + ['Russian'] + [text] + [translate])
                if lang == 'ru-en':
                    csv_writer.writerow(
                            ['Russian'] + ['English'] + [text] + [translate])
                print('Word/phrase was added to a dictionary')
    else:
        print('If you want to add this word to local dictionary, add -a to request.')
else:
    print('Wrong request!')
