import speech_recognition as sr
import subprocess as sub
import threading as tr
import keyboard
import datetime
import pyttsx3
import pywhatkit
import wikipedia
import os
from tkinter import *
from pygame import mixer
from PIL import Image, ImageTk

main_window = Tk()
main_window.title("Arturito")

main_window.geometry("800x450")
main_window.configure(bg='#E0EAFC')
main_window.resizable(0, 0)

commands = """
    Comandos disponibles;
    - Reproduce:[nombre de cancion]
    - Busca: [lo que quieras buscar]
    - Abre: [link de ayuda]
    - Alarma: [debes decir la hora en 
        formato de 24h]
    - Archivo: [nombre]
    - Terminar: [Para que el asistente
        deje de escuchar]
"""

label_title = Label(main_window, text="Arturito Asistente", bg='#36F0D5', fg="#000000", font=('Arial', 30, 'bold'))
label_title.pack(pady=10)

canvas_commands = Canvas(bg="#00ECFF", width=205, height=160)
canvas_commands.place(x=0, y=0)
canvas_commands.create_text(98, 80, text=commands, fill="#000000", font='Arial 10')

text_info = Text(main_window, bg="#00ECFF",fg="#000000")
text_info.place(x=0, y=160, height=640, width=205)

arturito_picture = ImageTk.PhotoImage(Image.open("arturito.jpg"))
window_picture = Label(main_window, image=arturito_picture)
window_picture.pack(pady=5)

name = "Arturito"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 145)

#Funciones para las voces del asistente


def spain_voice():
    change_voice(0)


def usa_voice():
    change_voice(2)


def change_voice(id):
    engine.setProperty('voice', voices[id].id)
    engine.setProperty('rate', 145)
    talk("Hola soy arturito")

#Funcion para cargar informacion


def charge_data(name_dict, name_file):
    try:
        with open(name_file) as f:
            for line in f:
                (key, val) = line.split(",")
                val = val.rstrip("\n")
                name_dict[key] = val
    except FileNotFoundError as e:
        pass

#Diccionarios para paginas, archivos y programas


sites = dict()
charge_data(sites, "paginas.txt")
files = dict()
charge_data(files, "archivos.txt")
programs = dict()
charge_data(programs, "programas.txt")

#Funcion para hablar


def talk(text):
    engine.say(text)
    engine.runAndWait()

#Funcion para escribir y leer


def read_and_talk():
    text = text_info.get("1.0", "end")
    talk(text)

#Funcion para texto de wikipedia


def print_text(text_wiki):
    text_info.insert(INSERT, text_wiki)

#Funcion para reconocer la voz y que guarde lo que habla el user


def listen():
    try:
        with sr.Microphone() as source:
            talk("Te escucho")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language="es")
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, '')
    except:
        pass
    return rec

#Funcion para que el asistente escriba en un block de notas


def write(f):
    talk("que quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, ya puedes ver tu anotacion")
    sub.Popen("nota.txt", shell=True)

#Funcion de para la alarma


def clock(rec):
    num = rec.replace('alarma', '')
    num = num.strip()
    talk("Alarma activada a las " + num + "horas")
    if num[0] != '0' and len(num) < 5:
        num = '0' + num
    print(num)
    while True:
        if datetime.datetime.now().strftime('%H:%M') == num:
            print("ya es hora!!")
            mixer.init()
            mixer.music.load("auronplay-alarma.mp3")
            mixer.music.play()
        else:
            continue
        if keyboard.read_key() == "s":
            mixer.music.stop()
            break

#Funciones para abrir archivos, programas, paginas


