import pymysql


class Database:
    def __init__(self, db_name, db_password, db_user, db_port, db_host):
        self.db_name = db_name
        self.db_password = db_password
        self.db_user = db_user
        self.db_port = db_port
        self.db_host = db_host

    @property
    def db(self):
        return pymysql.connect(
            database=self.db_name,
            password=self.db_password,
            user=self.db_user,
            host=self.db_host,
            port=self.db_port
        )

    def execute(self,
                sql: str,
                params: tuple = None,
                commit: bool = False,
                fetchall: bool = False,
                fetchone: bool = False
                ):
        if not params:
            params = ()

        db = self.db
        cursor = db.cursor()
        cursor.execute(sql, params)
        data = None

        if commit:
            db.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        db.close()
        return data

    def create_users_table(self):
        """
        Creates Users table if not exists, user's chat_id should be unique,
        otherwise it will not register user the second time in a database
        """
        sql = """
            CREATE TABLE IF NOT EXISTS Users(
                user_id INT PRIMARY KEY AUTO_INCREMENT,
                chat_id INT UNIQUE,
                full_name VARCHAR(255),
                user_name VARCHAR(255),
                is_subscribed INT DEFAULT 1
            )
        """
        self.execute(sql, commit=True)

    def create_open_lessons_table(self):
        """
        Create Open_lessons table if not exists
        """
        sql = """
            CREATE TABLE IF NOT EXISTS Open_lessons(
                lesson_id INT PRIMARY KEY AUTO_INCREMENT,
                lesson_name VARCHAR(255) UNIQUE,
                lesson_datetime VARCHAR(255)
            );
        """
        self.execute(sql, commit=True)

    def create_groups_table(self):
        """
        Creates Groups table if not exists, group_chat_id should be unique,
        otherwise it sends warning to an admin
        """
        sql = """
            CREATE TABLE IF NOT EXISTS Bot_groups(
                id INT PRIMARY KEY AUTO_INCREMENT,
                chat_id INT UNIQUE,
                name VARCHAR(255),
                lesson_days VARCHAR(255),
                lesson_time VARCHAR(255)
            );
        """
        self.execute(sql, commit=True)

    def create_courses_table(self):
        """
        Creates Courses table if not exists, course_name should be unique,
        otherwise it sends warning to an admin
        """
        sql = """
            CREATE TABLE IF NOT EXISTS Courses(
                course_id INT PRIMARY KEY AUTO_INCREMENT, 
                course_name VARCHAR(255) UNIQUE,
                course_desc_path VARCHAR(255),
                course_image_path VARCHAR(255)
            );
        """
        self.execute(sql, commit=True)

    def set_open_lesson(self, lesson_name: str):
        """
        Creates table for added open lesson, does not creates a table if table with this name already exists
        """
        sql = f"""
        CREATE TABLE IF NOT EXISTS {lesson_name.replace(" ", "_").capitalize()}(
            user_id INTEGER PRIMARY KEY AUTO_INCREMENT,
            chat_id INTEGER NOT NULL UNIQUE,
            full_name VARCHAR(30) NOT NULL,
            user_name VARCHAR(30),
            tel VARCHAR(30)
        )
        """
        return self.execute(sql, commit=True)

    def drop_open_lesson(self, table_name: str):
        """
        Drops open lesson table
        """
        sql = f"""
            DROP TABLE {table_name}
        """
        return self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f'{item} = %s' for item in parameters
        ])
        return sql, tuple(parameters.values())

    def register_user(self, chat_id: int, full_name: str, user_name: str):
        sql = """
        INSERT INTO Users (chat_id, full_name, user_name)
        VALUES (%s, %s, %s)
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
        sql, params = self.format_args(sql, **kwargs)
        return self.execute(sql, params, fetchone=True)

    def get_user_by_id(self, user_id: int):
        sql = """
            SELECT * FROM Users WHERE user_id = %s
        """
        return self.execute(sql, (user_id,), fetchone=True)

    def count_users(self):
        sql = """
            SELECT COUNT(*) FROM Users
        """
        return self.execute(sql, fetchone=True)

    def update_user_subscription_state(self, is_subscribed: int, chat_id: int):
        sql = """
            UPDATE Users SET is_subscribed = %s WHERE chat_id = %s
        """
        return self.execute(sql, (is_subscribed, chat_id), commit=True)

    def register_open_lesson(self, lesson_name: str, lesson_datetime: str):
        sql = f"""
            INSERT INTO Open_lessons(lesson_name, lesson_datetime)
            VALUES (%s, %s)
        """
        return self.execute(sql, (lesson_name.replace(" ", "_").capitalize(), lesson_datetime), commit=True)

    def register_course(self, course_name: str, desc_path: str, image_path: str):
        sql = f"""
            INSERT INTO Courses(course_name, course_desc_path, course_image_path)
            VALUES (%s, %s, %s)
        """
        return self.execute(sql, (course_name, desc_path, image_path), commit=True)

    def register_group(self, group_id: int, group_name: str, lesson_days: str, lesson_time: str):
        sql = """
            INSERT INTO Bot_groups(chat_id, name, lesson_days, lesson_time)
            VALUES (%s, %s, %s, %s)
        """
        return self.execute(sql, (group_id, group_name, lesson_days, lesson_time), commit=True)

    def register_student_to_open_lesson(self, table_name: str, chat_id: int, full_name: str, user_name: str, tel: str):
        sql = f"""
        INSERT INTO {table_name}(chat_id, full_name, user_name, tel)
        VALUES(%s, %s, %s, %s)
        """
        return self.execute(sql, (chat_id, full_name, user_name, tel), commit=True)

    #
    def get_groups(self):
        sql = """
            SELECT * FROM Bot_groups
        """
        return self.execute(sql, fetchall=True)

    def get_open_lessons(self):
        sql = """
            SELECT * FROM Open_lessons
        """

        return self.execute(sql, fetchall=True)

    def get_courses(self):
        sql = f"""
            SELECT * FROM Courses
        """
        return self.execute(sql, fetchall=True)

    #
    def get_users(self):
        sql = """
            SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def get_subscribed_users(self):
        sql = """
            SELECT * FROM Users WHERE is_subscribed = 1
        """
        return self.execute(sql, fetchall=True)

    def get_open_lesson_students(self, table_name: str):
        sql = f"""
            SELECT * FROM {table_name}
        """
        return self.execute(sql, fetchall=True)

    def get_course(self, course_id: int):
        sql = """
            SELECT * FROM Courses WHERE course_id = %s
        """
        return self.execute(sql, (course_id,), fetchone=True)

    def get_open_lesson(self, table_id: int):
        sql = f"""
            SELECT * FROM Open_lessons WHERE lesson_id = %s
        """
        return self.execute(sql, (table_id,), fetchone=True)

    def get_group(self, group_id: int):
        sql = """
            SELECT * FROM Bot_groups WHERE id = %s
        """
        return self.execute(sql, (group_id,), fetchone=True)

    def remove_from_courses_list(self, course_id: int):
        sql = """
            DELETE FROM Courses WHERE course_id = %s
        """
        return self.execute(sql, (course_id,), commit=True)

    def remove_from_open_lessons_list(self, table_name: str):
        sql = """
            DELETE FROM Open_lessons WHERE lesson_name = %s
        """
        return self.execute(sql, (table_name,), commit=True)

    def remove_from_groups_list(self, group_chat_id: int):
        sql = """
            DELETE FROM Bot_groups WHERE chat_id = %s
        """
        return self.execute(sql, (group_chat_id,), commit=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
