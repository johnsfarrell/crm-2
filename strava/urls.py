from strava.api.helpers.paths import generate_path
from strava.views import VIEWS

urlpatterns = [generate_path(name, method) for name, method in VIEWS.items()]
