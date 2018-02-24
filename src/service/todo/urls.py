from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

#from diary.views import DiaryViewSet
from users.views import CreateUserView, UserViewSet

router = DefaultRouter()
# Front End URLs

urlpatterns = [
# Commented Django admin url. Uncomment if needed.
#    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),

# Users API URLs
#    url(r'^users/$', UserViewSet.as_view()),
    url(r'^users/authenticate/$', obtain_jwt_token),
    url(r'^users/register/$', CreateUserView.as_view()),
#    url(r'^users/expire/$',),

# Diary API URLs
#    url(r'^diary/$', DiaryViewSet),
#    url(r'^diary/create/$', ),
#    url(r'^users/delete/$', ),
#    url(r'^users/permission/$', ),

# Meta API URLs
#    url(r'^meta/heartbeat/$', ),
#    url(r'^meta/members/$', ),

]
