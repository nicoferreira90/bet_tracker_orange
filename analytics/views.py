from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from bets.models import Bet
from .graph_functions import graph_results
from .analytic_functions import running_result, get_average_odds
from django.db.models import Avg, Sum

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

    def post(self, request, *args, **kwargs):
        # Process form data here
        filter_result = request.POST.get('result-filter')  # Retrieve the filter directly
        user_bets = self.get_filtered_bet_list(filter_result=filter_result)  # Pass the filter value
        print("User bets:", user_bets)  # Check the result

        context = self.get_context_data(**kwargs)  # Get existing context

        context['user_bets'] = user_bets

        context['bet_count'] = user_bets.count()

        context['bets_pending_count'] = user_bets.filter(result="Pending").count()

        context['bets_won_count'] = user_bets.filter(result="Win").count()

        context['bets_lost_count'] = user_bets.filter(result="Lose").count()

        context['bets_pushed_count'] = user_bets.filter(result="Push").count()

        if (user_bets.filter(result="Win").count()+user_bets.filter(result="Lose").count()) > 0: # avoid dividing by 0
            context['bet_win_percentage'] = 100*user_bets.filter(result="Win").count()/(user_bets.filter(result="Win").count()+user_bets.filter(result="Lose").count())
        else:
            context['bet_win_percentage'] = 0

        context["average_odds"] = user_bets.aggregate(Avg("odds", default=0))["odds__avg"]

        total_amount_wagered = user_bets.aggregate(total=Sum("stake"))
        context["total_amount_wagered"] = total_amount_wagered['total']

        running_result_list = running_result(user_bets)
        context["net_result"] = running_result_list[-1]

        roi = running_result_list[-1]/total_amount_wagered['total']
        context["roi"] = roi*100

        context['graph'] = self.get_user_result_graph(filter_result)  # Pass filter if needed

        return self.render_to_response(context)
    

    def get_filtered_bet_list(self, filter_result):
        """Return only bets made by the user, and also that meet the filter criteria."""
        bet_set = Bet.objects.filter(bet_owner=self.request.user)

        print("Received filter result:", filter_result)  # Debugging line

        if filter_result and filter_result != 'category-all':
            bet_set = bet_set.filter(result=filter_result)
        
        #print("Filtered bets:", bet_set)  # Debugging line to show the queryset
        return bet_set
    

    def get_user_result_graph(self, filter_result):
        user_bets = self.get_filtered_bet_list(filter_result)  # Pass the filter_result
        running_result_list = running_result(user_bets)
        graph = graph_results(running_result_list)
        return graph
    

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)  
        # No need to call get_filtered_bet_list here without the filter
        return context
    
    