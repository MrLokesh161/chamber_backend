# chamber/utils.py

from .models import MembershipPrices

def calculate_total_amount(membership_type, sales_turnover, journal_subscription, chamber_day_celebrations):
    admission_fee = MembershipPrices.admissionFee
    journal_subscription_fee = MembershipPrices.journalSubscription
    chamber_day_celebrations_fee = MembershipPrices.chamberDayCelebrations

    total_amount = 0

    if membership_type == 'life':
        total_amount = MembershipPrices.lifeMembership
    elif membership_type == 'trader':
        # Handle traders differently based on sales turnover
        total_amount += calculate_trader_amount(sales_turnover)
    else:
        total_amount += getattr(MembershipPrices, membership_type, 0)

    total_amount += admission_fee

    if journal_subscription:
        total_amount += journal_subscription_fee

    if chamber_day_celebrations:
        total_amount += chamber_day_celebrations_fee

    return total_amount

def calculate_trader_amount(sales_turnover):
    # Handle traders based on sales turnover
    if sales_turnover == 'upTo5Crore':
        return MembershipPrices.upTo5Crore
    elif sales_turnover == 'above5CroreUpTo10Crore':
        return MembershipPrices.above5CroreUpTo10Crore
    elif sales_turnover == 'above10CroreUpTo25Crore':
        return MembershipPrices.above10CroreUpTo25Crore
    elif sales_turnover == 'above25Crore':
        return MembershipPrices.above25Crore
    else:
        return 0  # Handle other cases if needed
