# main.py

import functions
import json
import os

DATA_FILE = "MyData.json"


def get_coordinates_input():
    """
    Запитує у користувача координати точки з перевіркою коректності
    
    Returns:
        tuple: (x, y) координати точки
    """
    prompt = functions.TRANSLATION_STRINGS.get("input_coords_prompt")
    
    while True:
        coords_str = input(f"{prompt} ")
        try:
            parts = coords_str.replace(',', ' ').split()
            if len(parts) != 2:
                raise ValueError
            x, y = map(float, parts)
            return x, y
        except ValueError:
            print("Помилка: Введіть дві координати через пробіл або кому (напр: -3 5 або -3, 5).")


def get_data_and_save():
    """
    Режим введення даних: запитує координати та мову, зберігає у файл
    """
    print(functions.TRANSLATION_STRINGS.get("data_input_mode"))
    
    # Отримуємо координати
    x, y = get_coordinates_input()
    
    # Отримуємо мову
    lang_prompt = functions.TRANSLATION_STRINGS.get("input_lang_prompt")
    lang_code = input(f"{lang_prompt} ")
    
    # Зберігаємо дані
    data_to_save = {
        "x": x,
        "y": y,
        "lang": lang_code
    }
    
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        
        saved_msg = functions.TRANSLATION_STRINGS.get("data_saved").format(DATA_FILE)
        print(saved_msg)
    except IOError as e:
        print(f"Помилка збереження файлу: {e}")


def process_data(data):
    """
    Обробляє дані з файлу та виводить результат
    
    Args:
        data (dict): словник з координатами та мовою
    """
    # Отримуємо дані
    lang = data.get("lang", "uk")
    if not lang:
        lang = "uk"
    
    x = data.get("x")
    y = data.get("y")
    
    # Перевірка коректності даних
    if x is None or y is None:
        raise json.JSONDecodeError("Неповні дані у файлі", "", 0)
    
    # Функція для перекладу (скорочення)
    t = lambda key: functions.translate_text(key, lang)
    
    # Виводимо мову
    print(f"{t('lang_label')}: {lang}")
    
    # Визначаємо чверть
    quadrant = functions.determine_quadrant(x, y)
    
    # Формуємо вивід
    point_text = t('point_label').format(x, y)
    
    if quadrant == 0:
        # Точка на осі
        result_text = t('on_axis_label')
        print(f"{point_text} {result_text}")
    else:
        # Точка в чверті
        quadrant_name = functions.get_quadrant_name(quadrant, lang)
        quadrant_text = t('quadrant_label').format(quadrant_name)
        print(f"{point_text} {quadrant_text}")


if __name__ == "__main__":
    try:
        # Спроба прочитати дані з файлу
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            file_data = json.load(f)
        
        # Обробляємо дані
        process_data(file_data)
        
    except (FileNotFoundError, json.JSONDecodeError):
        # Файл не знайдено або дані некоректні
        get_data_and_save()