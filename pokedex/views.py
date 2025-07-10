from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
import urllib.request
import json
from .models import pokemon
from .models import type
from django.conf import settings

Root = settings.BASE_DIR

def home(request):
    return render(request, 'home.html')

def filldb():
    def initializetypes():
        """Cria os tipos na DB na ordem certa"""
        typelist = ['Normal', 'Fire', 'Water', 'Electric', 'Grass', 
                    'Ice', 'Fighting', 'Poison', 'Ground', 'Flying', 
                    'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 
                    'Dark', 'Steel', 'Fairy']
        typecolors = ['#9f9e9f', '#e62829', '#2980ef', '#fac000', '#3fa129',
                      '#3dcef3', '#ff8000', '#9a3bdd', '#975019', '#81b9ef',
                      '#ef4179', '#91a119', '#afa981', '#704170', '#5060de',
                      '#624d4e', '#60a2b8', '#f070f0',]
        
        for i in range(len(typelist)):
            type.objects.get_or_create(type= typelist[i], color=typecolors[i])

    def gettypes(file):
        """Escaneia o arquivo json, procurando por 2 tipos pelo slot
          Return Example: 
    "('Fire','Water')" """
        type1 = None
        type2 = None

        for type in file["types"]:
            if type["slot"] == 1:
                type1 = type["type"]["name"]
            elif type["slot"] == 2:
                type2 = type["type"]["name"]
        return type1, type2
    
    def getdesc(index):
        """Obtém a descrição do pokemon, requisitando e tratando um arquivo json à PokeAPI"""
        url = f"https://pokeapi.co/api/v2/pokemon-species/{index}"
        request = urllib.request.Request(url)
        request.add_header('User-Agent', 'Bruxo')

        with urllib.request.urlopen(request) as species:
            file = json.loads(species.read().decode())

        for entry in file["flavor_text_entries"]:
            if entry["language"]["name"] == "en":
                desc = entry["flavor_text"].replace("\n", " ").replace("\f", " ")
                return desc
        
        return f'No avaliable description for {index}.'
    
    def getsprite(index):
        try:
            urllib.request.urlretrieve(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{index}.png', f'{Root}/static/images/PokemonIcons/{index}.png')
            urllib.request.urlretrieve(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{index}.png', f'{Root}/static/images/PokemonIcons/Shiny/{index}.png')

        except Exception as e:
            print(f'Erro ao baixar sprite: {e}')
        
    def dbadd(entry):
        """Adiciona os pokemons da transcrição de uma resposta em JSON do PokeAPI na DB, se não existirem.
        Args:
            entry: Transcrição do arquivo JSON com as informações necessárias."""
        try: 
            type2 = type.objects.get(type=entry['pkmn_type2'])
        except type.DoesNotExist: 
            type2 = None

        try:
            pokemon.objects.get_or_create(
                pkmn_id = entry['pkmn_id'],
                pkmn_name = entry['pkmn_name'],
                pkmn_height = entry['pkmn_height'],
                pkmn_weight = entry['pkmn_weight'],
                pkmn_type1 = type.objects.get(type=entry['pkmn_type1']),
                pkmn_type2 = type2,
                pkmn_desc  = entry['pkmn_desc'])

        except:
            reply = f'Erro ao adicionar ({index}){entry['pkmn_name'].capitalize()} ao Banco de Dados'
            print(reply)
        else:
            reply = f'({index}){entry['pkmn_name'].capitalize()} adicionado com sucesso!'
            print(reply)
        
    initializetypes()
    
    for i in range(1025):
        index = i + 1
        
        if pokemon.objects.filter(pkmn_id=index).exists(): #Vê se tem
            continue

        else: #Não tendo
            try: #tenta fazer
                url = urllib.request.Request(f'https://pokeapi.co/api/v2/pokemon/{index}') #requisição http
                url.add_header('User-Agent', 'Bruxo')  #pokeapi bloqueia requests sem User-Agent
                source = urllib.request.urlopen(url).read()
                file = json.loads(source) #transcreve source(arquivo json com infos do pokeapi para um dict

                entry = { #Dict com informações preparadas e formatadas
                    'pkmn_id': int(file['id']),
                    'pkmn_name': str(file['name']),
                    'pkmn_height': int(file['height']),
                    'pkmn_weight': int(file['weight']),
                    'pkmn_type1': str(gettypes(file)[0]).capitalize(),
                    'pkmn_type2': str(gettypes(file)[1]).capitalize(),
                    'pkmn_desc': str(getdesc(index)),
                    }

                dbadd(entry)
                getsprite(index)

            except urllib.error.HTTPError as e: #Não dando pra fazer, manda a real
                print(f'Erro({e}) com ({index}){entry['pkmn_name']}')
                continue
            except urllib.error.URLError:
                print(f'Falha ao acessar a API')
            else:
                continue


def pokedex(request):
    #Preencher a DB, caso esteja vazia(substituível por exibir diretamente os dados recebidos pela API)
    if len(pokemon.objects.all()) < 1025:      # 1025 = Número de pokémons atualmente
        filldb()  
    else:
        #barra de pesquisa
        q = request.GET.get('q')
        if q:
            pokemons = pokemon.objects.filter(
                Q(pkmn_id__contains = q) |
                Q(pkmn_name__icontains= q)
            )
        else:
            pokemons = pokemon.objects.all()
    
    context = {
        'pokemons': pokemons, 
        'q': q, 
        'pokemon_count': pokemons.count()
        }
    
    return render(request, 'pokedex.html', context)


def pokemon_entry(request, identifier):
    if identifier.isdigit():
        pokemon_entry = get_object_or_404(pokemon, pkmn_id=int(identifier))
    else:
        identifier = str(identifier).replace(' ', '-')
        pokemon_entry = get_object_or_404(pokemon, pkmn_name__iexact=identifier)
        
    context = {
        'ShowID' : pokemon_entry.pkmn_id,
        'ShowName' : str(pokemon_entry.pkmn_name).capitalize(),
        'ShowHeight' : f'{int(pokemon_entry.pkmn_height) / 10} m' if pokemon_entry.pkmn_height > 10 else f'{int(pokemon_entry.pkmn_height * 10)} cm',
        'ShowWeight' : f'{int(pokemon_entry.pkmn_weight) / 10} Kg' if pokemon_entry.pkmn_weight > 100 else f'{int(pokemon_entry.pkmn_weight * 10)} g',
        'Type1' : pokemon_entry.pkmn_type1,
        'Type2' : pokemon_entry.pkmn_type2,
        'Description': pokemon_entry.pkmn_desc
    }
    return render(request, 'pkmn_entry.html', context)
