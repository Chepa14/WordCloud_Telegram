import re
import os
import itertools as itt
import time

from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

users_name = set()


def get_data(url):
    with open(url, 'r', encoding='utf-8') as file:
        text = file.read()

    soup = BeautifulSoup(text, features='html.parser')
    messages = soup.find_all('div', class_=re.compile('message default'))
    messages_data = []
    last_user = ''
    for msg in messages:
        temp_soup = BeautifulSoup(str(msg), features='html.parser')

        if 'joined' in temp_soup.div['class']:
            msg_user = last_user
        else:
            msg_user = temp_soup.find('div', class_="from_name").text.strip()
            last_user = msg_user
            users_name.add(msg_user)
        try:
            msg_text = temp_soup.find('div', class_="text").text.strip()
            messages_data.append({
                'name': msg_user,
                'text': msg_text.lower()
            })
        except Exception as e:
            pass

    print(f'{len(messages_data)} messages in {os.path.split(url)[1]}')
    return messages_data


def get_data_from_path(path):
    data = []
    for filename in os.listdir(path):
        if filename.endswith('.html'):
            data = list(itt.chain(data,
                                  get_data(os.path.join(path, filename))))
        else:
            continue
    print('Общее количество сообщений - ' + str(len(data)))
    return data


def parse_data(data):
    words_by_name = {}
    for name in users_name:
        user_data = [el['text'] for el in data if el['name'] == name]
        words_by_name[name] = []
        for msg in user_data:
            words_by_name[name] = list(itt.chain(words_by_name[name], re.findall(r'\w+', msg)))
    print('Участники чата: ' + str(users_name))
    return words_by_name


def show_wordCloud(wordCloud, name):
    plt.figure(num=name)
    plt.imshow(wordCloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def create_wordCloud(words):
    for user_words in words.items():
        print('Создается облако слов...')
        wordCloud = WordCloud(width=500,
                              height=500,
                              max_words=1000,
                              min_font_size=3,
                              background_color="white").generate(' '.join(user_words[1]))
        correct_name = user_words[0].split(' ')[0]
        wordCloud.to_file(f"{int(time.time())}.png")
        # show_wordCloud(wordCloud, user_words[0])
        print('Успешно!')


def main():
    # data = get_data_from_path(r'C:\Users\Ivan\Downloads\Telegram Desktop\ChatExport_2021-01-22')
    data = get_data_from_path(r'C:\Users\Ivan\Downloads\Telegram Desktop\ChatExport_2021-03-29')
    parsed_words = parse_data(data)
    create_wordCloud(parsed_words)


if __name__ == '__main__':
    main()
