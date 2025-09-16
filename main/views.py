import json
import random
from datetime import datetime
from pathlib import Path
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from .forms import PlaceForm

DATA_FILE = Path(__file__).resolve().parent / "data.json"

def load_places():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_places(places):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(places, f, ensure_ascii=False, indent=2)

def index(request):
    preview = None
    if "random_preview" in request.GET:
        preview = _choose_weighted(load_places())
    return render(request, "main/index.html", {"preview": preview})

def place_list(request):
    places = load_places()
    return render(request, "main/place_list.html", {"places": places})

def place_detail(request, idx):
    places = load_places()
    try:
        place = places[idx]
    except IndexError:
        return redirect("place_list")
    return render(request, "main/place_detail.html", {"place": place, "idx": idx})

def add_place(request):
    if request.method == "POST":
        form = PlaceForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            places = load_places()
            new_place = {
                "name": data["name"],
                "description": data["description"],
                "type": data["type"],
                "location": data["location"],
                "rating": data["rating"],
                "created": datetime.now().strftime("%Y-%m-%d"),
                "photo": "main/static/img/okak.jpg",
            }
            places.append(new_place)
            save_places(places)
            return redirect("place_list")
    else:
        form = PlaceForm()
    return render(request, "main/add_place.html", {"form": form})

def _choose_weighted(places):
    if not places:
        return None
    weights = [p.get("rating", 1) for p in places]
    return random.choices(places, weights=weights, k=1)[0]

def random_place(request):
    places = load_places()
    if not places:
        return HttpResponseBadRequest("No places available")
    chosen = _choose_weighted(places)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"place": chosen})
    return redirect("/?random_preview=1")
