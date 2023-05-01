import sqlite3


class Database:
    def __init__(self, path_to_db='main.db'):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f'{item} = ?' for item in parameters
        ])
        return sql, tuple(parameters.values())

    def register_user(self, chat_id: int, full_name: str, user_name: str):
        sql = """
        INSERT INTO Users (chat_id, full_name, user_name)
        VALUES (?,?,?)
        """
        self.execute(sql, (chat_id, full_name, user_name), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = """
        SELECT * FROM Users WHERE 
        """
        sql, parameters = self.format_args(sql, **kwargs)

        return self.execute(sql, parameters, fetchone=True)

    def get_user(self, chat_id: int):
        sql = """
        SELECT * FROM Users WHERE chat_id = ?
        """
        return self.execute(sql, (chat_id,), fetchone=True)

    def get_user_by_id(self, user_id: int):
        sql = """
        SELECT * FROM Users WHERE user_id = ?
        """
        return self.execute(sql, (user_id,), fetchone=True)

    def count_users(self):
        sql = """
        SELECT COUNT(*) FROM Users
        """
        return self.execute(sql, fetchone=True)

    def update_user_subscription_state(self, is_subscribed: int, chat_id: int):
        sql = """
        UPDATE Users SET is_subscribed = ? WHERE chat_id = ?
        """
        return self.execute(sql, (is_subscribed, chat_id), commit=True)

    def register_open_lesson(self, lesson_name: str, lesson_datetime: str):
        sql = f"""
        INSERT INTO Open_lessons(lesson_name, lesson_datetime)
        VALUES (?,?)
        """
        return self.execute(sql, (lesson_name.replace(" ", "_").capitalize(), lesson_datetime), commit=True)

    def register_course(self, course_name: str, desc_path: str, image_path: str):
        sql = f"""
        INSERT INTO Courses(course_name, course_desc_path, course_image_path)
        VALUES (?,?,?)
        """

        return self.execute(sql, (course_name, desc_path, image_path), commit=True)

    def register_group(self, group_id: int, group_name: str, lesson_days: str, lesson_time: str):
        sql = """
        INSERT INTO Groups(group_chat_id, group_name, lesson_days, lesson_time)
        VALUES (?,?,?,?)
        """
        return self.execute(sql, (group_id, group_name, lesson_days, lesson_time), commit=True)

    def register_student_to_open_lesson(self, table_name: str, chat_id: int, full_name: str, user_name: str, tel: str):
        sql = f"""
        INSERT INTO {table_name}(chat_id, full_name, user_name, tel)
        VALUES(?,?,?,?)
        """
        return self.execute(sql, (chat_id, full_name, user_name, tel), commit=True)

    def set_open_lesson(self, lesson_name: str):
        sql = f"""
        CREATE TABLE {lesson_name.replace(" ", "_").capitalize()}(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL UNIQUE,
            full_name VARCHAR(30) NOT NULL,
            user_name VARCHAR(30),
            tel VARCHAR(30)
        )
        """

        return self.execute(sql, commit=True)

    def drop_open_lesson(self, table_name: str):
        sql = f"""
        DROP TABLE {table_name}
        """

        return self.execute(sql, commit=True)

    def get_groups(self):
        sql = """
        SELECT * FROM Groups
        """
        return self.execute(sql, fetchall=True)

    def get_open_lessons(self):
        sql = """
        SELECT * FROM Open_lessons 
        """

        return self.execute(sql, fetchall=True)

    def get_courses(self):
        sql = f"""SELECT * FROM Courses"""
        return self.execute(sql, fetchall=True)

    def get_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def get_subscribed_users(self):
        sql = """
        SELECT * FROM Users WHERE is_subscribed=1
        """
        return self.execute(sql, fetchall=True)

    def get_open_lesson_students(self, table_name: str):
        sql = f"""
        SELECT * FROM {table_name}
        """
        return self.execute(sql, fetchall=True)

    def get_course(self, course_id: int):
        sql = """
        SELECT * FROM Courses WHERE course_id = ?
        """
        return self.execute(sql, (course_id,), fetchone=True)

    def get_open_lesson(self, table_id: int):
        sql = f"""
        SELECT * FROM Open_lessons WHERE lesson_id = ?
        """

        return self.execute(sql, (table_id,), fetchone=True)

    def get_group(self, group_id: int):
        sql = """
        SELECT * FROM Groups WHERE group_id = ?
        """
        return self.execute(sql, (group_id,), fetchone=True)

    def remove_from_courses_list(self, course_id: int):
        sql = """
        DELETE FROM Courses WHERE course_id = ?
        """
        return self.execute(sql, (course_id,), commit=True)

    def remove_from_open_lessons_list(self, table_name: str):
        sql = """
        DELETE FROM Open_lessons WHERE lesson_name = ?
        """
        return self.execute(sql, (table_name,), commit=True)

    def remove_from_groups_list(self, group_chat_id: int):
        sql = """
        DELETE FROM Groups WHERE group_chat_id = ?
        """
        return self.execute(sql, (group_chat_id,), commit=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
