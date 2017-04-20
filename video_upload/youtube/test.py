from youtube_upload import video_upload
import argparse


if __name__ == '__main__':

  a = argparse.Namespace() #ikke ror
  a.auth_host_name='localhost' #ikke ror
  a.auth_host_port=[8080, 8090] #ikke ror
  a.category="22" #ikke ror
  a.description="Campal test"
  a.file="yellow.mp4" #filnavn og lokasjon
  a.keywords="test, nice"
  a.logging_level='ERROR' #ikke ror
  a.noauth_local_webserver=False #ikke ror
  a.privacyStatus='public' #ikke ror
  a.title='Campal test' #tittel
  video_upload(a)
