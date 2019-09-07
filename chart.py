import csv
import spotipy
import json
import requests
import lxml.html
import urllib.parse

client_id = ""
client_secret = ""

client_data = {}
with open('client.json') as f:
    client_data = json.load(f)

from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data
client_credentials_manager = SpotifyClientCredentials(client_id=client_data["client_id"], client_secret=client_data["client_secret"])
token = client_credentials_manager.get_access_token()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API
# result = sp.search(q='artist:"Sun Kil Moon" AND "Pray for Newtown"', type='track') #search query
# print(result["tracks"]["items"][0]["external_urls"]["spotify"])
# result['tracks']['items'][0]['artists']

csv_reader = csv.DictReader(open('asor.csv', mode='r'))
writer = csv.DictWriter(open('asor_out.csv', mode='w'),
                        fieldnames=csv_reader.fieldnames + ['url', 'id'])
writer.writeheader()
htm = open('asor.html','w')
htm.write(
    '<html lang="en">\n' +
    '<head>\n' +
    '    <meta charset="UTF-8">\n' +
    '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n' +
    '    <meta http-equiv="X-UA-Compatible" content="ie=edge">\n' +
    '    <title>מצעד העשור</title>\n' +
    '</head>\n' +
    '<body>')

num = 0
good = 0
for row in csv_reader:
    out = {}
    for key in row:
        out[key] = row[key]
    # out['image'] = 'hello'
    song = row['SONG NAME']
    artist = row['ARTIST NAME']
    result = sp.search(q='artist:"' + artist + '" AND "' + song + '"', type='track')
    try:
        out['url'] = result["tracks"]["items"][0]["external_urls"]["spotify"]
        out['id'] = result["tracks"]["items"][0]["id"]
        htm.write('<iframe src="https://open.spotify.com/embed/track/' + out['id'] +
            '" width="210" height="250" frameborder="0" allowtransparency="true" allow="encrypted-media" style="float:left;"></iframe>\n')
        good += 1
    except:
        htm.write('<div width="210" height="250" style="float:left; width: 210;">' + artist + '<br>' + song)
        try:
            urlparams = urllib.parse.urlencode({'type': 'master', 'artist': artist, 'track': song})
            # https://www.discogs.com/de/search/?type=master&artist=Dj+Dodger+Stadium&track=Love+songs
            # //*[@id="search_results"]/div/a/span[2]/img
            r = requests.get("https://www.discogs.com/de/search/?" + urlparams)
            html = lxml.html.fromstring(r.text)
            img = html.xpath('//*[@id="search_results"]/div/a/span/img')
            htm.write("<img src='" + img[0].attrib['data-src'] + "' width='200'/>")
        except:
            None
        htm.write('</div>\n')
        None
    writer.writerow(out)
    num += 1
print(f'Processed {num} songs, found {good} urls.')
htm.write('</body>\n</html>\n')
htm.close()

