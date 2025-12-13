from .types import *

from pydantic import BaseModel, Field, ConfigDict
from typing import Sequence, Optional
import re

XC_UPLOAD_URL = r'//xeno-canto.org/sounds/uploaded/{user_id}'

class Sono(BaseModel):
  small:  str = Field(
    description='URL to the small version of the sonogram image.',
    examples=[XC_UPLOAD_URL + r'/ffts/XC{recording_id}-small.png'],
  )
  med:    str = Field(
    description='URL to the medium sonogram image.',
    examples=[XC_UPLOAD_URL + r'/ffts/XC{recording_id}-med.png'],
  )
  large:  str = Field(
    description='URL to the large sonogram image.',
    examples=[XC_UPLOAD_URL + r'/ffts/XC{recording_id}-large.png'],
  )
  full:   str = Field(
    description='URL to the full-resolution sonogram image.',
    examples=[XC_UPLOAD_URL + r'/ffts/XC{recording_id}-full.png'],
  )

class Osci(BaseModel):
  small:  str = Field(
    description='URL to the small oscillogram image.',
    examples=[XC_UPLOAD_URL + r'/wave/XC{recording_id}-small.png'],
  )
  med:    str = Field(
    description='URL to the medium oscillogram image.',
    examples=[XC_UPLOAD_URL + r'/wave/XC{recording_id}-med.png'],
  )
  large:  str = Field(
    description='URL to the large oscillogram image.',
    examples=[XC_UPLOAD_URL + r'/wave/XC{recording_id}-large.png'],
  )

