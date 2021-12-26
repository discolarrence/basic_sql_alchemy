from models import (Base, session, Book, engine)
import datetime
import csv
import time


def menu():
    while True:
        print('''
        \nPROGRAMMING BOOKS
        \r1 add book
        \r2 view all books
        \r3 search for book
        \r4 book analysis
        \r5 exit''')

        choice = input('What would you like to do?')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            input('''
                \rPress enter to try again.''')


def clean_date(date_str):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] 
    split_date = date_str.split(' ')
    try:
        month = int(months.index(split_date[0]) + 1)
        day = int(split_date[1].split(',')[0])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
        \n***DATE ERROR***
        \rpress enter to try again''')
        return
    else:
        return return_date


def clean_price(price_str):
    try:
        price_float = float(price_str)
    except ValueError:
        input('''
        \n***PRICE ERROR***
        \rpress enter to try again''')
        return
    else:
        return int(price_float * 100)
    

def clean_id(id_str, options):
    try:
        book_id = int(id_str)
    except ValueError:
        input('''
        \n***ID ERROR***
        \rpress enter to try again''')
        return
    else:
        if book_id in options:
            return book_id
        else:
            input(f'''
            \n***ID ERROR***
            \roptions: {options}
            \rpress enter to try again''')
            return


def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()
            if book_in_db == None:
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author, published_date=date, price=price)
                session.add(new_book)
        session.commit()



def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            title = input('Title: ')
            author = input('Author: ')
            date_error = True
            while date_error:
                date = input('Published Date (Ex: October 24, 2017)')
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False
            price_error = True
            while price_error:        
                price = input('Price (Ex: 6.01)')
                price = clean_price(price)
                if type(price) == int:
                        price_error = False
            new_book = Book(title=title, author=author, published_date=date, price=price)
            session.add(new_book)
            session.commit() 
            print('Book added!')
            time.sleep(1.5)
        elif choice == '2':
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author} | {book.published_date} | {book.price}')
        elif choice == '3':
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id)
            id_error = True
            while id_error:
                id_choice = input(f'''
                    \nId Options: {id_options}
                    \rBook id: ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_book = session.query(Book).filter(Book.id==id_choice).first()
            print(f'''
            \n{the_book.title} by {the_book.author}
            \rPublished: {the_book.published_date}
            \rPrice: ${the_book.price /100}''')
            input('\nENTER to return to main menu')
        elif choice == '4':
            pass
        else:
            print('bye')
            app_running = False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app()