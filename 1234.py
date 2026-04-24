import requests
import json
import time
import os
from bs4 import BeautifulSoup as bfs
import random
time.sleep(1)
def get_genre_list():
    filename = "genre_list.txt"

    if not os.path.exists(filename):
        try:
            response = requests.get(link)
            time.sleep(random.uniform(1, 3))
            
            soup = bfs(response.text, "html.parser")
            genres_container = soup.find("div", class_="genres_list gm_radius")
            genre_links = genres_container.find_all("a", class_="abba")
            
            with open(filename, "w", encoding='utf-8') as f:
                for genre in genre_links:
                    href = genre.get("href")
                    if href:  
                        f.write(f"{href}\n")
                        
            print(f"Сохранено {len(genre_links)} ссылок на жанры")
            
        except requests.exceptions.RequestException as e:
            print(f"Возникла ошибка при запросе: {e}")
    else:
        print("Файл со ссылками на жанры игр уже существует, переходим к следующему этапу")
    time.sleep(1)
get_genre_list()


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
        print("Папки с жанрами для игр созданы. Переходим к следующему этапу")
    else:
        print("Найдены необходимые папки с жанрами игр. Переходим к следующему этапу")
    time.sleep(1)
make_genre_folders()

def making_games_link():
    path = 'C:\\python\\big\\Parser\\genres'
    filename = "genre_list.txt"
    web = link
    genre_lists = os.listdir(path)
    with open(filename, "r", encoding="utf-8") as f_1:
        for link in f_1: #Получаем ссылки на жанры
            full_genre_link = web + link
            parts = link.split('/')
            genre_name = parts[parts.index('genres') + 1]
            data = requests.get(full_genre_link) #Получаем сырой html код из которого будем получать списко игр
            time.sleep(random.uniform(1, 3))
            soup = bfs(data.text, "html.parser")
            soup = soup.find_all("a", class_="game_click")
            games = []
            for line in soup:
                href = line.get("href")
                games.append(href) #Делаем список игр одного жанра        
            for file in genre_lists:
                full_file_path = os.path.join(path, file, "games_link.txt")
                if file == genre_name:
                    with open(full_file_path, "w", encoding="utf-8") as f_2:
                        f_2.write("\n".join(games))
                        print(f"Записаны игры в папку {file}")
making_games_link()        
    
                  
    
