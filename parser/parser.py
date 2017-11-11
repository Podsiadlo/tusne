import re

template = '''<?xml version='1.0' encoding='UTF-8'?>
<song xmlns="http://openlyrics.info/namespace/2009/song" version="0.8" createdIn="OpenLP 2.4.5" modifiedIn="OpenLP 2.4.5" modifiedDate="2017-03-06T19:20:12">
  <properties>
    <titles>
      <title>${title}</title>
    </titles>
    <verseOrder>${order}</verseOrder>
    <authors>
      <author>NN</author>
    </authors>
    <songbooks>
      <songbook name="mSNE Tarnow" entry="1"/>
    </songbooks>
    <themes>
      <theme>Uwielbienie</theme>
    </themes>
  </properties>
  <lyrics>
    ${verses}
  </lyrics>
</song>'''
verse_template = '''<verse name="${verse_type}">
  <lines>${lines}</lines>
</verse>
'''


class Song(object):
    """docstring for Song."""
    verses = {}
    order = []
    title = ""
    last_verse = []

    def __init__(self, title, order=[], verses={}):
        super(Song, self).__init__()
        self.title = title
        self.order = order
        self.verses = verses

filename = "cz1.txt"

with open(filename) as f:
    content = f.readlines()
content = [x.strip() for x in content]

title_pattern = re.compile("{.*}")
verse_pattern = re.compile("[a-z]\d+[a-z]*:")

skip = False
songs = {}
active_song = ""
for line in content:
    if line is "":
        pass
    elif title_pattern.match(line):
        try:
            title = re.search("[^{}]+", line).group(0)
        except AttributeError:
            raise("Problem in extracting song title")
        active_song = title
        songs[title] = Song(title)
        songs[title].order = []
        songs[title].verses = {}
    elif verse_pattern.match(line):
        try:
            verse_type = re.search("[a-z]\d+[a-z]*", line).group(0)
        except AttributeError:
            raise("Problem in extractig verse type")
        if verse_type in songs[active_song].order:
            skip = True
            # print("Skipping " + verse_type + " in song " + songs[active_song].title + " because it has " + str(songs[active_song].order))
            songs[active_song].order.append(verse_type)
        else:
            skip = False
            songs[active_song].order.append(verse_type)
            songs[active_song].last_verse = verse_type
            songs[active_song].verses[verse_type] = []
            # print("Adding " + verse_type + " to song " + songs[active_song].title)
    elif not skip:
        songs[active_song].verses[songs[active_song].last_verse].append(line)
        # print("Adding line: " + line + " to " + active_song + "::" + songs[active_song].last_verse)
    # else:
        # print("Skipping line: " + line)

# for song in songs:
#     for verse in songs[song].order:
#         for song_line in songs[song].verses[verse]:
#             print(songs[song].title + "::" + verse + "::" + song_line)

for song in songs:
    songs[song].xml = template.replace("${title}", songs[song].title)
    order = ""
    for verse_type in songs[song].order:
        order = order + " " + verse_type
    songs[song].xml = songs[song].xml.replace("${order}", order)
    verses = ""
    for verse in songs[song].verses:
        lines = verse_template.replace("${verse_type}", verse)
        lyrics = ""
        for lyric_line in songs[song].verses[verse]:
            lyrics = lyrics + "<br/>" + lyric_line
        verses = verses + lines.replace("${lines}", lyrics)
    songs[song].xml = songs[song].xml.replace("${verses}", verses)
    # print(songs[song].xml)
    with open("msne/" + songs[song].title + " (NN).xml", "w") as f:
        f.write(songs[song].xml)


    # print(songs[song].xml)

# print(template + "\n\n\n\n")
# print(verse_template)
