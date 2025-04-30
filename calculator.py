import tkinter as tk
from tkinter import ttk
import pyttsx3  
import random

def launch_confetti():
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    
    canvas = tk.Canvas(root, width=w, height=h, bg="#FCE4EC", highlightthickness=0)
    canvas.place(x=0, y=0)
    confetti_items = []
    colors = ['#FF4081', '#FFAB40', '#FFC107', '#8BC34A', '#69F0AE', '#00E5FF', '#448AFF', '#7C4DFF']
    
    for _ in range(30):
        x = random.randint(0, w)
        y = random.randint(-50, 0)
        size = random.randint(5, 15)
        color = random.choice(colors)
        oval = canvas.create_oval(x, y, x+size, y+size, fill=color, outline=color)
        speed = random.randint(10, 20)
        confetti_items.append((oval, speed))
    
    def animate():
        for item, speed in confetti_items:
            canvas.move(item, 0, speed)
        if any(canvas.coords(item)[1] < h for item, _ in confetti_items):
            canvas.after(20, animate)
        else:
            canvas.destroy()
    
    animate()

def on_button_click(value):
    current_text = entry_var.get()
    if value == "C":
        entry_var.set("")
    elif value == "=":
        try:
            expr = entry_var.get()
            result = eval(expr)
            entry_var.set(str(result))
            engine.say(str(result))
            engine.runAndWait()
            if current_mode == "autismo":
                launch_confetti()
        except Exception as e:
            entry_var.set("Error")
            engine.say("Error")
            engine.runAndWait()
    else:
        if current_text == "Error":
            current_text = ""
        entry_var.set(current_text + str(value))
        if value in "0123456789":
            engine.say(value)
            engine.runAndWait()

def generate_challenge():
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    global current_challenge_answer
    current_challenge_answer = a + b
    challenge_label.config(text=f"¿Cuánto es {a} + {b}?")
    challenge_result_var.set("")
    challenge_entry.delete(0, tk.END)

def check_challenge_answer():
    try:
        user_answer = int(challenge_entry.get())
    except ValueError:
        challenge_result_var.set("Ingresa un número")
        return
    if user_answer == current_challenge_answer:
        challenge_result_var.set("¡Correcto!")
        engine.say("¡Correcto!")
        engine.runAndWait()
        launch_confetti()
        challenge_frame.after(2000, generate_challenge)
    else:
        challenge_result_var.set("Incorrecto, inténtalo de nuevo")
        engine.say("Incorrecto, inténtalo de nuevo")
        engine.runAndWait()

def set_mode(mode):
    global current_mode
    current_mode = mode
    if mode == "autismo":
        calculator_frame.pack(fill="both", expand=True)
        challenge_frame.pack_forget()
        root.configure(bg="#FCE4EC")
        entry.config(font=("Comic Sans MS", 24), foreground="black")
        pastel_colors = ['#FFB3BA', '#FFDFBA', '#FFFFBA', '#BAFFC9', '#BAE1FF']
        for i, button in enumerate(button_list):
            button.config(bg=pastel_colors[i % len(pastel_colors)], fg="black")
    elif mode == "visual":
        calculator_frame.pack(fill="both", expand=True)
        challenge_frame.pack_forget()
        root.configure(bg="black")
        entry.config(font=("Arial", 28), foreground="yellow", background="black")
        for button in button_list:
            button.config(bg="black", fg="yellow")
        engine.say("m")
        engine.runAndWait()
    elif mode == "desafio":
        calculator_frame.pack_forget()
        challenge_frame.pack(fill="both", expand=True)
        root.configure(bg="#E3F2FD")
        generate_challenge()
        engine.say("Modo desafío. Resuelve el problema.")
        engine.runAndWait()

engine = pyttsx3.init()

root = tk.Tk()
root.title("Calculadora para Niños")
root.geometry("400x600")
root.configure(bg="#FCE4EC")

current_mode = "autismo"

calculator_frame = tk.Frame(root, bg="#FCE4EC")
calculator_frame.pack(fill="both", expand=True)

entry_var = tk.StringVar()
entry = ttk.Entry(calculator_frame, textvariable=entry_var, font=("Comic Sans MS", 24), justify="right")
entry.pack(pady=20, padx=20, fill="x")

button_frame = tk.Frame(calculator_frame, bg="#FCE4EC")
button_frame.pack(pady=20)

buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["C", "0", "=", "+"]
]

button_list = []
pastel_colors = ['#FFB3BA', '#FFDFBA', '#FFFFBA', '#BAFFC9', '#BAE1FF']
for row in buttons:
    row_frame = tk.Frame(button_frame, bg="#FCE4EC")
    row_frame.pack()
    for i, btn in enumerate(row):
        b = tk.Button(row_frame, text=btn, font=("Comic Sans MS", 18, "bold"), width=5, height=2,
                      bg=pastel_colors[i % len(pastel_colors)], fg="black", bd=5, relief="ridge",
                      command=lambda b=btn: on_button_click(b))
        b.pack(side="left", padx=5, pady=5)
        button_list.append(b)

challenge_frame = tk.Frame(root, bg="#E3F2FD")
challenge_label = tk.Label(challenge_frame, text="Desafío", font=("Arial", 24), bg="#E3F2FD", fg="red")
challenge_label.pack(pady=20)

challenge_entry = tk.Entry(challenge_frame, font=("Arial", 24))
challenge_entry.pack(pady=10)

challenge_result_var = tk.StringVar()
challenge_result_label = tk.Label(challenge_frame, textvariable=challenge_result_var, font=("Arial", 18), bg="#E3F2FD", fg="green")
challenge_result_label.pack(pady=10)

verify_button = tk.Button(challenge_frame, text="Verificar", font=("Arial", 18, "bold"), bg="#8BC34A", fg="white", command=check_challenge_answer)
verify_button.pack(pady=10)

menubar = tk.Menu(root)
mode_menu = tk.Menu(menubar, tearoff=0)
mode_menu.add_command(label="Niños / Autismo", command=lambda: set_mode("autismo"))

mode_menu.add_command(label="Modo Desafío", command=lambda: set_mode("desafio"))
menubar.add_cascade(label="Modo Desafio", menu=mode_menu)
root.config(menu=menubar)


root.mainloop() 