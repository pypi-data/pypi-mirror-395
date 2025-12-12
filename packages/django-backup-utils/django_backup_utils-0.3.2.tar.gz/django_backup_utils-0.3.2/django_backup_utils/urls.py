from django.urls import path
from django_backup_utils import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("restore/<slug:pk>", login_required(views.RestoreBackupView.as_view()), name='restore-backup'),
    path("create/", login_required(views.CreateBackupView.as_view()), name='create-backup'),
    path("synchronize/", login_required(views.synchronize_backups_view), name='synchronize-backups'),
]
