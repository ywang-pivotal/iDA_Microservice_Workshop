iDA Usecases for Microservice Workshop
============

Language and Framework
----------------------
- Python 2.7.9
- Flask 0.10.1

Python packages required
------------------------
- Flask 0.10.1
- Werkzeug 0.10.1
- Flask-Uploads 0.1.3
- Shapely 1.5.8
- pandas 0.15.2

Applications attached
---------------------
- Address to postal code
..* Port Number: 1010
..* In terminal/cmd, navigate to the folder containing *webapp_address_postal.py* and run *python webapp_address_postal.py*
- Postal code to Lat/Lon
..* Port Number: 1020
..* In terminal/cmd, navigate to the folder containing *webapp_postal_latlon.py* and run *python webapp_postal_latlon.py*
- Lat/Lon to region
..* Port Number: 1030
..* In terminal/cmd, navigate to the folder containing *webapp_region_appender.py* and run *python webapp_region_appender.py*

In Firefox/Chrome, use the URL "http://localhost:*port-number*" to access the application.
A sample csv file *cc_info.csv* is attached for testing.



Lab One
===========================
To change the orginal codes and deploy them into cloud foundry.


address_to_postal
------------------
- create requirements.txt and add the below packages into requirements.txt

		Flask
		https://pypi.python.org/packages/source/W/Werkzeug/Werkzeug-0.10.4.tar.gz
		https://pypi.python.org/packages/source/F/Flask-Uploads/Flask-Uploads-0.1.3.tar.gz
		https://pypi.python.org/packages/source/S/Shapely/Shapely-1.5.8.tar.gz
		https://pypi.python.org/packages/source/p/pandas/pandas-0.15.2.tar.gz
		
- edit webapp_library.py replace the codes "app.run(port=port_number, debug = web_debug)" with "app.run(port=port_number, host='0.0.0.0',debug = web_debug)". Pass in the host value (0.0.0.0) otherwise it will use 127.0.0.1 by default, it does not work in PCF env.
- eidt webapp_address_portal.py and do the below changes, add "import os" and "port = int(os.getenv("VCAP_APP_PORT"))", replace "build_app(MD, address_to_postal, 1010, True, '_postcode.csv')" with "build_app(MD, address_to_postal, port, True, '_postcode.csv')"
	
		import address_to_postal
		import os

		from webapp_library import build_app
		if __name__ == '__main__':
		    port = int(os.getenv("VCAP_APP_PORT"))
		    build_app(MD, address_to_postal, port, True, '_postcode.csv')
			# build_app(MD, address_to_postal, 1010, True, '_postcode.csv')

- cf command to deploy address_to_postal : 
   
	cf push address_postal -b https://github.com/cloudfoundry/python-buildpack -m 512MB -c "python webapp_address_postal.py"


postal_to_latlon
----------------
- create requirements.txt and add the below packages into requirements.txt

		Flask
		https://pypi.python.org/packages/source/W/Werkzeug/Werkzeug-0.10.4.tar.gz
		https://pypi.python.org/packages/source/F/Flask-Uploads/Flask-Uploads-0.1.3.tar.gz
		https://pypi.python.org/packages/source/S/Shapely/Shapely-1.5.8.tar.gz
		https://pypi.python.org/packages/source/p/pandas/pandas-0.15.2.tar.gz
		
- edit webapp_library.py replace the codes "app.run(port=port_number, debug = web_debug)" with "app.run(port=port_number, host='0.0.0.0',debug = web_debug)". Pass in the host value (0.0.0.0) otherwise it will use 127.0.0.1 by default, it does not work in PCF env.

- eidt webapp_address_portal.py and do the below changes, add "import os" and "port = int(os.getenv("VCAP_APP_PORT"))", replace "build_app(MD, postal_to_latlon, 1020, True, '_merged.csv')" with "build_app(MD, postal_to_latlon, port, True, '_merged.csv')"

