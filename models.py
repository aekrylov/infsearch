from peewee import PostgresqlDatabase, UUIDField, Model, CharField, TextField, ForeignKeyField, CompositeKey, \
    IntegerField, DoubleField

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
    url = CharField(unique=True)
    title = CharField()
    text = TextField()
    keywords = CharField()
    author = CharField(null=True)

    student = ForeignKeyField(Student, to_field='id', db_column='student_id')

    class Meta:
        database = PEWEE_DB
        db_table = 'articles'


class Stem(Model):
    type = CharField(max_length=8)  # porter or pymystem
    term = CharField(max_length=32)

    class Meta:
        database = PEWEE_DB
        db_table = 'words'


class StemArticle(Model):
    stem = ForeignKeyField(Stem, on_delete='cascade', backref='articles')
    article = ForeignKeyField(Article, on_delete='cascade', backref='stems')
    count = IntegerField()

    class Meta:
        primary_key = CompositeKey('stem', 'article')
        database = PEWEE_DB
        db_table = 'words_articles'


class StemTfidf(Model):
    stem = ForeignKeyField(Stem, on_delete='cascade', backref='articles_tfidf')
    article = ForeignKeyField(Article, on_delete='cascade', backref='stems_tfidf')
    value = DoubleField()

    class Meta:
        primary_key = CompositeKey('stem', 'article')
        database = PEWEE_DB
        db_table = 'words_articles_tfidf'


def init_db(host='localhost', port=5432, user='postgres', password='postgres', dbname='postgres'):
    PEWEE_DB.init(dbname, host=host, port=port, user=user, password=password)
    PEWEE_DB.create_tables([Student, Article, Stem, StemArticle, StemTfidf])

    id = 'a3a623a44b874c55942d47b6c98e6a4c'
    me = Student(id=id, name='Антон', surname='Крылов', group_name='11-501')
    me.save()

    return id
