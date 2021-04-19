import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from geopy import distance

cred = credentials.Certificate("/home/pi/clean-community-firebase-adminsdk-7auv5-bbf407567a.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://clean-community.firebaseio.com/'
})

def senddata(lon,lad,ctemp,humidity,CO2,tVOC):
	ref = db.reference('/Readings')
	ref.push({
		'longitude':lon,
		'latitude':lad,
		'Temperature': ctemp,
        'Humidity': humidity,
		'CO2': CO2,
		'tVOC': tVOC
	})

def grabReadingdata():
	ref = db.reference('/Readings/')
	print(ref.get())
	
def grabReadingGPSdata():
	ref = db.reference('/Readings/')
	data = ref.get()
	for key, value in data.items():
		print("Lon: "+value["longitude"]+" Lad: "+value["latitude"])

def grabLocationdata():
	ref = db.reference('/Location/')
	print(ref.get())
	
def grabLocationGPSdata():
	ref = db.reference('/Location/')
	data = ref.get()
	for key, value in data.items():
		print("Lon: "+value["longitude"]+" Lad: "+value["latitude"])

def checkLocation(long,lat):
	ref = db.reference('/Location/')
	data = ref.get()
	current_location = [{'lat':lat,'lng':long}]
	for key, value in data.items():

		center_location= [{'lat':value["latitude"],'lng':value["longitude"]}]
		radius = value["radius"]/10

		centerLoc_tuple = tuple(center_location[0].values())
		currentLoc_tuple = tuple(current_location[0].values())

		dis = distance.distance(centerLoc_tuple,currentLoc_tuple)#in KM
		if dis <= radius:
			print("in a circle")
			#any code 
			return center_location

		return 0

def checkCircledata(long,lat):
	ref = db.reference('/Readings/')
	data = ref.get()
	current_location = [{'lat':lat,'lng':long}]
	try:
		for key, value in data.items():
			center_location= [{'lat':value["latitude"],'lng':value["longitude"]}]

			centerLoc_tuple = tuple(center_location[0].values())
			currentLoc_tuple = tuple(current_location[0].values())
			dis = distance.distance(centerLoc_tuple,currentLoc_tuple)

			if dis == 0:
				print("yes")
				return 1
				#add check if out of data add here
	except:
		print("No entires yet add")
	return 0