codes as below:
	
	import postal_to_latlon
    import os

	from webapp_library import build_app
	if __name__ == '__main__':
    	port = int(os.getenv("VCAP_APP_PORT"))
    	build_app(MD, postal_to_latlon, port, True, '_merged.csv')
		# build_app(MD, postal_to_latlon, 1020, True, '_merged.csv')
		
- cf command to deploy postal_to_latlon : 
 
	cf push postal_to_latlon -b https://github.com/cloudfoundry/python-buildpack -m 512MB -c "python webapp_postal_latlon.py"

region_appender
---------------
- create .buildpacks and add the below content into .buildpacks

  https://github.com/ddollar/heroku-buildpack-apt
  https://github.com/cloudfoundry/python-buildpack
  
- create Aptfile and add the below content into Aptfile
 
	libgeos-dev
	
- create requirements.txt and add the below packages into requirements.txt

		Flask
		https://pypi.python.org/packages/source/W/Werkzeug/Werkzeug-0.10.4.tar.gz
		https://pypi.python.org/packages/source/F/Flask-Uploads/Flask-Uploads-0.1.3.tar.gz
		https://pypi.python.org/packages/source/S/Shapely/Shapely-1.5.8.tar.gz
		https://pypi.python.org/packages/source/p/pandas/pandas-0.15.2.tar.gz
		
- edit webapp_library.py replace the codes "app.run(port=port_number, debug = web_debug)" with "app.run(port=port_number, host='0.0.0.0',debug = web_debug)". Pass in the host value (0.0.0.0) otherwise it will use 127.0.0.1 by default, it does not work in PCF env.

- eidt webapp_region_appender.py and do the below changes, add "import os" and "port = int(os.getenv("VCAP_APP_PORT"))", replace "build_app(MD, postal_to_latlon, 1020, True, '_merged.csv')" with "build_app(MD, postal_to_latlon, port, True, '_merged.csv')"

codes as below:

	import region_csv_appender
	import os

	from webapp_library import build_app
	if __name__ == '__main__':
    	port = int(os.getenv("VCAP_APP_PORT"))
    	build_app(MD, region_csv_appender, port, True, '_enriched.csv')
		#build_app(MD, region_csv_appender, 1030, True, '_enriched.csv')
		
- cf command to deploy region_appender : 
	cf push region_appender -b https://github.com/ddollar/heroku-buildpack-multi -m 512MB -c "python webapp_region_appender.py"

COORDINATOR
-------------
- create requirements.txt and add the below packages into requirements.txt
	
		Flask
		requests
		https://pypi.python.org/packages/source/W/Werkzeug/Werkzeug-0.10.4.tar.gz
		https://pypi.python.org/packages/source/F/Flask-Uploads/Flask-Uploads-0.1.3.tar.gz
		https://pypi.python.org/packages/source/S/Shapely/Shapely-1.5.8.tar.gz
		https://pypi.python.org/packages/source/p/pandas/pandas-0.15.2.tar.gz
		
- eidt web_coordinator.py and do the below changes. add "import os" and "port = int(os.getenv("VCAP_APP_PORT"))", replace "app.run(host='0.0.0.0', port=2000, debug = True)" with "app.run(host='0.0.0.0', port=port, debug = True)"

   codes as below:
   
		if __name__ == "__main__":
		    # app.run(host='0.0.0.0', port=2000, debug = True)
		    port = int(os.getenv("VCAP_APP_PORT"))
		    app.run(host='0.0.0.0', port=port, debug = True)
			
- cf command to deploy uploads_coordinator : 
 
	cf push uploads_coordinator -b https://github.com/cloudfoundry/python-buildpack -m 512MB -c "python web_coordinator.py"

What problems did we solved?
----------------------------


Lab Two
===========================
To create address_to_postal, postal_to_latlon and region_appender as user provided service and get COORDINATOR to bind to them

User Provided Services
---------------------------


COORDINATOR
---------------------------


What problems did we solved?
----------------------------
