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
	ctemp= float(ctemp)
	humidity=float(humidity)
	CO2=float(CO2)
	tVOC=float(tVOC)
	ref.push({
		'longitude':lon,
		'latitude':lad,
		'temp': ctemp,
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
		print("lat: "+value["latitude"]+" lng: "+value["longitude"])

def grabLocationdata():
	ref = db.reference('/Location/')
	print(ref.get())
	
def grabLocationGPSdata():

	ref = db.reference('/Location/')
	data = ref.get()
	for key, value in data.items():
		print("lat: "+value["latitude"]+" lng: "+value["longitude"])

def checkLocation(long,lat):
	ref = db.reference('/Location/')
	data = ref.get()
	current_location = [{'lat':lat,'lng':long}]
	print (current_location)
	for key, value in data.items():
		center_location= [{'lat':value["latitude"],'lng':value["longitude"]}]
		radius = value["radius"]/10
		print ("pass")
		centerLoc_tuple = tuple(center_location[0].values())
		currentLoc_tuple = tuple(current_location[0].values())
		print (currentLoc_tuple)
		print (centerLoc_tuple)
		dis = distance.distance(centerLoc_tuple,currentLoc_tuple)#in KM
		if dis <= radius:
			return center_location
	return 0

def checkCircledata(long,lat):
	ref = db.reference('/Readings/')
	data = ref.get()
	current_location = [{'lat':lat,'lng':long}]
	try:
		for key, value in data.items():
			center_location= [{'lat':value["latitude"],'lng':value["longitude"]}]
			print (center_location)
			if current_location == center_location:
				return  1
	except:
		print("failed")
	return 0
	
def grabdatareadings(long,lat):
	ref = db.reference('/Readings/')
	data = ref.get()
	current_location = [{'lat':lat,'lng':long}]
	try:
		for key, value in data.items():
			center_location= [{'lat':value["latitude"],'lng':value["longitude"]}]
			print(center_location)
			if current_location == center_location:
				return  value
	except:
		print("failed")
	return 0

