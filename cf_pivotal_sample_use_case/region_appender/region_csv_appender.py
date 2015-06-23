import json
import csv
from shapely.geometry import Point
from shapely.geometry import mapping, shape
from collections import namedtuple

"""
# Find the column most likely to contain lat/lng pair, and use the columns to tag each row with URA Planning Region info
# Can apply csv multiple times to enrich multiple lat/lng pairs (without duplication)
# WARN: will randomly choose columns if no lat/lng pair exists. User must check output result!

# The 3 reference files for lookup are "ura_planning_area.geojson", "ura_region.geojson" and "ura_subzone.geojson"

- input: csv file
- output: csv file appended with regions/planning regions/subzones
"""

#!Remember to set rootpath directory containing the geojson files!
rootPath = ""

def make_zones(fname):
    subzones = {}
    with open(fname) as json_file:
        subzones = json.load(json_file)    
    return [(f['properties'],shape(f['geometry']),f) for f in subzones['features']]    

subzone_shapes = make_zones(rootPath + "ura_subzone.geojson")
planning_area_shapes = make_zones(rootPath + "ura_planning_area.geojson")
region_shapes = make_zones(rootPath + "ura_region.geojson")
BestColumn = namedtuple('BestColumn', 'lat lon m n')

def filter_lon(i):
    try: 
        lon = abs(float(i) - 103.820268)
        if lon <= 2.0:
            return lon
        else:
            return 1000.0
    except:
        return 1000.0
    
def filter_lat(i):
    try: 
        lat = abs(float(i) - 1.363653)
        if lat <= 1.0:
            return lat
        else:
            return 1000.0
    except:
        return 100.0

def find_marked(header_row):
    marked = [0] * len(header_row)
    col_name_map = dict((k,i) for (i,k) in enumerate(header_row))
    for col_name in header_row:
        if "plnregion#" in col_name:
            marked[col_name_map[col_name.split("#")[1]]] = 1
            marked[col_name_map[col_name.split("#")[2]]] = 1
            print("Marked :" + col_name)
    return marked
    
def greedy_find_lat_lon(ldata, marked, header_row):
    curr_max = float("inf")
    max_col = None
    for (i,k) in enumerate(header_row[:-2]):
        if marked[i] == 0:
            col_pos = i
            header = [header_row[col_pos],header_row[col_pos+1]]
            lon_points = [filter_lon(l[col_pos]) for l in ldata]
            lat_points = [filter_lat(l[col_pos+1]) for l in ldata]   
            SSE = sum(lon_points) + sum(lat_points)
            lon = i
            lat = i+1
            lon_points = [filter_lat(l[col_pos]) for l in ldata]
            lat_points = [filter_lon(l[col_pos+1]) for l in ldata]  
            new_SSE = sum(lon_points) + sum(lat_points)
            if SSE > new_SSE:
                SSE = new_SSE
                lon = i+1
                lat = i
            col_name = "plnregion#"  + header_row[lat] + "#" + header_row[lon]            
            if curr_max > SSE:
                max_col = BestColumn(lon=lon, lat=lat, m=SSE, n=col_name)
                curr_max = SSE
    return max_col       

def find_region(p, ura_type):
    shapes = None
    if ura_type == "planning":
        shapes = planning_area_shapes
    elif ura_type == "region":
        shapes = region_shapes
    elif ura_type == "subzone":
        shapes = subzone_shapes
    for r,geom,i in shapes:
            if geom.contains(p):
                return r

def add_zone_info(lines, bestColumn, ura_type):   
    lat = bestColumn.lat
    lon = bestColumn.lon
    append_length = {"region":2, "planning":3, "subzone":4}
    for l in lines:     
        try:
            p_from = Point(float(l[lon]), float(l[lat]))
            from_r = find_region(p_from, ura_type)
            if from_r:
                if ura_type == "region":
                    yield l + [from_r['OBJECTID'],from_r['REGION_N']]
                elif ura_type == "planning":
                    yield l + [from_r['OBJECTID'],from_r['PLN_AREA_N'],from_r['REGION_N']]
                if ura_type == "subzone":
                    yield l + [from_r['OBJECTID'],from_r['SUBZONE_N'],from_r['PLN_AREA_N'],from_r['REGION_N']]
            else:
                yield l + [-1] + ['None']*append_length[ura_type]
        except:
            yield l + [-1] + ['None']*append_length[ura_type]

def append_region(lines, ura_type):
    header_row = lines[0]
    marked = find_marked(header_row)
    bestColumn = greedy_find_lat_lon(lines,marked,header_row)
    print(bestColumn)
    new_header_row = [lines[0] + [bestColumn.n + "#OBJECTID",
                                  bestColumn.n + "#REGION_N"]]
    if ura_type == "planning":
        new_header_row = [lines[0] + [bestColumn.n + "#OBJECTID",
                                      bestColumn.n + "#PLN_AREA_N",
                                      bestColumn.n + "#REGION_N"]]
    elif ura_type == "subzone":
        new_header_row = [lines[0] + [bestColumn.n + "#OBJECTID",
                                      bestColumn.n + "#SUBZONE_N",
                                      bestColumn.n + "#PLN_AREA_N",
                                      bestColumn.n + "#REGION_N"]]  
    return  new_header_row + [i for i in add_zone_info(lines[1:],bestColumn, ura_type)]


"""
MAIN CODE HERE
# Find the column most likely to contain lat/lng pair, and use the columns to tag each row with URA Planning Region info
# Can apply csv multiple times to enrich multiple lat/lng pairs (without duplication)
# WARN: will randomly choose columns if no lat/lng pair exists. User must check output result!

- input: csv file
- output: csv file appended with planning regions
"""
def main(filename, argv_list):
    ura_type = argv_list[0]
    num_run = argv_list[1]
    csvfile_in = open(filename, 'rb')
    csv_lines = list(csv.reader(csvfile_in, delimiter=',', quotechar='"'))
    result = append_region(csv_lines, ura_type)
    for i in range(int(num_run)-1):
        result = append_region(result, ura_type)
    csvfile_out = open(filename.split('.')[0] + '_enriched.csv', 'wb')
    wr = csv.writer(csvfile_out, quoting=csv.QUOTE_NONNUMERIC)
    for r in result:
        wr.writerow(r)
    print 'Output file saved as '+filename.split('.')[0]+'_enriched.csv'
        
if __name__ == '__main__':
    filename = raw_input("Name of the file to be processed: ")
    ura_type = raw_input("Select ura type (planning/region/subzone): ")
    if ura_type not in ("planning", "region", "subzone"):
        print "invalid ura_type"
    num_run = raw_input("Number of times to run (Number of latlon pair columns): ")
    main(filename, [ura_type, num_run])
