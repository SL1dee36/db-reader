import customtkinter
import sqlite3


def display_data(table_frame, table_name, cursor):
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()

    text_box = customtkinter.CTkTextbox(master=table_frame, width=500, height=300)
    text_box.pack()
    text_box.delete("1.0", customtkinter.END) 

    for row in data:
        text_box.insert("end", str(row) + "\n")

    return text_box 


def save_data(table_frame, table_name, cursor, conn, text_box):
    try:
        data = text_box.get("1.0", customtkinter.END).strip()

        rows = data.split("\n")

        cursor.execute(f"DELETE FROM {table_name}")

        for row in rows:
            values = row.strip("()").split(",")

            cursor.execute(f"INSERT INTO {table_name} VALUES ({','.join(['?'] * len(values))})", values)

        conn.commit()
        display_data(table_frame, table_name, cursor) 
    except Exception as e:
        customtkinter.CTkLabel(table_frame, text=f"Ошибка: {e}").pack()

def delete_record(table_frame, table_name, cursor, conn):
    def delete_data():
        record_id = id_entry.get()

        try:
            cursor.execute(f"DELETE FROM {table_name} WHERE rowid = ?", [record_id])
            conn.commit()
            display_data(table_frame, table_name, cursor) 
            delete_window.destroy()
        except Exception as e:
            customtkinter.CTkLabel(delete_window, text=f"Ошибка: {e}").pack()

    delete_window = customtkinter.CTkToplevel()
    delete_window.title("Удалить запись")

    customtkinter.CTkLabel(delete_window, text="ID записи:").pack()
    id_entry = customtkinter.CTkEntry(delete_window)
    id_entry.pack()

    delete_button = customtkinter.CTkButton(delete_window, text="Удалить", command=delete_data)
    delete_button.pack()

def create_table_widgets(table_frame, table_name, cursor, conn):
    text_box = display_data(table_frame, table_name, cursor) 

    save_button = customtkinter.CTkButton(master=table_frame, text="Сохранить",
                                        command=lambda: save_data(table_frame, table_name, cursor, conn, text_box))
    save_button.pack()

    delete_button = customtkinter.CTkButton(master=table_frame, text="Удалить",
                                          command=lambda: delete_record(table_frame, table_name, cursor, conn))
    delete_button.pack()