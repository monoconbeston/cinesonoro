#!/usr/bin/env python3
"""
===============================================================================
          GENERADOR DE MAZO DIGITAL & APP - CINESONORO (V20)
===============================================================================
Juego simplificado de adivinar el NOMBRE DE LA PELÍCULA.
Sin tablero. Modo Celulares (Mazo, Escáner, Conteo con meta personalizable).
Desafíos con película/canción OCULTA (el participante acciona para ver en secreto
su tema para tararear, palabras prohibidas o mímica) + temporizador de 40s.
===============================================================================
"""

import os
import time
import json
import re
import random
import base64
import urllib.parse
import urllib.request
import requests


CONFIG_FILE = "config_cinesonoro.json"

CATALOGO_100_PELICULAS = [
    # Oscar & Clásicos (25)
    {"title": "Titanic", "song": "My Heart Will Go On", "artist": "Celine Dion", "year": "1997", "search_query": "Titanic My Heart Will Go On Celine Dion", "forbidden_words": ["Barco", "Iceberg", "DiCaprio"]},
    {"title": "El Padrino", "song": "Main Title / Speak Softly Love", "artist": "Nino Rota", "year": "1972", "search_query": "The Godfather Main Title Nino Rota", "forbidden_words": ["Mafia", "Corleone", "Oferta"]},
    {"title": "Gladiador", "song": "Now We Are Free", "artist": "Hans Zimmer", "year": "2000", "search_query": "Gladiator Now We Are Free Hans Zimmer", "forbidden_words": ["Roma", "Coliseo", "Máximo"]},
    {"title": "La Lista de Schindler", "song": "Theme from Schindler's List", "artist": "John Williams", "year": "1993", "search_query": "Schindler's List Theme John Williams", "forbidden_words": ["Holocausto", "Lista", "Alemania"]},
    {"title": "La La Land", "song": "City of Stars", "artist": "Ryan Gosling & Emma Stone", "year": "2016", "search_query": "La La Land City of Stars Ryan Gosling", "forbidden_words": ["Jazz", "Piano", "Emma Stone"]},
    {"title": "Rocky", "song": "Gonna Fly Now", "artist": "Bill Conti", "year": "1976", "search_query": "Rocky Gonna Fly Now Bill Conti", "forbidden_words": ["Boxeo", "Balboa", "Filadelfia"]},
    {"title": "Fiebre de Sábado por la Noche", "song": "Stayin' Alive", "artist": "Bee Gees", "year": "1977", "search_query": "Saturday Night Fever Stayin Alive Bee Gees", "forbidden_words": ["Disco", "Travolta", "Baile"]},
    {"title": "Psicosis", "song": "The Murder (Shower Scene)", "artist": "Bernard Herrmann", "year": "1960", "search_query": "Psycho Shower Scene Bernard Herrmann", "forbidden_words": ["Ducha", "Motel", "Cuchillo"]},
    {"title": "El Bueno, el Malo y el Feo", "song": "The Good, the Bad and the Ugly", "artist": "Ennio Morricone", "year": "1966", "search_query": "The Good the Bad and the Ugly Ennio Morricone", "forbidden_words": ["Oeste", "Desierto", "Pistola"]},
    {"title": "Tiburón", "song": "Main Title (Jaws)", "artist": "John Williams", "year": "1975", "search_query": "Jaws Main Title John Williams", "forbidden_words": ["Playas", "Dientes", "Océano"]},
    {"title": "Casablanca", "song": "As Time Goes By", "artist": "Frank Sinatra", "year": "1942", "search_query": "Casablanca As Time Goes By Frank Sinatra", "forbidden_words": ["Francia", "Piano", "Siempre"]},
    {"title": "La Vida es Bella", "song": "La Vita è Bella", "artist": "Nicola Piovani", "year": "1997", "search_query": "La Vita e Bella Nicola Piovani", "forbidden_words": ["Italia", "Campo", "Juego"]},
    {"title": "Cinema Paradiso", "song": "Love Theme", "artist": "Ennio Morricone", "year": "1988", "search_query": "Cinema Paradiso Love Theme Ennio Morricone", "forbidden_words": ["Cine", "Proyector", "Sicilia"]},
    {"title": "Forrest Gump", "song": "Feather Theme", "artist": "Alan Silvestri", "year": "1994", "search_query": "Forrest Gump Feather Theme Alan Silvestri", "forbidden_words": ["Correr", "Bombones", "Chocolates"]},
    {"title": "Armagedón", "song": "I Don't Want to Miss a Thing", "artist": "Aerosmith", "year": "1998", "search_query": "Armageddon I Dont Want to Miss a Thing Aerosmith", "forbidden_words": ["Asteroide", "Bruce Willis", "Espacio"]},
    {"title": "Mamma Mia!", "song": "Mamma Mia", "artist": "ABBA", "year": "2008", "search_query": "Mamma Mia ABBA", "forbidden_words": ["Grecia", "Padre", "Boda"]},
    {"title": "Grease", "song": "You're the One That I Want", "artist": "John Travolta & Olivia Newton-John", "year": "1978", "search_query": "Grease You're the One That I Want John Travolta", "forbidden_words": ["Escuela", "Autos", "Chaqueta"]},
    {"title": "Nace una Estrella", "song": "Shallow", "artist": "Lady Gaga & Bradley Cooper", "year": "2018", "search_query": "A Star Is Born Shallow Lady Gaga", "forbidden_words": ["Cantante", "Guitarra", "Concierto"]},
    {"title": "El Gran Showman", "song": "This Is Me", "artist": "Keala Settle", "year": "2017", "search_query": "The Greatest Showman This Is Me", "forbidden_words": ["Circo", "Barnum", "Espectáculo"]},
    {"title": "Slumdog Millionaire", "song": "Jai Ho", "artist": "A.R. Rahman", "year": "2008", "search_query": "Slumdog Millionaire Jai Ho AR Rahman", "forbidden_words": ["India", "Preguntas", "Millonario"]},
    {"title": "Sonrisas y Lágrimas", "song": "Do-Re-Mi", "artist": "Julie Andrews", "year": "1965", "search_query": "The Sound of Music Do Re Mi Julie Andrews", "forbidden_words": ["Monja", "Familia", "Austria"]},
    {"title": "8 Mile", "song": "Lose Yourself", "artist": "Eminem", "year": "2002", "search_query": "8 Mile Lose Yourself Eminem", "forbidden_words": ["Rap", "Detroit", "Batalla"]},
    {"title": "Footloose", "song": "Footloose", "artist": "Kenny Loggins", "year": "1984", "search_query": "Footloose Kenny Loggins", "forbidden_words": ["Bailar", "Prohibido", "Pueblo"]},
    {"title": "Ghost: La Sombra del Amor", "song": "Unchained Melody", "artist": "The Righteous Brothers", "year": "1990", "search_query": "Ghost Unchained Melody Righteous Brothers", "forbidden_words": ["Fantasma", "Barro", "Cerámica"]},
    {"title": "Amadeus", "song": "Lacrimosa", "artist": "Mozart", "year": "1984", "search_query": "Amadeus Lacrimosa Mozart", "forbidden_words": ["Compositor", "Salieri", "Ópera"]},

    # Marvel, DC, Sagas & Sci-Fi (25)
    {"title": "Star Wars", "song": "Main Title / Imperial March", "artist": "John Williams", "year": "1977", "search_query": "Star Wars Main Title John Williams", "forbidden_words": ["Darth Vader", "Jedi", "Galaxia"]},
    {"title": "Harry Potter", "song": "Hedwig's Theme", "artist": "John Williams", "year": "2001", "search_query": "Harry Potter Hedwig Theme John Williams", "forbidden_words": ["Magia", "Hogwarts", "Varita"]},
    {"title": "El Señor de los Anillos", "song": "Concerning Hobbits", "artist": "Howard Shore", "year": "2001", "search_query": "The Lord of the Rings Concerning Hobbits Howard Shore", "forbidden_words": ["Anillo", "Frodo", "Mordor"]},
    {"title": "Los Vengadores", "song": "The Avengers Main Theme", "artist": "Alan Silvestri", "year": "2012", "search_query": "The Avengers Main Title Alan Silvestri", "forbidden_words": ["Thanos", "Marvel", "Superhéroes"]},
    {"title": "Pantera Negra", "song": "All the Stars", "artist": "Kendrick Lamar & SZA", "year": "2018", "search_query": "Black Panther All the Stars Kendrick Lamar", "forbidden_words": ["Wakanda", "Rey", "Vibranium"]},
    {"title": "Guardianes de la Galaxia", "song": "Hooked on a Feeling", "artist": "Blue Swede", "year": "2014", "search_query": "Guardians of the Galaxy Hooked on a Feeling", "forbidden_words": ["Groot", "Casete", "Mapache"]},
    {"title": "Batman: El Caballero de la Noche", "song": "Why So Serious?", "artist": "Hans Zimmer", "year": "2008", "search_query": "The Dark Knight Why So Serious Hans Zimmer", "forbidden_words": ["Guasón", "Joker", "Ciudad Gótica"]},
    {"title": "Misión Imposible", "song": "Theme from Mission: Impossible", "artist": "Lalo Schifrin", "year": "1996", "search_query": "Mission Impossible Theme Lalo Schifrin", "forbidden_words": ["Tom Cruise", "Agente", "Máscara"]},
    {"title": "007: Skyfall", "song": "Skyfall", "artist": "Adele", "year": "2012", "search_query": "Skyfall Adele 007", "forbidden_words": ["James Bond", "Espía", "Licencia"]},
    {"title": "Jurassic Park", "song": "Theme from Jurassic Park", "artist": "John Williams", "year": "1993", "search_query": "Jurassic Park Theme John Williams", "forbidden_words": ["Dinosaurio", "T-Rex", "Isla"]},
    {"title": "Volver al Futuro", "song": "Back to the Future Theme", "artist": "Alan Silvestri", "year": "1985", "search_query": "Back to the Future Main Title Alan Silvestri", "forbidden_words": ["DeLorean", "Marty", "Doc"]},
    {"title": "Indiana Jones", "song": "The Raiders March", "artist": "John Williams", "year": "1981", "search_query": "Indiana Jones The Raiders March John Williams", "forbidden_words": ["Látigo", "Sombrero", "Arqueólogo"]},
    {"title": "El Origen (Inception)", "song": "Time", "artist": "Hans Zimmer", "year": "2010", "search_query": "Inception Time Hans Zimmer", "forbidden_words": ["Sueños", "Trompo", "DiCaprio"]},
    {"title": "Matrix", "song": "Clubbed to Death", "artist": "Rob Dougan", "year": "1999", "search_query": "Matrix Clubbed to Death Rob Dougan", "forbidden_words": ["Pastilla", "Neo", "Simulación"]},
    {"title": "Piratas del Caribe", "song": "He's a Pirate", "artist": "Hans Zimmer", "year": "2003", "search_query": "Pirates of the Caribbean He's a Pirate Hans Zimmer", "forbidden_words": ["Jack Sparrow", "Barco", "Isla"]},
    {"title": "Spider-Man: Into the Spider-Verse", "song": "Sunflower", "artist": "Post Malone & Swae Lee", "year": "2018", "search_query": "Spider-Verse Sunflower Post Malone", "forbidden_words": ["Telaraña", "Miles Morales", "Multiverso"]},
    {"title": "Iron Man", "song": "Back in Black", "artist": "AC/DC", "year": "2008", "search_query": "Iron Man Back in Black ACDC", "forbidden_words": ["Tony Stark", "Armadura", "Marvel"]},
    {"title": "Top Gun", "song": "Danger Zone", "artist": "Kenny Loggins", "year": "1986", "search_query": "Top Gun Danger Zone Kenny Loggins", "forbidden_words": ["Piloto", "Avión", "Tom Cruise"]},
    {"title": "Cazafantasmas", "song": "Ghostbusters", "artist": "Ray Parker Jr.", "year": "1984", "search_query": "Ghostbusters Ray Parker Jr", "forbidden_words": ["Fantasmas", "Moco", "Auto"]},
    {"title": "Rápidos y Furiosos 7", "song": "See You Again", "artist": "Wiz Khalifa & Charlie Puth", "year": "2015", "search_query": "Fast and Furious 7 See You Again Wiz Khalifa", "forbidden_words": ["Autos", "Familia", "Carreras"]},
    {"title": "Superman", "song": "Main Title (Superman)", "artist": "John Williams", "year": "1978", "search_query": "Superman Main Title John Williams", "forbidden_words": ["Capa", "Kryptonita", "Krypton"]},
    {"title": "Terminator 2", "song": "Main Title (Terminator)", "artist": "Brad Fiedel", "year": "1991", "search_query": "Terminator 2 Main Title Brad Fiedel", "forbidden_words": ["Robot", "Futuro", "Schwarzenegger"]},
    {"title": "Tron: Legacy", "song": "Derezzed", "artist": "Daft Punk", "year": "2010", "search_query": "Tron Legacy Derezzed Daft Punk", "forbidden_words": ["Videojuego", "Motos", "Neón"]},
    {"title": "Dune", "song": "Paul's Dream", "artist": "Hans Zimmer", "year": "2021", "search_query": "Dune Paul's Dream Hans Zimmer", "forbidden_words": ["Desierto", "Gusano", "Especia"]},
    {"title": "Mad Max: Fury Road", "song": "Brothers In Arms", "artist": "Junkie XL", "year": "2015", "search_query": "Mad Max Fury Road Brothers In Arms Junkie XL", "forbidden_words": ["Camión", "Desierto", "Guitarra"]},

    # Disney & Animación (25)
    {"title": "El Rey León", "song": "Circle of Life / Hakuna Matata", "artist": "Elton John", "year": "1994", "search_query": "The Lion King Circle of Life Elton John", "forbidden_words": ["Simba", "Mufasa", "Sabana"]},
    {"title": "Frozen", "song": "Let It Go", "artist": "Idina Menzel", "year": "2013", "search_query": "Frozen Let It Go Idina Menzel", "forbidden_words": ["Hielo", "Elsa", "Olaf"]},
    {"title": "Coco", "song": "Recuérdame (Remember Me)", "artist": "Carlos Rivera", "year": "2017", "search_query": "Coco Recuérdame Remember Me", "forbidden_words": ["México", "Guitarra", "Muertos"]},
    {"title": "Aladdín", "song": "A Whole New World", "artist": "Brad Kane & Lea Salonga", "year": "1992", "search_query": "Aladdin A Whole New World", "forbidden_words": ["Genio", "Lámpara", "Alfombra"]},
    {"title": "La Sirenita", "song": "Under the Sea", "artist": "Samuel E. Wright", "year": "1989", "search_query": "The Little Mermaid Under the Sea", "forbidden_words": ["Ariel", "Cangrejo", "Mar"]},
    {"title": "Toy Story", "song": "You've Got a Friend in Me", "artist": "Randy Newman", "year": "1995", "search_query": "Toy Story You've Got a Friend in Me Randy Newman", "forbidden_words": ["Woody", "Buzz", "Juguetes"]},
    {"title": "Moana", "song": "How Far I'll Go", "artist": "Auli'i Cravalho", "year": "2016", "search_query": "Moana How Far I'll Go Auli'i Cravalho", "forbidden_words": ["Océano", "Isla", "Maui"]},
    {"title": "Encanto", "song": "We Don't Talk About Bruno", "artist": "Encanto Cast", "year": "2021", "search_query": "Encanto We Don't Talk About Bruno", "forbidden_words": ["Colombia", "Mirabel", "Familia"]},
    {"title": "La Bella y la Bestia", "song": "Beauty and the Beast", "artist": "Celine Dion & Peabo Bryson", "year": "1991", "search_query": "Beauty and the Beast Celine Dion", "forbidden_words": ["Rosa", "Castillo", "Vajilla"]},
    {"title": "Shrek", "song": "All Star", "artist": "Smash Mouth", "year": "2001", "search_query": "Shrek All Star Smash Mouth", "forbidden_words": ["Ogro", "Burro", "Pantano"]},
    {"title": "Los Increíbles", "song": "The Incredibles Theme", "artist": "Michael Giacchino", "year": "2004", "search_query": "The Incredibles Main Theme Michael Giacchino", "forbidden_words": ["Traje", "Familia", "Superhéroes"]},
    {"title": "Mulan", "song": "I'll Make a Man Out of You", "artist": "Donny Osmond", "year": "1998", "search_query": "Mulan I'll Make a Man Out of You", "forbidden_words": ["China", "Dragón", "Ejército"]},
    {"title": "Tarzán", "song": "You'll Be in My Heart", "artist": "Phil Collins", "year": "1999", "search_query": "Tarzan You'll Be in My Heart Phil Collins", "forbidden_words": ["Selva", "Monos", "Gorila"]},
    {"title": "Hércules", "song": "Go the Distance", "artist": "Michael English", "year": "1997", "search_query": "Hercules Go the Distance", "forbidden_words": ["Grecia", "Dios", "Olimpo"]},
    {"title": "Up: Una Aventura de Altura", "song": "Married Life", "artist": "Michael Giacchino", "year": "2009", "search_query": "Up Married Life Michael Giacchino", "forbidden_words": ["Globos", "Casa", "Anciano"]},
    {"title": "Monsters, Inc.", "song": "If I Didn't Have You", "artist": "Randy Newman", "year": "2001", "search_query": "Monsters Inc If I Didn't Have You", "forbidden_words": ["Sully", "Mike", "Puertas"]},
    {"title": "Buscando a Nemo", "song": "Nemo Egg", "artist": "Thomas Newman", "year": "2003", "search_query": "Finding Nemo Nemo Egg Thomas Newman", "forbidden_words": ["Pez", "Dory", "Anémona"]},
    {"title": "Spider-Man: Across the Spider-Verse", "song": "Am I Dreaming", "artist": "Metro Boomin", "year": "2023", "search_query": "Across the Spider-Verse Am I Dreaming Metro Boomin", "forbidden_words": ["Multiverso", "Gwen", "Miles"]},
    {"title": "Mi Villano Favorito 2", "song": "Happy", "artist": "Pharrell Williams", "year": "2013", "search_query": "Despicable Me 2 Happy Pharrell Williams", "forbidden_words": ["Minions", "Gru", "Banana"]},
    {"title": "Madagascar", "song": "I Like to Move It", "artist": "Real 2 Reel", "year": "2005", "search_query": "Madagascar I Like to Move It", "forbidden_words": ["Zoológico", "Lémur", "Pingüinos"]},
    {"title": "El Extraño Mundo de Jack", "song": "This Is Halloween", "artist": "Danny Elfman", "year": "1993", "search_query": "The Nightmare Before Christmas This Is Halloween", "forbidden_words": ["Calabaza", "Navidad", "Halloween"]},
    {"title": "Kung Fu Panda", "song": "Oogway Ascends", "artist": "Hans Zimmer", "year": "2008", "search_query": "Kung Fu Panda Oogway Ascends Hans Zimmer", "forbidden_words": ["Panda", "Fideos", "Dragón"]},
    {"title": "Cómo Entrenar a Tu Dragón", "song": "Test Drive", "artist": "John Powell", "year": "2010", "search_query": "How to Train Your Dragon Test Drive John Powell", "forbidden_words": ["Vikingos", "Chimuelo", "Volar"]},
    {"title": "Super Mario Bros. La Película", "song": "Peaches", "artist": "Jack Black", "year": "2023", "search_query": "Super Mario Bros Peaches Jack Black", "forbidden_words": ["Bowser", "Princesa", "Fontanero"]},
    {"title": "Anastasia", "song": "Once Upon a December", "artist": "Liz Callaway", "year": "1997", "search_query": "Anastasia Once Upon a December", "forbidden_words": ["Rusia", "Palacio", "Princesa"]},

    # Culto & Populares (25)
    {"title": "Pulp Fiction", "song": "Misirlou", "artist": "Dick Dale", "year": "1994", "search_query": "Pulp Fiction Misirlou Dick Dale", "forbidden_words": ["Tarantino", "Travolta", "Maletín"]},
    {"title": "E.T. el Extraterrestre", "song": "Flying Theme", "artist": "John Williams", "year": "1982", "search_query": "E.T. Flying Theme John Williams", "forbidden_words": ["Alien", "Bicicleta", "Dedo"]},
    {"title": "El Club de la Pelea", "song": "Where Is My Mind?", "artist": "Pixies", "year": "1999", "search_query": "Fight Club Where Is My Mind Pixies", "forbidden_words": ["Jabón", "Brad Pitt", "Regla"]},
    {"title": "Trainspotting", "song": "Born Slippy", "artist": "Underworld", "year": "1996", "search_query": "Trainspotting Born Slippy Underworld", "forbidden_words": ["Escocia", "Drogas", "Drogas"]},
    {"title": "Kill Bill: Vol. 1", "song": "Battle Without Honor or Humanity", "artist": "Tomoyasu Hotei", "year": "2003", "search_query": "Kill Bill Battle Without Honor or Humanity", "forbidden_words": ["Katana", "Amarillo", "Novia"]},
    {"title": "Space Jam", "song": "Space Jam Theme", "artist": "Quad City DJ's", "year": "1996", "search_query": "Space Jam Quad City DJs", "forbidden_words": ["Básquetbol", "Michael Jordan", "Bugs Bunny"]},
    {"title": "Hombres de Negro", "song": "Men in Black", "artist": "Will Smith", "year": "1997", "search_query": "Men in Black Will Smith", "forbidden_words": ["Aliens", "Gafas", "Traje"]},
    {"title": "Dirty Dancing", "song": "(I've Had) The Time of My Life", "artist": "Bill Medley & Jennifer Warnes", "year": "1987", "search_query": "Dirty Dancing The Time of My Life", "forbidden_words": ["Baile", "Hotel", "Salto"]},
    {"title": "Pretty Woman", "song": "Oh, Pretty Woman", "artist": "Roy Orbison", "year": "1990", "search_query": "Pretty Woman Roy Orbison", "forbidden_words": ["Compras", "Hotel", "Richard Gere"]},
    {"title": "El Profesional (Léon)", "song": "Shape of My Heart", "artist": "Sting", "year": "1994", "search_query": "Leon The Professional Shape of My Heart Sting", "forbidden_words": ["Planta", "Asesino", "Niña"]},
    {"title": "Drive", "song": "Nightcall", "artist": "Kavinsky", "year": "2011", "search_query": "Drive Nightcall Kavinsky", "forbidden_words": ["Auto", "Chaqueta", "Guantes"]},
    {"title": "Réquiem por un Sueño", "song": "Lux Aeterna", "artist": "Clint Mansell", "year": "2000", "search_query": "Requiem for a Dream Lux Aeterna Clint Mansell", "forbidden_words": ["Televisión", "Adicción", "Música"]},
    {"title": "La Naranja Mecánica", "song": "Funeral of Queen Mary", "artist": "Wendy Carlos", "year": "1971", "search_query": "A Clockwork Orange Funeral of Queen Mary", "forbidden_words": ["Sombrero", "Leche", "Violencia"]},
    {"title": "Apocalypse Now", "song": "Ride of the Valkyries", "artist": "Wagner", "year": "1979", "search_query": "Apocalypse Now Ride of the Valkyries Wagner", "forbidden_words": ["Helicópteros", "Vietnam", "Río"]},
    {"title": "El Quinto Elemento", "song": "The Diva Dance", "artist": "Inva Mula", "year": "1997", "search_query": "The Fifth Element The Diva Dance", "forbidden_words": ["Azul", "Ópera", "Piedras"]},
    {"title": "Beetlejuice", "song": "Day-O (Banana Boat Song)", "artist": "Harry Belafonte", "year": "1988", "search_query": "Beetlejuice Day-O Harry Belafonte", "forbidden_words": ["Fantasma", "Tres Veces", "Cena"]},
    {"title": "Flashdance", "song": "Flashdance... What a Feeling", "artist": "Irene Cara", "year": "1983", "search_query": "Flashdance What a Feeling Irene Cara", "forbidden_words": ["Agua", "Silla", "Baile"]},
    {"title": "Escuela de Rock", "song": "School of Rock Theme", "artist": "Jack Black", "year": "2003", "search_query": "School of Rock Jack Black", "forbidden_words": ["Profesor", "Guitarra", "Banda"]},
    {"title": "Bohemian Rhapsody", "song": "Bohemian Rhapsody", "artist": "Queen", "year": "2018", "search_query": "Bohemian Rhapsody Queen", "forbidden_words": ["Freddie", "Concierto", "Bigote"]},
    {"title": "Rocketman", "song": "Tiny Dancer", "artist": "Elton John", "year": "2019", "search_query": "Rocketman Tiny Dancer Elton John", "forbidden_words": ["Piano", "Gafas", "Vestuario"]},
    {"title": "Barbie", "song": "Dance the Night / I'm Just Ken", "artist": "Dua Lipa & Ryan Gosling", "year": "2023", "search_query": "Barbie Dance the Night Dua Lipa", "forbidden_words": ["Rosa", "Muñeca", "Ken"]},
    {"title": "Oppenheimer", "song": "Can You Hear The Music", "artist": "Ludwig Göransson", "year": "2023", "search_query": "Oppenheimer Can You Hear The Music Ludwig Goransson", "forbidden_words": ["Bomba", "Átomo", "Física"]},
    {"title": "El Graduado", "song": "The Sound of Silence", "artist": "Simon & Garfunkel", "year": "1967", "search_query": "The Graduate The Sound of Silence Simon Garfunkel", "forbidden_words": ["Piscina", "Iglesia", "Boda"]},
    {"title": "Amélie", "song": "La Valse d'Amélie", "artist": "Yann Tiersen", "year": "2001", "search_query": "Amelie La Valse d'Amelie Yann Tiersen", "forbidden_words": ["París", "Fotomatón", "Duende"]},
    {"title": "Interstellar", "song": "First Step / Cornfield Chase", "artist": "Hans Zimmer", "year": "2014", "search_query": "Interstellar First Step Hans Zimmer", "forbidden_words": ["Espacio", "Reloj", "Agujero"]}
]

