from models import Podcast

def list_podcasts(request):
    # add a list of all podcasts to every request
    podcasts = Podcast.objects.order_by('name')

    return {'podcasts': podcasts}
