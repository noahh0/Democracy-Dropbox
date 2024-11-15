import csv
from geopy import distance

# use the WA state ballot box location data to
#   determine the distance from the POPULATION-WEIGHTED center
#   of each block group to the nearest ballot box
# save distance IN KM for each block group by geo_id
def main():
  ballot_box_coords = []
  with open(
    './../../../data/ballot_boxes_2020/Voting_Locations_and_Ballot_Boxes.csv'
    ) as bbox_csv:
    bbox_reader = csv.reader(bbox_csv, delimiter=',')
    i = 0
    for row in bbox_reader:
      i += 1
      if i <= 1:
        continue
      if row[-2] and row[-1]:
        ballot_box_coords.append((float(row[-2]), float(row[-1])))
  
  dists = []
  with open(
    './../../../data/bg_pop_centers_2020/CenPop2020_Mean_BG53.csv'
    ) as pop_center_csv:
    pop_center_reader = csv.reader(pop_center_csv, delimiter=',')
    i = 0
    for row in pop_center_reader:
      i += 1
      if i <= 1:
        continue
      geo_id = '1500000US' + ''.join(row[:4])
      center = (float(row[-2]), float(row[-1]))
      min_dist = float('inf')
      for bb_coord in ballot_box_coords:
        d = distance.distance(center, bb_coord).km
        min_dist = min(min_dist, d)
      dists.append([geo_id, str(min_dist)])

  with open('./find_dist_out.csv', mode='w') as out_csv:
    out_writer = csv.writer(out_csv, 
                            delimiter=',', 
                            quotechar='"', 
                            quoting=csv.QUOTE_MINIMAL)
    out_writer.writerow(['geo_id', 'dist_to_nearest_ballot_box_km'])
    for row in dists:
      out_writer.writerow(row)


if __name__ == '__main__':
  main()