print("Total catalog length:", len(CATALOGO_100_PELICULAS))


DESAFIOS = {
    "tararea": [
        {"desc": "Tararea el tema principal sin cantar letras ni decir palabras."},
        {"desc": "Tararea el ritmo principal de la canción usando solo 'Mmm-mmm' o 'La-la-la'."}
    ],
    "palabra_prohibida": [
        {"desc": "Describe la película sin mencionar las 3 palabras prohibidas indicadas."},
        {"desc": "Explica la trama al equipo omitiendo completamente las 3 palabras vetadas."}
    ],
    "mimica": [
        {"desc": "Actúa en silencio la escena principal de la película sin hablar ni emitir sonidos."},
        {"desc": "Haz mímica del personaje principal o del momento más famoso de la película en 40 segundos."}
    ]
}


def cargar_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def guardar_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def obtener_token_client_credentials(client_id, client_secret):
    if not client_id or not client_secret:
        return None
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
    
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode("utf-8")
    
    req = urllib.request.Request(auth_url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data.get("access_token")
    except Exception as e:
        print(f"  ⚠️ Error al conectar con Spotify API: {e}")
    return None

def buscar_cancion_spotify(queries, token):
    if isinstance(queries, str):
        queries = [queries]
    
    for q in queries:
        if not q or not q.strip():
            continue
        clean_q = re.sub(r'[/():-]', ' ', q).strip()
        clean_q = re.sub(r'\s+', ' ', clean_q)
        search_url = f"https://api.spotify.com/v1/search?q={urllib.parse.quote(clean_q)}&type=track&limit=1"
        
        for intento in range(2):
            req = urllib.request.Request(search_url, headers={"Authorization": f"Bearer {token}"})
            try:
                time.sleep(0.25)  # Pausa de 250ms entre consultas para evitar Rate Limit
                with urllib.request.urlopen(req, timeout=10) as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode("utf-8"))
                        tracks = data.get("tracks", {}).get("items", [])
                        if tracks:
                            t = tracks[0]
                            album = t.get("album", {})
                            release_date = album.get("release_date", "0000")
                            year = release_date.split("-")[0] if release_date else "----"
                            return {
                                "id": t["id"],
                                "song": t["name"],
                                "artist": ", ".join([a["name"] for a in t.get("artists", [])]),
                                "year": year,
                                "preview_url": t.get("preview_url")
                            }
                        break
            except urllib.error.HTTPError as err:
                if err.code == 429:
                    retry_after = 3
                    try:
                        retry_after = int(err.headers.get("Retry-After", 3)) + 1
                    except Exception:
                        pass
                    if retry_after > 5:
                        print(f"    ℹ️ Spotify pausado por límite de velocidad ({retry_after}s). Usando iTunes Audio...")
                        return {"rate_limited": True}
                    else:
                        print(f"    ⏳ Pausando {retry_after}s...")
                        time.sleep(retry_after)
                        continue
                else:
                    break
            except Exception:
                break
    return None


