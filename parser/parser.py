import re
import sys
import getopt

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

title_pattern = re.compile("{.*}")
verse_pattern = re.compile("[a-z]\d+[a-z]*:")

def main(argv):
    input_file, output_dir, print_titles, dry_run = parse_arguments(argv)
    content = read_file(input_file)
    songs = parse_lines(content)
    if not dry_run:
        save_songs(songs, output_dir)
    if print_titles:
        for song in songs:
            print(song)

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

def parse_arguments(argv):
    input_file = ""
    output_dir = ""
    print_titles = False
    dry_run = False
    try:
        opts, args = getopt.getopt(argv,"tdi:o:",["ifile=","odir="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <input_file> -o <output_dir>'
            sys.exit()
        elif opt in ("-i", "--ifile", "--input-file", "--input"):
            input_file = arg
        elif opt in ("-o", "--odir", "--output-dir", "--output"):
            output_dir = arg
        elif opt in ("-t", "--titles", "--print-titles"):
            print_titles = True
        elif opt in ("-d", "--dry", "--dry-run"):
            dry_run = True
    return (input_file, output_dir, print_titles, dry_run)

def read_file(input_file):
    with open(input_file) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


def parse_lines(lines):
    skip = False
    songs = {}
    active_song = ""
    for line in lines:
        if line is "":
            pass
        elif title_pattern.match(line):
            try:
                title = re.search("[^{}]+", line).group(0)
            except AttributeError:
                raise("Problem in extracting song title")
            if title not in songs:
                active_song = title
                songs[title] = Song(title)
                songs[title].order = []
                songs[title].verses = {}
            else:
                sys.stderr.write("Song \"" + title + "\" is duplicated. Skipping...\n")
        elif verse_pattern.match(line):
            try:
                verse_type = re.search("[a-z]\d+[a-z]*", line).group(0)
            except AttributeError:
                raise("Problem in extractig verse type")
            if verse_type in songs[active_song].order:
                skip = True
                songs[active_song].order.append(verse_type)
            else:
                skip = False
                songs[active_song].order.append(verse_type)
                songs[active_song].last_verse = verse_type
                songs[active_song].verses[verse_type] = []
        elif not skip:
            songs[active_song].verses[songs[active_song].last_verse].append(line)
    return songs

def save_songs(songs, output_dir):
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
                if lyrics == "":
                    lyrics = lyric_line
                else:
                    lyrics = lyrics + "<br/>" + lyric_line
            verses = verses + lines.replace("${lines}", lyrics)
        songs[song].xml = songs[song].xml.replace("${verses}", verses)
        with open(output_dir + "/" + songs[song].title + " (NN).xml", "w") as f:
            f.write(songs[song].xml)

if __name__ == "__main__":
   main(sys.argv[1:])
