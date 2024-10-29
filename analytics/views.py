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
        filter_result = request.POST.get('result-filter')  # Retrieve the result filter directly

        filter_date_option = request.POST.get('dateOption') # Retrieve the date filter directly

        if filter_date_option == 'custom': # Retrieve the custom date range from the form, only if the option 'custom' option is selected

            filter_date_start = request.POST.get('filterDateStart')
            print("date start", filter_date_start)

            filter_date_end = request.POST.get('filterDateEnd')
            print("date end", filter_date_end)
        else:
            filter_date_start = None
            filter_date_end = None

        user_bets = self.get_filtered_bet_list(filter_result=filter_result,
                                               filter_date_option=filter_date_option, 
                                               filter_date_start=filter_date_start, 
                                               filter_date_end = filter_date_end) 

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

        if total_amount_wagered['total'] == 0:
            roi = None
            print("roi", roi)
        else:
            roi = running_result_list[-1]/total_amount_wagered['total']
            context["roi"] = roi*100
            print("roi", roi)

        context['graph'] = self.get_user_result_graph(user_bets)  # Pass filter if needed

        return self.render_to_response(context)
    

    def get_filtered_bet_list(self, filter_result, filter_date_option=None, filter_date_start=None, filter_date_end=None):
        """Return only bets made by the user, and also that meet the filter criteria."""
        bet_set = Bet.objects.filter(bet_owner=self.request.user)

        print("Received filter result:", filter_result)  # Debugging line
        print("Received filter date_range:", filter_date_option)
        print("Received start date:", filter_date_start)
        print("Received end date:", filter_date_end)

        if filter_result != 'category-all':
            bet_set = bet_set.filter(result=filter_result)
            print("After filtering by result:", bet_set)
        
        if filter_date_option == 'custom':
            bet_set = bet_set.filter(date_added__range=[filter_date_start, filter_date_end])
            print("After filtering by date range:", bet_set)
        
        return bet_set
    

    def get_user_result_graph(self, user_bets):
        print("getting graph...")
        running_result_list = running_result(user_bets)
        graph = graph_results(running_result_list)
        return graph
    

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)  
        # No need to call get_filtered_bet_list here without the filter
        return context
    
    