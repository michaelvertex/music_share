from django.shortcuts import render
from django.http import HttpResponse
import requests


from .secrets import discogs_key, discogs_secret

from .models import Posts


def index(request):
    posts = Posts.objects.all()[:10]
    context = {
        'title': 'Latest Posts',
        'posts': posts
    }
    return render(request, 'posts/index.html', context)


def details(request, id):
    post = Posts.objects.get(id=id)
    context = {
        'post': post
    }

    artist = 'nirvana'
    url = f'https://api.discogs.com/database/search?type=artist&q={artist}&key={discogs_key}&secret={discogs_secret}'
    r = requests.get(url)
    artist_id = r.json()['results'][0]['id']

    url2 = f'https://api.discogs.com/artists/{artist_id}/releases?sort=year&sort_order=desc'
    r2 = requests.get(url2)
    print(r2.json())

    for release in r2.json()['releases']:
        print(str(release['year']) + ' ' + release['title'])



    # extract relevant data from the response
    # pass it to the template to be rendered



    return render(request, 'posts/details.html', context)