def buscar_preview_itunes(title, song, artist):
    queries = [
        f"{title} {song} {artist}",
        f"{song} {artist}"
    ]
    for q in queries:
        clean_q = re.sub(r'[/():-]', ' ', q).strip()
        clean_q = re.sub(r'\s+', ' ', clean_q)
        url = f"https://itunes.apple.com/search?term={urllib.parse.quote(clean_q)}&media=music&entity=song&limit=1"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            time.sleep(0.15)
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    results = data.get("results", [])
                    if results:
                        return results[0].get("previewUrl")
        except Exception:
            pass
    return None

def enriquecer_con_spotify(peliculas, client_id, client_secret):
    token = obtener_token_client_credentials(client_id, client_secret)
    if not token:
        print("⚠️ No se pudo obtener token de Spotify. Usando catálogo integrado con respaldo de iTunes.")
        return peliculas
    
    print("🎵 Conectado exitosamente con Spotify. Procesando las 100 películas en tiempo real...")
    enriquecidas = []
    exitos = 0
    fallos = 0
    
    spotify_disabled = False
    for i, p in enumerate(peliculas, 1):
        q1 = p.get("search_query") or f"{p['title']} {p.get('song', '')} {p.get('artist', '')}"
        q2 = f"{p.get('song', '')} {p.get('artist', '')}"
        
        queries = [q1, q2]
        res = None
        if not spotify_disabled:
            res = buscar_cancion_spotify(queries, token)
            if res and res.get("rate_limited"):
                spotify_disabled = True
                res = None
        
        preview_audio = None
        fuente = "Fallback"
        
        if res and res.get("id"):
            p["id"] = res["id"]
            if res.get("song") and res["song"] != "Banda Sonora Original":
                p["song"] = res["song"]
            if res.get("artist") and res["artist"] != "Varios Artistas":
                p["artist"] = res["artist"]
            if res.get("year") and res["year"] != "----":
                p["year"] = res["year"]
            preview_audio = res.get("preview_url")
            fuente = "Spotify"
        
        if not preview_audio:
            itunes_url = buscar_preview_itunes(p['title'], p.get('song', ''), p.get('artist', ''))
            if itunes_url:
                preview_audio = itunes_url
                if fuente == "Spotify":
                    fuente = "Spotify + iTunes Audio"
                else:
                    fuente = "iTunes Audio"

        p["audio_url"] = preview_audio or ""
        exitos += 1
        print(f"  [{i}/{len(peliculas)}] ✅ [{fuente}] {p['title']} -> '{p['song']}' ({p['artist']})")
        enriquecidas.append(p)
        
    print(f"\n📊 Procesamiento completado exitosamente para las {len(peliculas)} películas.")
    return enriquecidas