class RecordingsRecord(BaseModel):
  model_config = ConfigDict(
    populate_by_name=True,
    validate_by_name=True,
  )
  animal_genus:                     str = Field(
    alias='gen',
    description='Generic (genus) name of the species.',
    examples=['Troglodytes'],
  )
  animal_species_name:              str = Field(
    alias='sp',
    description='Specific epithet (species name).',
    examples=['troglodytes'],
  )
  animal_subspecies_name:           str = Field(
    alias='ssp',
    description='Subspecies epithet.',
  )
  animal_group:                     Noneable.Group = Field(
    alias='grp',
    description='Biological group the species belongs to.',
  )
  animal_species_common_name:       str = Field(
    alias='en',
    description='English name of the species.',
    examples=['Eurasian Wren'],
  )
  animal_background:                Noneable.StringSequence = Field(
    alias='also',
    description='List of background species identified in the recording.',
    examples=[['Turdus viscivorus', 'Parus major']],
  )
  animal_sex:                       Noneable.Sex = Field(
    alias='sex',
    description='Sex of the recorded animal.',
  )
  animal_life_stage:                Noneable.LifeStage = Field(
    alias='stage',
    description='Life stage of the animal.',
  )
  animal_was_seen:                  Noneable.Bool = Field(
    alias='animal-seen',
    description='Whether the recorded animal was seen.',
  )
  recording_id:                     XcId = Field(
    alias='id',
    description='Catalogue number of the recording on Xeno-Canto.',
    examples=['694038'],
  )
  recording_author:                 str = Field(
    alias='rec',
    description='Name of the recordist.',
    examples=['Jacobo Ramil Millarengo'],
  )
  recording_country:                str = Field(
    alias='cnt',
    description='Country where the recording was made.',
    examples=['Spain'],
  )
  recording_locality_name:          str = Field(
    alias='loc',
    description='Locality name or detailed location.',
    examples=['Sisalde, Ames, A Coruña, Galicia'],
  )
  recording_latitude:               Noneable.Float = Field(
    alias='lat',
    description='Latitude in decimal degrees.',
    examples=['42.8373'],
  )
  recording_longitude:              Noneable.Float = Field(
    alias='lon',
    description='Longitude in decimal degrees.',
    examples=['-8.652'],
  )
  recording_altitude:               Noneable.Float = Field(
    alias='alt',
    description='Altitude of the recording location in meters.',
    examples=['30'],
  )
  recording_sound_type:             Noneable.SoundType = Field(
    alias='type',
    description='Sound type of the recording.',
    examples=['song'],
  )
  recording_method:                 Noneable.RecordingMethod = Field(
    alias='method',
    description='Recording method used.',
    examples=['field recording'],
  )
  recording_page_url:               str = Field(
    alias='url',
    description='URL of the Xeno-Canto detail page.',
    examples=['//xeno-canto.org/694038'],
  )
  recording_file_url:               str = Field(
    alias='file',
    description='Direct download URL for the audio file.',
    examples=[r'//xeno-canto.org/694038/download'],
  )
  recording_file_name:              str = Field(
    alias='file-name',
    description='Original filename of the audio file.',
    examples=['XC694038-211223_02Carrizo variaci\u00f3ns dunha frase bastante stereotipada siteD 9.30 Sisalde.mp3'],
  )
  recording_license:                str = Field(
    alias='lic',
    description='License URL of the recording.',
    examples=['//creativecommons.org/licenses/by-nc-sa/4.0/'],
  )
  recording_quality:                Noneable.Quality = Field(
    alias='q',
    description='Quality rating of the recording.',
  )
  recording_length:                 Noneable.Timedelta = Field(
    alias='length',
    description='Length of the recording in minutes and seconds.',
    examples=['4:08'],
  )
  recording_time:                   Noneable.Time = Field(
    alias='time',
    description='Time of day when the recording was made.',
    examples=['09:30'],
  )
  recording_date:                   Noneable.Date = Field(
    alias='date',
    description='Date the recording was made.',
    examples=['2021-12-23'],
  )
  recording_upload_date:            Noneable.Date = Field(
    alias='uploaded',
    description='Date the recording was uploaded.',
    examples=['2021-12-27'],
  )
  recording_remarks:                str = Field(
    alias='rmk',
    description='Additional remarks by the recordist.',
    examples=['Male repeating a stereotyped phrase. HPF 270 Hz.'],
  )
  recording_playback_used:          Noneable.Bool = Field(
    alias='playback-used',
    description='Whether playback was used to lure the animal.',
  )
  recording_temp:                   Noneable.Float = Field(
    alias='temp',
    description='Temperature during recording (if applicable).',
  )
  recording_register_number:        Noneable.String = Field(
    alias='regnr',
    description='Registration number (if specimen collected).',
  )
  recording_is_automatic:           Noneable.Bool = Field(
    alias='auto',
    description='Indicator for automatic/non-supervised recording.',
    examples=['unknown'],
  )
  recording_device:                 Noneable.String = Field(
    alias='dvc',
    description='Recording device used.',
  )
  recording_microphone:             Noneable.String = Field(
    alias='mic',
    description='Microphone used.',
  )
  recording_sample_rate:            Noneable.Int = Field(
    alias='smp',
    description='Sample rate of the recording.',
    examples=['44100'],
  )
  recording_sonograms:              Sono = Field(
    alias='sono',
    description='An object with the URLs to the four versions of sonograms.',
  )
  recording_oscillograms:           Osci = Field(
    alias='osci',
    description='An object with the URLs to the three versions of oscillograms.',
  )

class RecordingsResponse(BaseModel):
  model_config = ConfigDict(
    populate_by_name=True,
    validate_by_name=True,
  )
  num_recordings:   int = Field(
    alias='numRecordings',
    description='Total number of recordings in the query results.',
  )
  num_species:      int = Field(
    alias='numSpecies',
    description='Number of species represented in the results.',
  )
  page:             int = Field(
    alias='page',
    description='Current page number of the query results.',
  )
  num_pages:        int = Field(
    alias='numPages',
    description='Total number of pages available for this query.',
  )
  recordings:       Sequence[RecordingsRecord] = Field(
    description='List of recording objects on this page.',
  )

