# PlayLisP
## The PlayList Processor

**PlayLisP** is a playlist processor. It is a Python library that can be used to script playlist-generators. Shuffle, select 10 tracks from a playlist, mix it with another one, and produce a new playlist.

Actually it is just an experiment and works with *Spotify* only.

## Usage

The main idea is to allow chain-combination of Spotify's playlist. For instance, you can create a script that combine several playlists into a random 20-tracks.

```python
    pl = PlayLisp()
    playlist_id_1 = 'some_playlist_id' # You can get this from Spotify application!
    playlist_id_2 = 'some_other_playlist_id'
    playlist_1 = pl.playlist(playlist_id_1)
    playlist_2 = pl.playlist(playlist_id_2)
    output = playlist_1.interleave(playlist_2).take_first(20).shuffle().collect()
    print(str(output)) # Preview
    print("Save Playlist")
    output_playlist_id = 'id_of_playlist_you_want_to_replace'
    pl.save_on(output_playlist_id, output)
``` 

And things like that. I would like to add many other functionality such as sorting by date, filtering by genre, "playlist subtraction" and more.

After you have done this script, you can put it on `cron` and get your daily playlist! :)

## How to run

This is still W.I.P., so making this work is not user-friendly.

### Install Dependencies

First, you need to have installed `pipenv`

    pip install pipenv

Then, from inside the folder run

    pipenv install --system
    
### Create a Spotify App

Create a new Spotify app from [here](https://developer.spotify.com/my-applications/#!/applications/create).  

### Write a configuration file

For now, you need to manually create a configuration file. Go in the `config` folder and create a `local.ini` file. It **must** contains the following info

```ini
[Spotify]

client_id: the spotify client ide
client_secret: the spotify app client secret
username: your username
redirect_url: http://localhost/ # Keep this in this way
```

### Running a PlayLisp script

You can run a PlayLisP as a library and scripting it in Python **or you can script a playlist in Lisp!!**

First, create a sample `test.plisp` script with the following content

```lisp
(define "main" (playlist "some playlist id"))

(define "result" (shuffle (interleave main main)))

(print result)

(save result "some output playlist id")
```

**WARNING, output playlist will be overwritten!**

Now, you can run playlist with

    python run.py --file test.plist
    
Note that the first time you will need to follow the on-screen instructions for authentication.

## Really?

Yes. I know it is very "raw". But it works. I swear. It will get better with time.
