from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import json
import requests
# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=100)

	data_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User,on_delete=models.CASCADE)


	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail',kwargs={'pk':self.pk})

	def agenda(self):
		tag = str(self.title)
		url = 'https://www.instagram.com/explore/tags/'+tag+'/?__a=1'
		ig_data_dict = requests.get(url)
		hello = []
		if ig_data_dict is not None:
			ig_data_dict = ig_data_dict.json()
			graphy = ig_data_dict.get('graphql',None)
			data = graphy.get('hashtag',None)
			# top_post = data.get('edge_hashtag_to_top_posts',None)
			top_post = data.get('edge_hashtag_to_media',None)
			top_post = top_post.get('edges')
			for post in top_post:
				para = post.get('node')
				url_pro = 'https://www.instagram.com/p/'+para.get('shortcode')+'/?__a=1'
				user = requests.get(url_pro)
				if user is not None:
					user_data = user.json()
					pics = user_data.get('graphql',None)
					data = pics.get('shortcode_media',None)
					data = data.get('owner',None)
					data = data.get('username',None)
					hello.append(data)
		else:
			hello = 'opps wrong'
		return hello