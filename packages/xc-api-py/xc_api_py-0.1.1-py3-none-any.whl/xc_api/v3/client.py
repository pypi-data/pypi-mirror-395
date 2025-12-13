from .models import *

from urllib.request import Request, urlopen, HTTPError, urlretrieve
import json
from io import StringIO
import csv
from typing import Optional, Iterable
from pathlib import Path
import warnings
from concurrent.futures import ThreadPoolExecutor

class Client:
  '''
  https://xeno-canto.org/explore/api
  
  TODO Add concise documentation
  '''
  
  BASE_URL = 'https://xeno-canto.org/api/3'
  PER_PAGE_MIN = 50
  PER_PAGE_MAX = 500

  def __init__(
    self,
    api_key: str,
    downloads_dir: Optional[str | Path] = None,
  ):
    self.key = api_key
    self.downloads_dir = downloads_dir

  def _fetch_data(
    self,
    endpoint_url: str,
    query: Optional[dict] = None,
  ):
    url = f'{__class__.BASE_URL}/{endpoint_url.lstrip('/')}?key={self.key}'
    if query:
      url += '&' + '&'.join(f'{k}={v}' for k, v in query.items())

    req = Request(
      url=url,
      method='GET',
    )
    
    with urlopen(req) as resp:
      body = resp.read().decode('utf-8')
      content_type: str = resp.getheader('Content-Type')
      
      if content_type.startswith('text/csv'):
        raise NotImplementedError()
        # buffer = StringIO(body)
        # return csv.DictReader(buffer)
      
      elif content_type.startswith('application/json'):
        return json.loads(body)
  
  def _safe_search_recordings(
    self,
    search_query: RecordingsSearchQuery,
    page: int = 1
  ) -> RecordingsResponse | None:
    query = dict(
      query=search_query.to_query_string(),
      page=page,
      per_page=__class__.PER_PAGE_MIN,
    )
    
    try:
      data = self._fetch_data(
        endpoint_url='/recordings', # DO NOT CHANGE
        query=query,
      )
      return RecordingsResponse.model_validate(data)
    except HTTPError:
      return None

  def search_recordings(
    self,
    search_query: RecordingsSearchQuery,
  ):
    resp = self._safe_search_recordings(search_query) # NOTE Probing request
    if not resp:
      raise RuntimeError() # TODO Refactor as verbose error
    yield from resp.recordings
    for page in range(1, resp.num_pages + 1):
      resp = self._safe_search_recordings(search_query, page)
      if resp:
        yield from resp.recordings # TODO ACE yield only up to the limit count

  def get_recording_by_id(
    self,
    recording_id: XcId,
  ):
    query = RecordingsSearchQuery(
      recording_id=recording_id
    )
    resp = self._safe_search_recordings(query)
    if not resp:
      raise RuntimeError() # TODO Refactor as verbose error
    return resp.recordings[0]

  def _download_file(
    self,
    url: str,
    local_file_path: str | Path,
  ):
    path, _ = urlretrieve(url, local_file_path)
    return path

  def download(
    self,
    records: RecordingsRecord | Iterable[RecordingsRecord],
    save_to_dir: Optional[str | Path] = None,
    max_workers: Optional[int] = None,
  ):
    if isinstance(records, RecordingsRecord):
      records = [records]

    if save_to_dir:
      download_dir = Path(save_to_dir)

    elif self.downloads_dir:
      download_dir = Path(self.downloads_dir)
    
    else:
      download_dir = Path.cwd()
    
    futures = dict()

    for record in records:
      with ThreadPoolExecutor(max_workers=max_workers) as executor:
        try:
          futures[record.recording_id] = executor.submit(
            self._download_file,
            record.recording_file_url,
            Path(download_dir, record.recording_file_name)
          )
          
        except HTTPError as exc:
          warnings.warn(f'Failed to download recording {record.recording_id}: {exc}')
          return None
    
    downloads = {
      recording_id: future.result()
      for recording_id, future
      in futures.items()
    }

    return downloads