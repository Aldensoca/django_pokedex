# Pokédex Django Web App

A **Pokédex web application** built with Django. 
This project dynamically fetches Pokémon data from [PokeAPI](https://pokeapi.co), stores it in a local database, and provides a clean interface to browse and search all Pokémon.

## How to Run Locally

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/pokedex-django.git
cd pokedex-django
```
2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```
3. **Install dependencies**
```bash
pip install -r requirements.txt
```
4. **Run the development server**
```bash
python manage.py runserver
```
6. **Open your browser**
```bash
http://127.0.0.1:8000/
```
**Note**: On first visit to the Pokédex page, the app will automatically fetch and store all Pokémon data from PokeAPI. This process can take a few minutes.

## Known Issues
- Initial data fetching may be slow.
- No pagination yet for the Pokédex grid.
- No visual feedback for the initial data fetching.

## Roadmap Ideas
- Add pagination.
- Show shiny sprites on toggle.
- Type filtering.
- Improve error messages in the UI.
- Docker container for easy setup.

## Contributing
Pull requests are welcome! Feel free to fork the repo and submit PRs.
