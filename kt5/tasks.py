import os
from datetime import date


class Task:
    def __init__(self, title, due, completed=False):
        title = title.strip()
        if not title or '\n' in title or '\r' in title:
            raise ValueError('Введите непустое название задачи в одну строку.')
        self.title = title
        self.due = date.fromisoformat(due)
        if self.due.isoformat() != due:
            raise ValueError('Используйте формат даты ГГГГ-ММ-ДД.')
        self.completed = completed

    def status(self, today=None):

        if today is None:
            today = date.today()
        if self.completed:
            return 'Выполнена'
        if self.due < today:
            return 'Просрочена'
        if self.due == today:
            return 'Сегодня'
        return 'Будущая'

    def to_line(self):
        return '{0}|{1}|{2}\n'.format(self.due.isoformat(), int(self.completed), self.title)


class TaskFile:
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        if not os.path.exists(self.filename):
            return []
        tasks = []
        with open(self.filename, encoding='utf-8') as source:
            for number, line in enumerate(source, 1):
                if not line.strip():
                    continue
                fields = line.rstrip('\r\n').split('|', 2)
                try:
                    if len(fields) != 3 or fields[1] not in ('0', '1'):
                        raise ValueError('Ожидается дата|0 или 1|название')
                    tasks.append(Task(fields[2], fields[0], fields[1] == '1'))
                except ValueError as error:
                    raise ValueError('Строка {0}: {1}'.format(number, error)) from error
        return tasks

    def save(self, tasks):

        temporary = self.filename + '.tmp'
        try:
            with open(temporary, 'w', encoding='utf-8') as target:
                for task in tasks:
                    target.write(task.to_line())
            os.replace(temporary, self.filename)
        finally:
            if os.path.exists(temporary):
                os.remove(temporary)
