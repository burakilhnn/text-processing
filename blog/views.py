from django.shortcuts import render,get_object_or_404, redirect
from .models import Pdf
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .read_file import read_pdf
from .filters import PdfFilter

def home(request):
    return render(request,'blog/home.html')

def filter(request):
    pdfs = Pdf.objects.all()
    myFilter = PdfFilter(request.GET, queryset=pdfs)
    pdfs = myFilter.qs
    context = {'pdfs':pdfs,'myFilter':myFilter}
    return render(request, 'blog/filter.html',context)

class UserPostListView(ListView):
    model = Pdf
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Pdf.objects.filter(author=user)

class PostDetailView(DetailView):
    model = Pdf

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Pdf
    template_name = 'blog/upload.html'
    fields = ['file']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin ,UpdateView):
    model = Pdf
    fields = ['title','file']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin ,DeleteView):
    model = Pdf
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False


def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['fupload']
        pdf = Pdf(file=file, author=request.user)
        pdf.save()
        read_pdf(pdf.file.path,pdf.id)
        return redirect('/')
    return render(request, 'blog/upload.html')