from urllib3 import PoolManager, exceptions
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox


def logs(url, result):
    '''Оформляет результат, отправляет его на запись в текстовое окно приложения
    и (Если выбран соответсвующий вариант) сохраняет в отдельный текстовый файл'''
    string = str()
    if url_write.get():     #Оформляет выводимые ссылки
        string += url + " - "
    else:
        if len(url) <= 27:
            string += url
        else:
            string += url[0:24] + "..."
        string += " - "
    string += result + '\n'
    history_writer(string)
    if create_logs.get():
        history_file.write(string)
    root.update()


def history_writer(string):
    '''Записывает полученную строку в текстовом окне приложения'''
    st_history.configure(state="normal")
    st_history.insert(tk.END, string)
    st_history.configure(state="disabled")
    st_history.yview(tk.END)    #Для удобства листает текст вниз


def provider():
    '''Открывает проводник для выбора файла'''
    folder_name = tk.filedialog.askopenfilename(filetype=[("Текстовый файл", "*.txt")])
    ntr_path.delete(0, len(ntr_path.get()))
    ntr_path.insert(0, folder_name)


def urls_in_file():
    '''Берет из файла каждую строку целиком, запуская проверку для них и подсчитывая результат'''
    try:
        tmp_open = open(ntr_path.get(), 'r')
    except FileNotFoundError:
        tk.messagebox.showinfo("Ошибка", "Файл не найден")
        return
    tmp_mass = tmp_open.read().split('\n')
    tmp_open.close()
    success = 0
    for url in tmp_mass:
        success += get_url_status(url)
    history_writer("\nНайдено: {0}\nНе найдено: {1}\n\n".format(success, len(tmp_mass)-success))


def get_url_status(url=None):
    '''Принимает строку, делает запрос, возвращает ответ об ошибке или успехе'''
    if url is None:
        url = ntr_path.get()
    http = PoolManager()
    try:
        resp = http.request("GET", url)
    except exceptions.MaxRetryError:
        logs(url, "Превышено ожидание" + '\n')
        return 0
    except exceptions.LocationValueError:
        messagebox.showinfo("Ошибка", "Не указана ссылка")
        return 0
    if resp.status != 404 or resp.status != 400:
        logs(url, "Найдена")
        return 1
    logs(url, "Не найдена")
    return 0


'''Инициализирует окно'''
root = tk.Tk()
window = (436, 380)
root.geometry("{0}x{1}".format(window[0], window[1]))
root.resizable(width=False,
               height=False)
root.title("CTUS")
history_file = open("Результат.txt", "a")     

'''Задает параметры всем обьектам окна'''
ntr_path = tk.Entry(root, width=62)
btn_file_check = tk.Button(root,
                           text="Проверить из файла",
                           command=urls_in_file)
btn_url_check = tk.Button(root,
                          text="Проверить url",
                          command=get_url_status)
btn_find = tk.Button(root,
                     text="...",
                     command=provider)
lbl_main = tk.Label(root,
                    text="Введите адрес строки или \n выберите файл в формате '.txt'",
                    font="Arial 18")
lbl_warning = tk.Label(root,
                       text="Важно! Кжадый URL-адрес должен начинаться с новой строки")
st_history = scrolledtext.ScrolledText(root,
                                       width=49,
                                       height=8,
                                       state="disabled")
create_logs = tk.BooleanVar()
create_logs.set(0)
check_btn_create_logs = tk.Checkbutton(root,
                                       text="Сохранить результат в отдельный файл",
                                       variable=create_logs)
url_write = tk.BooleanVar()
url_write.set(0)
check_btn_url_write = tk.Checkbutton(root,
                                     text="Указывать ссылки целиком",
                                     variable=url_write)

'''Инициализирует все обьекты окна с произвольно задаными координатами'''
ntr_path.place(x=18, y=160)
btn_file_check.place(x=90, y=191)
btn_url_check.place(x=240, y=191)
btn_find.place(x=18+62*6+6, y=156)
lbl_main.place(x=30, y=20)
lbl_warning.place(x=40, y=80)
st_history.place(x=12, y=230)
check_btn_create_logs.place(x=60, y=106)
check_btn_url_write.place(x=60, y=128)

root.mainloop()
history_file.close()
quit()
