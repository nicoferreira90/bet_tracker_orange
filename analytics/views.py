from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from bets.models import Bet
from .graph_functions import graph_results
from .analytic_functions import running_result

class AnalyticsPageView(LoginRequiredMixin, TemplateView):
    template_name = "analytics/analytics_page.html"
    login_url = "/users/login/"

    def get_context_data(self):
        context = super().get_context_data()
        context["user_bets"] = Bet.objects.filter(bet_owner=self.request.user)
        return context
    
class AnalyticsWithResultsView(LoginRequiredMixin, TemplateView):
    template_name = "analytics/analytics_with_results.html"
    login_url = "/users/login/"

    def get_user_result_graph(self):
        user_bets = Bet.objects.filter(bet_owner=self.request.user)
        running_result_list = running_result(user_bets)
        graph = graph_results(running_result_list)
        return graph

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)  
        context["user_bets"] = Bet.objects.filter(bet_owner=self.request.user)
        context["graph"] = self.get_user_result_graph()
        return context
    
    