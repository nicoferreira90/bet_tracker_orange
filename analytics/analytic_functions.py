from bets.analytics import bet_payout


def running_result(user_bets):
    """Calculate the profit or loss result of all the graded bets, after every bet, as an array."""
    result_array = [0]
    accumualted_total_result = 0
    for bet in user_bets:
        if bet.result == "Win" or bet.result == "Lose" or bet.result == "Push":
            bet_profit = bet_payout(bet.stake, bet.odds, bet.result) - bet.stake
            accumualted_total_result += bet_profit
            # print(accumualted_total_result)
            result_array.append(accumualted_total_result)

    # print(result_array)
    return result_array
