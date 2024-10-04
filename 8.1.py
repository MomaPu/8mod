import sqlite3
from peewee import * 

db = SqliteDatabase('db2.sqlite')
#cursor = db.cursor()

# cursor.execute(''' CREATE TABLE Students(id int, name VARCHAR(32), surname VARCHAR(32), age int, city VARCHAR(20))''')
# cursor.execute(''' CREATE TABLE Courses(id int, name VARCHAR(32), time_start VARCHAR(32), time_end VARCHAR(20))''')
# cursor.execute(''' CREATE TABLE Student_courses(student_id int, course_id int)''')

#cursor.executemany('''INSERT INTO Students (id, name, surname, age, city) VALUES (?, ?, ?, ?, ?)''',
 #[
  #   (1, 'Max', 'Brooks', 24, 'Spb'),
   #  (2, 'John', 'Stones', 15, 'Spb'),
    # (3, 'Andy', 'Wings', 45, 'Manchester'),
     #(4, 'Kate', 'Brooks', 34, 'Spb')
 #])

#cursor.executemany('''INSERT INTO Courses (id, name, time_start,
 #time_end) VALUES (?, ?, ?, ?)''', [
   # (1, 'python', '21.07.21', '21.08.21'),
  #  (2, 'java', '13.07.21', '16.08.21')
#])

#cursor.executemany('''INSERT INTO Student_courses (student_id,
# course_id) VALUES(?,?)''', [
 #   (1, 1),
 #   (2, 1),
 #   (3, 1),
 #   (4, 2)
#])

#cursor.execute('SELECT * FROM Students WHERE age > 30') # старше 30

#cursor.execute(''' # изучающие питон
  #  SELECT Students.name
 #   FROM Students
 #   JOIN Student_courses ON Students.id = Student_courses.student_id
 #   WHERE Student_courses.course_id = 1
#''')

# изучающие питон и из спб
#cursor.execute('''
#   SELECT Students.*
#    FROM Students
#    JOIN Student_courses ON Students.id = Student_courses.student_id
#    JOIN Courses ON Student_courses.course_id = Courses.id
#   WHERE Students.city = 'Spb' AND Courses.name = 'python';
#''')
#print(cursor.fetchall())

class Students(Model):
    student_id = IntegerField(primary_key=True)
    name = CharField(column_name='name')
    surname = CharField(column_name='surname')
    age = IntegerField(column_name='age')
    city = CharField(column_name='city')

    class Meta:
        database = db 

class Courses(Model):
    course_id = IntegerField(primary_key=True)
    name = CharField(column_name='name')
    time_start = CharField(column_name = 'time_start')
    time_end = CharField(column_name='time_end')

    class Meta:
        database = db

class Student_courses(Model):
    student_id = ForeignKeyField(Students, backref='courses')  
    course_id = ForeignKeyField(Courses, backref='students')
    class Meta:
        database = db

print('>30')
for student in Students.select():
    if student.age > 30:
      print(student.name)

print('Изучающие python')
for student_course in Student_courses.select().where(Student_courses.course_id == 1):
    student = Students.get(Students.student_id == student_course.student_id)
    print(student.name)

print('Изучающие python и из spb')
query = (Students
         .select()
         .join(Student_courses)
         .join(Courses)
         .where((Students.city == 'Spb') & (Courses.name == 'python')))

for student in query:
  print(student.name)


db.close()