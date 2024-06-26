import sys
import threading
import pyglet
import time
import PIL.Image
from tkinter import *
import tkinter as tk
import pystray 


def clock():
    # Добавление иконки в трей
    image = PIL.Image.open("clock.ico")
    icon = pystray.Icon("name", image, "Будильник")

    # Отображение иконки
    icon.visible = True

    # Чистка иконки при выходе
    icon.stop()

def run_clock():
    # Запуск иконки в отдельном потоке
    thread = threading.Thread(target=clock)
    thread.daemon = True  # Установить поток как фоновый
    thread.start()

root = Tk()
root.geometry("430x450")
root.resizable(width=False, height=False)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
cn = Canvas(root, bg='white', height=30, width=30)
canvas = Canvas(root, bg='white', height=screen_height, width=screen_width)
root.title('Будильник')

sound = None  # Объявить sound как глобальную переменную

def start():
    text_houre = text_hour.get()
    text_minutese = text_minutes.get()
    timee = str(time.strftime("%H:%M:%S", time.localtime()))
    count = (int(text_hour.get()) - int(timee[:2])) * 60 + (int(text_minutes.get()) - int(timee[3:5]))
    if count > -1 and (int(text_houre) <= 23 and int(text_minutese) <= 59):
        mus = variable.get()
        l = Label(root, text=f'Установлен на {text_hour.get()}:{text_minutes.get()}',
                            bg='#FFCC00', fg='#000000', bd=2, font='Verdana', width=33, height=2)
        l.place(x=0, y=340)
        l = Label(root, text=f'Воспроизведется через {count} мин.',
                            bg='#FFCC00', fg='#000000', bd=2, font='Verdana', width=33, height=2)
        l.place(x=0, y=400)
        root.update()
        time.sleep(1)
        root.destroy()

        i = True
        while True:
            timee = str(time.strftime("%H:%M:%S", time.localtime()))
            if timee[:5] == f'{text_houre}:{text_minutese}' and i:
                i = False
                sound = pyglet.media.load(f'{mus}.mp3', streaming=True)
                sound.play()

                # Создать окно "Доброе утро!"
                window = Tk()
                window.geometry("200x100")
                window.resizable(False, False)

                # Рассчитать координаты для центрирования окна
                screen_width = window.winfo_screenwidth()
                screen_height = window.winfo_screenheight()
                window_width = window.winfo_width()
                window_height = window.winfo_height()
                x_coordinate = (screen_width / 2) - (window_width / 2)
                y_coordinate = (screen_height / 2) - (window_height / 2)

                # Установить координаты окна
                window.geometry(f"+{int(x_coordinate)}+{int(y_coordinate)}")

                # Создать метку "Доброе утро!"
                label = tk.Label(window, text="Доброе утро!", font=("Arial", 20))
                label.pack()

                # Кнопка выхода из программы
                btn_stop = Button(window, text="Выключить будильник", width=20, height=2, bg='#FFCC00',
                                 fg='#000000', font=('Verdana', 10, 'bold'), command=sys.exit)
                btn_stop.pack()

                window.mainloop()

                time.sleep(15)
                sys.exit()
            time.sleep(1)
    else:   
        l = Label(root, text='Проверьте вводимые данные!',
                            bg='#FFCC00', fg='#000000', bd=2, font='Verdana', width=33, height=2)
        l.place(x=0, y=340)

lbl = Label(root, text=f'Текущее время: {str(time.strftime("%H:%M:%S", time.localtime()))[:5]}',
                    bg='#FFCC00', fg='#000000', bd=2, font='Verdana', width=80, height=2)
lbl2 = Label(root, text='Установить будильник на:',
                    bg='#DA692F', fg='#000000', bd=2, font='Verdana', width=26, height=1)
hour = Label(root, text='Введите час',
                    bg='#DA692F', fg='#000000', bd=2, font='Verdana', width=15, height=1)
minutes = Label(root, text='Введите минуту',
                    bg='#DA692F', fg='#000000', bd=2, font='Verdana', width=15, height=1)
text_hour = Entry(root, bg='#CECECE', font='Cambria', justify='center', width=5)
text_minutes = Entry(root, bg='#CECECE', font='Cambria', justify='center', width=5)
btn = Button(text="⏰ Установить будильник ⏰", width=35, height=2, bg='#6EA6C1',
                        fg='#000000', font=('Verdana', 13, 'bold'), command=start)

miusik = Label(root, text=f'Выберете мелодию:',
                    bg='#FFCC00', fg='#000000', bd=2, font='Verdana', width=20, height=2)
variable = StringVar(root)
shr = OptionMenu(root, variable, 'Мелодия 1', 'Мелодия 2', 'Мелодия 3')

lbl.pack()
lbl2.place(x=0, y=60)
hour.place(x=45, y=100)
minutes.place(x=45, y=140)
text_hour.place(x=260, y=100)
text_minutes.place(x=260, y=140)
miusik.place(x=10, y=190)
shr.place(x=280, y=205)
btn.place(x=0, y=270)
canvas.pack()

# Запуск иконки в отдельном потоке
run_clock()

root.mainloop()