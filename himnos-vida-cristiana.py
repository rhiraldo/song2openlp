import os

def parse_song_file(filename):
    song_data_list = []
    current_song = None

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if line.startswith("#"):
                if current_song is not None:
                    song_data_list.append(current_song)

                title = line[1:].strip()
                current_song = {"title": title, "verses": [], "chorus": []}

            elif line.startswith("```"):
                if current_song is not None:
                    current_song["chorus"] = []
                    for chorus_line in file:
                        chorus_line = chorus_line.strip()
                        if chorus_line.startswith("```"):
                            break
                        if chorus_line:
                            current_song["chorus"].append(chorus_line)

            elif line and line[0].isdigit() and line[1] == ".":
                verse_parts = line.split(" ", 1)
                if len(verse_parts) > 1 and current_song is not None:
                    verse_number, verse_text = verse_parts
                    verse = {"number": verse_number[:-1], "text": verse_text.strip()}
                    current_song["verses"].append(verse)

    if current_song is not None:
        song_data_list.append(current_song)

    return song_data_list

def generate_opensong_xml(song_data):
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += f'<song xmlns="http://openlyrics.info/namespace/2009/song" version="0.8" createdIn="OpenLP 2.4.6" modifiedIn="OpenLP 2.4.6" modifiedDate="2013-01-21T15:21:45">\n'
    xml += f'  <properties>\n'
    xml += f'    <titles>\n'
    xml += f'      <title>{song_data["title"]}</title>\n'
    xml += f'    </titles>\n'
    xml += f'    <authors>\n'
    xml += f'      <author>Himnos de la vida Cristiana</author>\n'
    xml += f'    </authors>\n'
    xml += f'  </properties>\n'
    xml += f'  <lyrics>\n'

    for verse in song_data['verses']:
        verse_number = verse['number']
        verse_text = verse['text'].replace('\n', '<br/>')
        xml += f'    <verse name="v{verse_number}">\n'
        xml += f'      <lines>{verse_text}</lines>\n'
        xml += f'    </verse>\n'

    if song_data.get('chorus'):
        xml += f'    <chorus>\n'
        for line in song_data['chorus']:
            chorus_text = line.replace('\n', '<br/>')
            xml += f'      <lines>{chorus_text}</lines>\n'
        xml += f'    </chorus>\n'
 
    xml += f'  </lyrics>\n'
    xml += f'</song>'

    return xml

def generate_opensong_xml_files(song_data_list):
    for song_data in song_data_list:
        xml = generate_opensong_xml(song_data)
        title = song_data['title'].replace(" ", "_")
        filename = f"{title}.xml"
        with open(filename, "w") as file:
            file.write(xml)
        print(f"Generated XML file: {filename}")

filename = "resources/himnos-vida-cristiana.md"   # Replace with the actual file name
parsed_song_list = parse_song_file(filename)
generate_opensong_xml_files(parsed_song_list)
