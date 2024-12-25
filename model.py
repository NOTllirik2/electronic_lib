from sqlalchemy import (
    Column, Integer, String, Date, BigInteger, ForeignKey, CheckConstraint,
    Boolean, DECIMAL, UniqueConstraint, create_engine, insert, delete, and_, or_, select, update, func, select, Table,
    Text, Float, DateTime, Time, desc)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date

from typing import Optional, List, Tuple
from datetime import datetime, timezone

Base = declarative_base()

# Ассоциативная таблица для связи "многие ко многим" между книгами и авторами
book_author_association = Table(
    'book_author',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('author_id', Integer, ForeignKey('authors.id'), primary_key=True)
)

book_genre_association = Table(
    'book_genre',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)

user_book_association = Table(
    'user_book',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('timestamp', DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)),
)

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)  # Содержимое комментария
    created_at = Column(DateTime, default=datetime.now, nullable=False)  # Дата создания
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Связь с пользователем
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)  # Связь с книгой

    # Отношения
    user = relationship('User', back_populates='comments')
    book = relationship('Book', back_populates='comments')

    def __repr__(self):
        return f"<Comment(id='{self.id}', user_id='{self.user_id}', book_id='{self.book_id}', created_at='{self.created_at}')>"

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(225), nullable=False, unique=True)  # Название жанра

    # Связь многие ко многим с книгами
    books = relationship('Book', secondary=book_genre_association, back_populates='genres')

    def __repr__(self):
        return f"<Genre(name='{self.name}')>"


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(225), nullable=False)
    publication_date = Column(Date, nullable=True)
    isbn = Column(String(225), unique=True, nullable=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=True)
    content = Column(Text, nullable=True)

    # Связь многие ко многим с авторами
    authors = relationship('Author', secondary=book_author_association, back_populates='books')

    # Связь многие ко многим с жанрами
    genres = relationship('Genre', secondary=book_genre_association, back_populates='books')

    # Связь один ко многим с транзакциями
    transactions = relationship('Transaction', back_populates='book')

    comments = relationship('Comment', back_populates='book')

    # Связь многие ко многим с пользователями (покупатели)
    buyers = relationship(
        'User',
        secondary=user_book_association,
        back_populates='purchased_books'
    )

    def __repr__(self):
        return f"<Book(title='{self.title}', id='{self.id}')>"


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(225), nullable=False)
    biography = Column(Text, nullable=True)

    # Связь многие ко многим с книгами
    books = relationship('Book', secondary=book_author_association, back_populates='authors')

    def __repr__(self):
        return f"<Author(name='{self.name}')>"


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(225), unique=True, nullable=False)
    email = Column(String(225), unique=True, nullable=False)
    password_hash = Column(String(225), nullable=False)
    role = Column(String(225), nullable=False)  # 'reader', 'buyer', 'admin' и т.д.

    # Связь один ко многим с транзакциями
    transactions = relationship('Transaction', back_populates='user')

    # Связь многие ко многим с книгами (покупки)
    purchased_books = relationship(
        'Book',
        secondary=user_book_association,
        back_populates='buyers'
    )

    comments = relationship('Comment', back_populates='user')

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    data_time = Column('timestamp', DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    transaction_type = Column(String(225), nullable=False)
    card_num = Column(String(225), nullable=False)
    amount = Column(Float, nullable=True)

    # Связи один ко многим с пользователями и книгами
    user = relationship('User', back_populates='transactions')
    book = relationship('Book', back_populates='transactions')

    def __repr__(self):
        return f"<Transaction(user_id={self.user_id}, book_id={self.book_id}, type='{self.transaction_type}')>"


# Создание подключения к базе данных MySQL
engine = create_engine('mysql+pymysql://root:6547@localhost/my_library')

# Создание базы данных и таблиц
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

def create_session(host, username, password, database, port=3306):
    try:
        database_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
        engine = create_engine(database_url, echo=False)
        Base.metadata.create_all(engine)

        global session  # Обновляем глобальную сессию
        Session = sessionmaker(bind=engine)
        session = Session()

        return session
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        raise
def getFeidls(table_name):
    table = Base.metadata.tables.get(table_name)
    return [column.name for column in table.columns]


def getTable(name):
    table_obj = Base.metadata.tables.get(name)
    return [session.query(table_obj).all(), getFeidls(name)]


def addTable(table: str, fields: List[str], values: List[List[str]]):
    values_ = []
    for value in values:
        cleaned_list = [s.strip("'") if isinstance(s, str) else s for s in value]
        values_.append(cleaned_list)

    table_obj = Base.metadata.tables.get(table)
    if table_obj is None:
        raise ValueError(f"Таблица '{table}' не найдена.")

    data = [dict(zip(fields, row)) for row in values_]

    stmt = insert(table_obj).values(data)
    session.execute(stmt)
    session.commit()


def dellTable(table: str, fields: List[str], value: List[str]):
    value = [s.strip("'") if isinstance(s, str) else s for s in value]

    table_obj = Base.metadata.tables.get(table)
    if table_obj is None:
        raise ValueError(f"Таблица '{table}' не найдена.")

    conditions = [table_obj.c[field] == val for field, val in zip(fields, value)]

    stmt = delete(table_obj).where(and_(*conditions))
    session.execute(stmt)
    session.commit()


def updateTable(
        table: str,
        changedField: str,
        newValue: str,
        fields: List[str],
        value: List[str]
):
    value = [s.strip("'") if isinstance(s, str) else s for s in value]
    table_obj = Base.metadata.tables.get(table)
    if table_obj is None:
        raise ValueError(f"Таблица '{table}' не найдена.")

    conditions = [table_obj.c[field] == val for field, val in zip(fields, value)]

    stmt = (
        update(table_obj)
        .where(and_(*conditions))
        .values({changedField: newValue})
    )

    compiled_stmt = stmt.compile(compile_kwargs={"literal_binds": True})

    # Выводим строковое представление запроса с привязанными значениями
    print(str(compiled_stmt))  # Запрос с привязанными значениями
    session.execute(stmt)
    session.commit()


def test():
    book = session.query(Book).filter_by(id=8).first()
    book2 = session.query(Book).filter_by(id=9).first()

    author = session.query(Author).filter_by(id=7).first()
    genre = session.query(Genre).filter_by(id=2).first()

    if book and author:
        # Добавляем автора к книге (связь многие ко многим)
        book.authors.append(author)
        book2.genres.append(genre)

        # Сохраняем изменения в базе данных
        session.commit()


def addBooksAndAuthors():
    # Создаем авторов
    author1 = Author(name='J.K. Rowling', biography='Автор знаменитой серии книг о Гарри Поттере.')
    author2 = Author(name='J.R.R. Tolkien', biography='Автор "Властелина колец" и "Хоббита".')
    author3 = Author(name='George Orwell', biography='Автор книг "1984" и "Животноводческая ферма".')
    author4 = Author(name='Harper Lee', biography='Автор романа "Убить пересмешника".')
    author5 = Author(name='Mark Twain', biography='Автор книг о Томе Сойере и Гекльберри Финне.')

    # Создаем жанры
    genre_fantasy = Genre(name='Fantasy')
    genre_dystopian = Genre(name='Dystopian')
    genre_fiction = Genre(name='Fiction')
    genre_adventure = Genre(name='Adventure')

    # Создаем книги
    book1 = Book(
        title='Harry Potter and the Sorcerer\'s Stone',
        publication_date=date(1997, 6, 26),
        isbn='9780747532699',
        description='Первая книга из серии о Гарри Поттере.',
        price=20.99
    )
    book2 = Book(
        title='The Hobbit',
        publication_date=date(1937, 9, 21),
        isbn='9780345339683',
        description='Книга о приключениях Бильбо Бэггинса.',
        price=15.99
    )
    book3 = Book(
        title='1984',
        publication_date=date(1949, 6, 8),
        isbn='9780451524935',
        description='Роман-антиутопия о тоталитарном обществе.',
        price=12.99
    )
    book4 = Book(
        title='To Kill a Mockingbird',
        publication_date=date(1960, 7, 11),
        isbn='9780061120084',
        description='Роман о расовых предрассудках в США.',
        price=10.99
    )
    book5 = Book(
        title='The Adventures of Tom Sawyer',
        publication_date=date(1876, 1, 1),
        isbn='9780486290686',
        description='Книга о приключениях Тома Сойера.',
        price=8.99
    )

    # Связываем авторов с книгами
    book1.authors.append(author1)
    book2.authors.append(author2)
    book3.authors.append(author3)
    book4.authors.append(author4)
    book5.authors.append(author5)

    # Связываем жанры с книгами
    book1.genres.append(genre_fantasy)
    book2.genres.append(genre_fantasy)
    book3.genres.append(genre_dystopian)
    book4.genres.append(genre_fiction)
    book5.genres.append(genre_adventure)

    # Добавляем данные в сессию
    session.add_all([author1, author2, author3, author4, author5])
    session.add_all([genre_fantasy, genre_dystopian, genre_fiction, genre_adventure])
    session.add_all([book1, book2, book3, book4, book5])

    # Сохраняем изменения
    session.commit()

def addContent():
    for id in range(8, 13):
        book = session.query(Book).filter(Book.id == id).first()
        if id != 8:
            book.content = ("Очень интересная книга о " + book.title + "\n") * 100
        else:
            with open('Гарри.txt', 'r', encoding='utf-8') as file:
                text = file.read()
                book.content = text

        session.commit()
