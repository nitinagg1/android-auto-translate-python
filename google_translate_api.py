from googleapiclient.discovery import build


def translate_strings(source_list, target_lang):

  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build('translate', 'v2',
            developerKey='')
  return service.translations().list(
      source='en',
      target=target_lang,
      q=source_list
  ).execute()

