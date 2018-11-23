from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.post_list, name='post_list'),
	url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
	url(r'^post/new/$', views.post_new, name='post_new'),
	url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
	url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
	url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
	url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
	url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
	url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
	url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^blockchain_start/$', views.blockchain_start, name='blockchain_start'),
	url(r'^blockchain_start/login', views.ethereum_login, name='ethereum_login'),
	url(r'^blockchain_start/create/$', views.contract_create, name='contract_create'),
	url(r'^blockchain_start/ready/$', views.contract_ready, name='contract_ready'),
	url(r'^blockchain_start/sell/$', views.contract_sell, name='contract_sell'),
	url(r'^blockchain_start/buy/$', views.contract_buy, name='contract_buy'),
	url(r'^blockchain_start/cheapest/$', views.cheapest, name='cheapest'),
	url(r'^blockchain_start/expensive/$', views.expensive, name='expensive'),
	url(r'^blockchain_start/matching/$', views.matching, name='matching'),
]
