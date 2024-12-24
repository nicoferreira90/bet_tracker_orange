from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from bets.models import Bet
from tags.models import Tag
from .graph_functions import graph_results
from .analytic_functions import running_result
from django.db.models import Avg, Sum


class AnalyticsPageView(LoginRequiredMixin, TemplateView):
    template_name = "analytics/analytics_with_results.html"
    login_url = reverse_lazy("account_login")

    def get(self, request, *args, **kwargs):
        # Process form data here

        if (
            request.GET.get("type-filter") == None
        ):  # if the page is being rendered without a form submission
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        else:  # if the page is being rendered with a form submission
            filter_type = request.GET.get(
                "type-filter"
            )  # Retrieve the type filter directly

            filter_site = request.GET.get(
                "site-filter"
            )  # Retrieve the site filter directly

            filter_tag = request.GET.get("tag-filter")

            filter_date_option = request.GET.get(
                "dateOption"
            )  # Retrieve the date filter directly

            if (
                filter_date_option == "custom"
            ):  # Retrieve the custom date range from the form, only if the option 'custom' option is selected

                filter_date_start = request.GET.get("filterDateStart")
                print("date start", filter_date_start)

                filter_date_end = request.GET.get("filterDateEnd")
                print("date end", filter_date_end)
            else:
                filter_date_start = None
                filter_date_end = None

            user_bets = self.get_filtered_bet_list(
                filter_type=filter_type,
                filter_site=filter_site,
                filter_tag=filter_tag,
                filter_date_option=filter_date_option,
                filter_date_start=filter_date_start,
                filter_date_end=filter_date_end,
            )

            context = self.get_context_data(**kwargs)  # Get existing context

            context["user_bets"] = user_bets

            context["bet_count"] = user_bets.count()

            context["bets_pending_count"] = user_bets.filter(result="Pending").count()

            context["bets_won_count"] = user_bets.filter(result="Win").count()

            context["bets_lost_count"] = user_bets.filter(result="Lose").count()

            context["bets_pushed_count"] = user_bets.filter(result="Push").count()

            if (
                user_bets.filter(result="Win").count()
                + user_bets.filter(result="Lose").count()
            ) > 0:  # avoid dividing by 0
                context["bet_win_percentage"] = (
                    100
                    * user_bets.filter(result="Win").count()
                    / (
                        user_bets.filter(result="Win").count()
                        + user_bets.filter(result="Lose").count()
                    )
                )
            else:
                context["bet_win_percentage"] = 0

            context["average_odds"] = user_bets.aggregate(Avg("odds", default=0))[
                "odds__avg"
            ]

            total_amount_wagered = user_bets.aggregate(total=Sum("stake"))
            context["total_amount_wagered"] = total_amount_wagered["total"]

            context["total_amount_wagered"] = total_amount_wagered["total"]

            running_result_list = running_result(user_bets)
            context["net_result"] = running_result_list[-1]

            if (
                total_amount_wagered["total"] == 0
                or total_amount_wagered["total"] == None
            ):
                roi = None
                print("roi", roi)
            else:
                roi = running_result_list[-1] / total_amount_wagered["total"]
                context["roi"] = roi * 100
                print("roi", roi)

            context["graph"] = self.get_user_result_graph(
                user_bets
            )  # Pass filter if needed

            return self.render_to_response(context)

    def get_filtered_bet_list(
        self,
        filter_type,
        filter_site,
        filter_tag,
        filter_date_option=None,
        filter_date_start=None,
        filter_date_end=None,
    ):
        """Return only bets made by the user, and also that meet the filter criteria."""
        bet_set = Bet.objects.filter(bet_owner=self.request.user)

        print("Received filter type:", filter_type)  # Debugging line
        print("Received filter site:", filter_site)  # Debugging line
        print("Recieved Tag to filter by:", filter_tag)
        print("Received filter date_range:", filter_date_option)
        print("Received start date:", filter_date_start)
        print("Received end date:", filter_date_end)

        if filter_type != "category-all":
            bet_set = bet_set.filter(bet_type=filter_type)

        if filter_site != "":
            bet_set = bet_set.filter(site=filter_site)
            print("After filtering by site:", bet_set)

        if filter_tag != "":
            bet_set = bet_set.filter(tags__label=filter_tag)

        if filter_date_option == "custom":
            bet_set = bet_set.filter(
                date_added__range=[filter_date_start, filter_date_end]
            )
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
