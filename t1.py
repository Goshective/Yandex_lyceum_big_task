import os
import sys

import pygame
import requests

def create_response():
    response = requests.get(search_api_server, params=search_params)
    if not response:
        print("Ошибка выполнения запроса:\n")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    return response


def change_picture_size(turn):
    global delta
    try:
        d = float(delta) * turn
    except:
        print("Ошибка ввода: масштаб - не число")
        sys.exit(1)
    if d < min_delta:
        delta = f"{min_delta:.4f}"
    elif d > max_delta:
        delta = f"{max_delta:.4f}"
    else:
        delta = f"{d:.3f}"
    search_params["spn"] = ",".join([delta, delta])

    response = create_response()
    with open(map_file, "wb") as file: # write image in file to show it later
        file.write(response.content)

map_file = "map.png"
search_api_server = "http://static-maps.yandex.ru/1.x"
api_key = "40d1649f-0493-4b70-98ba-98533de7710b"

toponym_longitude, toponym_lattitude = "-107.583388", "34.896502"
max_delta, min_delta = 2, 0.00002
delta = "0.1"
base_delta = delta

search_params = {
    "apikey": api_key,
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([delta, delta]),
    "l": "sat"
}

pygame.init()

running = True
inp1 = input("Введите координаты места в формате k,k (пропуск - стандартные нстройки):\n")
inp2 = input("Введите масштаб одним числом (пропуск - стандартные нстройки):\n")
if inp1 != "":
    toponym_longitude, toponym_lattitude = inp1.split(",")
    search_params["ll"] = ",".join([toponym_longitude, toponym_lattitude])
if inp2 != "":
    delta = inp2
    search_params["l"] = "sat"
change_picture_size(1)
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                change_picture_size(1.6)
            elif event.key == pygame.K_PAGEUP:
                change_picture_size(0.625)

        if base_delta != delta:
            screen.blit(pygame.image.load(map_file), (0, 0))
            base_delta = delta
        pygame.display.flip()

pygame.quit()

os.remove(map_file)