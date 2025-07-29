from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.db.models import Q
from todo.models import Todo

class TodoListView(LoginRequiredMixin, ListView):
    queryset = Todo.objects.all()
    template_name = 'todo/todo_list.html'
    paginate_by = 10
    ordering = ('-created_at',)

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        if self.request.user.is_superuser:
            queryset = super().get_queryset()

        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return queryset

class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = 'todo/todo_info.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404('해당 Todo 조회 권한이 없습니다.')
        return obj

    def get_context_data(self, **kwargs):
        # context = {'todo': self.object.__dict__}
        context = super().get_context_data(**kwargs)
        todo_dict = self.object.__dict__.copy()
        todo_dict['user'] = self.object.user
        context['todo'] = todo_dict
        return context

class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ['title', 'description', 'start_date', 'end_date']
    template_name = 'todo/todo_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.id})

class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ['title', 'description', 'start_date', 'end_date', 'is_completed']
    template_name = 'todo/todo_update.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404('해당 Todo 수정 권한이 없습니다.')
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.id})

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404('해당 Todo 삭제 권한이 없습니다.')
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_list')
