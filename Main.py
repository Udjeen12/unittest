class TaskManager:  # Класс для управления списком задач

    def __init__(self, logger=None, notifier=None, storage=None):
        self.tasks = {}  # Храним задачи в виде {id: {"title": str, "completed": bool}}
        self.logger = logger
        self.notifier = notifier
        self.storage = storage

    def add_task(self, task_id, title):  # Добавление новой задачи
        if task_id in self.tasks:
            raise ValueError("Задача с таким ID уже существует")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Название задачи должно быть непустой строкой")
        self.tasks[task_id] = {"title": title, "completed": False}
        if self.logger:
            self.logger.log(f"Добавлена задача: {title}")
        if self.storage:
            self.storage.save_task(task_id, self.tasks[task_id])

    def remove_task(self, task_id):  # Удаляет задачу
        if task_id not in self.tasks:
            raise KeyError("Задача с таким ID не найдена")
        del self.tasks[task_id]
        if self.logger:
            self.logger.log(f"Удалена задача с ID: {task_id}")

    def complete_task(self, task_id):  # Отмечает задачу как выполненную
        if task_id not in self.tasks:
            raise KeyError("Задача с таким ID не найдена")
        self.tasks[task_id]["completed"] = True
        if self.logger:
            self.logger.log(f"Задача {task_id} завершена")
        if self.notifier:
            self.notifier.notify(f"Задача {task_id} выполнена!")

    def get_task(self, task_id):  # Возвращает задачу по id
        if task_id not in self.tasks:
            raise KeyError("Задача с таким ID не найдена")
        return self.tasks[task_id]

    def get_all_tasks(self):  # Возвращает список всех задач
        return self.tasks

    def search_tasks(self, keyword):  # Ищет задачу по ключевому слову
        if not isinstance(keyword, str):
            raise ValueError("Ключевое слово должно быть строкой")
        return {
            task_id: task
            for task_id, task in self.tasks.items()
            if keyword.lower() in task["title"].lower()
        }




import unittest
from unittest.mock import Mock
class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.mock_logger = Mock()
        self.mock_notifier = Mock()
        self.mock_storage = Mock()
        self.manager = TaskManager(
            logger=self.mock_logger,
            notifier=self.mock_notifier,
            storage=self.mock_storage
        )

    def test_logger_called_on_add_task(self):
        self.manager.add_task(1, "Задача с логом")
        self.mock_logger.log.assert_called_once_with("Добавлена задача: Задача с логом")

    def test_notifier_called_on_complete_task(self):
        self.manager.add_task(1, "Задача с уведомлением")
        self.manager.complete_task(1)
        self.mock_notifier.notify.assert_called_once_with("Задача 1 выполнена!")

    def test_storage_called_on_add_task(self):
        self.manager.add_task(1, "Задача для сохранения")
        self.mock_storage.save_task.assert_called_once_with(
            1, {"title": "Задача для сохранения", "completed": False}
        )

    def test_logger_called_on_remove_task(self):
        self.manager.add_task(1, "Удаляемая")
        self.manager.remove_task(1)
        self.mock_logger.log.assert_called_with("Удалена задача с ID: 1")
    def test_add_task(self):  #Тест на добавление задачи
        self.manager.add_task(1, "Сделать домашку")
        self.assertEqual(self.manager.get_task(1), {"title": "Сделать домашку", "completed": False})

    def test_add_task_duplicate_id(self):  #Тест на дублирование id
        self.manager.add_task(1, "Первая задача")
        with self.assertRaises(ValueError):
            self.manager.add_task(1, "Дублирование ID")

    def test_add_task_invalid_title(self):   #Тест на добавление задач с некорректными названиями
        with self.assertRaises(ValueError):
            self.manager.add_task(2, "")  # Пустая строка
        with self.assertRaises(ValueError):
            self.manager.add_task(3, "  ")  # Пробелы

    def test_remove_task(self):              #Тест на удаление
        self.manager.add_task(1, "Удаляемая задача")
        self.manager.remove_task(1)
        with self.assertRaises(KeyError):
            self.manager.get_task(1)

    def test_remove_task_nonexistent(self):  #Тест на удаление задачи с несуществующим id
        with self.assertRaises(KeyError):
            self.manager.remove_task(99)  # ID, которого нет

    def test_complete_task(self):            #Тест на выполнение задачи
        self.manager.add_task(1, "Завершить задачу")
        self.manager.complete_task(1)
        self.assertTrue(self.manager.get_task(1)["completed"])

    def test_complete_task_nonexistent(self):  #Тест на выполнение несуществующей задачи
        with self.assertRaises(KeyError):
            self.manager.complete_task(99)

    def test_get_task(self):                  # Тест на вывод задачи по id
        self.manager.add_task(1, "Тестовая задача")
        self.assertEqual(self.manager.get_task(1), {"title": "Тестовая задача", "completed": False})

    def test_get_task_nonexistent(self):      # Тест на вывод задачи c несуществующим id
        with self.assertRaises(KeyError):
            self.manager.get_task(42)

    def test_get_all_tasks(self):            # Тест на вывод всех задач
        self.manager.add_task(1, "Первая задача")
        self.manager.add_task(2, "Вторая задача")
        self.assertEqual(len(self.manager.get_all_tasks()), 2)

    def test_search_tasks(self):            #Тест на поиск задач по ключевому слову
        self.manager.add_task(1, "Купить молоко")
        self.manager.add_task(2, "Купить хлеб")
        self.manager.add_task(3, "Постирать одежду")
        result = self.manager.search_tasks("Купить")
        self.assertEqual(len(result), 2)
        self.assertIn(1, result)
        self.assertIn(2, result)

    def test_search_tasks_invalid_keyword(self):    #Тест на поиск задач с некорректными ключевыми словами
        with self.assertRaises(ValueError):
            self.manager.search_tasks(123)  # Передан не строковый аргумент

if __name__ == "__main__":
    unittest.main()
