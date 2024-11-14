import csv
import requests

# inclusive, exclusive
START = 0
END   = 420 

# call the census geocoder API with a formatted csv (<10k records) 
# and write response to a file
# note: API response takes ~5 minutes each time
def call(batch_num: int):
  url = 'https://geocoding.geo.census.gov/geocoder/geographies/addressbatch'
  files = {'addressFile': ( f'aggr_votr_tmp_{batch_num}.csv', 
                            open( f'./temp/aggr_votr_tmp_{batch_num}.csv', 
                                  mode='rb'), 
                            'text/csv')}
  data = {'benchmark': 'Public_AR_Census2020', 
          'vintage': 'Census2020_Census2020'}
  response = requests.post(url, files=files, data=data)
  with open(f'./temp/aggr_votr_resp{batch_num}.csv', mode='wb') as f:
    f.write(response.content)

# call API for each file in range
def main():
  for i in range(START, END):
    call(i)

if __name__ == '__main__':
  main()