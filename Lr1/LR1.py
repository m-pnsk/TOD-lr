import mysql.connector
from mysql.connector import connect, Error
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

cnx = mysql.connector.connect(user='root', password='1234',
                              host='localhost', database='school_db')
cursor = cnx.cursor()


def create_students_table():
    create_table_query = '''
    CREATE TABLE students (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        age INT,
        email VARCHAR(255)
    )
    '''
    cursor.execute(create_table_query)
    cnx.commit()


def add_5_students():
    insert_student_query = """
    INSERT INTO students (name, age, email)
    VALUES (%s, %s, %s)
    """
    students = [
        ('Kostya Butenko', 22, 'kosty@gmail.com'),
        ('Andriy Gladkov', 24, 'andriy@gmail.com'),
        ('Bogdan Hasanov', 22, 'bogdan@gmail.com'),
        ('Nastya Shvydiuk', 21, 'nastya@gmail.com'),
        ('Roman Kucher', 23, 'roman@gmail.com')
    ]

    cursor.executemany(insert_student_query, students)
    cnx.commit()


def get_all_students():
    select_allStudents_query = '''
    SELECT * FROM students
    '''
    try:
        with connect(host="localhost", port=3306, user='root', password='1234',
                     db='school_db') as connection:
            df = pd.read_sql(select_allStudents_query, connection)
        print(df)
    except Error as e:
        print(e)


def get_student_byName(name):
    select_studentByName_query = '''
    SELECT * FROM students WHERE name = %s
    '''
    cursor.execute(select_studentByName_query, (name,))
    result = cursor.fetchall()
    for row in result:
        print(row)


def update_studentAge(student_id, new_age):
    update_studentAge_query = '''
    UPDATE students SET age = %s WHERE id = %s
    '''
    cursor.execute(update_studentAge_query, (new_age, student_id))
    cnx.commit()


def delete_student_byId(student_id):
    delete_student_query = '''
    DELETE FROM students WHERE id = %s
    '''
    cursor.execute(delete_student_query, (student_id,))
    cnx.commit()


def add_2_students_transaction():
    try:
        cnx.start_transaction()
        insert_query = '''
        INSERT INTO students (name, age, email) VALUES (%s, %s, %s)
        '''
        new_students = [
            ('Mykola Panasiuk', 21, 'mykola@gmail.com'),
            ('Viktor Ivanov', 22, 'victor@gmail.com')
        ]
        cursor.executemany(insert_query, new_students)
        cnx.commit()

    except mysql.connector.Error as error:
        print(f"Transaction failed: {error}")
        cnx.rollback()


def create_courses_table():
    create_courses_table_query = '''
    CREATE TABLE courses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        description VARCHAR(255),
        credits INT
    )
    '''
    cursor.execute(create_courses_table_query)


def add_3_courses():
    courses = [
        ('Mathematics', 'Advanced calculus', 4),
        ('Physics', 'Classical mechanics', 3),
        ('Informatics', 'Introduction to programming', 3)
    ]
    insert_courses_query = '''
    INSERT INTO courses (name, description, credits) VALUES (%s, %s, %s)
    '''
    cursor.executemany(insert_courses_query, courses)
    cnx.commit()


def create_StudentCurses_table():
    create_student_courses_table_query = '''
    CREATE TABLE student_courses (
        student_id INT,
        course_id INT,
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (course_id) REFERENCES courses(id)
    )
    '''
    cursor.execute(create_student_courses_table_query)


def fill_StudentCurses_table():
    student_courses = [
        (2, 3),
        (3, 2),
        (4, 1),
        (5, 1),
        (6, 1),
        (6, 2),
        (6, 3),
        (4, 3)
    ]
    insert_StudentCourses_query = '''
        INSERT INTO student_courses (student_id, course_id) VALUES (%s, %s)
        '''
    cursor.executemany(insert_StudentCourses_query, student_courses)
    cnx.commit()


def get_students_byCourse(course_name):
    select_students_by_course_query = '''
    SELECT s.name as studentName, c.name as courseName
    FROM students s
    JOIN student_courses sc ON s.id = sc.student_id
    JOIN courses c ON c.id = sc.course_id
    WHERE c.name = %s
    '''
    try:
        with connect(host="localhost", port=3306, user='root', password='1234',
                     db='school_db') as connection:
            df = pd.read_sql(select_students_by_course_query, connection, params=(course_name,))
        print(df)
    except Error as e:
        print(e)


def get_courses_byStudent(student_name):
    select_courses_by_student_query = '''
        SELECT c.name as courses, s.name
        FROM courses c
        JOIN student_courses sc ON c.id = sc.course_id
        JOIN students s ON s.id = sc.student_id
        WHERE s.name = %s
    '''

    try:
        with connect(host="localhost", port=3306, user='root', password='1234',
                     db='school_db') as connection:
            df = pd.read_sql(select_courses_by_student_query, connection, params=(student_name,))
        print(df)
    except Error as e:
        print(e)


def get_allStudents_with_allCourses():
    select_students_courses_query = '''
        SELECT s.name, c.name as courses
        FROM students s
        JOIN student_courses sc ON s.id = sc.student_id
        JOIN courses c ON c.id = sc.course_id
        ORDER BY s.name
    '''
    try:
        with connect(host="localhost", port=3306, user='root', password='1234',
                     db='school_db') as connection:
            df = pd.read_sql(select_students_courses_query, connection)
        print(df)
    except Error as e:
        print(e)


if __name__ == '__main__':
    create_students_table()
    add_5_students()
    get_all_students()
    print()
    get_student_byName('Roman Kucher')
    print()
    update_studentAge(3, 21)
    get_all_students()
    print()
    delete_student_byId(1)
    get_all_students()
    print()
    add_2_students_transaction()
    get_all_students()
    print()

    create_courses_table()
    add_3_courses()
    create_StudentCurses_table()
    fill_StudentCurses_table()
    print()
    get_students_byCourse('Mathematics')
    print()
    get_courses_byStudent('Mykola Panasiuk')
    print()
    get_allStudents_with_allCourses()





