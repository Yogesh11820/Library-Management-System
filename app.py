from flask import Flask, request,jsonify
from sqlobject import *
from model import *
from datetime import datetime
import os
from api.routes import studentreg,studentdetails,bookadd,genrebasedbook,bookdetails,bookborrowed,bookreturned,bookupdate,studentupdate,bookdelete,studentdelete,topreaders,highdemandbook


db_uri = f'mysql://root:root@localhost/LMSSystem'
connection = connectionForURI(db_uri)
sqlhub.processConnection = connection

Students.createTable(ifNotExists=True)
Books.createTable(ifNotExists=True)
Transactions.createTable(ifNotExists=True)
 
app = Flask(__name__)


app.register_blueprint(studentreg,url_prefix='/students_registration')
app.register_blueprint(studentdetails,url_prefix='/student_details')
app.register_blueprint(bookadd,url_prefix='/book_add')
app.register_blueprint(genrebasedbook,url_prefix='/genrebased_book')
app.register_blueprint(bookdetails,url_prefix='/book_details')
app.register_blueprint(bookborrowed,url_prefix='/book_borrowed')
app.register_blueprint(bookreturned,url_prefix='/book_returned')
app.register_blueprint(bookupdate,url_prefix='/bookdata_update')
app.register_blueprint(studentupdate,url_prefix='/studentdata_update')
app.register_blueprint(bookdelete,url_prefix='/book_delete')
app.register_blueprint(studentdelete,url_prefix='/student_delete')   
app.register_blueprint(topreaders,url_prefix='/top_readers')  
app.register_blueprint(highdemandbook,url_prefix='/highdemand_book')
     

    