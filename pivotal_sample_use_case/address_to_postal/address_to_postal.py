'''
Given a csv file andthe name of the column containing address (with postal code),
this function will append a new column into the csv containing the corresponding postal code.

- input: csv file, name of address column
- output: csv file with appended postal code column
'''
import csv
import re

'''Remember to set rootpath directory containing any relevant files!'''
rootPath = ""

def find_postal(address):
	num_list = list(map(int, re.findall(r'\d+', address)))
	if not num_list:
		return 0
	for elem in num_list:
		if elem >= 10000:
			return elem
	return 0

def append_postal(lines, colname, outname):
	header = lines[0]
	address_index = header.index(colname)
	header.append(outname)
	for i in range(1, len(lines)):
		postal = find_postal(lines[i][address_index])
		lines[i].append(postal)
	return lines

def main(filename, input_argv):
	colname = input_argv[0]
	outname = input_argv[1]
	inputfile = open(filename, 'rb')
	csv_lines = list(csv.reader(inputfile, delimiter=',', quotechar='"'))
	result = append_postal(csv_lines, colname, outname)
	outputfile = open(filename.split('.')[0] + '_postcode.csv', 'wb')
	wr = csv.writer(outputfile)
	for row in result:
		wr.writerow(row)
	print 'Output file saved as ' +filename.split('.')[0]+'_postcode.csv'
	

if __name__ == "__main__":
	filename = raw_input("Name of the file to be processed: ")
	colname = raw_input("Name of the column containing address: ")
	out_colname = raw_input("Name of the output column containing postal code: ")
	main(filename, [colname, out_colname])