import requests
from django.shortcuts import render
from .forms import MovieSearchForm
from .models import Movie
from decouple import config  # ✅ Import for secure config

def home(request):
    form = MovieSearchForm()
    movie_data = None

    if request.method == 'POST':
        form = MovieSearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            print(f"[DEBUG] Searching for: {title}")

            api_key = config('OMDB_API_KEY')  # 🔐 Securely load from .env
            url = f'http://www.omdbapi.com/?apikey={api_key}&t={title}'

            try:
                response = requests.get(url)
                data = response.json()
                print(f"[DEBUG] API response: {data}")

                if data.get('Response') == 'True':
                    movie_data = {
                        'title': data.get('Title'),
                        'year': data.get('Year'),
                        'poster': data.get('Poster'),
                        'plot': data.get('Plot'),
                    }

                    if not Movie.objects.filter(title=movie_data['title'], year=movie_data['year']).exists():
                        Movie.objects.create(**movie_data)
                else:
                    print(f"[DEBUG] Movie not found: {data.get('Error')}")

            except requests.exceptions.RequestException as e:
                print(f"[ERROR] API request failed: {e}")
        else:
            print("[DEBUG] Form is invalid")
            print(form.errors)

    saved_movies = Movie.objects.all()
    return render(request, 'movies/home.html', {
        'form': form,
        'movie_data': movie_data,
        'saved_movies': saved_movies,
    })
