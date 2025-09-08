from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import requests

# def home(request):
#     return HttpResponse("Hello from AI Art Explorer!")

# def search_art(request):
#     return HttpResponse("Search Art Page")

# # Create your views here.
def home(request):
    return render(request, 'gallery/home.html')

def search_art(request):
    query = request.GET.get('query')
    artworks = []

    if query:
        # Search endpoint
        search_url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={query}"
        response = requests.get(search_url, params={"q": query}).json()

        object_ids = response.get("objectIDs", [])[:20]

        for obj_id in object_ids:
            obj_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}"
            art_data = requests.get(obj_url).json()

            image_url = art_data.get("primaryImageSmall")
            if not image_url:
                continue

            artworks.append({
                "title": art_data.get("title"),
                "artist": art_data.get("artistDisplayName"),
                "image": art_data.get("primaryImageSmall"),
                "year": art_data.get("objectDate"),
            })

    return render(request, "gallery/results.html", {"artworks": artworks, "query": query})