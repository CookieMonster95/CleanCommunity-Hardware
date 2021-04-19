import firebase

ctemp=input("Hi, please input Temp:")
lat=input("please input Latitude:")
lon=input("please input Long:")
humidity=input("please input humidity:")
CO2=input("please input CO2:")
tVOC=input("please input tVOC:")

locationCheck=firebase.checkLocation(lon,lat)
if locationCheck != 0:
	gpsLocation = locationCheck[0]

	circleLatitude=gpsLocation['lat']
	circleLongitude=gpsLocation['lng']
	sensorData=firebase.checkCircledata(circleLongitude,circleLatitude)
	if sensorData != 1:
		firebase.senddata(lon,lat,ctemp,humidity,CO2,tVOC)


