from django.shortcuts import render
from django.http import HttpResponse
from .models import Book,BookInstance
from django.views.generic import CreateView,DetailView,ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

def index(request):
  num_books = Book.objects.all().count()
  num_instance = BookInstance.objects.all().count()
  num_instances_available = BookInstance.objects.filter(status__exact='a').count()

  context = {
    'num_books':num_books,
    'num_instance':num_instance,
    'num_instances_available':num_instances_available
  }
  
  return render(request,'catalog/index.html',context=context)

class BookCreate(LoginRequiredMixin,CreateView):
  model = Book
  fields = '__all__'

class BookDetail(DetailView):
  model = Book

@login_required
def my_view(request):
  return render(request,'catalog/my_view.html')

class SignUpForm(CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy('login')
  template_name = "catalog/signup.html"

class ProfileView(ListView):
  model = BookInstance
  paginate_by = 5
  template_name = 'catalog/profile.html'

  def get_queryset(self):
    return BookInstance.objects.filter(borrower=self.request.user).all()