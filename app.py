import customtkinter
import sqlite3
from src.editer import create_table_widgets

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("DB Reader")
        self.geometry("600x600")

        self.db_path = None
        self.conn = None
        self.cursor = None

        # Frame 1
        self.frame_1 = customtkinter.CTkFrame(master=self)
        self.frame_1.pack(expand=True, fill="both")

        self.load_button = customtkinter.CTkButton(master=self.frame_1, text="Загрузить БД", command=self.load_db)
        self.load_button.pack(pady=20)

        self.read_button = customtkinter.CTkButton(master=self.frame_1, text="Прочитать", command=self.show_frame_2, state="disabled")
        self.read_button.pack(pady=20)

        # Frame 2
        self.frame_2 = customtkinter.CTkFrame(master=self)

        self.tabview = customtkinter.CTkTabview(self.frame_2)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        self.tables = []

        self.refresh_button = customtkinter.CTkButton(master=self.frame_2, text="Обновить", command=self.refresh_data)
        self.refresh_button.pack(pady=10)

        self.back_button = customtkinter.CTkButton(master=self.frame_2, text="Вернуться на главную", command=self.show_frame_1)
        self.back_button.pack(pady=10)

    def load_db(self):
        file_path = customtkinter.filedialog.askopenfilename(defaultextension=".db")
        if file_path:
            self.db_path = file_path
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()

            self.remove_quotes_from_all_tables()

            self.read_button.configure(state="normal")

    def remove_quotes_from_all_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in self.cursor.fetchall()]

        for table in tables:
            self.remove_quotes_from_table(table)

    def remove_quotes_from_table(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        data = self.cursor.fetchall()

        self.cursor.execute(f"DELETE FROM {table_name}")

        for row in data:
            new_row = [str(value).replace('"', '').replace("'", "") for value in row]
            self.cursor.execute(f"INSERT INTO {table_name} VALUES ({','.join(['?'] * len(new_row))})", new_row)

        self.conn.commit()

    def show_frame_2(self):
        self.frame_1.pack_forget()
        self.frame_2.pack(expand=True, fill="both")

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.tables = [table[0] for table in self.cursor.fetchall()]

        for tab_name in self.tabview.get():
            self.tabview.delete(tab_name)

        for table in self.tables:
            self.tabview.add(table)
            table_frame = customtkinter.CTkFrame(master=self.tabview.tab(table))
            table_frame.pack(expand=True, fill="both")

            create_table_widgets(table_frame, table, self.cursor, self.conn)

    def show_frame_1(self):
        self.frame_2.pack_forget()
        self.frame_1.pack(expand=True, fill="both")

    def refresh_data(self):
        self.show_frame_2()

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()