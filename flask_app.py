from flask import Flask, request, redirect, url_for, render_template
from projectadmin import ask, hotel, citynames,book,createuser,info
from geojson import *
from flights import *
import random

uid='aa'
psw='aa'
city=''
app= Flask(__name__)
bid=0

@app.route('/',methods=["GET", "POST"])

def index():

    if request.method == "POST":
        global uid,psw
        uid=request.form['uname']
        psw=request.form['psw']
        return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/login')
def login():
    if ask(uid,psw)==1:
        return render_template('loginsuccess.html')
        
    else:
        return'''
<h1>Login Failed</h1>
<button onclick="window.location.href = '/';">Click Here</button>'''
email=''
@app.route('/newuser',methods=["GET", "POST"])
def newusrform():
    global name,uid,psw,email
    if request.method=="POST":
        email=request.form['email']
        name=request.form['name']
        uid=request.form['uname']
        psw=request.form['psw']
        return redirect(url_for('create'))
    else:
        return render_template('newusr.html')
        
    
@app.route('/create')

def create():
    if createuser(name,uid,psw,email)==1:
        return '''
<h1>Login Success</h1>
<button onclick="window.location.href = '/login#';">Click Here</button>
'''
    else:
        return '''
<h1>Username exists</h1>
<button onclick="window.location.href = '/newuser';">Retry</button>'''

hotels=[]
f=0

@app.route('/hotel',methods=["GET", "POST"])
def hotel1():
    if request.method == "POST":
        global city
        global f
        global select,prange,hotels,hname
        hname=request.form.get('hotel')
        try:
            hname=request.form.get('hotel')
            test=hname[:3]
            return redirect(url_for('hbook'))
        except:
            prange=int(request.form.get('prange'))
            city=request.form['city']
            city=city.lower()
            select=request.form.get('sort')
            hotels=citynames(city,select,prange)
            f=1
            return render_template('hotel.html')+'''
                {}
        </center>
    </form>
    </body>
    </html>
    '''.format(citynames(city,select,prange))
        

    else:
        return render_template('hotel.html')+'</form>'
    


@app.route('/city', methods=["GET", "POST"])
def city():
    c= citynames(city,select,prange)#returns hotel names in the city as buttons
    if request.method == "POST":
        global hname
        hname=request.form['hotel']
        return redirect(url_for('hbook'))
    else:
        return '''
    <form action=# method="post">
    <h1><b>Hotels in {}</b></h1>
    {}
    </form>'''.format(city,c)

@app.route('/plan',methods=["GET", "POST"])
def plan():
    if request.method == "POST":
        origin=request.form['origin']
        city=request.form['city']
        return render_template('banner.html').format('Places to visit')+'<center>'+ans(origin,city)
    else:
        
        return render_template('banner.html').format('SURPRISE')+'''<center>
    <form action="#" method="post">
    <label for="origin"><b>Origin</b></label>
    <input type="text" placeholder="Enter origin" name="origin" required>
    <p>
    <label for='sort'>Select city</label>
    <select name='city'>
    <option value='Delhi'>Delhi</a></option>
    <option value='Mumbai'>Mumbai</a></option>
    <option value='Hyderabad'>Hyderabad</a></option>
    </select>
    <input type="submit" value="Go">
    </form>'''


@app.route('/hbook', methods=["GET", "POST"])
def hbook():
    if request.method == "POST":
        global date,month,year,rooms,bdate
        bdate=''
        date=request.form['date']
        month=request.form['month']
        year=request.form['year']
        rooms=request.form['rooms']
        bdate=date+month+year
        return redirect(url_for('hbooking'))
    else:
        return render_template('hbook.html')

@app.route('/hbooking')
def hbooking():
    no=int(rooms)
    #return hname
    x=book(uid,bid,hname,bdate,int(no))
    if(x=='-1'):
       return render_template('banner.html').format('Hotel')+'''
<h1>Room not available</h1>'''
    else:
        return render_template('banner.html').format('Hotel')+'''
<b>{}</b>'''.format(x)+'''<button onclick="window.location.href = '/login#';">Go to home page</button>'''



