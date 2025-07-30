from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.db.models import Q
from todo.models import Todo, Comment
from django.core.paginator import Paginator
from todo.forms import CommentForm, TodoForm, TodoUpdateForm
from django.contrib import messages

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

    def get_queryset(self):
        # queryset = Todo.objects.all().prefetch_related('comments', 'comments__user')
        return super().get_queryset().select_related('user').prefetch_related('comments__user')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404('해당 Todo 조회 권한이 없습니다.')
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['todo_dict'] = self.object.__dict__
        context['comment_form'] = CommentForm()

        comments = self.object.comments.all().order_by('-created_at')
        paginator = Paginator(comments, 5)
        page_number = self.request.GET.get('page', '1')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        return context

class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todo/todo_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        messages.success(self.request, '할 일이 생성되었습니다.')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.id})

class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    form_class = TodoUpdateForm
    template_name = 'todo/todo_update.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404('해당 Todo 수정 권한이 없습니다.')
        return obj

    def form_valid(self, form):
        messages.success(self.request, '할 일이 수정되었습니다.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.id})

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404('해당 Todo 삭제 권한이 없습니다.')
        return obj

    def form_valid(self, form):
        self.object.delete()
        messages.success(self.request, '할 일이 삭제되었습니다.')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('cbv_todo_list')

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['message']
    pk_url_kwarg = 'todo_id'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.todo = Todo.objects.get(id=self.kwargs['todo_id'])
        self.object.save()
        messages.success(self.request, '댓글이 추가되었습니다.')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.kwargs['todo_id']})

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['message']

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404('해당 댓글 수정 권한이 없습니다.')
        return obj

    def form_valid(self, form):
        messages.success(self.request, '댓글이 수정되었습니다.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.todo_id})

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404('해당 댓글 삭제 권한이 없습니다.')
        return obj

    def form_valid(self, form):
        self.object.delete()
        messages.success(self.request, '댓글이 삭제되었습니다.')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        # return reverse_lazy('cbv_todo_list') = 기본 요구사항
        # 댓글 삭제 후 Todo 상세 페이지로 돌아가며 댓글 섹션으로 스크롤
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.todo.id}) + '#comment_wrapper'