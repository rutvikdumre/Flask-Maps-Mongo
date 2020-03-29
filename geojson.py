import urllib.request
import json
def loc(origin,dest):
    origin=origin.replace(' ','+')
    dest=dest.replace(' ','+')
    key='AIzaSyB-pc5ArKNmzk0PRIHdGkEeRXQRY3ER2-A'
    endpoint='https://maps.googleapis.com/maps/api/directions/json?'
    #origin=input("Where are you:").replace(' ','+')
    #dest=input("Where you wanna go?").replace(' ','')
    req='origin={}&destination={}&key={}'.format(origin,dest,key)
    request= endpoint+req
    response= urllib.request.urlopen(request).read()
    directions=json.loads(response)
    #return('Distance: ', end='')
    #print(directions['routes'][0]['legs'][0])
    return directions['routes'][0]['legs'][0]['distance']['text'],directions['routes'][0]['legs'][0]['duration']['text'],directions['routes'][0]['legs'][0]['end_address']
    
#print(loc('city mall','mistry complex'))
def ans(origin,city):
    places={'Mumbai':['Marine drive','Juhu beach','Siddhivinayak temple','Haji ali dargah','Elephanta caves'],
    'Delhi':['India gate','Qutub minar','Red fort','Humayun tomb'],'Hyderabad':['Charminar','Golconda Fort','Ramoji Film City','Hussain Sagar Lake']}
    l=''
    for i in places[city]:
        try:
            dist,time,end=loc(origin,i)
            l+='<p><h3>{}<h3></p>'.format(i)+'<p><b>Distance:</b> {}<b> ETA:</b>{}<p>'.format(dist,time)+'<p><a href="https://www.google.com/maps/place/{}">Get location</a></p>'.format(i)
        except:
            pass
    return l