arv,dep='',''
@app.route('/flight',methods=["GET", "POST"])
def fly():
    if request.method == "POST":
        global date,month,year,arv,dep,bdate
        date=request.form['date']
        month=request.form['month']
        year=request.form['year']
        dep=request.form['From']
        arv=request.form['To']
        dep=dep.title()
        arv=arv.title()
        bdate=date+month+year
        return redirect(url_for('flyer'))
    else:
        return render_template('flight.html')+'''
    <form action="#" method="post">
    <label for="origin"><b>Date</b></label>
    <input type="text" placeholder="Date" name="date" required>
    <input type="text" placeholder="Month" name="month" required>
    <input type="text" placeholder="Year" name="year" required><br>
    <label for="dest"><b>From</b></label>
    <input type="text" name="From" required>
    <label for="dest"><b>To</b></label>
    <input type="text" name="To" required>
    <input type="submit" value="Go">
    </form>'''
fno=''
select=''
price=''
@app.route('/flyer',methods=["GET", "POST","POST1"])
def flyer():
    global n,fno,select,price
    
    if request.method == "POST":
        try:
            
            fno=request.form['flight'][0:3]
            n=int(request.form['no'])
            return redirect(url_for('fbook'))
        except:
            price=int(request.form.get('prange'))
            select=request.form.get('sort')
            return redirect(url_for('flyer'))

            
    else:
        return render_template('flight.html')+'''<center>
    <form action="#" method="post">
     <p><label for=range>Price range<input type="range" min='5000' max='10000' name='prange' list='marks'></label></p>
<datalist id='marks'>
  <option value="5500" label="0%"></option>
  <option value="6000"></option>
  <option value="6500"></option>
  <option value="7000"></option>
  <option value="7500" label='7500'></option>
  <option value="8000"></option>
  <option value="8500"></option>
  <option value="9000"></option>
  <option value="9500"></option>
  <option value="10000" label='10000'></option>
</datalist>
    <label for='sort'>Sort by</label>
  <select name='sort'>
    <option value='plh'>None</a></option>
    <option value='plh'>Price L-H</a></option>
    <option value='rhl'>Price H-L</a></option>
   </select>
   <button onclick="window.location.href = '/';">Apply</button>
   </form>
    <form action="#" method="post">
    <label for="origin"><b>No. of tickets:</b></label>
    <input type="text" placeholder="Number of Tickets" name="no" required>
    '''+fromto(price,dep,arv,select)+'''
    </form>'''

@app.route('/fbook',methods=["GET", "POST"])
def fbook():
    bid=random.randrange(1000,10000)
    return render_template('banner.html').format('Flight')+favl(uid,bid,n,fno,bdate)+'''<button onclick="window.location.href = '/login#';">Click Here</button>'''

@app.route('/track',methods=["GET", "POST"])
def track():
    if request.method == "POST":
        global bid
        bid=request.form.get('bid')
        return redirect(url_for('booking'))
    #render_template('banner.html').format('Booking')+tbooking(int(x))+'''<button onclick="window.location.href = '/login#';">Go to home</button>'''
    else:
        return render_template('banner.html').format('Booking')+'''
    <form action="#" method="post">
    <label for="origin"><b>Booking ID:</b></label>
    <input type="text" placeholder="bid" name="bid" required>
    <input type="submit" value="Go">
    </form>'''


@app.route('/booking',methods=["GET", "POST"])
def booking():
    if request.method=="POST":
        dest=request.form.get('getloc')
        origin=request.form.get('origin')
        dist,time,end=loc(origin,dest)
        return render_template('banner.html').format('Booking')+'<center><p><h3>{}<h3></p><p><b>Distance:</b> {}<b> ETA:</b>{}</p><p>{}</p>'.format(dest,dist,time,end)
    else:
       return render_template('banner.html').format('Booking')+'''<form action=# method=post>'''+tbooking(int(bid))+'''<p>Your location<input type="text" placeholder="origin" name="origin" required><p><a href="/login#">Go to Home</a>''' 

@app.route('/userbooking',methods=["GET", "POST"])
def userbooking():
    if request.method == "POST":
        bid=request.form['bid']
        return render_template('banner.html').format('User Booking')+info(uid)+'<p>'+tbooking(int(bid))[:-79]+'''<button onclick="window.location.href = '/login#';">Go to home</button>'''
    else:
        return render_template('banner.html').format('User Booking')+info(uid)+'<form action="#" method="post">'+showbooking(uid)+' </form>'



if __name__=='__main__':
    app.run(debug=True)


