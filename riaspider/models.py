import uuid

from peewee import PostgresqlDatabase, UUIDField, Model, CharField, TextField, ForeignKeyField

PEWEE_DB = PostgresqlDatabase(None)


class Student(Model):
    id = UUIDField(primary_key=True)
    name = CharField(max_length=64)
    surname = CharField(max_length=64)
    group_name = CharField(max_length=16)

    class Meta:
        database = PEWEE_DB
        db_table = 'students'


class Article(Model):
    id = UUIDField(primary_key=True)
    title = CharField()
    text = TextField()
    keywords = CharField()

    student = ForeignKeyField(Student, to_field='id', db_column='student_id')

    class Meta:
        database = PEWEE_DB
        db_table = 'articles'


def init_db():
    Student.create_table()
    Article.create_table()

    id = 'a3a623a44b874c55942d47b6c98e6a4c'
    me = Student(id=id, name='Антон', surname='Крылов', group_name='11-501')
    me.save(force_insert=True)

    return id