class RecordingsSearchQuery(BaseModel):
  # NOTE https://xeno-canto.org/help/search#advanced
  model_config = ConfigDict(
    populate_by_name=True,
  )
  animal_group:             Optional[Group] = Field(
    serialization_alias='grp',
    title='Group',
    description="Use the grp tag to narrow down your search to a specific group.\
      This tag is particularly useful in combination with one of the other tags. Valid group values are (...).\
        You can also use their respective ids (1 to 5), so grp:2 will restrict your search to grasshoppers.\
          Soundscapes are a special case, as these recordings may include multiple groups.\
            Use grp:soundscape or grp:0 to search these.",
    examples=[
      'birds',
      'grasshoppers',
      'bats',
      'frogs',
      'land mammals'
    ],
    default=None,
  )
  animal_genus:             Optional[str] = Field(
    serialization_alias='gen',
    title='Genus/Subspecies',
    description="Genus is part of a species' scientific name, so it is searched by default when performing a basic search (as mentioned above).\
      But you can use the gen tag to limit your search query only to the genus field.\
        So gen:zonotrichia will find all recordings of sparrows in the genus Zonotrichia.\
          Similarly, ssp can be used to search for subspecies.\
            These fields use a 'starts with' rather than 'contains' query and accept a 'matches' operator.",
    default=None,
  )
  animal_species:           Optional[str] = Field(
    serialization_alias='sp',
    title='Species',
    default=None,
  )
  animal_sex:               Optional[Sex] = Field(
    serialization_alias='sex',
    title='Sex',
    description="Formerly included under 'sound types', the sex tag can now be used independently.\
      Valid values for this tag are: (...).\
        This tag always uses a 'matches' operator.",
    default=None,
  )
  animal_life_stage:        Optional[LifeStage] = Field(
    serialization_alias='stage',
    title='Life stage',
    description="Values of the stage tag were previously included under 'sound types' as well.\
      Valid values are: (...).\
        This tag always uses a 'matches' operator.",
    default=None,
  )
  animal_was_seen:          Optional[XcBool] = Field(
    serialization_alias='seen',
    title='Animal seen',
    description="Two tags (seen and playback respectively) that previously were stored as part of Recordist remarks, but now can be used independently.\
      Both only accept yes and no as input.\
        For example, use seen:yes playback:no to search for recordings where the animal was seen,\
          but not lured by playback.",
    default=None,
  )
  animal_background:        Optional[str] = Field(
    serialization_alias='also',
    title='Background species',
    description="To search for recordings that have a given species in the background, use the also tag.\
      Use this field to search for both species (common names in English and scientific names)\
        and families (scientific names).",
    examples=[
      {'formicariidae': 'will return all recordings that have a member of the Antthrush family identified as a background voice.'},
    ],
    default=None,
  )
  recording_author:         Optional[str] = Field(
    serialization_alias='rec',
    title='Recordist',
    description="To search for all recordings from a particular recordist, use the rec tag. (...).\
      This field accepts a 'matches' operator.",
    examples=[
      {'John': 'will return all recordings from recordists whose names contain the string "John".'}
    ],
    default=None,
  )
  recording_country:        Optional[str] = Field(
    serialization_alias='cnt',
    title='Country',
    description="To return all recordings that were recorded in the a particular country, use the cnt tag.\
      (...).\
        This field uses a 'starts with' query and accepts a 'matches' operator.",
    examples=[
      {'brazil': 'return all recordings from the country of \"Brazil\"'},
    ],
    default=None,
  )
  recording_location:       Optional[str] = Field(
    serialization_alias='loc',
    title='Location',
    description="To return all recordings from a specific location, use the loc tag.\
      For example loc:tambopata.\
        This field uses a 'any of the individual words in the text starts with' query,\
          requires at least three characters and accepts a 'matches' operator.",
    default=None,
  )
  recording_remarks:        Optional[str] = Field(
    serialization_alias='rmk',
    title='Recordist remarks',
    description="Many recordists leave remarks about the recording and this field can be searched using the rmk tag, e.g. rmk:flock.\
      The remarks field contains free text, so it is unlikely to produce complete results.\
        Note that information about whether the recorded animal was seen or if playback was used, formerly stored in remarks,\
          now can be searched using dedicated fields! This field searches for individuals words in the text starting with the term(s);\
            it also accepts a 'matches' operator.",
    default=None,
  )
  recording_playback_used:  Optional[XcBool] = Field(
    serialization_alias='playback',
    title='Playback used',
    description="Two tags (seen and playback respectively) that previously were stored as part of Recordist remarks, but now can be used independently.\
      Both only accept yes and no as input.\
        For example, use seen:yes playback:no to search for recordings where the animal was seen,\
          but not lured by playback.",
    default=None,
  )
  recording_latitude:       Optional[float] = Field(
    serialization_alias='lat',
    title='Latitude',
    description="There are two sets of tags that can be used to search via geographic coordinates.\
      The first set of tags is lat and lon.\
        These tags can be used to search within one degree in either direction of the given coordinate, for instance:\
          lat:-12.234 lon:-69.98.\
            This field also accepts '<' and '>' operators; e.g. use lat:\">66.5\" to search for all recordings made above the Arctic Circle.",
    default=None,
  )
  recording_longitude:      Optional[float] = Field(
    serialization_alias='lon',
    title='Longitude',
    description="There are two sets of tags that can be used to search via geographic coordinates.\
      The first set of tags is lat and lon.\
        These tags can be used to search within one degree in either direction of the given coordinate, for instance:\
          lat:-12.234 lon:-69.98. This field also accepts '<' and '>' operators;\
            e.g. use lat:\">66.5\" to search for all recordings made above the Arctic Circle.",
    default=None,
  )
  recording_geo_box:        Optional[str] = Field(
    serialization_alias='box',
    title='Box',
    description="(...) The second tag allows you to search for recordings that occur within a given rectangle,\
      and is called box.\
        It is more versatile than lat and lon, but is more awkward to type in manually,\
          so we have made a map-based search tool to make things simpler.\
            The general format of the box tag is as follows: box:LAT_MIN,LON_MIN,LAT_MAX,LON_MAX.\
              Note that there must not be any spaces between the coordinates.",
    default=None,
  )
  recording_sound_type:     Optional[SoundType] = Field(
    serialization_alias='type',
    title='Sound type',
    description="To search for recordings of a particular sound type, use the type tag.\
      For instance, type:song will return all recordings identified as songs.\
        Note that options may pertain to a specific group only, e.g. 'searching song' is a search term used for grasshoppers,\
          but not for birds.\
            Valid values for this tag are: (...). This tag always uses a 'matches' operator.\
              Up until 2022, the 'type' tag used to search a free text field.\
                We have retained the option to search for non-standardized sound types by using the othertype tag.\
                  This tag also accepts a 'matches' operator, e.g. othertype:\"=wing flapping\".",
    examples=[
      'aberrant',
      'advertisement call',
      'agonistic call',
      'alarm call',
      'begging call',
      'call',
      'calling song',
      'courtship song',
      'dawn song',
      'defensive call',
      'distress call',
      'disturbance song',
      'drumming',
      'duet',
      'echolocation',
      'feeding buzz',
      'female song',
      'flight call',
      'flight song',
      'imitation',
      'mating call',
      'mechanical sound',
      'nocturnal flight call',
      'release call',
      'rivalry song',
      'searching song',
      'social call',
      'song',
      'subsong',
      'territorial call'
    ],
    default=None,
  )
  recording_method:         Optional[RecordingMethod] = Field(
    serialization_alias='method',
    title='Recording method',
    description="The method tag accepts the following, group-dependent values: (...).\
      Do not forget to enclose the term between double quotes!\
        This tag always uses a 'matches' operator.",
    default=None,
  )
  recording_id:             Optional[XcId] = Field(
    serialization_alias='nr',
    title='XC number',
    description="All recordings on xeno-canto are assigned a unique catalog number (generally displayed in the form XC76967).\
      To search for a known recording number, use the nr tag: for example nr:76967.\
        You can also search for a range of numbers as nr:88888-88890.",
    default=None,
  )
  recording_license:        Optional[str] = Field(
    serialization_alias='lic',
    title='Recording license',
    description="Recordings on xeno-canto are licensed under a small number of different Creative Commons licenses.\
      You can search for recordings that match specific license conditions using the lic tag.\
        License conditions are Attribution (BY), NonCommercial (NC), ShareAlike (SA), NoDerivatives (ND) and Public Domain/copyright free (CC0).\
          Conditions should be separated by a '-' character.\
            For instance, to find recordings that are licensed under an Attribution-NonCommercial-ShareAlike license, use lic:BY-NC-SA;\
              for \"no rights reserved\" recordings, use lic:PD.\
                See the Creative Commons website for more details about the individual licenses.",
    default=None,
  )
  recording_quality:        Optional[RecordingQuality | str] = Field(
    serialization_alias='q',
    title='Recording quality',
    description="Recordings are rated by quality.\
      Quality ratings range from A (highest quality) to E (lowest quality).\
        To search for recordings that match a certain quality rating, use the q tag.\
          This field also accepts '<' and '>' operators.",
    examples=[
      {'A':    'will return recordings with a quality rating of A.'},
      {'"<C"': 'will return recordings with a quality rating of D or E.'},
      {'">C"': 'will return recordings with a quality rating of B or A.'}
    ],
    default=None,
  )
  recording_length:         Optional[float | int | str] = Field(
    serialization_alias='len',
    title='Recording length',
    description="To search for recordings that match a certain length (in seconds), use the len tag.\
      This field also accepts '<' , '>' and '=' operators.",
    examples=[
      {'10':       'will return recordings with a duration of 10 seconds (with a margin of 1%, so actually between 9.9 and 10.1 seconds'},
      {'10-15':    'will return recordings lasting between 10 and 15 seconds.'},
      {'"<30"':    'will return recordings half a minute or shorter in length.'},
      {'">120"':   'will return recordings longer than two minutes in length.'},
      {'"=19.8"':  'will return recordings lasting exactly 19.8 seconds, dropping the default 1% margin.'},
    ],
    default=None,
  )
  recording_area:           Optional[str] = Field(
    serialization_alias='area',
    title='World area',
    examples=[
      'africa',
      'america',
      'asia',
      'australia',
      'europe',
    ],
    default=None,
  )
  recording_temp:           Optional[float] = Field(
    serialization_alias='temp',
    title='Recording temperature',
    description='The temp tag for temperature currently also applies only to grasshoppers.\
      This field also accepts \'<\' and \'>\' operators.\
        Use temp:25 to search for sounds recorded between 25-26 °C or temp:">20" for temperatures over 20 °C.',
    default=None,
  )
  since:                    Optional[str] = Field(
    description='The since tag allows you to search for recordings that have been uploaded since a certain date.\
      Using a simple integer value such as since:3 will find all recordings uploaded in the past 3 days.\
        If you use a date with a format of YYYY-MM-DD, it will find all recordings uploaded since that date (e.g. since:2012-11-09).\
          Note that this search considers the upload date, not the date that the recording was made.',
    default=None,
  )
  recording_year:           Optional[str] = Field(
    serialization_alias='year',
    default=None,
  )
  recording_month:          Optional[str] = Field(
    serialization_alias='month',
    default=None,
  )
  collection_year:          Optional[str] = Field(
    serialization_alias='colyear',
    default=None,
  )
  collection_month:         Optional[str] = Field(
    serialization_alias='colmonth',
    default=None,
  )
  regnr:                    Optional[str] = Field(
    default=None,
  )
  recording_automatic:      Optional[str] = Field(
    serialization_alias='auto',
    default=None,
  )
  recording_device:         Optional[str] = Field(
    serialization_alias='dvc',
    default=None,
  )
  recording_microphone:     Optional[str] = Field(
    serialization_alias='mic',
    default=None,
  )
  recording_sample_rate:    Optional[SampleRate] = Field(
    serialization_alias='smp',
    default=None,
  )

  def to_query_string(self) -> str:
    query_dict = self.model_dump(
      by_alias=True,
      exclude_none=True
    )
    query_parts = []
    
    for tag, value in query_dict.items():
      if re.search('[ <>=]', str(value)): # Nest value in double quotes if needed
        value = f'"{value}"'
      query_parts.append(f'{tag}:{value}')

    return '+'.join(query_parts)
