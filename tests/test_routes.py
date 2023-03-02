import pytest,requests,json
from app import app, Students, Books, Transactions


def test_students_registration():

    url = "http://127.0.0.1:5000/Students_Registration"

    # for new registration

    data = {
              "Roll_No" : 200 ,
              "Name" : "Yogesh Patil",
              "Branch" : "Electronics"
           }
    response = requests.post(url,json=data)
    assert response.status_code == 200
    assert json.loads(response.content) == {'message': 'Student information added Successfully'}

    #credentials required
    data  = {"Roll_No" : 200, "Name" : "Puneet"}

    response = requests.post(url,json=data)
    assert response.status_code == 400
    assert json.loads(response.content) == {'msg' : 'All credentials required'}

   # already registered 
   
    data = {'Roll_No' : 101, 'Name' : 'Aditya Patil', 'Branch' : 'Electronics'}

    response = requests.post(url,json=data)
    assert response.status_code == 409
    assert json.loads(response.content) == {'error': 'Already registered'}


def test_book_add():

        url = "http://127.0.0.1:5000/Book_add"

        # for new book

        data = {"title" : "Alchemist", "isbn" :  1123, "author" : "Paulo Coelho", "pages" :500, "quantity" : 30}

        response = requests.post(url,json=data)
        assert response.status_code == 200
        assert json.loads(response.content) == {'msg' : 'New Book added successfully'}

        # already added book

        data = {"title" : "Alchemist", "isbn" :  1123, "author" : "Paulo Coelho", "pages" :500, "quantity" : 30}

        response = requests.post(url,json=data)
        assert response.status_code == 409
        assert json.loads(response.content) == {'msg' : 'Book already in the stock'}

        # credentials required

        data = {"title" : "Harry Potter", "author" : "J. K. Rowling", "pages" :1500, "quantity" : 30}

        response = requests.post(url,json=data)
        assert response.status_code == 400
        assert json.loads(response.content) == {'msg' : 'All credentials required'}

def test_book_borrowed():
      
      url = 'http://127.0.0.1:5000/Book_borrowed'

      # book issued

      data = {"Roll_No" : 101, "book_name" : "The Lord of Rings"}

      response = requests.get(url,json=data)
      assert response.status_code == 200
      assert json.loads(response.content) == {'msg' : 'Book issued successfully'}

     # book not exist

      data = {"Roll_No" : 101, "book_name" : "Mahabharat"}

      response = requests.get(url,json=data)
      assert response.status_code == 404
      assert json.loads(response.content) == {'msg' : 'book does not exist'}

     # book out of stock 

      data = {"Roll_No" : 101, "book_name" : "Ramayan" }

      response = requests.get(url,json=data)

      assert response.status_code == 503
      assert json.loads(response.content) == {'msg' : 'book out of stock'}

    # add debt test
    
     # student not found 

      data = {"Roll_No" : 1078, "book_name" : "Alchemist" }

      response = requests.get(url,json=data)

      assert response.status_code == 401
      assert json.loads(response.content) == {'msg' : "Incorrect Roll_No or You're not registered"}

      #credentials required 

      data = {}
      response = requests.get(url,json=data)

      assert response.status_code == 400
      assert json.loads(response.content) == {'msg' : 'All credentials required'}

def test_book_returned():
      
      url = 'http://127.0.0.1:5000/Book_returned'

      #book returned
      
      data = {"transaction_id" : 1}
      response = requests.put(url,json=data)
      assert response.status_code == 200
      assert json.loads(response.content) == {'msg' : 'Book return successfully'}

      #transaction not found 

      data = {"transaction_id" : 55}
      response = requests.put(url,json=data)
      print(response)
      assert response.status_code == 404
      assert json.loads(response.content) == {'msg' : 'No transaction found'}
      
      # credentials required
      data = {}
      response = requests.put(url,json=data)
      assert response.status_code == 400
      assert json.loads(response.content) == {'msg' : 'All credentials required'}
      
      # book already returned
      data = {"transaction_id" : 1}
      response = requests.put(url,json=data)
      assert response.status_code == 409
      assert json.loads(response.content) == {'msg' : 'Book already returned'}


def test_update_bookdata():

      url = 'http://127.0.0.1:5000/BookData_Update'

      # update book title

      data = {'title' : 'lockey' , 'New_title' : 'Locke&Key' , 'New_author' : '-' }

      response = requests.put(url,json=data)
      assert response.status_code == 200
      assert json.loads(response.content) ==  {'msg' : 'Book title updated successfully'}


     # update book author 

      data = {'title' : 'Harry Potter' , 'New_title' : '-' , 'New_author' : 'J. K. Rowling'}
      response = requests.put(url,json=data)
      assert response.status_code == 200
      assert json.loads(response.content) ==  {'msg' : 'Book author updated successfully'}
     
      #credentials required
      data = {}
      response = requests.put(url,json=data)
      assert response.status_code == 400
      assert json.loads(response.content) ==  {'msg' : 'All credentials required'}

   
      #book not found
      data = {'title' : 'let us see' ,'New_title': 'let us C', 'New_author' : '-'}
      response = requests.put(url,json=data)
      assert response.status_code == 404
      assert json.loads(response.content) ==  {'msg' : 'Book not found'}


