from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
from .views import (
    CourseList,
    CourseDetail,
    CourseCreation,
    CourseUpdate,
    CourseDelete
)
urlpatterns = [
    url(r'^$',views.principal, name='home'),
    url(r'^CourseList/', login_required(CourseList.as_view()), name='list'),
    url(r'^(?P<pk>\d+)', login_required(CourseDetail.as_view()), name='detail'),
    url(r'^Course/new',views.playera,name="playera"),
    url(r'^pdf',views.pdf,name="pdf"),
    url(r'^grafica',views.grafica,name="grafica"),
    url(r'^editar/(?P<pk>\d+)', login_required(CourseUpdate.as_view()), name='edit'),
    url(r'^borrar/(?P<pk>\d+)', login_required(CourseDelete.as_view()), name='delete'),
]