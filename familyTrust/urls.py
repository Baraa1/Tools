from django.urls import path
from .views import *

urlpatterns = [
    path('', Trust.as_view(), name='trust'),
    # Members
    path('members/', MembersView.as_view(), name='members'),
    path('members/add-member/', AddMemberView.as_view(), name='add-member'),
    path('members/update-member/<int:pk>/', UpdateMemberView.as_view(), name='update-member'),
    path('members/delete-member/<int:pk>/', DeleteMemberView.as_view(), name='delete-member'),
    # Loans
    path('loans/', LoansView.as_view(), name='loans'),
    path('loans/add-loan/', AddLoanView.as_view(), name='add-loan'),
    path('loans/update-loan/<int:pk>/', UpdateLoanView.as_view(), name='update-loan'),
    path('loans/delete-loan/<int:pk>/', DeleteLoanView.as_view(), name='delete-loan'),
    # Investments
    path('investments/', InvestmentsView.as_view(), name='investments'),
    path('investments/add-investment/', AddInvestmentView.as_view(), name='add-investment'),
    path('investments/update-investment/<int:pk>/', UpdateInvestmentView.as_view(), name='update-investment'),
    path('investments/delete-investment/<int:pk>/', DeleteInvestmentView.as_view(), name='delete-investment'),
    # Subscriptions
    path('subscriptions/', SubscriptionsView.as_view(), name='subscriptions'),
    path('subscriptions/add-subscription/', AddSubscriptionView.as_view(), name='add-subscription'),
    path('subscriptions/update-subscription/<int:pk>/', UpdateSubscriptionView.as_view(), name='update-subscription'),
    path('subscriptions/delete-subscription/<int:pk>/', DeleteSubscriptionView.as_view(), name='delete-subscription'),
    # Transactions
    path('transactions/', TransactionsView.as_view(), name='transactions'),
    path('transactions/add-transaction/', AddTransactionView.as_view(), name='add-transaction'),
    path('transactions/update-transaction/<int:pk>/', UpdateTransactionView.as_view(), name='update-transaction'),
    path('transactions/delete-transaction/<int:pk>/', DeleteTransactionView.as_view(), name='delete-transaction'),
]