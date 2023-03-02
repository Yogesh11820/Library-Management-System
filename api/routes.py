from flask import Blueprint ,request ,jsonify
from model import Students,Books,Transactions
from datetime import datetime

studentreg = Blueprint('studentreg',__name__)


@studentreg.route('/',methods=['POST'])
def students_registration():

    Roll_No = request.json.get('Roll_No')
    Name = request.json.get('Name')
    Branch = request.json.get('Branch')
    
    if not Roll_No or not Name or not Branch:
        return jsonify({'msg' : 'All credentials required'}),400
    
    student = Students.selectBy(Roll_No=Roll_No).getOne(None)
    if student:
        return jsonify({'error': 'Already registered'}),409
    student = Students(Roll_No=Roll_No,Name=Name,Branch=Branch,Debt=0)
    
    return jsonify({'message' : 'Student information added Successfully'}),200


studentdetails = Blueprint('studentdetails',__name__)

@studentdetails.route('/',methods=['GET'])
def student_details():
     Roll_No = request.json.get('Roll_No')
     if not Roll_No:
          return jsonify({'msg' : 'All credentials required'}),400
     
     student = Students.selectBy(Roll_No=Roll_No).getOne(None)

     if student:
          student_info = {'id' : student.id,'Roll_No' : student.Roll_No , 'Name' : student.Name , 'Branch' : student.Branch , 'Debt' : student.Debt, 'Readerpoints' : student.Readerpoints}
          return jsonify(student_info),200
     return jsonify({'msg' : 'student not found'}),404
        
     

bookadd = Blueprint('bookadd',__name__)

@bookadd.route('/',methods=['POST'])
def book_add(): 

    title = request.json.get('title')
    author = request.json.get('author')
    genres = request.json.get('genres')
    isbn = request.json.get('isbn')
    pages = request.json.get('pages')
    quantity = request.json.get('quantity')

    if not title or not isbn or not author or not pages or not genres or quantity<0 :
         return jsonify({'msg' : 'All credentials required'}),400
    
    book_copy = Books.selectBy(isbn=isbn).getOne(None)

    if book_copy:
        return jsonify({'msg' : 'Book already in the stock'}),409
    
    else:
        book_copy = Books(title=title, isbn=isbn, genres=genres, author=author, pages=pages, quantity=quantity)
        return jsonify({'msg' : 'New Book added successfully'}),200
    

bookdetails = Blueprint('bookdetails',__name__)

@bookdetails.route('/',methods=['GET'])
def book_details():
     
     title = request.json.get('title')
     author = request.json.get('author')
     
     if not title or not author:
          return jsonify({'msg' : 'All credentials required'}),400
     
     book = Books.selectBy(title=title, author=author).getOne(None)
     if book:
          book_info = {'id' : book.id, 'title' : book.title, 'genres' : book.genres, 'isbn' : book.isbn, 'author' : book.author, 'pages' : book.pages, 'quantity' : book.quantity, 'Rating' : book.Ratings}
          return jsonify(book_info)
          
     return jsonify({'msg' : 'student not found'}),404
     


genrebasedbook = Blueprint('genresbasedbook',__name__)

@genrebasedbook.route('/',methods=['GET'])
def genrebased_book():
     category = request.json.get('category')
     if not category:
          return jsonify({'msg' : 'All credentials required'}),400

     booklist = Books.selectBy(genres=category)
     if booklist:
          for book in booklist:
               book_info = []
               book_info.append({"id" : book.id, "title" : book.title, "author" : book.author, "available copies" : book.quantity, "rating" : book.Ratings})
               return jsonify(book_info),200
     return jsonify({'msg' : 'Sorry, we could not find a book matching your search criteria'}),404


bookborrowed = Blueprint('bookborrowd',__name__)

@bookborrowed.route('/',methods=['GET'])
def book_borrowed():
    
    Roll_No = request.json.get('Roll_No')
    book_name = request.json.get('book_name')
    if not Roll_No or not book_name:
         return jsonify({'msg' : 'All credentials required'}),400

    student = Students.selectBy(Roll_No=Roll_No).getOne(None)
    if student:
            book_stock = Books.selectBy(title=book_name).getOne(None)
            
            if book_stock is None:
                return jsonify({'msg' : 'book does not exist'}),404
            
            elif book_stock.quantity==0:
               return jsonify({'msg' : 'book out of stock'}),503
            
            elif student.Debt>=500:
                return jsonify({'msg' : 'Sorry, We can not issued you the book because youre debt is more than 500 '}),403
            
            else :
                book_stock.quantity-=1
                book_stock.Ratings+=1
                student.Debt+=20
                student.Readerpoints+=1
                transactions = Transactions(Student_id=student.id, Book_id=book_stock.id )

                return jsonify({'msg' : 'Book issued successfully'}),200
            
    else:
        return jsonify({'msg' : "Incorrect Roll_No or You're not registered"}),401   


bookreturned = Blueprint('bookreturned',__name__)
 
@bookreturned.route('/',methods=['PUT'])
def book_returned():

    transaction_id = request.json.get('transaction_id')
    
    if not transaction_id:
         return jsonify({'msg' : 'All credentials required'}),400


    transaction_info = Transactions.selectBy(id=transaction_id).getOne(None)

    
    if transaction_info:
            if (transaction_info.status=="Borrowed"):
                book_info = Books.selectBy(id = transaction_info.Book_id).getOne(None)
                book_info.quantity+=1
                transaction_info.Returned_date = datetime.now()
                transaction_info.status =  "Returned"
                student_info = Students.selectBy(id=transaction_info.Student_id).getOne(None)
                student_info.Debt-=20 
                return jsonify({'msg' : 'Book return successfully'}),200

            return jsonify({'msg' : 'Book already returned'}),409
        
    return jsonify({'msg' : 'No transaction found'}),404
    

