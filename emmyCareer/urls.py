from django.conf.urls import url
from django.contrib.auth.views import login

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^resumeHelper/$', views.resumeHelper, name='resumeHelper'),
    url(r'^onlineCounselling/$', views.onlineCounselling, name='onlineCounselling'),
    url(r'^onlineCounselling/payment/$', views.precounsellingPayform, name='precounsellingPayment'),
    url(r'^resumeHelper/detail/$', views.resumeReviewPayform, name='resumeReviewPayment'),
    url(r'^resumeHelper/detailwzo/$', views.resumeReviewPayformWithoutSign, name='resumeReviewPaymentWithoutSign'),
    url(r'^resumeHelper/detailwzo2/$', views.resumeReviewPayformWithoutSign2, name='resumeReviewPaymentWithoutSign2'),
    url(r'^inquiry/$', views.inquiry, name='inquiry'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup/success/$', views.signup_success, name='signup_success'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^signout/$', views.signout, name='signout'),
    url(r'^userhome/$', views.userhome, name='userhome'),
    url(r'^sample/$', views.sample, name='sample'),
    #url(r'^tips/(?P<id>[a-zA-Z0-9]+)/$', views.tipDetail, name='tipDetail'),
]
