from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.urls import reverse_lazy
from .models import Tag
from .forms import TagForm
from bets.models import Bet

class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = "tags/tag_list.html"
    login_url = "/users/login/"

    def get_queryset(self):
        """Override the get_queryset method so that BetHistoryView only displays bets made by the current user."""
        return Tag.objects.filter(tag_owner=self.request.user)

class NewTagView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = "tags/new_tag.html"
    login_url = "/users/login/"
    success_url = reverse_lazy("tag_list")

    def form_valid(self, form):
        # Set the owner of the bet to the current user
        form.instance.tag_owner = self.request.user
        return super().form_valid(form)
    
    # try this...
    def get_form(self, *args, **kwargs):
        # Get the form and modify the queryset for the associated_bets field
        form = super().get_form(*args, **kwargs)
        form.fields['associated_bets'].queryset = Bet.objects.filter(bet_owner=self.request.user)
        return form

        
class UpdateTagView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = "tags/update_tag.html"
    login_url = "/users/login/"
    success_url = reverse_lazy("tag_list")

    def test_func(self):
        """Checks if bet owner is the same as the current user."""
        obj = self.get_object()
        return obj.tag_owner == self.request.user
    
    def get_form(self, *args, **kwargs):
        # Get the form and modify the queryset for the associated_bets field
        form = super().get_form(*args, **kwargs)
        form.fields['associated_bets'].queryset = Bet.objects.filter(bet_owner=self.request.user)
        return form

class DeleteTagView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tag
    template_name = "tags/delete_tag.html"
    success_url = reverse_lazy("tag_list")
    login_url = login_url = "/users/login/"

    def test_func(self):
        """Checks if bet owner is the same as the current user."""
        obj = self.get_object()
        return obj.tag_owner == self.request.user

    
class BetTagPageView(LoginRequiredMixin, UserPassesTestMixin, DetailView):

    model = Bet
    template_name = "tags/bet_tag_page.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)

        if request.POST.get('tag-select'):
            chosen_tag = Tag.objects.get(label=request.POST.get('tag-select'))
            chosen_tag.associated_bets.add(self.object)
        else:
            removed_tag = Tag.objects.get(id=request.POST.get('tag-id'))
            removed_tag.associated_bets.remove(self.object)
        context["bet"] = self.get_object()

        return self.render_to_response(context)
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)

        return self.render_to_response(context)


    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)  
        context["bet"] = self.get_object()
        print("debug line")
        print(context["bet"])
        context["inactive_tags"] = Tag.objects.filter(tag_owner=self.request.user).exclude(associated_bets=context["bet"]).distinct()
        print(context["inactive_tags"])
        context["pk"] = self.get_object().pk
        print(context["pk"])
        return context
    

    def test_func(self):
        """Checks if bet owner is the same as the current user."""
        obj = self.get_object()
        return obj.bet_owner == self.request.user

class BetNewTagView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = "tags/new_tag.html"
    login_url = "/users/login/"
    success_url = reverse_lazy("bet_tag_page")

    def get_success_url(self):
        # Get the pk of the bet from the GET parameters
        bet_pk = self.request.GET.get('bet_pk')
        return reverse_lazy("bet_tag_page", kwargs={'pk': bet_pk})

    def form_valid(self, form):
        # Set the owner of the bet to the current user
        form.instance.tag_owner = self.request.user
        return super().form_valid(form)
    
    def get_form(self, *args, **kwargs):
        # Get the form and modify the queryset for the associated_bets field
        form = super().get_form(*args, **kwargs)
        form.fields['associated_bets'].queryset = Bet.objects.filter(bet_owner=self.request.user)
        return form