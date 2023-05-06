from django.urls import path
from news import views
urlpatterns = [
    #path('scrape/', scrape, name="scrape"),
    #path('', news_list, name="home"),
    #path('', views.get_all, name='home'),
    path('', views.index, name='home'),
    #path('category/<str:category>', views.get_all, name='get_all'),
    #path('search', views.search, name='search'),
    #path('sync_now', views.sync_now, name='sync_now'),
    #path('api/<str:category>', views.GetDataAPI.as_view(), name='api'),
    #path('search/<str:query>', views.SearchAPI.as_view(), name='search_api'),


]