def test_studentdata_update():
      
      #update name
      url = 'http://127.0.0.1:5000/StudentData_Update'

      data = {"Roll_No" : 102, "New_Name" : "Avinash Atkale", "New_Roll_No" : "-", "New_Branch" : "-"}

      response = requests.put(url,json=data)
      assert response.status_code == 200
      assert json.loads(response.content) ==  {'msg' : 'Student name updated successfully'}

      #update branch
      data = {"Roll_No" : 103, "New_Name" : "-", "New_Roll_No" : "-", "New_Branch" : "CSE"}

      response = requests.put(url,json=data)
      assert response.status_code == 200
      assert json.loads(response.content) ==  {'msg' : 'Student branch updated successfully'}

      #update rollno
      data = {"Roll_No" : 113, "New_Name" : "-", "New_Roll_No" : 104, "New_Branch" : "-"}

      response = requests.put(url,json=data)
      assert response.status_code == 200
      assert json.loads(response.content) ==  {'msg' : 'Student rollno updated successfully'}


      #update name and rollno
      data = {"Roll_No" : 106, "New_Name" : "Mukesh Jain", "New_Roll_No" : 1, "New_Branch" : "-"}

      response = requests.put(url,json=data)
      assert response.status_code == 200
      assert json.loads(response.content) ==  {'msg' : 'Student name and rollno updated successfully'}


      #update name and branch
      data = {"Roll_No" : 145, "New_Name" : "Sumit Thakur", "New_Roll_No" : "-", "New_Branch" : "Electrical"}

      response = requests.put(url,json=data)
      assert response.status_code == 200
      assert json.loads(response.content) ==  {'msg' : 'Student name and branch updated successfully'}


      #update rollno and branch
      data = {"Roll_No" : 115, "New_Name" : "-", "New_Roll_No" : 2, "New_Branch" : "Civil"}

      response = requests.put(url,json=data)
      assert response.status_code == 200
      assert json.loads(response.content) ==  {'msg' : 'Student rollno and branch updated successfully'}

      #credentials required      
      
      data = {}
      response = requests.put(url,json=data)
      assert response.status_code == 400
      assert json.loads(response.content) == {'msg' : 'All credentials required'}


      #student not found
      data = {"Roll_No" : 1089, "New_Name" : "-", "New_Roll_No" : 124, "New_Branch" : "Civil"}

      response = requests.put(url,json=data)
      assert response.status_code == 404
      assert json.loads(response.content) ==  {'msg' : 'student not found'}


def test_bookdelete():

      url = 'http://127.0.0.1:5000/Book_Delete'
      

      #book deleted
      data = {'book_id' : 5}
      response = requests.delete(url,json=data)
      assert response.status_code == 200
      assert json.loads(response.content) ==  {'msg' : 'book data deleted'}


      #book not found
      data = {'book_id' : 51}
      response = requests.delete(url,json=data)
      assert response.status_code == 404
      assert json.loads(response.content) ==  {'msg' : 'Book not found'} 

      #credentials required
      data = {}
      response = requests.delete(url,json=data)
      assert response.status_code == 400
      assert json.loads(response.content) == {'msg' : 'All credentials required'}

      #cannot delete book
      data = {'book_id' : 10}
      response = requests.delete(url,json=data)
      assert response.status_code == 403
      assert json.loads(response.content) ==  {'msg' : 'Sorry, you cannot delete this book'} 



def test_studentdelete():

      url = 'http://127.0.0.1:5000/Student_Delete'
      

      #student deleted
      data = {"Roll_No" : 150}
      response = requests.delete(url,json=data)
      assert response.status_code == 200
      assert json.loads(response.content) ==  {'msg' : 'student data deleted'}


      #student not found
      data = {"Roll_No" : 78}
      response = requests.delete(url,json=data)
      assert response.status_code == 404
      assert json.loads(response.content) ==  {'msg' : 'student not found'}

      #credentials required      
      data = {}
      response = requests.delete(url,json=data)
      assert response.status_code == 400
      assert json.loads(response.content) == {'msg' : 'All credentials required'}

      #pending debt
      data = {"Roll_No" : 100}
      response = requests.delete(url,json=data)
      assert response.status_code == 403
      assert json.loads(response.content) ==  {'msg' : 'Because of pending debt you cannot delete this student data'}