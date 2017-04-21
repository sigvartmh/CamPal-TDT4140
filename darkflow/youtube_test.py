from youtube_upload import video_upload
import argparse


def upload_to_youtube():
  a = argparse.Namespace() #ikke ror
  a.auth_host_name='localhost' #ikke ror
  a.auth_host_port=[8080, 8090] #ikke ror
  a.category="22" #ikke ror
  a.description="Campal test"
  a.file="lecture_0.mkv" #filnavn og lokasjon
  a.keywords="test, nice"
  a.logging_level='ERROR' #ikke ror
  a.noauth_local_webserver=False #ikke ror
  a.privacyStatus='public' #ikke ror
  a.title='Campal test' #tittel
  video_upload(a)

if __name__ == '__main__':
    upload_to_youtube()
