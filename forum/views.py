from django.shortcuts import render, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Topic, Post, Comment
from .forms import CreateCommentForm, CreateTopicForm
from django.contrib.auth.models import User


class TopicListView(ListView):
    model = Topic
    template_name = 'forum/innovforum.html'  
    context_object_name = 'topics'

class TopicDetailView(DetailView):
    model = Topic

    def get_context_data(self, **kwargs):
        context = super(TopicDetailView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(topic=self.kwargs.get('pk'))
        return context


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    fields = ['Τίτλος', 'Περιγραφή']
    

    def form_valid(self, form):
        form.instance.Συγγραφέας = self.request.user
        return super().form_valid(form)
    
    def submit_post(self):
        topic= Topic(Συγγραφέας= self.request.user)
        return topic

class TopicUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Topic
    fields = ['Τίτλος', 'Περιγραφή']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        topic = self.get_object()
        if self.request.user == topic.Συγγραφέας:
            return True
        return False

        
class TopicDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Topic
    success_url = 'http://127.0.0.1:8000/forum/'

    def test_func(self):
        topic = self.get_object()
        if self.request.user == topic.Συγγραφέας:
            return True
        return False   
 


class PostDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Post
    form_class = CreateCommentForm

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.kwargs.get('pk'))
        context['form'] = CreateCommentForm
        
        return context

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        user= User(request.user.id)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        form.instance.Συγγραφέας = self.request.user
        form.instance.topic = Topic.objects.get(pk=self.kwargs['pk'])
        return super(PostDetailView, self).form_valid(form)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['Τίτλος', 'Περιεχόμενο']

    def form_valid(self, form):
        form.instance.Συγγραφέας = self.request.user
        form.instance.topic = Topic.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['Τίτλος', 'Περιεχόμενο']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.Συγγραφέας:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = 'http://127.0.0.1:8000/forum/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.Συγγραφέας:
            return True
        return False    

