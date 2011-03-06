from models import Podcast
from utils import compare_esperanto_strings

def list_podcasts(request):
    # add a list of all podcasts to every request
    # sorted alphabetically according to the Esperanto alphabet
    podcasts = Podcast.objects.all()
    podcasts = sorted(podcasts, cmp=compare_esperanto_strings,
                      key=lambda p:p.name)

    return {'podcasts': podcasts}
