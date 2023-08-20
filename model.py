from sqlobject import *
from datetime import datetime


class Students(SQLObject):
    Roll_No = IntCol(notNone=False, unique=True)
    Name = StringCol(length=30, notNone=False)
    Branch = StringCol(length=30, notNone=False)
    Debt = IntCol(notNone=False)
    Readerpoints = IntCol(notNone=False, default=0)

class Books(SQLObject):
    title = StringCol(length=30, notNone=False)
    author = StringCol(length=30, notNone=False)
    genres = StringCol(length=30, notNone=False)
    isbn = IntCol(notNone=False, unique=True)
    pages = IntCol(notNone=False)
    quantity = IntCol(notNone=False, default=0)
    Ratings = IntCol(notNone=False, default=0)

class Transactions(SQLObject):
    Student_id = IntCol(notNone=False)
    Book_id = IntCol(notNone=False)
    Borrowed_date = DateCol(default=datetime.now())
    Returned_date = DateCol(notNone=False, default=None)
    status = StringCol(length=30, notNone=False, default="Borrowed")


