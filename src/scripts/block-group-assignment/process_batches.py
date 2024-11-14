import csv

# read saved responses from census geocoder API
# match each code with 2020 census data to find
#   number of voters in each block group,
#   save results as csv
# record and print number of records for which:
#   the voter voted from outside WA state
#   the geocoder could not find a match (PO boxes, others not in database)
#   the geo_id returned by the geocoder did not match to a block group from census data
def main():
  out_dict = {}
  count_no_match = count_not_in_wa = count_invalid_geo_id = count_total = 0
  
  with open(
    './../data/race_18plus_by_bg_2020/DECENNIALPL2020.P3-Data.csv'
    ) as pop_csv:
    pop_reader = csv.reader(pop_csv, delimiter=',')
    i = 0
    for [geo_id, name, pop, *_] in pop_reader:
      i += 1
      if i <= 2:
        continue
      out_dict[geo_id] = [name, pop, 0]
  
  for i in range(420):
    with open(f'./temp/aggr_votr_resp{i}.csv') as batch_csv:
      batch_reader = csv.reader(batch_csv, delimiter=',')
      for row in batch_reader:
        if 'WA' not in row[1]:
          count_not_in_wa += 1
        elif row[2] == 'No_Match':
          count_no_match += 1
        else:
          geo_id = '1500000US' + ''.join(row[-4:])[:-3]
          if geo_id not in out_dict.keys():
            count_invalid_geo_id += 1
          else:
            out_dict[geo_id][2] += 1
        count_total += 1

  print('no match:', count_no_match / count_total)
  print('not in WA:', count_not_in_wa / count_total)
  print('invalid geo_id:', count_invalid_geo_id / count_total)

  with open('./aggr_votr_out.csv', mode='w') as out_csv:
    out_writer = csv.writer(out_csv, 
                            delimiter=',', 
                            quotechar='"', 
                            quoting=csv.QUOTE_MINIMAL)
    out_writer.writerow([ 'geo_id', 
                          'block_group_name', 
                          'total_voting_age_pop', 
                          'num_voted'])
    for id, [name, pop, voted] in out_dict.items():
      out_writer.writerow([id, name, pop, str(voted)])


if __name__ == "__main__":
  main()