import click
from database import session, init_db
from models import Artist, Album, Song

@click.group()
def cli():
    pass  

@cli.command()
def show_songs():
    songs = session.query(Song).all()
    if songs:
        click.echo("********** All Songs **********")
        for song in songs:
            if song.album and song.album.artist:
                click.echo(f"Title: {song.title}")
                click.echo(f"Artist: {song.album.artist.name}")
                click.echo(f"Album: {song.album.title}")
                click.echo(f"Genre: {song.genre}")
                click.echo(f"Release Year: {song.release_year}")
                click.echo(f"Duration: {song.duration} seconds")
                click.echo("--------------------------------")
            else:
                click.echo(f"Song '{song.title}' has missing album or artist information.")
    else:
        click.echo("No songs found.")


@cli.command()
@click.option('--title', prompt='Title', help='Title of the song')
@click.option('--artist', prompt='Artist', help='Name of the artist')
@click.option('--album', prompt='Album', help='Title of the album')
@click.option('--genre', prompt='Genre', help='Genre of the song')
@click.option('--release_year', prompt='Release Year', help='Year of release')
@click.option('--duration', prompt='Duration', help='Duration of the song in seconds')
def add_music(title, artist, album, genre, release_year, duration):
    # Check if the artist already exists
    artist_obj = session.query(Artist).filter_by(name=artist).first()
    if not artist_obj:
        artist_obj = Artist(name=artist)

    # Check if the album already exists
    album_obj = session.query(Album).filter_by(title=album).first()
    if not album_obj:
        album_obj = Album(title=album, artist=artist_obj)

    # Add the song
    song = Song(title=title, genre=genre, release_year=release_year, duration=duration, album=album_obj)
    session.add(song)
    session.commit()
    click.echo('Music added successfully.')

@cli.command()
@click.option('--title', prompt='Enter the title of the music you want to edit', help='Title of the music')
def edit_music(title):
    song = session.query(Song).filter_by(title=title).first()
    if song:
        click.echo(f'Editing {title}')
        new_title = click.prompt('New Title', default=song.title)
        new_genre = click.prompt('New Genre', default=song.genre)
        new_release_year = click.prompt('New Release Year', default=song.release_year)
        new_duration = click.prompt('New Duration', default=song.duration)
        
        song.title = new_title
        song.genre = new_genre
        song.release_year = new_release_year
        song.duration = new_duration
        
        session.commit()
        click.echo('Music edited successfully.')
    else:
        click.echo(f'Music with title {title} not found.')

@cli.command()
@click.option('--title', prompt='Enter the title of the music you want to delete', help='Title of the music')
def delete_music(title):
    song = session.query(Song).filter_by(title=title).first()
    if song:
        session.delete(song)
        session.commit()
        click.echo('Music deleted successfully.')
    else:
        click.echo(f'Music with title {title} not found.') 

@cli.command()
@click.option('--title', prompt='Enter the title of the music you want to check', help='Title of the music')
def check_song(title):
    song = session.query(Song).filter_by(title=title).first()
    if song:
        click.echo(f"Title: {song.title}")
        click.echo(f"Artist: {song.album.artist.name}")
        click.echo(f"Album: {song.album.title}")
        click.echo(f"Genre: {song.genre}")
        click.echo(f"Release Year: {song.release_year}")
        click.echo(f"Duration: {song.duration} seconds")
    else:
        click.echo(f'Music with title {title} not found.')    
          

if __name__ == "__main__":
    init_db()
    cli()
  
