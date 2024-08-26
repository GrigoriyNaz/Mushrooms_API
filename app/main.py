from fastapi import FastAPI, HTTPException
from utils import *
from models import *
import os

# Получаем путь к директории текущего скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))

# Переходим на уровень выше
parent_dir = os.path.dirname(script_dir)

# Получаем путь к JSON
path_to_mushrooms = os.path.join(parent_dir, 'mushrooms.json')
path_to_baskets = os.path.join(parent_dir, 'baskets.json')

app = FastAPI()

@app.get("/")
def home_page():
    return {"message": "Стартовая страница"}

@app.get("/mushrooms/{mushroom_id}", response_model=Mushroom)
def get_all_mushrooms_id(mushroom_id: int):
    mushrooms = json_to_dict_list(path_to_mushrooms)
    for mushroom in mushrooms:
        if mushroom["mushroom_id"] == mushroom_id:
            return mushroom

    raise HTTPException(status_code=404, detail='Не найден такой гриб.')

@app.get("/baskets/{basket_id}", response_model=Basket)
def get_all_baskets_id(basket_id: int):
    baskets = json_to_dict_list(path_to_baskets)
    mushrooms = json_to_dict_list(path_to_mushrooms)
    for basket in baskets:
        if basket["basket_id"] == basket_id:
            for i in range(len(basket["mushrooms"])):
                for mushroom in mushrooms:
                    if basket["mushrooms"][i] == mushroom["mushroom_id"]:
                        basket["mushrooms"][i] = mushroom
                        break
            return basket
    raise HTTPException(status_code=404, detail='Не найдена такая корзинка.')


@app.post("/basket/add")
def add_basket(basket: Basket_for_post) -> Basket:
    baskets = json_to_dict_list(path_to_baskets)
    basket_id = len(baskets) + 1
    new_basket = {"basket_id": basket_id, "owner":basket.owner,
                  "capacity": basket.capacity, "mushrooms": basket.mushrooms}
    baskets.append(new_basket)
    dict_list_to_json(baskets, path_to_baskets)
    return new_basket

@app.post("/mushrooms/add")
def add_mushrooms_to_basket(mushroom: Mushroom_to_add) -> Basket:
    baskets = json_to_dict_list(path_to_baskets)
    mushrooms = json_to_dict_list(path_to_mushrooms)
    basket_id = mushroom.basket_id
    flag = False
    for added_mushroom in mushrooms:
        if added_mushroom["mushroom_id"] == mushroom.mushroom_id:
            flag = True
            break
    if not flag:
        raise HTTPException(status_code=404, detail='Не найден такой гриб.')
    weight = added_mushroom["weight"]
    for b in range(len(baskets)):
        if baskets[b]["basket_id"] == basket_id:
            count = 0
            for i in baskets[b]["mushrooms"]:
                for new_mushroom in mushrooms:
                    if new_mushroom["mushroom_id"] == i:
                        count += new_mushroom["weight"]
                        break
            if weight <= baskets[b]["capacity"] - count:
                baskets[b]["mushrooms"].append(mushroom.mushroom_id)
                dict_list_to_json(baskets, path_to_baskets)
                return baskets[b]
            raise HTTPException(status_code=405, detail='Вес гриба слишком большой')
    raise HTTPException(status_code=404, detail='Не найдена такая корзинка.')

@app.delete("/delete_mushroom")
def delete_mushroom_from_basket(mushroom: Mushroom_to_add) -> Basket:
    baskets = json_to_dict_list(path_to_baskets)
    mushrooms = json_to_dict_list(path_to_mushrooms)
    for i in range(len(baskets)):
        if baskets[i]["basket_id"] == mushroom.basket_id:
            try:
                baskets[i]["mushrooms"].remove(mushroom.mushroom_id)
                dict_list_to_json(baskets, path_to_baskets)
                return baskets[i]
            except:
                raise HTTPException(status_code=404, detail='Не найден такой гриб в корзинке.')
    raise HTTPException(status_code=404, detail='Не найдена такая корзинка.')