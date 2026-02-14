class Person:
    def __init__(self, name):
        self.name = name
    def greet(self):
        print("Hello, my name is " + self.name)
p1 = Person("Ayanat")
p1.greet()

class Calculator:
    def minus(self, a, b):
        return a - b
    def division(self, a, b):
        return a / b
calc = Calculator()
print(calc.minus(5, 3))
print(calc.division(56, 7))

class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []
    def add_song(self, song):
        self.songs.append(song)
        print(f"Added: {song}")
    def remove_song(self, song):
        self.songs.remove(song)
        print(f"Removed: {song}")
    def show_songs(self):
        print(f"Playlist '{self.name}'")
        for song in self.songs:
            print(f"- {song}")
my_playlist = Playlist("Favs")
my_playlist.add_song("ICU")
my_playlist.add_song("Spoiler!!!")
my_playlist.add_song("George the lobster")
my_playlist.show_songs()