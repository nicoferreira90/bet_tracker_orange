
def bet_payout(wager, odds, result):
    "Calculates the payout of an individual Bet object."
    if result=="Lose":
        return 0
    elif result=="Push":
        return wager
    elif result=="Win":
        return wager*odds
    elif result=="Pending":
        return str("Pending")