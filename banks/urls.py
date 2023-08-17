from django.urls import path
from . import views


app_name="banks"
urlpatterns = [ 
    path('add/', views.AddBank.as_view(), name='add'),
    path('<int:pk>/branches/add/', views.AddBranch.as_view(), name='branchadd'),
    path('all/', views.ListBank.as_view(), name='allbanks'),
    path('<int:pk>/details/', views.DetailBank.as_view(), name='bank_details'),
    path('branch/<int:pk>/edit/', views.EditBranch.as_view(), name='edit_branch'),
    path('branch/<int:pk>/details/', views.branchdetail, name='branch_details'),
    path('<int:pk>/branches/all/', views.allbranchdetail, name='bank_allbranch_details'),
]
