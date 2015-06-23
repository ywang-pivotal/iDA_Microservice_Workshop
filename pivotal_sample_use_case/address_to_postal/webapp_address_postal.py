MD = {
    "name": "Address to Postal Code",
    "supported_file_type": ["csv"],
    "input_type": "upload_first",
    "output_type": "auto",
    "description": "For a csv file, given the name of the column \
    containing the address, this function append a new column \
    containing the corresponding postal code",
    "parameter": [{
        "name": "address_colname",
        "description": "Name of the column containing address",
        "type": "string",
        "source": "search_column",
        "range": None,
        "default": None,
        "new_column": None
    },{
        "name": "postcode_colname",
        "description": "Name of the appended postcode column",
        "type": "string",
        "source": "user_input",
        "range": None,
        "default": "Postal Code",
        "new_column": True
    }]
}

import address_to_postal

from webapp_library import build_app
if __name__ == '__main__':
	build_app(MD, address_to_postal, 1010, True, '_postcode.csv')