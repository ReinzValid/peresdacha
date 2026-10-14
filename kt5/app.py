import os
import tkinter as tk
from tkinter import messagebox
from datetime import date
from tasks import Task, TaskFile

COLORS = {
    'Просрочена': '#a51d2d',
    'Сегодня': '#995300',
    'Будущая': '#125fa5',
    'Выполнена': '#38733c',
}


class TodoApp:
    def __init__(self, root, storage):
        self.root = root
        self.storage = storage
        self.tasks = []
        self.edit_index = None
        self.writable = True
        self.root.title('Напоминалка — ToDo')
        self.root.geometry('850x520')
        self.root.minsize(700, 450)
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        self.build_window()
        self.load_tasks()
        self.refresh()
        self.root.after(60000, self.refresh_clock)

    def build_window(self):
        tk.Label(self.root, text='Мои задачи', font=('Arial', 20, 'bold')).pack(pady=(15, 5))
        self.summary = tk.Label(self.root, text='')
        self.summary.pack()
        legend = tk.Frame(self.root)
        legend.pack(pady=8)
        for status, color in COLORS.items():
            tk.Label(legend, text='● ' + status, fg=color).pack(side=tk.LEFT, padx=12)

        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20)
        self.listbox = tk.Listbox(frame, font=('Arial', 12), activestyle='none',
                                  selectbackground='#e1e9f5', selectforeground='#142535',
                                  exportselection=False)
        scrollbar = tk.Scrollbar(frame, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind('<Double-Button-1>', self.edit_task)

        editor = tk.Frame(self.root)
        editor.pack(fill=tk.X, padx=20, pady=12)
        tk.Label(editor, text='Задача').grid(row=0, column=0, sticky='w')
        tk.Label(editor, text='Дата (ГГГГ-ММ-ДД)').grid(row=0, column=1, sticky='w', padx=8)
        self.title_entry = tk.Entry(editor, font=('Arial', 12))
        self.title_entry.grid(row=1, column=0, sticky='ew')
        self.date_entry = tk.Entry(editor, width=16, font=('Arial', 12))
        self.date_entry.grid(row=1, column=1, padx=8)
        self.date_entry.insert(0, date.today().isoformat())
        self.save_button = tk.Button(editor, text='Добавить', command=self.save_task)
        self.save_button.grid(row=1, column=2)
        tk.Button(editor, text='Отменить правку', command=self.reset_editor).grid(row=1, column=3, padx=8)
        editor.columnconfigure(0, weight=1)
        self.title_entry.bind('<Return>', self.save_task)
        self.date_entry.bind('<Return>', self.save_task)

        actions = tk.Frame(self.root)
        actions.pack(pady=(0, 10))
        tk.Button(actions, text='Изменить', command=self.edit_task).pack(side=tk.LEFT, padx=5)
        tk.Button(actions, text='Выполнено / вернуть', command=self.toggle_task).pack(side=tk.LEFT, padx=5)
        tk.Button(actions, text='Удалить', command=self.delete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(actions, text='Выход', command=self.close).pack(side=tk.LEFT, padx=5)
        self.feedback = tk.Label(self.root, text='Изменения сохраняются автоматически.')
        self.feedback.pack(pady=(0, 10))

    def load_tasks(self):
        try:
            self.tasks = self.storage.load()
        except (OSError, UnicodeError, ValueError) as error:

            self.writable = False
            messagebox.showerror('Не удалось прочитать задачи', str(error), parent=self.root)
            self.feedback.configure(text='Исправьте файл задач и перезапустите программу.', fg=COLORS['Просрочена'])

    def refresh(self):
        today = date.today()
        selected = self.listbox.curselection()
        self.listbox.delete(0, tk.END)
        active = 0
        for index, task in enumerate(self.tasks):
            status = task.status(today)
            marker = '✓' if task.completed else '○'
            self.listbox.insert(tk.END, '{0}  {1}  |  {2}  |  {3}'.format(
                marker, task.due.isoformat(), status, task.title))
            self.listbox.itemconfig(index, fg=COLORS[status])
            if not task.completed:
                active += 1
        if selected and selected[0] < len(self.tasks):
            self.listbox.selection_set(selected[0])
        self.summary.configure(text='Сегодня: {0}    Всего задач: {1}    Активных: {2}'.format(
            today.isoformat(), len(self.tasks), active))

    def refresh_clock(self):
        self.refresh()
        self.root.after(60000, self.refresh_clock)

    def selected_index(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showinfo('Выберите задачу', 'Сначала выберите задачу в списке.', parent=self.root)
            return None
        return selected[0]

    def commit(self, changed):
        if not self.writable:
            messagebox.showerror('Файл недоступен', 'Исправьте файл задач и перезапустите программу.', parent=self.root)
            return False
        try:
            self.storage.save(changed)
        except (OSError, UnicodeError) as error:
            messagebox.showerror('Не удалось сохранить', str(error), parent=self.root)
            return False
        self.tasks = changed
        self.feedback.configure(text='Задачи сохранены.', fg=COLORS['Выполнена'])
        self.refresh()
        return True

    def save_task(self, event=None):
        try:
            task = Task(self.title_entry.get(), self.date_entry.get().strip())
        except ValueError:
            messagebox.showerror('Проверьте ввод', 'Введите название и реальную дату в формате ГГГГ-ММ-ДД.', parent=self.root)
            return
        changed = self.tasks.copy()
        if self.edit_index is None:
            changed.append(task)
        else:
            task.completed = self.tasks[self.edit_index].completed
            changed[self.edit_index] = task
        if self.commit(changed):
            self.reset_editor()

    def reset_editor(self):
        self.edit_index = None
        self.title_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, date.today().isoformat())
        self.save_button.configure(text='Добавить')

    def edit_task(self, event=None):
        index = self.selected_index()
        if index is None:
            return
        task = self.tasks[index]
        self.reset_editor()
        self.edit_index = index
        self.title_entry.insert(0, task.title)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, task.due.isoformat())
        self.save_button.configure(text='Сохранить')
        self.title_entry.focus_set()

    def toggle_task(self):
        index = self.selected_index()
        if index is None:
            return
        original = self.tasks[index]
        changed = self.tasks.copy()
        changed[index] = Task(original.title, original.due.isoformat(), not original.completed)
        if self.commit(changed):
            self.reset_editor()

    def delete_task(self):
        index = self.selected_index()
        if index is None:
            return
        if messagebox.askyesno('Удалить задачу?', self.tasks[index].title, parent=self.root):
            changed = self.tasks.copy()
            del changed[index]
            if self.commit(changed):
                self.reset_editor()

    def close(self):
        if messagebox.askyesno('Выход', 'Закрыть напоминалку?', parent=self.root):
            self.root.destroy()


def main():
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tasks.txt')
    root = tk.Tk()
    TodoApp(root, TaskFile(filename))
    root.mainloop()


if __name__ == '__main__':
    main()
