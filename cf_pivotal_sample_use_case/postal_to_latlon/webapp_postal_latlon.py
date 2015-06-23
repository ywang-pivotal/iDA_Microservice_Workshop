MD = {
	"name": "Postcode to LatLon",
	"supported_file_type": ["csv"],
	"input_type": "upload_first",
	"output_type": "auto",
	"description": "For a csv file, given the name of the column \
	containing the postal code, this function append two new columns \
	containing the corresponding latitude and longitude",
	"parameter": [{
		"name": "postcode_colname",
		"description": "Name of the column containg postal code",
		"type": "string",
		"source": "search_column",
		"range": None,
		"default": None,
        "new_column": None
	}]
}

import postal_to_latlon
import os

from webapp_library import build_app
if __name__ == '__main__':
    port = int(os.getenv("VCAP_APP_PORT"))
    build_app(MD, postal_to_latlon, port, True, '_merged.csv')
	# build_app(MD, postal_to_latlon, 1020, True, '_merged.csv')