def generar_html_cinesonoro(peliculas, out_filename="index.html"):
    peliculas_json = json.dumps(peliculas, ensure_ascii=False)
    desafios_json = json.dumps(DESAFIOS, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CineSonoro: El Juego de Películas</title>
    
    <!-- Configuración PWA Móvil -->
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="CineSonoro">
    <meta name="theme-color" content="#0d050e">

    <!-- Librería QR Scanner -->
    <script src="https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.min.js"></script>

    <style>
        :root {{
            --bg-dark: #0d050e;
            --card-bg: rgba(22, 11, 28, 0.95);
            --accent-gold: #ffb703;
            --accent-red: #e63946;
            --text-main: #ffffff;
            --text-muted: #a0a0b0;
            --success: #38b000;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
            -webkit-tap-highlight-color: transparent;
        }}

        body {{
            background: var(--bg-dark);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            padding: 15px;
            overflow-x: hidden;
        }}

        .container {{
            width: 100%;
            max-width: 420px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 15px;
        }}

        /* --- NAVEGACIÓN PRINCIPAL ENTRE MODOS --- */
        .mode-nav {{
            display: flex;
            width: 100%;
            max-width: 420px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 4px;
            gap: 4px;
            margin-bottom: 5px;
            border: 1px solid rgba(255, 183, 3, 0.2);
        }}

        .nav-btn {{
            flex: 1;
            padding: 10px 4px;
            border: none;
            background: transparent;
            color: var(--text-muted);
            font-weight: 800;
            font-size: 0.8rem;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: center;
        }}

        .nav-btn.active {{
            background: var(--accent-gold);
            color: #000;
            box-shadow: 0 2px 10px rgba(255, 183, 3, 0.4);
        }}

        /* --- VISTAS DE CADA MODO --- */
        .app-view {{
            display: none;
            width: 100%;
            animation: fadeIn 0.3s ease-in-out;
        }}

        .active-view {{
            display: block;
        }}

        /* --- CABECERA --- */
        .header-title {{
            font-size: 1.5rem;
            font-weight: 900;
            letter-spacing: 1.5px;
            background: linear-gradient(135deg, #ffb703 0%, #e63946 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-transform: uppercase;
            margin-bottom: 2px;
            text-align: center;
        }}

        .subtitle {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-bottom: 10px;
            text-align: center;
        }}

        /* --- 1. MODO MAZO / CARTAS --- */
        .card-display {{
            background: var(--card-bg);
            border: 2px solid var(--accent-gold);
            border-radius: 24px;
            padding: 20px;
            width: 100%;
            min-height: 380px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8), 0 0 20px rgba(255, 183, 3, 0.15);
            text-align: center;
        }}

        .card-type-badge {{
            position: absolute;
            top: -12px;
            background: var(--accent-gold);
            color: #000;
            font-weight: 900;
            font-size: 0.75rem;
            padding: 4px 14px;
            border-radius: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
        }}

        .card-mask {{
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}

        .mask-icon {{
            font-size: 3rem;
            margin-bottom: 8px;
            filter: drop-shadow(0 0 10px rgba(255, 183, 3, 0.5));
        }}

        .movie-title-revealed {{
            font-size: 1.6rem;
            font-weight: 900;
            color: var(--accent-gold);
            margin: 10px 0 5px 0;
            line-height: 1.2;
            text-shadow: 0 0 10px rgba(255, 183, 3, 0.3);
        }}

        .movie-details {{
            font-size: 0.9rem;
            color: var(--text-muted);
            margin-bottom: 12px;
        }}

        .timer-container {{
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 183, 3, 0.3);
            border-radius: 16px;
            padding: 10px;
            width: 100%;
            margin-top: 10px;
        }}

        .timer-display {{
            font-size: 2.2rem;
            font-weight: 900;
            color: var(--accent-gold);
            font-family: monospace;
            margin: 2px 0;
        }}

        /* --- BOTONES --- */
        .btn {{
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 16px;
            font-weight: 900;
            font-size: 0.95rem;
            cursor: pointer;
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            background: linear-gradient(135deg, var(--accent-gold) 0%, #ff8800 100%);
            color: #000;
            box-shadow: 0 4px 15px rgba(255, 183, 3, 0.3);
        }}

        .btn:active {{
            transform: scale(0.97);
        }}

        .btn-secondary {{
            background: rgba(255, 255, 255, 0.1);
            color: var(--text-main);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: none;
        }}

        .btn-gold {{
            background: linear-gradient(135deg, #00f5d4 0%, #00b4d8 100%);
            color: #000;
            box-shadow: 0 4px 15px rgba(0, 245, 212, 0.3);
        }}

        /* --- 2. MODO ESCÁNER QR --- */
        #scanner-box {{
            width: 100%;
            border-radius: 20px;
            overflow: hidden;
            border: 2px solid var(--accent-gold);
            background: #000;
            display: none;
        }}

        #reader {{
            width: 100%;
        }}

        .spotify-container {{
            position: relative;
            width: 100%;
            border-radius: 16px;
            overflow: hidden;
            border: 2px solid var(--accent-gold);
            background: #000;
        }}

        .spotify-mask-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(13, 5, 14, 0.95);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--accent-gold);
            font-weight: 900;
            font-size: 1rem;
            cursor: pointer;
            z-index: 10;
            backdrop-filter: blur(5px);
        }}

        /* --- 3. MODO CONTEO / MARCADOR DE EQUIPOS --- */
        .scoreboard {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 10px;
        }}

        .team-card {{
            background: rgba(0, 0, 0, 0.5);
            border: 1.5px solid rgba(255, 183, 3, 0.3);
            border-radius: 18px;
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .team-name {{
            font-size: 1.1rem;
            font-weight: 900;
            color: var(--text-main);
            text-align: left;
        }}

        .team-score {{
            font-size: 2.2rem;
            font-weight: 900;
            color: var(--accent-gold);
            font-family: monospace;
            min-width: 50px;
        }}

        .score-btns {{
            display: flex;
            gap: 8px;
        }}

        .btn-score {{
            width: 38px;
            height: 38px;
            border-radius: 50%;
            border: none;
            font-size: 1.2rem;
            font-weight: 900;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .btn-plus {{
            background: var(--success);
            color: #000;
        }}

        .btn-minus {{
            background: rgba(255, 255, 255, 0.15);
            color: white;
        }}

        .winner-banner {{
            background: linear-gradient(135deg, var(--accent-gold) 0%, #ff8800 100%);
            color: #000;
            padding: 20px;
            border-radius: 20px;
            font-weight: 900;
            font-size: 1.3rem;
            margin-bottom: 15px;
            animation: pulse 1s infinite alternate;
            display: none;
            text-align: center;
        }}

        @keyframes pulse {{
            from {{ transform: scale(1); }}
            to {{ transform: scale(1.03); }}
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
</head>
<body>

    <!-- NAVEGACIÓN ENTRE MODOS -->
    <div class="mode-nav">
        <button class="nav-btn active" id="nav-mazo" onclick="cambiarModo('mazo')">🎴 Mazo</button>
        <button class="nav-btn" id="nav-escaner" onclick="cambiarModo('escaner')">📷 Escáner</button>
        <button class="nav-btn" id="nav-conteo" onclick="cambiarModo('conteo')">📊 Conteo (<span id="nav-target-display">10</span> pts)</button>
    </div>

    <div class="container">
        <!-- CABECERA DE LA APP -->
        <div class="header-title">🍿 CINESONORO</div>
        <div class="subtitle" id="sub-status">Adivina la Película</div>

        <!-- ==================== VISTA 1: MODO MAZO ==================== -->
        <div id="view-mazo" class="app-view active-view">
            <div class="card-display" id="deck-card">
                <div class="card-type-badge" id="deck-badge">🎬 PELÍCULA NORMAL</div>
                
                <!-- Máscara 1: Para Películas Normales y QR+ (Música y QR) -->
                <div class="card-mask" id="deck-normal-mask" style="display: block;">
                    <div class="mask-icon">🎬</div>
                    <div style="font-weight: 800; color: var(--accent-gold); margin-bottom: 8px;">¿QUÉ PELÍCULA ES?</div>
                    
                    <!-- Código QR para Escanear (30s de Música) -->
                    <div id="deck-qr-container" style="margin: 10px 0; text-align: center;">
                        <img id="deck-qr-img" src="" alt="QR Música" style="width: 150px; height: 150px; border-radius: 12px; border: 2px solid var(--accent-gold); box-shadow: 0 4px 15px rgba(255,183,3,0.3); background: #fff; padding: 4px;">
                        <div style="font-size: 0.78rem; color: var(--accent-gold); margin-top: 6px; font-weight: 800;">📱 Escanea este QR para escuchar la música</div>
                    </div>

                    <!-- Reproductor NATIVO Integrado en la App (Sin redirección, 100% oculto) -->
                    <div id="deck-player-container" style="margin: 15px 0; width: 100%;">
                        <audio id="game-audio" preload="auto"></audio>
                        
                        <button id="btn-play-audio" onclick="toggleAudioMazo()" style="background: linear-gradient(135deg, var(--accent-gold) 0%, #ff8800 100%); color: #000; font-weight: 900; font-size: 1rem; padding: 16px; border-radius: 18px; border: none; width: 100%; display: flex; align-items: center; justify-content: space-between; gap: 12px; box-shadow: 0 4px 15px rgba(255, 183, 3, 0.4); cursor: pointer; transition: all 0.2s ease;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div id="audio-btn-circle" style="width: 44px; height: 44px; border-radius: 50%; background: #0d050e; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; color: var(--accent-gold); flex-shrink: 0; box-shadow: 0 0 10px rgba(0,0,0,0.5);">▶️</div>
                                <div style="text-align: left;">
                                    <div id="audio-btn-text" style="font-size: 0.95rem; font-weight: 900; letter-spacing: 0.5px; color: #000;">ESCUCHAR CANCIÓN</div>
                                    <div id="audio-btn-sub" style="font-size: 0.72rem; color: rgba(0,0,0,0.7); font-weight: 700; margin-top: 2px;">🔒 Carátula y Datos Ocultos</div>
                                </div>
                            </div>
                            <div id="audio-timer-badge" style="font-size: 0.85rem; font-weight: 900; background: #0d050e; color: var(--accent-gold); padding: 6px 12px; border-radius: 12px; display: none;">30s</div>
                        </button>
                    </div>
                    
                    <button class="btn btn-gold" id="btn-revelar-normal" onclick="revelarPeliculaMazo()" style="margin-top: 10px;">👁️ REVELAR PELÍCULA</button>
                </div>

                <!-- Máscara 2: Para DESAFÍOS (Tararea, Palabra Prohibida, Mímica) -->
                <div class="card-mask" id="deck-challenge-mask" style="display: none; background: rgba(13,5,14,0.95); border: 2px solid var(--accent-gold); border-radius: 16px; padding: 20px;">
                    <div class="mask-icon" style="font-size: 2.5rem; margin-bottom: 10px;">🔒</div>
                    <div style="font-weight: 900; color: var(--accent-gold); font-size: 1.1rem; margin-bottom: 6px;">DESAFÍO EN SECRETO</div>
                    <div style="font-size: 0.85rem; color: #ddd; margin-bottom: 15px; line-height: 1.4;">
                        Un participante toma el teléfono. La película y la canción están ocultas para que tus compañeros puedan adivinar.
                    </div>
                    <button class="btn btn-gold" onclick="accionarVerDesafioPrivado()" style="font-size: 0.92rem; font-weight: 900; padding: 14px;">
                        👁️ VER MI DESAFÍO Y PELÍCULA (EN SECRETO)
                    </button>
                </div>

                <!-- Panel Secreto del Participante (Tras accionar) -->
                <div id="deck-challenge-secret" style="display: none; background: rgba(255,183,3,0.06); border: 1.5px solid var(--accent-gold); border-radius: 16px; padding: 15px; width: 100%; text-align: center;">
                    <div style="font-size: 0.75rem; color: var(--accent-gold); font-weight: 900; text-transform: uppercase; letter-spacing: 1px;">
                        🎬 PELÍCULA A INTERPRETAR:
                    </div>
                    <div class="movie-title-revealed" id="secret-title-text" style="font-size: 1.4rem; color: #fff; margin: 6px 0; font-weight: 900;">
                        TITANIC
                    </div>
                    <div class="movie-details" id="secret-details-text" style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">
                        Tema: My Heart Will Go On (1997)
                    </div>

                    <div id="secret-instruction-box" style="background: rgba(0,0,0,0.6); border-radius: 12px; padding: 12px; margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.15);">
                        <div id="secret-type-title" style="font-size: 0.9rem; font-weight: 900; color: #00f5d4; margin-bottom: 6px;">
                            🎵 DESAFÍO: TARAREA
                        </div>
                        <div id="secret-instruction-text" style="font-size: 0.88rem; color: #fff; line-height: 1.4; white-space: pre-line;">
                            Tararea el tema principal sin usar palabras ni cantar letras.
                        </div>
                    </div>

                    <!-- Reproductor Secreto NATIVO (30s) -->
                    <div id="secret-player-box" style="margin: 12px 0; background: rgba(0,0,0,0.5); border-radius: 12px; padding: 10px; border: 1px solid rgba(255,183,3,0.3);">
                        <div style="font-size: 0.78rem; color: var(--accent-gold); font-weight: 800; margin-bottom: 6px;">
                            🎧 ¿No recuerdas la canción? Escúchala 30s en secreto:
                        </div>
                        <button class="btn btn-secondary" id="btn-secret-play" style="padding: 10px 12px; font-size: 0.85rem; width: 100%; background: rgba(255,183,3,0.15); border: 1px solid var(--accent-gold); color: #fff; font-weight: 800;" onclick="toggleSecretAudio()">
                            ▶️ ESCUCHAR CANCIÓN (30s SECRETO)
                        </button>
                    </div>

                    <!-- Temporizador de 40s -->
                    <div class="timer-container" id="timer-box" style="margin-bottom: 15px;">
                        <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Tiempo Restante:</div>
                        <div class="timer-display" id="timer-count" style="font-size: 2.2rem; font-weight: 900; color: var(--accent-gold); font-family: monospace; margin: 4px 0;">40s</div>
                        <button class="btn btn-secondary" style="padding: 8px 15px; font-size: 0.8rem; width: auto;" onclick="iniciarTemporizador(40)">⏱️ INICIAR 40 SEGUNDOS</button>
                    </div>

                    <button class="btn btn-gold" onclick="revelarPeliculaMazo()" style="font-size: 0.85rem; padding: 10px;">👁️ REVELAR A TODOS</button>
                </div>

                <!-- Detalle Revelado para Todos -->
                <div id="deck-revealed" style="display: none; padding: 15px; text-align: center; width: 100%;">
                    <div style="font-size: 0.8rem; color: var(--accent-gold); font-weight: 900; text-transform: uppercase;">Película Revelada:</div>
                    <div class="movie-title-revealed" id="deck-title-text" style="font-size: 1.6rem; color: #fff; margin: 8px 0; font-weight: 900;">TITANIC</div>
                    <div class="movie-details" id="deck-details-text" style="font-size: 0.9rem; color: var(--text-muted);">Banda Sonora: My Heart Will Go On (1997)</div>
                </div>
            </div>

            <button class="btn" onclick="sacarCartaMazo()" style="margin-top: 15px; font-size: 1rem; font-weight: 900;">🎲 SACAR NUEVA CARTA</button>
        </div>

        <!-- ==================== VISTA 2: MODO ESCÁNER QR ==================== -->
        <div id="view-escaner" class="app-view">
            <div id="scanner-box">
                <div id="reader"></div>
            </div>

            <div id="scanner-player" style="display: none;">
                <div class="spotify-container" id="spotify-target"></div>
                <button class="btn btn-gold" id="btn-revelar-qr" onclick="revelarPeliculaQR()" style="margin-top: 15px;">👁️ REVELAR PELÍCULA</button>
                <button class="btn btn-secondary" onclick="activarCamaraQR()" style="margin-top: 10px;">📷 ESCANEAR OTRO QR</button>
            </div>
        </div>

        <!-- ==================== VISTA 3: MODO CONTEO DE EQUIPOS ==================== -->
        <div id="view-conteo" class="app-view">
            <div class="winner-banner" id="winner-banner">
                🏆 ¡GANADOR! 🏆<br>
                <span id="winner-team-name">EQUIPO 1</span>
            </div>

            <div class="target-config-box" style="background: rgba(255, 183, 3, 0.08); border: 1px solid var(--accent-gold); border-radius: 16px; padding: 12px 15px; margin-bottom: 15px; text-align: center;">
                <div style="font-size: 0.85rem; color: var(--accent-gold); font-weight: 800; margin-bottom: 8px; text-transform: uppercase;">
                    🎯 Meta de Aciertos para Ganar
                </div>
                <div style="display: flex; align-items: center; justify-content: center; gap: 8px; flex-wrap: wrap;">
                    <label style="font-size: 0.8rem; color: var(--text-muted);">Objetivo:</label>
                    <input type="number" id="input-meta-puntos" min="1" max="99" value="10" 
                        onchange="actualizarMetaPuntos(this.value)" 
                        style="width: 65px; background: #000; color: #fff; border: 1.5px solid var(--accent-gold); border-radius: 8px; padding: 6px; text-align: center; font-weight: 900; font-size: 1.05rem;">
                    <div style="display: flex; gap: 4px;">
                        <button class="btn" style="padding: 5px 8px; font-size: 0.75rem; background: rgba(255,183,3,0.2); border: 1px solid var(--accent-gold);" onclick="actualizarMetaPuntos(5)">5</button>
                        <button class="btn" style="padding: 5px 8px; font-size: 0.75rem; background: rgba(255,183,3,0.2); border: 1px solid var(--accent-gold);" onclick="actualizarMetaPuntos(10)">10</button>
                        <button class="btn" style="padding: 5px 8px; font-size: 0.75rem; background: rgba(255,183,3,0.2); border: 1px solid var(--accent-gold);" onclick="actualizarMetaPuntos(15)">15</button>
                        <button class="btn" style="padding: 5px 8px; font-size: 0.75rem; background: rgba(255,183,3,0.2); border: 1px solid var(--accent-gold);" onclick="actualizarMetaPuntos(20)">20</button>
                    </div>
                </div>
            </div>

            <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 10px; text-align: center;">
                El primer equipo en adivinar <strong id="meta-display-text" style="color: var(--accent-gold);">10 películas</strong> gana la partida.
            </div>

            <div class="scoreboard" id="scoreboard-list">
                <!-- Tarjetas de Equipos -->
            </div>

            <button class="btn btn-secondary" style="margin-top: 20px;" onclick="agregarEquipo()">➕ Agregar Nuevo Equipo</button>
            <button class="btn btn-secondary" style="margin-top: 10px; background: rgba(230,57,70,0.2);" onclick="reiniciarMarcador()">🔄 Reiniciar Marcador</button>
        </div>
    </div>

    <script>
        const PELICULAS = {peliculas_json};
        const DESAFIOS = {desafios_json};

        let currentCard = null;
        let html5QrCode = null;
        let timerInterval = null;
        let musicTimerInterval = null;
        let secretMusicTimerInterval = null;

        // Marcador de Equipos y Meta Personalizable
        let metaPuntos = parseInt(localStorage.getItem('cinesonoro_meta_puntos')) || 10;
        let equipos = JSON.parse(localStorage.getItem('cinesonoro_equipos')) || [
            {{ id: 1, nombre: "Equipo 1", puntos: 0 }},
            {{ id: 2, nombre: "Equipo 2", puntos: 0 }}
        ];

        window.addEventListener('load', () => {{
            sincronizarMetaUI();
            renderMarcador();
            sacarCartaMazo();
        }});

        function sincronizarMetaUI() {{
            const input = document.getElementById('input-meta-puntos');
            if (input) input.value = metaPuntos;
            const textDisplay = document.getElementById('meta-display-text');
            if (textDisplay) textDisplay.innerText = metaPuntos + ' película' + (metaPuntos > 1 ? 's' : '');
            const navDisplay = document.getElementById('nav-target-display');
            if (navDisplay) navDisplay.innerText = metaPuntos;
        }}

        function actualizarMetaPuntos(val) {{
            let num = parseInt(val);
            if (isNaN(num) || num < 1) num = 1;
            metaPuntos = num;
            localStorage.setItem('cinesonoro_meta_puntos', metaPuntos);
            sincronizarMetaUI();
            verificarGanador();
        }}

        // --- NAVEGACIÓN ENTRE MODOS ---
        function cambiarModo(modo) {{
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.app-view').forEach(v => v.classList.remove('active-view'));

            document.getElementById('nav-' + modo).classList.add('active');
            document.getElementById('view-' + modo).classList.add('active-view');

            if (modo === 'escaner') {{
                activarCamaraQR();
            }} else if (html5QrCode) {{
                html5QrCode.stop().catch(() => {{}});
            }}
        }}

        // --- LÓGICA MODO MAZO ---
        function sacarCartaMazo() {{
            clearInterval(timerInterval);
            clearInterval(musicTimerInterval);
            clearInterval(secretMusicTimerInterval);
            const badge = document.getElementById('music-timer-badge');
            if (badge) badge.style.display = 'none';

            // Reseteo completo de máscaras
            document.getElementById('deck-normal-mask').style.display = 'none';
            document.getElementById('deck-challenge-mask').style.display = 'none';
            document.getElementById('deck-challenge-secret').style.display = 'none';
            document.getElementById('deck-revealed').style.display = 'none';
            
            const titleMask = document.getElementById('deck-title-mask');
            if (titleMask) titleMask.style.display = 'flex';

            // Selección aleatoria
            const rand = Math.random() * 100;
            const pelicula = PELICULAS[Math.floor(Math.random() * PELICULAS.length)];

            // URL y QR de Spotify
            const spotifyUrl = `https://open.spotify.com/track/${{pelicula.id || ''}}`;
            const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=${{encodeURIComponent(spotifyUrl)}}`;
            
            document.getElementById('deck-qr-img').src = qrUrl;
            pausarAudioMazo();
            pausarSecretAudio();

            if (rand < 75) {{
                // Película Normal (75% de probabilidad)
                currentCard = {{ type: 'normal', data: pelicula }};
                document.getElementById('deck-badge').innerText = '🎬 PELÍCULA NORMAL';
                document.getElementById('deck-badge').style.background = 'var(--accent-gold)';
                document.getElementById('deck-normal-mask').style.display = 'block';
            }} else if (rand < 82) {{
                // Tararea (7% de probabilidad)
                const d = DESAFIOS.tararea[Math.floor(Math.random() * DESAFIOS.tararea.length)];
                currentCard = {{ type: 'desafio', subtype: 'tararea', data: pelicula, challenge: d }};
                document.getElementById('deck-badge').innerText = '🎵 DESAFÍO: TARAREA (40s)';
                document.getElementById('deck-badge').style.background = '#00f5d4';
                prepararDesafioPrivado(pelicula, '🎵 DESAFÍO: TARAREA', d.desc, '#00f5d4');
                document.getElementById('deck-challenge-mask').style.display = 'block';
            }} else if (rand < 89) {{
                // Palabra Prohibida (7% de probabilidad)
                const fw = pelicula.forbidden_words || ['Película', 'Personaje', 'Cine'];
                const textInst = `Explica la película sin mencionar las siguientes 3 palabras prohibidas:
1. 🚫 ${{I_fw(fw, 0)}}
2. 🚫 ${{I_fw(fw, 1)}}
3. 🚫 ${{I_fw(fw, 2)}}`;
                currentCard = {{ type: 'desafio', subtype: 'palabra_prohibida', data: pelicula, challenge: {{ desc: textInst }} }};
                document.getElementById('deck-badge').innerText = '🚫 DESAFÍO: PALABRA PROHIBIDA (40s)';
                document.getElementById('deck-badge').style.background = '#ff0055';
                prepararDesafioPrivado(pelicula, '🚫 DESAFÍO: PALABRA PROHIBIDA', textInst, '#ff0055');
                document.getElementById('deck-challenge-mask').style.display = 'block';
            }} else if (rand < 95) {{
                // Mímica (6% de probabilidad)
                const d = DESAFIOS.mimica[Math.floor(Math.random() * DESAFIOS.mimica.length)];
                currentCard = {{ type: 'desafio', subtype: 'mimica', data: pelicula, challenge: d }};
                document.getElementById('deck-badge').innerText = '🎭 DESAFÍO: MÍMICA (40s)';
                document.getElementById('deck-badge').style.background = '#b388eb';
                prepararDesafioPrivado(pelicula, '🎭 DESAFÍO: MÍMICA', d.desc, '#b388eb');
                document.getElementById('deck-challenge-mask').style.display = 'block';
            }} else {{
                // Carta Racha QR+
                currentCard = {{ type: 'racha', data: pelicula }};
                document.getElementById('deck-badge').innerText = '🔥 CARTA QR+ (RACHA)';
                document.getElementById('deck-badge').style.background = '#ffb703';
                document.getElementById('deck-normal-mask').style.display = 'block';
            }}

            document.getElementById('deck-title-text').innerText = pelicula.title;
            document.getElementById('deck-details-text').innerText = `Banda Sonora: ${{pelicula.song}} (${{pelicula.year}})`;
        }}

        function I_fw(arr, idx) {{
            return (arr && arr[idx]) ? arr[idx] : 'Palabra ' + (idx + 1);
        }}

        function prepararDesafioPrivado(pelicula, tituloDesafio, instruccionText, color) {{
            document.getElementById('secret-title-text').innerText = pelicula.title;
            document.getElementById('secret-details-text').innerText = `Tema: ${{pelicula.song}} (${{pelicula.year}})`;
            
            document.getElementById('secret-type-title').innerText = tituloDesafio;
            document.getElementById('secret-type-title').style.color = color;
            document.getElementById('secret-instruction-text').innerText = instruccionText;
            
            pausarSecretAudio();
            const btn = document.getElementById('btn-secret-play');
            if (btn) btn.innerText = '▶️ ESCUCHAR CANCIÓN (30s SECRETO)';

            document.getElementById('timer-count').innerText = '40s';
        }}

        const gameAudio = document.getElementById('game-audio') || new Audio();
        let gameAudioMode = null;

        function toggleAudioMazo() {{
            if (!currentCard || !currentCard.data) return;
            const pelicula = currentCard.data;
            
            const audioPlayer = document.getElementById('game-audio') || gameAudio;

            if (!audioPlayer.paused && gameAudioMode === 'normal') {{
                pausarAudioMazo();
                return;
            }}

            pausarSecretAudio();

            const audioUrl = pelicula.audio_url || '';
            if (!audioUrl) {{
                alert("No se encontró vista previa de audio MP3 para esta película.");
                return;
            }}

            audioPlayer.src = audioUrl;
            gameAudioMode = 'normal';
            audioPlayer.currentTime = 0;

            audioPlayer.play().then(() => {{
                const circle = document.getElementById('audio-btn-circle');
                if (circle) circle.innerText = '⏸️';
                const text = document.getElementById('audio-btn-text');
                if (text) text.innerText = 'PAUSAR CANCIÓN';
                const sub = document.getElementById('audio-btn-sub');
                if (sub) sub.innerText = '🎶 Música Sonando en la App (30s)';
                const badge = document.getElementById('audio-timer-badge');
                if (badge) badge.style.display = 'block';
                iniciarTimerAudio(30);
            }}).catch(err => {{
                console.error("Error al reproducir audio:", err);
                alert("Toca 'ESCUCHAR CANCIÓN' de nuevo para reproducir el audio.");
            }});
        }}

        function pausarAudioMazo() {{
            const audioPlayer = document.getElementById('game-audio') || gameAudio;
            audioPlayer.pause();
            clearInterval(musicTimerInterval);
            gameAudioMode = null;

            const circle = document.getElementById('audio-btn-circle');
            if (circle) circle.innerText = '▶️';
            const text = document.getElementById('audio-btn-text');
            if (text) text.innerText = 'ESCUCHAR CANCIÓN';
            const sub = document.getElementById('audio-btn-sub');
            if (sub) sub.innerText = '🔒 Carátula y Datos Ocultos';
            const badge = document.getElementById('audio-timer-badge');
            if (badge) badge.style.display = 'none';
        }}

        function iniciarTimerAudio(segundos) {{
            clearInterval(musicTimerInterval);
            let rest = segundos;
            const badge = document.getElementById('audio-timer-badge');
            if (badge) badge.innerText = rest + 's';

            const audioPlayer = document.getElementById('game-audio') || gameAudio;

            musicTimerInterval = setInterval(() => {{
                rest--;
                if (badge) badge.innerText = rest + 's';
                if (rest <= 0 || audioPlayer.paused || audioPlayer.ended) {{
                    pausarAudioMazo();
                    if (rest <= 0) {{
                        const text = document.getElementById('audio-btn-text');
                        if (text) text.innerText = '⏰ 30s CUMPLIDOS (VOLVER A ESCUCHAR)';
                    }}
                }}
            }}, 1000);
        }}

        function toggleSecretAudio() {{
            if (!currentCard || !currentCard.data) return;
            const pelicula = currentCard.data;
            const audioPlayer = document.getElementById('game-audio') || gameAudio;

            if (!audioPlayer.paused && gameAudioMode === 'secret') {{
                pausarSecretAudio();
                return;
            }}

            pausarAudioMazo();

            const audioUrl = pelicula.audio_url || '';
            if (!audioUrl) {{
                alert("No se encontró vista previa de audio MP3 para esta película.");
                return;
            }}

            audioPlayer.src = audioUrl;
            gameAudioMode = 'secret';
            audioPlayer.currentTime = 0;

            audioPlayer.play().then(() => {{
                iniciarSecretAudioTimer(30);
            }}).catch(err => {{
                console.error("Error al reproducir audio secreto:", err);
            }});
        }}

        function pausarSecretAudio() {{
            const audioPlayer = document.getElementById('game-audio') || gameAudio;
            audioPlayer.pause();
            clearInterval(secretMusicTimerInterval);
            gameAudioMode = null;

            const btn = document.getElementById('btn-secret-play');
            if (btn) btn.innerText = '▶️ ESCUCHAR CANCIÓN (30s SECRETO)';
        }}

        function iniciarSecretAudioTimer(segundos) {{
            clearInterval(secretMusicTimerInterval);
            let rest = segundos;
            const btn = document.getElementById('btn-secret-play');
            const audioPlayer = document.getElementById('game-audio') || gameAudio;

            secretMusicTimerInterval = setInterval(() => {{
                rest--;
                if (btn) btn.innerText = '⏸️ MÚSICA SECRETA SONANDO (' + rest + 's)... TOCAR PARA PAUSAR';
                if (rest <= 0 || audioPlayer.paused || audioPlayer.ended) {{
                    pausarSecretAudio();
                    if (rest <= 0 && btn) {{
                        btn.innerText = '⏰ ¡30s FINALIZADOS! TOCAR PARA ESCUCHAR DE NUEVO';
                    }}
                }}
            }}, 1000);
        }}

        function accionarVerDesafioPrivado() {{
            document.getElementById('deck-challenge-mask').style.display = 'none';
            document.getElementById('deck-challenge-secret').style.display = 'block';
        }}

        function iniciarTemporizador(segundos) {{
            clearInterval(timerInterval);
            let rest = segundos;
            document.getElementById('timer-count').innerText = rest + 's';

            timerInterval = setInterval(() => {{
                rest--;
                document.getElementById('timer-count').innerText = rest + 's';
                if (rest <= 0) {{
                    clearInterval(timerInterval);
                    document.getElementById('timer-count').innerText = '⏰ ¡TIEMPO!';
                }}
            }}, 1000);
        }}

        function revelarPeliculaMazo() {{
            document.getElementById('deck-normal-mask').style.display = 'none';
            document.getElementById('deck-challenge-secret').style.display = 'none';
            document.getElementById('deck-revealed').style.display = 'block';
        }}

        // --- LÓGICA MODO ESCÁNER QR ---
        function activarCamaraQR() {{
            document.getElementById('scanner-box').style.display = 'block';
            document.getElementById('scanner-player').style.display = 'none';

            if (!html5QrCode) {{
                html5QrCode = new Html5Qrcode("reader");
            }}

            html5QrCode.start(
                {{ facingMode: "environment" }},
                {{ fps: 10, qrbox: 220 }},
                (decodedText) => {{
                    try {{
                        const url = new URL(decodedText);
                        const songId = url.searchParams.get('id') || decodedText.split('/track/')[1];
                        if (songId) {{
                            html5QrCode.stop().then(() => mostrarReproductorQR(songId));
                        }}
                    }} catch(e) {{
                        if (decodedText.includes('/track/')) {{
                            const parts = decodedText.split('/track/');
                            const songId = parts[1].split('?')[0];
                            html5QrCode.stop().then(() => mostrarReproductorQR(songId));
                        }}
                    }}
                }},
                () => {{}}
            ).catch(() => {{}});
        }}

        function mostrarReproductorQR(songId) {{
            document.getElementById('scanner-box').style.display = 'none';
            document.getElementById('scanner-player').style.display = 'block';

            document.getElementById('spotify-target').innerHTML = `
                <iframe src="https://open.spotify.com/embed/track/${{songId}}?utm_source=generator&theme=0" 
                    width="100%" height="80" frameborder="0" allow="autoplay; clipboard-write; encrypted-media"></iframe>
                <div class="spotify-mask-overlay" id="qr-mask" onclick="revelarPeliculaQR()">🍿 Toca aquí para ver la película</div>
            `;
        }}

        function revelarPeliculaQR() {{
            const mask = document.getElementById('qr-mask');
            if (mask) mask.style.display = 'none';
        }}

        // --- LÓGICA MODO CONTEO (MARCADOR DE EQUIPOS) ---
        function renderMarcador() {{
            const list = document.getElementById('scoreboard-list');
            list.innerHTML = '';

            equipos.forEach(e => {{
                const item = document.createElement('div');
                item.className = 'team-card';
                item.innerHTML = `
                    <div class="team-name" onclick="renombrarEquipo(${{e.id}})">${{e.nombre}} ✏️</div>
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <div class="team-score">${{e.puntos}}</div>
                        <div class="score-btns">
                            <button class="btn-score btn-minus" onclick="modificarPuntos(${{e.id}}, -1)">-</button>
                            <button class="btn-score btn-plus" onclick="modificarPuntos(${{e.id}}, 1)">+</button>
                        </div>
                    </div>
                `;
                list.appendChild(item);
            }});

            localStorage.setItem('cinesonoro_equipos', JSON.stringify(equipos));
            verificarGanador();
        }}

        function modificarPuntos(id, delta) {{
            const eq = equipos.find(e => e.id === id);
            if (eq) {{
                eq.puntos = Math.max(0, eq.puntos + delta);
                renderMarcador();
            }}
        }}

        function agregarEquipo() {{
            const num = equipos.length + 1;
            equipos.push({{ id: Date.now(), nombre: 'Equipo ' + num, puntos: 0 }});
            renderMarcador();
        }}

        function renombrarEquipo(id) {{
            const eq = equipos.find(e => e.id === id);
            if (eq) {{
                const nuevo = prompt('Nombre del equipo:', eq.nombre);
                if (nuevo) {{
                    eq.nombre = nuevo.trim();
                    renderMarcador();
                }}
            }}
        }}

        function reiniciarMarcador() {{
            if (confirm('¿Reiniciar puntos a cero?')) {{
                equipos.forEach(e => e.puntos = 0);
                document.getElementById('winner-banner').style.display = 'none';
                renderMarcador();
            }}
        }}

        function verificarGanador() {{
            const ganador = equipos.find(e => e.puntos >= metaPuntos);
            const banner = document.getElementById('winner-banner');
            if (ganador) {{
                document.getElementById('winner-team-name').innerText = ganador.nombre.toUpperCase() + ' (' + metaPuntos + ' PELÍCULAS)';
                banner.style.display = 'block';
            }} else {{
                banner.style.display = 'none';
            }}
        }}
    </script>
</body>
</html>"""

    with open(out_filename, "w", encoding="utf-8") as f:
        f.write(html_content)

def cargar_peliculas_locales():
    if os.path.exists("peliculas.txt"):
        pelis = []
        with open("peliculas.txt", "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = [p.strip() for p in line.split("-")]
                title = parts[0]
                song = parts[1] if len(parts) > 1 else "Banda Sonora Original"
                artist = parts[2] if len(parts) > 2 else "Varios Artistas"
                year = parts[3] if len(parts) > 3 else "2000"
                search_q = f"{title} {song} {artist}".strip()
                pelis.append({
                    "title": title,
                    "song": song,
                    "artist": artist,
                    "year": year,
                    "search_query": search_q,
                    "forbidden_words": [title.split()[0], artist.split()[0], str(year)]
                })
        if len(pelis) >= 80:
            print(f"ℹ️ Se cargaron {len(pelis)} películas personalizadas desde 'peliculas.txt'.")
            return pelis
        else:
            print(f"ℹ️ 'peliculas.txt' contiene solo {len(pelis)} películas. Usando el Catálogo Maestro de 100 Películas para la experiencia completa.")
    
    print("🎬 Cargando Catálogo Maestro de 100 Películas...")
    return CATALOGO_100_PELICULAS

def main():
    print("=" * 75)
    print("      GENERADOR DE MAZO DIGITAL & APP - CINESONORO (V20)")
    print("=" * 75)
    
    config = cargar_config()
    client_id = config.get("client_id", "").strip()
    client_secret = config.get("client_secret", "").strip()
    
    if not client_id or not client_secret:
        print("\n💡 Para buscar canciones reales automáticamente en Spotify:")
        print("1. Crea una App en https://developer.spotify.com/dashboard")
        print("2. Obtén tu Client ID y Client Secret")
        print("3. Guárdalos en 'config_cinesonoro.json' o ingrésalos a continuación.")
        
        try:
            cid_in = input("\n1. Ingresa tu Spotify Client ID (Presiona Enter para omitir): ").strip()
            if cid_in:
                cs_in = input("2. Ingresa tu Spotify Client Secret: ").strip()
                if cs_in:
                    client_id = cid_in
                    client_secret = cs_in
                    guardar_config({"client_id": client_id, "client_secret": client_secret})
                    print("✅ Credenciales guardadas en 'config_cinesonoro.json'.")
        except Exception:
            pass

    peliculas = cargar_peliculas_locales()
    
    if client_id and client_secret:
        peliculas = enriquecer_con_spotify(peliculas, client_id, client_secret)
    else:
        print("\nℹ️ Buscando vistas previas de audio de 30s para las películas...")
    for i, p in enumerate(peliculas, 1):
        if not p.get("audio_url"):
            p["audio_url"] = buscar_preview_itunes(p['title'], p.get('song', ''), p.get('artist', '')) or ""

    print(f"\nSe procesaron {len(peliculas)} películas exitosamente.")
    
    generar_html_cinesonoro(peliculas, "index.html")
    print("✅ ¡Se ha generado exitosamente la aplicación web 'index.html'!")
    
    generar_html_cinesonoro(peliculas, "index_cine.html")
    print("✅ ¡Se ha generado exitosamente la aplicación web 'index_cine.html'!\n")

if __name__ == "__main__":
    main()
