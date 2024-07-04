import pyautogui
import time
import cv2
import numpy as np
import win32gui
import win32con

def activate_window(window_title):
    try:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd != 0:
            win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)  # Показать окно, если оно было свернуто
            win32gui.SetForegroundWindow(hwnd)  # Поднять окно на передний план
            return True
        else:
            print(f"Окно с заголовком '{window_title}' не найдено")
            return False
    except Exception as e:
        print(f"Ошибка при активации окна '{window_title}': {str(e)}")
        return False

# Пример использования
window_title = "Banana"
if activate_window(window_title):
    print(f"Окно с заголовком '{window_title}' активировано")
    time.sleep(1)#waitnig activate Banana window
else:
    print(f"Окно с заголовком '{window_title}' не было найдено или не удалось активировать")

# Загрузка изображения банана
banana_image_path = 'banana.png'
banana_image = cv2.imread(banana_image_path)

# Функция для поиска банана на экране
def find_banana_on_screen():
    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

    # Используем сохраненное изображение банана для сравнения
    result = cv2.matchTemplate(screen, banana_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_loc if max_val > 0.8 else None

# Определение функции для кликов
def click_slightly_below_center(x, y, width, height):
    center_x = x + width // 2
    center_y = y + height // 2 + 50  # Подстройка для клика чуть ниже центра
    pyautogui.click(center_x, center_y)

# Функция, которая будет вызываться в каждом потоке
def click_multiple_times(count, x, y, width, height):
    for _ in range(count):
        click_slightly_below_center(x, y, width, height)

# Уменьшение задержки между кликами
pyautogui.PAUSE = 0.05  # Задержка между кликами

# Поиск банана на экране
banana_position = find_banana_on_screen()
if not banana_position:
    print("Изображение банана не найдено на экране")
    exit(1)

# Координаты верхнего левого угла и размер банана
top_left_x, top_left_y = banana_position
height, width, _ = banana_image.shape

# Количество кликов
total_clicks = 100

# Выполнение кликов
click_multiple_times(total_clicks, top_left_x, top_left_y, width, height)

print("Все клики выполнены")
