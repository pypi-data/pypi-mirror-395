from xc_api.v3 import Client, RecordingsSearchQuery
from pprint import pprint
from itertools import islice

if __name__ == '__main__':
  client = Client(
    API_KEY,
    downloads_dir=r"C:\Users\user\Desktop\New folder (2)"
  )
  
  query = RecordingsSearchQuery(
    animal_sex='male',
    animal_was_seen='yes',
    animal_life_stage='nestling',
    animal_group='birds',
  )
  
  records_generator = client.search_recordings(query)

  records = islice(records_generator, 10)
  
  dl = client.download(records)
  
  pprint(dl)