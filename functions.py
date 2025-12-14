# functions.py

from deep_translator import GoogleTranslator

# Словник всіх текстових рядків українською
TRANSLATION_STRINGS = {
    "lang_label": "Мова",
    "point_label": "Точка A({}, {})",
    "quadrant_label": "знаходиться в {} координатній чверті",
    "on_axis_label": "знаходиться на осі координат",
    "quadrant_1": "І",
    "quadrant_2": "ІІ",
    "quadrant_3": "ІІІ",
    "quadrant_4": "ІV",
    "input_coords_prompt": "Введіть координати точки A(x, y):",
    "input_lang_prompt": "Введіть мову інтерфейсу:",
    "data_saved": "Дані збережено в файл [{}]",
    "data_input_mode": "Файл не знайдено. Запуск режиму вводу даних...",
    "invalid_input": "Помилка: некоректні координати!",
}


def determine_quadrant(x, y):
    """
    Визначає координатну чверть для точки A(x, y)
    
    Args:
        x (float): координата x
        y (float): координата y
    
    Returns:
        int: номер чверті (1, 2, 3, 4) або 0 якщо точка на осі
    """
    if x > 0 and y > 0:
        return 1
    elif x < 0 and y > 0:
        return 2
    elif x < 0 and y < 0:
        return 3
    elif x > 0 and y < 0:
        return 4
    else:
        return 0  # точка на осі координат


def translate_text(text_key, lang_code):
    """
    Перекладає текст відповідно до мови інтерфейсу
    
    Args:
        text_key (str): ключ тексту для перекладу
        lang_code (str): код мови ('uk', 'en', тощо)
    
    Returns:
        str: перекладений текст
    """
    base_text = TRANSLATION_STRINGS.get(text_key, text_key)
    
    # Якщо мова українська або не вказана, повертаємо базовий текст
    if lang_code == 'uk' or lang_code is None:
        return base_text
    
    try:
        # Перекладаємо з української на вказану мову
        translated = GoogleTranslator(source='uk', target=lang_code).translate(base_text)
        return translated
    except Exception as e:
        print(f"Помилка перекладу: {e}")
        return base_text


def get_quadrant_name(quadrant, lang_code):
    """
    Повертає назву чверті відповідно до мови
    
    Args:
        quadrant (int): номер чверті (1-4) або 0 для осі
        lang_code (str): код мови
    
    Returns:
        str: назва чверті
    """
    quadrant_keys = {
        1: 'quadrant_1',
        2: 'quadrant_2',
        3: 'quadrant_3',
        4: 'quadrant_4',
    }
    
    if quadrant == 0:
        return translate_text('on_axis_label', lang_code)
    
    key = quadrant_keys.get(quadrant, 'quadrant_1')
    return translate_text(key, lang_code)