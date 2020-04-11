from django.shortcuts import render
from .models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
# Create your views here.
import json
import requests

def index(request):
	return render(request,'scraper/index.html')



class PostListView(LoginRequiredMixin,ListView):
	model = Post
	template_name = 'scraper/home.html'
	context_object_name = 'posts'

class PostDetailView(LoginRequiredMixin,DetailView):
	model = Post

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Post
	success_url = reverse_lazy('post-list')
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False



class PostCreateView(LoginRequiredMixin,CreateView):
	model = Post
	fields = ['title']

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model = Post
	fields = ['title']

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


def about(request):
	return render(request,'about.html')