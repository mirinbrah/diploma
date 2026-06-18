import tkinter as tk
from tkinter import messagebox
import sqlite3
import requests
from parser import get_latest_news
import database
from setting import *


def parse_and_save():
    listbox.delete(0, tk.END)
    news = get_latest_news()

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM news")

    for title, link in news:
        cursor.execute("INSERT OR IGNORE INTO news (title, link) VALUES (?, ?)", (title, link))
        listbox.insert(tk.END, title)

    conn.commit()
    conn.close()
    messagebox.showinfo("Успех", "Новости загружены!")
#обработка ошибок

def send_newsletter():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT telegram_id FROM users")
    users = cursor.fetchall()

    cursor.execute("SELECT title, link FROM news LIMIT 5")
    news_items = cursor.fetchall()
    conn.close()

    if not users:
        messagebox.showerror("Ошибка", "Нет подписчиков в базе!")
        return
    if not news_items:
        messagebox.showerror("Ошибка", "Нет новостей для рассылки!")
        return

    text = "🔥 Свежие IT-новости:\n\n"
    for idx, (title, link) in enumerate(news_items, 1):
        text += f"{idx}. {title}\n{link}\n\n"

    for user in users:
        user_id = user[0]
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={'chat_id': user_id, 'text': text})

    messagebox.showinfo("Успех", "Рассылка завершена!")


database.init_db()

root = tk.Tk()
root.title("Админ-панель: Агрегатор")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Arial", 10))
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=listbox.yview)

btn_parse = tk.Button(root, text="Спарсить Хабр", command=parse_and_save, width=30, bg="#add8e6")
btn_parse.pack(pady=5)

btn_send = tk.Button(root, text="Разослать в Telegram", command=send_newsletter, width=30, bg="#90ee90")
btn_send.pack(pady=10)

root.mainloop()