bookupdate = Blueprint('bookupdate',__name__)

@bookupdate.route('/',methods=['PUT'])
def bookdata_update():

    title = request.json.get('title')
    New_title =  request.json.get('New_title')
    New_author = request.json.get('New_author')
            
    if  not title or not New_title or not New_author :
         return jsonify({'msg' : 'All credentials required'}),400
    book_info = Books.selectBy(title=title).getOne(None)

    if book_info:
            if(New_title!='-'  and  New_author=='-'):
                book_info.title = New_title
                return jsonify({'msg' : 'Book title updated successfully'}),200
            elif(New_title=='-' and New_author!='-'):
                book_info.author = New_author
                return jsonify({'msg' : 'Book author updated successfully'}),200
            
    else:
        return jsonify({'msg' : 'Book not found'}),404


studentupdate = Blueprint('studentupdate',__name__)

@studentupdate.route('/',methods=['PUT'])
def studentdata_update():

    Roll_No = request.json.get('Roll_No')
    New_Name =  request.json.get('New_Name')
    New_Roll_No = request.json.get('New_Roll_No')
    New_Branch = request.json.get('New_Branch')
    if not Roll_No or not New_Name or not New_Roll_No or not New_Roll_No:
         return jsonify({'msg' : 'All credentials required'}),400
    student_info = Students.selectBy(Roll_No=Roll_No).getOne(None)

    if student_info:
            if(New_Roll_No=='-' and New_Branch=='-' and New_Name!='-'):
                student_info.Name = New_Name
                return jsonify({'msg' : 'Student name updated successfully'}),200
            elif(New_Roll_No=='-' and New_Branch!='' and New_Branch!='-' and New_Name=='-'):
                student_info.Branch = New_Branch
                return jsonify({'msg' : 'Student branch updated successfully'}),200
            elif(New_Roll_No!='-' and New_Branch=='-' and New_Name=='-'):
                student_info.Roll_No = New_Roll_No
                return jsonify({'msg' : 'Student rollno updated successfully'}),200
            elif(New_Name!='-' and New_Roll_No!='-' and New_Branch=='-'):
                student_info.Name = New_Name
                student_info.Roll_No = New_Roll_No
                return jsonify({'msg' : 'Student name and rollno updated successfully'}),200
            elif(New_Name!='-' and New_Roll_No=='-' and New_Branch!='-'):
                student_info.Name = New_Name
                student_info.Branch = New_Branch
                return jsonify({'msg' : 'Student name and branch updated successfully'}),200
            elif(New_Name=='-' and New_Roll_No!='-' and New_Branch!='-'):
                student_info.Roll_No = New_Roll_No
                student_info.Branch = New_Branch
                return jsonify({'msg' : 'Student rollno and branch updated successfully'}),200
            
    else:
        return jsonify({'msg' : 'student not found'}),404
    

bookdelete = Blueprint('bookdelete',__name__)

@bookdelete.route('/',methods=['DELETE'])
def book_delete():

    book_title = request.json.get('book_title')
    book_author = request.json.get('book_author')
    if not book_title or not book_author:
         return jsonify({'msg' : 'All credentials required'}),400
    book_info = Books.selectBy(title=book_title,author=book_author).getOne(None)

    if book_info:
            if book_info.quantity < 30:
                 return jsonify({'msg' : 'Sorry, you cannot delete this book'}),403
            book_info.destroySelf()                         # delete the book
            return ({'msg' : 'book data deleted'}),200
    return jsonify({'msg' : 'Book not found'}),404



studentdelete = Blueprint('studentdelete',__name__)

@studentdelete.route('/',methods=['DELETE'])
def student_delete():
     
     Roll_No = request.json.get('Roll_No')
     if not Roll_No:
          return jsonify({'msg' : 'All credentials required'}),400
     Student_info = Students.selectBy(Roll_No=Roll_No).getOne(None)

     if Student_info:
          if Student_info.Debt > 0:
               return jsonify({'msg' : 'Because of pending debt you cannot delete this student data'}),403
          Student_info.destroySelf()
          return jsonify({'msg' : 'student data deleted'}),200
     return jsonify({'msg' : 'student not found'}),404


topreaders = Blueprint('topreaders',__name__)

@topreaders.route('/')
def top_readers():
    
     cnt = request.json.get('cnt')
     if not cnt:
          return jsonify({'msg' : 'All credentials required'}),400
     top_readers = Students.select().orderBy('-Readerpoints').limit(cnt)
     
     readerslist = []

     for reader in top_readers:
          readerslist.append({'id' : reader.id ,'Name' : reader.Name,'Totalbookreads' : reader.Readerpoints})

     return jsonify(readerslist)


highdemandbook = Blueprint('highdemandbook',__name__)

@highdemandbook.route('/')
def highdemand_book():
    
     cnt = request.json.get('cnt')
     if not cnt:
          return jsonify({'msg' : 'All credentials required'}),400
     top_books = Books.selectBy().orderBy('-Ratings').limit(cnt)

     books_list = []

     for top_book in top_books:
          books_list.append({'Title' : top_book.title, 'Genres' : top_book.genres , 'Quantity' : top_book.quantity,'Rating' : top_book.Ratings})
     return jsonify(books_list)
          

