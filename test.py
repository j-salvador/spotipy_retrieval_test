import os
import pprint
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
import time
from json.decoder import JSONDecodeError
import tempfile
import webbrowser
from pathlib import Path


def method_two():
    user = spotipy_object.current_user()
    display_name = user['id']
    followers = user['followers']['total']

    while True:
        print("\n>>> Welcome,", display_name, "!")
        print(">>> You have", str(followers), "followers.")
        print()
        print("0 - Search for an artist")
        print("1 - Exit")
        print()
        choice = input("Your choice:")

        if choice == "0":
            print("You chose 0")
            search_query = input("OK, which artist do you want to search up?\n")
            search_results = spotipy_object.search(search_query, 1, 0, 'artist')
            print(json.dumps(search_results, sort_keys=True, indent=4))

            # Artist details
            artist = search_results['artists']['items'][0]
            print(artist['name'])
            print(str(artist['followers']['total']), "followers")
            print("Genres:",
                  artist['genres'][0],
                  artist['genres'][1],
                  artist['genres'][2],
                  artist['genres'][3],
                  artist['genres'][4])
            webbrowser.open(artist['images'][0]['url'])
            artist_id = artist['id']

            # Album and track details
            track_URIs = []
            track_art = []
            z = 0

            # Extract album data
            album_results = spotipy_object.artist_albums(artist_id)

        elif choice == "1":
            break


def artist_top_tracks(sp):
    # if len(sys.argv) > 1:
    #     urn = sys.argv[1]
    # else:
    #     urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'

    choice = input("Which artist do you want to search for?")
    artist_details = get_artist(sp, choice)
    artist_uri = artist_details['uri']

    print("Choice:", choice, "\nArtist URI:", artist_uri)
    response = sp.artist_top_tracks(artist_uri)

    # pprint.pprint(response['tracks'][0])

    for track in response['tracks']:
        print("\n" + track['name'],
              "\n\t\tLink:", track['external_urls']['spotify'],
              "\n\t\tTrack ID:",track['id'],
              "\n\t\tPopularity:", track['popularity'])

        print("\t\tAlbum artwork:", track['album']['images'][0]['url'])


def artist_top_x_tracks(sp):
    choice = input("Which artist do you want to search for?")
    selection_amount = input("How many songs (up to 10) do you want to retrieve? ")
    if int(selection_amount) > 10:
        selection_amount = 10

    artist_details = get_artist(sp, choice)
    artist_uri = artist_details['uri']

    print("Retrieving the top {} songs by {} - [{}]".format(selection_amount, artist_details['name'], artist_uri))
    response = sp.artist_top_tracks(artist_uri)

    print(".")
    print("..")
    print("...")

    song_names = []
    album_art_list = []
    artist_image = artist_details['images'][0]['url']

    for i in range(0,int(selection_amount)):
        track = response['tracks'][i]
        print("\n" + str(i + 1) + ".", track['name'],
              "\n\t\tLink:", track['external_urls']['spotify'],
              "\n\t\tTrack ID:", track['id'],
              "\n\t\tPopularity:", track['popularity'],
              "\n\t\tAlbum artwork:", track['album']['images'][1]['url'])

        song_names.append(track['name'])
        album_art_list.append(track['album']['images'][1]['url'])

    display_on_webpage(artist_image, song_names, album_art_list)
    print("\n\nSuccessfully retrieved the desired selection")


def display_on_webpage(artist_image, song_names, album_art_urls):
    dir_path = str(Path.home())+  "\\Desktop\\MY_nudes"

    css_file_name = generate_css(dir_path, artist_image)
    html_path = generate_html(album_art_urls, dir_path, song_names, css_file_name)

    webbrowser.open(html_path)


def write_to_file(filepath, text):
    try:
        f = open(filepath, 'a')
        f.write(text)
    except:
        print("FUG")
    finally:
        f.close()


def clear_file(file_path):
    try:
        f = open(file_path, "w")
    finally:
        f.close()


def write_list_of_song_and_art(album_art_urls, file_path, song_names):
    counter = 1
    for name, url in zip(song_names, album_art_urls):
        write_to_file(file_path,
                      "<p>" + str(counter) + ". " + name + "<br/><img src=" + url + " width=150 height=150/></p>")
        counter += 1


def generate_html(album_art_urls, path, song_names, css_file_name):
    file_path = path + "\\spotify_selection.html"
    clear_file(file_path)

    write_to_file(file_path, "<html>")

    head = "<head>" \
           "<title>kiddine p[orn</title>" \
           "<link rel='stylesheet' href='" + css_file_name + "' type='text/css' />" \
           "</head>"

    write_to_file(file_path, head)
    write_to_file(file_path, "<body><h1>Albums:</h1>")

    write_list_of_song_and_art(album_art_urls, file_path, song_names)

    write_to_file(file_path, "</body></html>")
    return file_path


def generate_css(path, artist_image):
    css_path = path + "\\spotify_style.css"
    clear_file(css_path)
    # FOR AN ACTUAL IMAGE FULLSCREEN - SCALES WITH WINDOW SIZE
    #body_string = "body {" \
     #             "  background: url('" + artist_image + "') no-repeat center center fixed;" \
      #            "    -webkit-background-size: cover;" \
       #           "    -moz-background-size: cover;" \
       #           "    -o-background-size: cover;" \
        #          "    background-size: cover; }"

    write_to_file(css_path, "body {background-color: rgb(200,200,200);}")
    return css_path


def get_artist(sp, name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None



# get username
#username = sys.argv[1]  # mine: b01b3e1f61444b11a6991faae783844a

username = "b01b3e1f61444b11a6991faae783844a"
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

# Erase cache and prompt ffor user permission
try:
    token = util.prompt_for_user_token(username, scope)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

# create spotify object
spotipy_object = spotipy.Spotify(auth=token)

artist_top_x_tracks(spotipy_object)