def open_files():
    global namefiles_entry, pathfiles_entry
    window_files = Toplevel()
    window_files.title("Agregar Archivos")
    window_files.configure(bg="#3CCB35")
    window_files.geometry("300x200")
    window_files.resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(window_files)} center')

    title_label = Label(window_files, text="Agrega un archivo", fg="white", bg="#4BD76F", font=("Arial", 15))
    title_label.pack(pady=3)

    name_label = Label(window_files, text="Nombre del archivo", fg="white", bg="#4BD76F", font=("Arial", 10))
    name_label.pack(pady=2)
    namefiles_entry = Entry(    window_files)
    namefiles_entry.pack(pady=1)

    path_label = Label(window_files, text="Dirección del archivo", fg="white", bg="#4BD76F", font=("Arial", 10))
    path_label.pack(pady=2)
    pathfiles_entry = Entry(window_files, width=35)
    pathfiles_entry.pack(pady=1)

    save_button = Button(window_files, text="Guardar", fg="white", bg="#4BD76F", font=("Arial",10),command=add_files)
    save_button.pack(pady=1)


def open_pages():
    global namepages_entry, pathpages_entry
    window_pages = Toplevel()
    window_pages.title("Agregar paginas web")
    window_pages.configure(bg="#3CCB35")
    window_pages.geometry("300x200")
    window_pages.resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(window_pages)} center')

    title_label = Label(window_pages, text="Agrega una pagina", fg="white", bg="#4BD76F", font=("Arial", 15))
    title_label.pack(pady=3)

    name_label = Label(window_pages, text="Nombre de la pagina", fg="white", bg="#4BD76F", font=("Arial", 10))
    name_label.pack(pady=2)
    namepages_entry = Entry(window_pages)
    namepages_entry.pack(pady=1)

    path_label = Label(window_pages, text="URL de la pagina", fg="white", bg="#4BD76F", font=("Arial", 10))
    path_label.pack(pady=2)
    pathpages_entry = Entry(window_pages, width=35)
    pathpages_entry.pack(pady=1)

    save_button = Button(window_pages, text="Guardar", fg="white", bg="#4BD76F", font=("Arial",10), command=add_pages)
    save_button.pack(pady=4)


def open_programs():
    global nameprograms_entry, pathprograms_entry
    window_programs = Toplevel()
    window_programs.title("Agregar programas")
    window_programs.configure(bg="#3CCB35")
    window_programs.geometry("300x200")
    window_programs.resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(window_programs)} center')

    title_label = Label(window_programs, text="Agrega un programa", fg="white", bg="#4BD76F", font=("Arial", 15))
    title_label.pack(pady=3)

    name_label = Label(window_programs, text="Nombre del programa", fg="white", bg="#4BD76F", font=("Arial", 10))
    name_label.pack(pady=2)
    nameprograms_entry = Entry(window_programs)
    nameprograms_entry.pack(pady=1)

    path_label = Label(window_programs, text="Dirección del programa", fg="white", bg="#4BD76F", font=("Arial", 10))
    path_label.pack(pady=2)
    pathprograms_entry = Entry(window_programs, width=35)
    pathprograms_entry.pack(pady=1)

    save_button = Button(window_programs, text="Guardar", fg="white", bg="#4BD76F", font=("Arial",10), command=add_programs)
    save_button.pack(pady=4)

#Funciones para añadir archivos, programas, paginas


def add_files():
    name_file = namefiles_entry.get().strip()
    path_file = pathfiles_entry.get().strip()

    files[name_file] = path_file
    save_data(name_file, path_file, "archivos.txt")
    namefiles_entry.delete(0, "end")
    pathfiles_entry.delete(0, "end")


def add_programs():
    name_program = nameprograms_entry.get().strip()
    path_program = pathprograms_entry.get().strip()

    programs[name_program] = path_program
    save_data(name_program, path_program, "programas.txt")
    nameprograms_entry.delete(0, "end")
    pathprograms_entry.delete(0, "end")


def add_pages():
    name_page = namepages_entry.get().strip()
    path_page = pathpages_entry.get().strip()

    sites[name_page] = path_page
    save_data(name_page, path_page, "paginas.txt")
    namepages_entry.delete(0, "end")
    pathpages_entry.delete(0, "end")

#Funcion para guardar datos de pag, archivos, programas


def save_data(key, value, file_name):
    try:
        with open(file_name, 'a') as f:
            f.write(key + "," + value + "\n")
    except FileNotFoundError:
        file = open(file_name, 'a')
        file.write(key + "," + value + "\n")


#Funciones principales


