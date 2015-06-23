'''
Given a csv file with a column containing postal code, 
this function will append 3 columns into the csv file,
namely latitude: 'lat', lonogitude: 'lon' and constituency: 'constituency'

The reference file for lookup is "postal_consti_final.csv"

- input: csv file
- output: csv file with appended columns
'''

'''the main package used here is pandas'''
import pandas as pd

#!Remember to set rootpath directory containing the reference files!
rootPath = ""

def pcToLatLon(inputfile, colname):

	ref = pd.read_csv(rootPath + 'postal_consti_final.csv', dtype={'postcode':str})
	postcode_col = colname
	inputfile[postcode_col] = inputfile[postcode_col].map(lambda x: ("%.f" % x).zfill(6) if not pd.isnull(x) else '000000')
	inputfile = inputfile.merge(ref, how='left', left_on=colname, right_on='postcode')
	inputfile.drop('postcode', axis=1, inplace=True)
	return inputfile

def main(filename, input_argv):
	column_name = input_argv[0]
	inputfile = pd.read_csv(filename)
	outputfile = pcToLatLon(inputfile, column_name)
	outputfile.to_csv(filename.split('.')[0]+'_merged.csv', index=False)
	print 'Output file saved as '+filename.split('.')[0]+'_merged.csv'

if __name__ == "__main__":
	filename = raw_input("Name of the file to be processed: ")
	column_name = raw_input("Name of the column containing postcode: ")
	main(filename, [column_name])