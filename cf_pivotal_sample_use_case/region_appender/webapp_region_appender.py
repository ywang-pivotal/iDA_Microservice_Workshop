MD = {
	"name": "Region Appender",
	"supported_file_type": ['csv'], 
	"input_type": "auto", 
	"output_type": "'auto",
	"description": "For a csv file, this function will search \
	for the latlon pair columns and append the corresponding Region Info", 
	"parameter": [{
		"name": "ura_type",
		"description": "Type of region to be appended",
		"type": "string", 
		"source": "from_options",
		"range": ('region','planning','subzone'),
		"default": None, #the default value
        "new_column": None
	},{
		"name": "num_run",
		"description": "Number of runs (number of latlon pairs)",
		"type": "integer",
		"source": "user_input",
		"range": None,
		"default": 1,
        "new_column": None
	}]
}
import region_csv_appender

from webapp_library import build_app
if __name__ == '__main__':
    port = int(os.getenv("VCAP_APP_PORT"))
	#build_app(MD, region_csv_appender, 1030, True, '_enriched.csv')
    build_app(MD, region_csv_appender, port, True, '_enriched.csv')