def say_my_name():
    talk("Hola, ¿como te llamas?")
    name = listen()
    name = name.strip()
    talk("Bienvenido {}".format(name))
    
    try:
        with open("name.txt", 'w') as f:
            f.write(name)
    except FileNotFoundError:
        file = open("name.txt", 'w')
        file.write(name)   


def say_hello():
        if os.path.exists("name.txt"):
            with open("name.txt") as f:
                for name in f:
                    talk(f"Hola, Bienvienido {name}")
        else:
            say_my_name()


def thread_hello():
    t = tr.Thread(target=say_hello)
    t.start()

thread_hello()


def reproduce(rec):
    video = rec.replace('reproduce', '')
    print("Reproducioendo" + video)
    talk("Reproduciendo" + video)
    pywhatkit.playonyt(video)


def busca(rec):
    search = rec.replace('busca', '')
    wikipedia.set_lang("es")
    wiki = wikipedia.summary(search, 1)
    talk(wiki)
    print_text(search + ": " + wiki)


def alarma(rec):
    t = tr.Thread(target=clock, args=(rec,))
    t.start()


def abre(rec):
    task = rec.replace('abre', '').strip()
    if task in sites:
        for task in sites:
            if task in rec:
                sub.call(f'start chrome.exe {sites[task]}', shell=True)
                talk(f'Abriendo {task}')
    elif task in programs:
        for task in programs:
            if task in rec:
                talk(f'abriendo {task}')
                sub.Popen(programs[task])
    else:
        talk("parece que aun no lo has agregado, usa los botones de agregar")


def archivo(rec):
    file = rec.replace('archivo', '').strip()
    if file in files:
        for file in files:
            if file in rec:
                sub.Popen([files[file]], shell=True)
                talk(f'Abriendo {file}')
    else:
        talk("parece que aun no has agregado el archivo, usa los botones de agregar")


def escribe(rec):
    try:
        with open('documento.txt', 'a') as f:
            write(f)
    except FileNotFoundError as e:
        file = open("documento.txt", 'w')
        write(file)


#Diccionario con palabras claves

key_words = {
    'reproduce': reproduce,
    'busca': busca,
    'alarma': alarma,
    'abre': abre,
    'archivo': archivo,
    'escribe': escribe
}

#Funcion principal


def run_Arturito():
    while True:
        rec = listen()
        if 'busca' in rec:
            key_words['busca'](rec)
        else:
            for word in key_words:
                if word in rec:
                    key_words[word](rec)
        if 'termina' in rec:
            talk("Hasta pronto")
            break

#Botones


button_voice_spain = Button(main_window, text="Voz españa", fg="white", bg="#002EFF", font=("Arial", 10),
                            command=spain_voice)
button_voice_spain.place(x=525, y=80, width=110, height=30)
button_voice_usa = Button(main_window, text="Voz Usa", fg="white", bg="#002EFF", font=("Arial", 10),
                          command=usa_voice)
button_voice_usa.place(x=645, y=80, width=110, height=30)

button_listen = Button(main_window, text="Escucha", fg="white", bg="#002EFF", font=("Arial", 15),
                       command=run_Arturito)
button_listen.pack(pady=10)

button_speak = Button(main_window, text="Hablar", fg="white", bg="#608487", font=("Arial", 10),
                      command=read_and_talk)
button_speak.place(x=525, y=120, width=110, height=30)

button_add_files = Button(main_window, text="agregar archivo", fg="white", bg="#3CCB35", font=("Arial", 10),
                          command=open_files)
button_add_files.place(x=525, y=160, width=110, height=30)
button_add_pages = Button(main_window, text="agregar pagina", fg="white", bg="#3CCB35", font=("Arial", 10),
                          command=open_pages)
button_add_pages.place(x=525, y=200, width=110, height=30)
button_add_programs = Button(main_window, text="agregar programa", fg="white", bg="#3CCB35", font=("Arial", 10),
                             command=open_programs)
button_add_programs.place(x=525, y=240, width=110, height=30)


main_window.mainloop()

if __name__ == "__main__":
    run_Arturito()
