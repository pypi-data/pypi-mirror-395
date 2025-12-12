import logging
from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from django_backup_utils import forms
from django_backup_utils import models, helpers
from django_backup_utils.exceptions import BackupNotFound
from django_backup_utils.management.commands import loadbackup, createbackup, listbackups

logger = logging.getLogger(__name__)





def synchronize_backups_view(request):


    logger.debug("synchronize_backups_view()")
    if request.user.has_perm('django_backup_utils.add_backup'):
        logger.debug(f"user {request.user} has permission to synchronize")
        command = listbackups.Command()
        try:
            sorted_backups = helpers.get_backup_list_by_time(settings.BACKUP_ROOT)
        except FileNotFoundError as e:
            messages.error(request, f"could not synchronize: {e}")
            return HttpResponseRedirect(reverse_lazy("admin:django_backup_utils_backup_changelist"))

        helpers.synchronize_backups(sorted_backups)

        if not sorted_backups:
            word = f"no backups"
        elif len(sorted_backups) == 1:
            word = f"{len(sorted_backups)} backup"
        elif len(sorted_backups) > 1:
            word = f"{len(sorted_backups)} backups"

        messages.success(request, f"synchronized {word}")
        return HttpResponseRedirect(reverse_lazy("admin:django_backup_utils_backup_changelist"))
    else:
        raise PermissionDenied


class CreateBackupView(FormView):
    template_name = "django_backup_utils/backup_createbackup.html"
    success_url = reverse_lazy('admin:django_backup_utils_backup_changelist')
    form_class = forms.CreateForm
    extra_context = {}

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('django_backup_utils.add_backup'):
            return super(CreateBackupView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        self.extra_context['site_header'] = admin.site.site_header
        return super(CreateBackupView, self).get_context_data()

    def form_valid(self, form):
        command = createbackup.Command()
        excludes = []
        exclude = form.cleaned_data.get('exclude')
        form.cleaned_data.pop('exclude')
        if exclude:
            excludes = str(exclude).split(" ")
        command.handle(silent=True, exclude=excludes, **form.cleaned_data)
        messages.success(self.request, "backup has been created")
        return super(CreateBackupView, self).form_valid(form)


class RestoreBackupView(FormView):
    template_name = "django_backup_utils/backup_loadbackup.html"
    success_url = reverse_lazy('admin:django_backup_utils_backup_changelist')
    form_class = forms.RestoreForm
    extra_context = {}

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('django_backup_utils.can_restore_backup'):
            return super(RestoreBackupView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get(self, request, pk, *args, **kwargs):
        obj = models.Backup.objects.get(pk=pk)
        if Path(obj.backup).is_file():
            self.extra_context['object'] = obj
            self.extra_context['site_header'] = admin.site.site_header
        else:
            raise BackupNotFound(f"{obj.backup} not found")
        return super(RestoreBackupView, self).get(request)

    def form_valid(self, form):
        obj = self.extra_context['object']
        command = loadbackup.Command()
        command.handle(tarpath=obj.backup, noinput=True, silent=True, **form.cleaned_data, )
        messages.success(self.request, "backup has been restored")
        return super(RestoreBackupView, self).form_valid(form)
