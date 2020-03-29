import pymongo
from tkinter import *
import random
client = pymongo.MongoClient("mongodb+srv://rutvik:rutvik@project1-r9nwq.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database("travel")
h=db.hotel
user=db.user
havl=db.havl
login= 0
b=db.booking

def ask(uid,pas):
    x=user.find_one({'_id':uid})
    if(x==None):
        print("User not found")
        return 0
    else:
        y=(x['password'])
        if(y==pas):
            print("Login Successful")
            return 1
        else:
            print("Wrong password")
            return 0
def createuser(name,uid,psw,email):
    x=user.find_one({'_id':uid})
    if(x!=None):
        return 0
    else:
        data={'name':name, '_id':uid, 'password':psw,'email':email}
        x=user.insert_one(data)
        return 1
    
def hotel(x):
    x=db.hotel.find({'city':city})
    if(x!=None):
        return  1
    else:
        return 0
    
def citynames(city,select,prange):
    p=db.hotel.find({'city':city,'price':{'$lt':prange}})
    ans=''
    if select=='plh':
        x=p.sort('price',1)
    elif select=='phl':
        x=p.sort('price',-1)
    elif select=='rhl':
        x=p.sort('rating',-1)
    for i in x:
        ans+='<p><input type="submit" name="hotel" value="{}"> Price: {}</p>'.format(i['name'],i['price'])
    return ans

def book(uid,bid,hname,date,no):
    no=int(no)
    hid=h.find_one({'name':hname})['_id']
    x=havl.find_one({'date':date},{'hid':hid})['_id']
    n=havl.find_one({'_id':x})['room']
    if(x!=None):
        if(n>=no):
           
            bid=random.randrange(1000,10000)
            ans='<p>Hotel Booking</p><p>Booking ID:{}</p> <p>Hotel: {}</p><p>Date: {}</p><p>No. of rooms booked: {}</p><p>Room price: {}</p>'.format(bid,hname,date,no,(no*h.find_one({'_id':hid})['price']))
            ans1='<p>Get location of <input type="submit" value="{} {}" name="getloc">'.format(hname,h.find_one({'_id':hid})['city'])
            while(True):   
                try:
                    b.insert_one({'_id':bid,'bill':(ans+ans1),'uid':uid})
                    break
                except:
                    bid=random.randrange(1000,10000)
                    

            havl.update_one({'hid':hid,'date':date},{'$inc':{'room':-no}})
            havl.find_one({'hid':hid,'date':date})['room']
            return ans
        else:
            return '-1'
    else:
        return '-1'
def info(uid):
    x=user.find_one({'_id':uid})
    return '''<h1>User Details:</h1><p>Name: {}</p><p>Email ID: {}</p>'''.format(x['name'],x['email'])
#citynames('mumbai','plh',10000)
