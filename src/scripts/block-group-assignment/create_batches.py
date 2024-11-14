import csv

# read voter data files and write into batches of 10k records
# formatted for census geocoder API
def main():
  batch = []
  batches = []
  for voter_data in [ 
    './../data/wa_voters/Ballot Status Report 11242020 A-J.csv',
    './../data/wa_voters/Ballot Status Report 11242020 King A-K.csv',
    './../data/wa_voters/Ballot Status Report 11242020 King L-Z.csv',
    './../data/wa_voters/Ballot Status Report 11242020 Kit-P.csv',
    './../data/wa_voters/Ballot Status Report 11242020 Sa-Sn.csv',
    './../data/wa_voters/Ballot Status Report 11242020 Sp-Y.csv']:
    with open(voter_data, encoding='latin-1') as voter_csv:
      voter_reader = csv.reader(voter_csv, delimiter=',')
      j = 0
      for [ _, _, _, _, _, _, _, _, _, _, _, 
            address, 
            city, 
            state, 
            zipc, 
            *_] in voter_reader:
        j += 1
        if j <= 1:
          continue
        batch.append([str(len(batch) + 1), address, city, state, zipc])
        if len(batch) == 10000:
          batches.append(batch)
          batch = []
          count_total += 10000
      batches.append(batch)
      count_total += len(batch)

  for i, batch in enumerate(batches):
    with open(f'./temp/aggr_votr_tmp_{i}.csv', mode='w') as query_csv:
      query_writer = csv.writer(query_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      for row in batch:
        query_writer.writerow(row)


if __name__ == '__main__':
  main()