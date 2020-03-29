import pymongo
import random
client = pymongo.MongoClient("mongodb+srv://rutvik:rutvik@project1-r9nwq.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database("travel")
f=db.flight
fa=db.favl
b=db.booking
def fromto(prange,dep,arv,select):
    l=''
    x=f.find({'dep':dep,'arv':arv,'price':{'$lte':prange}})
    if select=='':
        pass
    elif select=='plh':
        x=x.sort('price')
        for i in x:
            l+='\n'+'<p><input type="submit" name="flight" value="{} {}      Price:{}"></p>'.format(i['_id'],i['company'],i['price'])
    elif select=='rhl':
        x=x.sort('price',-1)
        for i in x:
            l+='\n'+'<p><input type="submit" name="flight" value="{} {}      Price:{}"></p>'.format(i['_id'],i['company'],i['price'])
    elif select=='slh':
        y=fa.sort('avl',-1)
        ans={}

    return l

def favl(uid,bid,no,fno,bdate):
    x=fa.find_one({'fid':fno,'date':bdate})['avl']
    if(x>=no):
        y=x-no
        ans0='<h1>Booking Success</h1>'
        ans="<p>Flight Booking</p><p>Booking ID:{}</p></p><p>Id:{}</p><p>Company:{}</p><p>Departure:{}  Arrival:{}  Date:{}</p><p>Total amount:{}</p>".format(bid,fno,f.find_one({'_id':fno})['company'],f.find_one({'_id':fno})['dep'],f.find_one({'_id':fno})['arv'],bdate,no*f.find_one({'_id':fno})['price'])
        ans1='<p>Get location of <input type="submit" value="{} Airport" name="getloc">'.format(f.find_one({'_id':fno})['dep'])
        #bid=random.randrange(1000,10000)
        while(True):
            try:
                b.insert_one({'_id':bid,'bill':(ans+ans1),'uid':uid})
                break
            except:
                bid=random.randrange(1000,10000)
                ans0='<h1>Booking Success</h1>'
                ans="<p>Flight Booking</p><p>Booking ID:{}</p></p><p>Id:{}</p><p>Company:{}</p><p>Departure:{}  Arrival:{}  Date:{}</p><p>Total amount:{}</p>".format(bid,fno,f.find_one({'_id':fno})['company'],f.find_one({'_id':fno})['dep'],f.find_one({'_id':fno})['arv'],bdate,no*f.find_one({'_id':fno})['price'])
                ans1='<p>Get location of <input type="submit" value="{} Airport" name="getloc">'.format(f.find_one({'_id':fno})['dep'])
                
        
        fa.update_one({'fid':fno,'date':bdate},{'$set':{'avl':y}})
        
        
        return ans0+ans
    else:
        return "Not enough seats available"

def tbooking(x):
    return b.find_one({'_id':x})['bill']
    
def showbooking(uid):
    x=b.find({'uid':uid})
    ans=''
    for i in x:
        ans+='<p><input type="submit" value={} name="bid"></p>'.format(i['_id'])
    return ans

    
print(showbooking('usr0'))
