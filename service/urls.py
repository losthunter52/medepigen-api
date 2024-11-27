from django.urls import path
from .views import user, participante

urlpatterns = [
    path('login/', user.login, name='login'),
    path('users/', user.list_users, name='list_users'),
    path('users/add/', user.add_user, name='add_user'),
    path('users/edit/<str:username>/', user.edit_user, name='edit_user'),
    path('users/delete/<str:username>/', user.delete_user, name='delete_user'),
    path('users/clone/', user.clone_user, name='clone_user'),

    # -- participantes --
    path('participantes/', participante.list_participantes, name='list_participantes'),
    path('participantes/<int:id>/', participante.list_participante, name='list_participante'),
    path('participantes/add/', participante.add_participante, name='add_participante'),
    path('participantes/edit/<int:id>/', participante.edit_participante, name='edit_participante'),
    path('participantes/delete/<int:id>/', participante.delete_participante, name='delete_participante'),
]