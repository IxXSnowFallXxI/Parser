import requests
import json
import time
import os
from bs4 import BeautifulSoup as bfs
import random

path = 'C:\\python\\big\\Parser\\genres'
filename = "C:\\python\\big\\Parser\\genre_list.txt"
web = '...'
genre_lists = os.listdir(path)
name = "games_link.txt"
number_of_page = "number_of_page.txt"
logger_path = "C:\\python\\big\\Parser\\logger.txt"
genres_link = "..."
time.sleep(0.5)
for i in range(3):
    print(".", end="")
    time.sleep(0.5)
print("\nЗапуск парсера")
for i in range(3):
    print(".", end="")
    time.sleep(0.5)
def get_genre_list():

    if not os.path.exists(filename):
        try:
            response = requests.get(genres_link)
            time.sleep(random.uniform(1, 3))
            
            soup = bfs(response.text, "html.parser")
            genres_container = soup.find("div", class_="genres_list gm_radius")
            genre_links = genres_container.find_all("a", class_="abba")
            
            with open(filename, "w", encoding='utf-8') as f:
                for genre in genre_links:
                    href = genre.get("href")
                    if href:  
                        f.write(f"{href}\n")
                        
            print(f"\nСохранено {len(genre_links)} ссылок на жанры")
            
        except requests.exceptions.RequestException as e:
            print(f"\nВозникла ошибка при запросе: {e}")
    else:
        print("\nФайл со ссылками на жанры игр уже существует, переходим к следующему этапу")
get_genre_list()

for i in range(3):
    print(".", end="")
    time.sleep(0.5)

def make_genre_folders():
    path = 'C:\\python\\big\\Parser\\genres'
    filename = "genre_list.txt"
    if not os.path.exists(path):
        os.mkdir(path)
        with open(filename, "r", encoding='utf-8') as f:
            for file in f:
                parts = file.split('/')
                folder_name = parts[parts.index('genres') + 1]
                full_path = os.path.join(path, folder_name)
                os.mkdir(full_path)
                txt_file_path = os.path.join(full_path, "games_link.txt")
                with open(txt_file_path, "x", encoding="utf-8") as txt_file:
                    pass
        print("\nПапки с жанрами для игр созданы. Переходим к следующему этапу")
    else:
        print("\nНайдены необходимые папки с жанрами игр. Переходим к следующему этапу")
make_genre_folders()

for i in range(3):
    print(".", end="")
    time.sleep(0.5)

def CountPages():
    filename = "genre_list.txt"
    web = 'https://vgtimes.ru'
    path = 'C:\\python\\big\\Parser\\genres'
    number_of_page = "number_of_page.txt"
    genre_lists = os.listdir(path)
    flag = True
    for genre in genre_lists:
        try:
            path_to_txt = os.path.join(path, genre, number_of_page)
            if os.path.getsize(path_to_txt) == 0:
                flag = False
                break
            else:
                continue
        except Exception as e:
            with open(path_to_txt, "w", encoding='utf-8') as f:
                f.write("1")
    if not flag:
        with open(filename, "r") as f:
            for link in f:
                full_genre_link = web + link
                parts = link.split('/')
                genre_name = parts[parts.index('genres') + 1]
                data = requests.get(full_genre_link)
                time.sleep(random.uniform(1, 3))
                soup = bfs(data.text, "html.parser")
                soup = soup.find_all('a', class_="")
                max_page = 0
                for l in soup:
                    href = l.get("href")
                    href = href.split("/")
                    page = int(href[href.index("page") + 1])
                    if page >= max_page:
                        max_page = page
                    full_path = os.path.join(path, genre_name, number_of_page)
                with open(full_path, "w", encoding='utf-8') as f:
                    f.write(str(max_page))
                print(f"\nВ жанре {genre_name} содержится {max_page} страниц с играми. Добавили их в папку.")
    else:
        print("\nСписок страниц с играми уже существует, переходим к следующему этапу.")
CountPages()
for i in range(3):
    print(".", end="")
    time.sleep(0.5)        

def LogChecker(logger_path):
    if os.path.exists(logger_path) and os.path.getsize(logger_path) > 0:
        with open(logger_path, "r") as log_file:
            log = log_file.read().split("/")
            n = str(int(log[1]))
            flag = log[0]
            print(f"\nЕсть сохраненные логи.В прошлый раз закончили на жанре {flag}, на {n} странице.")
        return int(n)+1, flag

    else:
        n = 0       
        return int(n), None
        
               
def GameLinkMaker(path, filename, web, genre_lists, name, number_of_page, logger_path): #получаем ссылки на игры разных жанров.
    n, flag = LogChecker(logger_path)
    with open(filename, "r", encoding="utf-8") as f_1:
        for link in f_1: 
            part = link.split('/')
            genre_name = part[part.index('genres') + 1]
            genre_link = "/".join(part[1:4])
            number_path = os.path.join(path, genre_name, number_of_page)
            full_file_path = os.path.join(path, genre_name, name)
            if flag:
                if genre_name == flag:
                    number_path = os.path.join(path, genre_name, number_of_page) #Путь к количеству страниц
                    full_file_path = os.path.join(path, genre_name, name)
            with open(number_path, "r") as f:
                pages = int(f.read())     
            for i in range(n, int(pages)):
                full_genre_link = f"{web}/{genre_link}/page/{str(i+1)}/#games_list"
                page_num = str(i)
                yield full_genre_link, full_file_path, genre_name, page_num

def GameListMaker(path, filename, web, genre_lists, name, number_of_page, logger_path):
    generator = GameLinkMaker(path, filename, web, genre_lists, name, number_of_page, logger_path)
    for full_genre_link, full_file_path, genre_name, page_num in generator:
        data = requests.get(full_genre_link) #Получаем сырой html код из которого будем получать списко игр
        time.sleep(random.uniform(3, 8))
        soup = bfs(data.text, "html.parser")
        soup = soup.find_all("a", class_="game_click")
        games = []
        for line in soup:
             href = line.get("href")
             if href:
                 games.append(href) #Делаем список игр одного жанра'''

        if games:
            with open(full_file_path, "a", encoding="utf-8") as f_2:
                f_2.write("\n".join(games) + "\n")
            print(f"Записаны игры в папку {genre_name}")
            with open(logger_path, "w", encoding="utf-8") as log:
                log.write(f"{genre_name}/{page_num}")
            print(f"Сделан лог файл. ({genre_name}/{page_num})")
            
GameListMaker(path, filename, web, genre_lists, name, number_of_page, logger_path)


                  
    
