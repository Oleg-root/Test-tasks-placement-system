from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Vacancy, Solution, Response, Notification
from .forms import UploadFileForm, ResponseForm


# def home(request):
#     context = {
#         'vacancies': Vacancy.objects.all()
#     }
#     return render(request, 'test_app/home.html', context) # still returns HttpResponse

def about(request):
    return render(request, 'test_app/about.html', {'title': 'About'})

# @login_required
# def solutions_for_user(request):
#     solutions = Solution.objects.filter(receiver=request.user.username)
#
#     return render(request, 'test_app/received_solutions.html', {'solutions': solutions})

def upload_file(request, pk):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            p = Vacancy.objects.get(id=pk)
            solution = Solution.objects.create(author=request.user,
                                               receiver=p.author.username,
                                               associated_vacancy=p,
                                               file=request.FILES['file'],
                                               )
            solution.save()
            messages.success(request, f'Solution for vacancy ({p.title}) uploaded!')
            return redirect('home')
    else:
        if request.user.is_authenticated:
            if request.user == Vacancy.objects.get(id=pk).author:
                return redirect('home')

            form = UploadFileForm()
        else:
            messages.warning(request, f'You need to login in order to view this page.')

            return redirect('/login/?next=/upload/')

    return render(request, 'users/upload.html', {'form': form})

def create_response(request, pk):
    if request.method == "POST":
        form = ResponseForm(request.POST)
        if form.is_valid():
            s = Solution.objects.get(id=pk)
            response = Response.objects.create(author=request.user,
                                               receiver=s.author.username,
                                               associated_solution=s,
                                               content=form.cleaned_data.get('content'))
            response.save()
            s.responded = True
            s.save()
            messages.success(request, f'Response uploaded!')
            return redirect('home')
    else:
        if request.user.is_authenticated:
            if request.user == Solution.objects.get(id=pk).author:
                return redirect('home')

            form = ResponseForm()
        else:
            messages.warning(request, f'You need to login in order to view this page.')

            return redirect('/login/?next=/response/')

    return render(request, 'test_app/respond.html', {'form': form})


class SolutionListView(LoginRequiredMixin, ListView):
    model = Solution
    template_name = 'test_app/received_solutions.html'
    context_object_name = 'solutions'
    paginate_by = 3

    def get_queryset(self):
        return Solution.objects.filter(receiver=self.request.user).order_by('-date_uploaded')

class ResponseListView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'test_app/received_responses.html'
    context_object_name = 'responses'
    paginate_by = 3

    def get_queryset(self):
        return Response.objects.filter(receiver=self.request.user).order_by('-date_created')

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'test_app/notifications.html'
    context_object_name = 'notifications'
    paginate_by = 5

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user).order_by('-date_created')

class VacancyListView(ListView):
    model = Vacancy
    template_name = 'test_app/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'vacancies'
    ordering = ['-date_posted']
    paginate_by = 3

class UserVacancyListView(ListView):
    model = Vacancy
    template_name = 'test_app/user_vacancies.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'vacancies'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Vacancy.objects.filter(author=user).order_by('-date_posted')


class VacancyDetailView(DetailView):
    model = Vacancy

class VacancyCreateView(LoginRequiredMixin, CreateView):
    model = Vacancy
    fields = ['title', 'content', 'task']


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class VacancyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vacancy
    fields = ['title', 'content', 'task']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        vacancy = self.get_object()  # getting the current vacancy(which we're trying to update)
        if self.request.user == vacancy.author:
            return True
        else:
            return False


class VacancyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Vacancy
    success_url = '/'

    def test_func(self):
        vacancy = self.get_object()
        if self.request.user == vacancy.author:
            return True
        else:
            return False

class SolutionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Solution
    success_url = '/received_solutions/'


    def test_func(self):
        s = self.get_object()
        if self.request.user.username == s.receiver:
            return True
        else:
            return False

class ResponseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Response
    success_url = '/received_responses/'


    def test_func(self):
        r = self.get_object()
        if self.request.user.username == r.receiver:
            return True
        else:
            return False

class NotificationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Notification
    success_url = '/notifications/'


    def test_func(self):
        n = self.get_object()
        if self.request.user == n.receiver:
            return True
        else:
            return False
