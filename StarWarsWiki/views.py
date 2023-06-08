import requests
from django.shortcuts import redirect, render
from django.http import Http404

def index(request):
    return render(request, "index.html")

def error_404(request):
    return render(request, '404.html')

def characters(request):
    url = 'https://akabab.github.io/starwars-api/api/all.json'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        characters = data
    else:
        error_message = 'Une erreur s\'est produite lors de la récupération des personnages de Star Wars.'
        return render(request, 'error.html', {'error_message': error_message})

    # Extraction des affiliations uniques pour le filtrage
    affiliations = set()
    for character in characters:
        affiliations.update(character['affiliations'])

    # Filtrage par affiliation
    affiliation = request.GET.get('affiliation')
    if affiliation:
        characters = [character for character in characters if affiliation in character['affiliations']]

    context = {
        'characters': characters,
        'affiliations': affiliations,
    }
    return render(request, 'characters.html', context)


def get_character_details(character_id):
    url = f'https://akabab.github.io/starwars-api/api/id/{character_id}.json'
    response = requests.get(url)

    if response.status_code == 200:
        character_details = response.json()
        return character_details
    else:
        return None

def character_details(request, character_id):
    # Convertir l'ID du personnage en une chaîne de caractères
    character_id = str(character_id)

    # Récupérer les détails du personnage (vous devrez implémenter cette logique)
    character = get_character_details(character_id)

    context = {'character': character}
    return render(request, 'character_details.html', context)

# def character_details(request, character_id):
#     # Convertir l'ID du personnage en une chaîne de caractères
#     character_id = str(character_id)

#     # Charger le template correspondant à l'ID du personnage
#     template_name = f"{character_id}.html"
#     try:
#         return render(request, template_name, {'character_id': character_id})
#     except:
#         # Récupérer les détails du personnage (vous devrez implémenter cette logique)
#         character = get_character_details(character_id)

#         if not character:
#             return render(request, 'error.html', status=404)

#         context = {'character': character}
#         return render(request, 'id/character_details.html', context)
    
def films(request):
    url = 'https://swapi.dev/api/films/'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        films = data['results']
    else:
        error_message = 'Une erreur s\'est produite lors de la récupération des films de Star Wars.'
        return render(request, 'error.html', {'error_message': error_message})

    context = {'films': films}
    return render(request, 'films.html', context)

def planets(request):
    planets = []
    next_url = 'https://swapi.dev/api/planets/'

    while next_url:
        response = requests.get(next_url)

        if response.status_code == 200:
            data = response.json()
            planets += data['results']
            next_url = data['next']
        else:
            error_message = 'Une erreur s\'est produite lors de la récupération des planets de Star Wars.'
            return render(request, 'error.html', {'error_message': error_message})
        
    context = {'planets': planets}
    return render(request, 'planets.html', context)

def species(request):
    species = []
    next_url = 'https://swapi.dev/api/species/'

    while next_url:
        response = requests.get(next_url)

        if response.status_code == 200:
            data = response.json()
            species += data['results']
            next_url = data['next']
        else:
            error_message = 'Une erreur s\'est produite lors de la récupération des espèces de Star Wars.'
            return render(request, 'error.html', {'error_message': error_message})
    
    for specie in species:
        homeworld_url = specie['homeworld']
        if homeworld_url:
            homeworld_response = requests.get(homeworld_url)
        
            if homeworld_response.status_code == 200:
                homeworld_data = homeworld_response.json()
                specie['homeworld'] = homeworld_data['name']
            else:
                specie['homeworld'] = 'Inconnu'
        else:
            specie['homeworld'] = 'Inconnu'
        
    context = {'species': species}
    return render(request, 'species.html', context)

def starships_vehicles(request):
    starships = []
    next_url_starships = 'https://swapi.dev/api/starships/'
    vehicles = []
    next_url_vehicles = 'https://swapi.dev/api/vehicles/'

    try:
        while next_url_starships:
            response = requests.get(next_url_starships)
            response.raise_for_status()

            data = response.json()
            starships += data['results']
            next_url_starships = data['next']
        
        while next_url_vehicles:
            response = requests.get(next_url_vehicles)
            response.raise_for_status()

            data = response.json()
            vehicles += data['results']
            next_url_vehicles = data['next']
    except requests.exceptions.RequestException as e:
        error_message = 'Une erreur s\'est produite lors de la récupération des données de Star Wars.'
        return render(request, 'error.html', {'error_message': error_message, 'exception_message': str(e)})

    context = {'starships': starships, 'vehicles': vehicles}
    return render(request, 'starships_vehicles.html', context)

