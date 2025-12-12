from django import forms


class RestoreForm(forms.Form):
    flush = forms.BooleanField(label="Flush Database", required=False)
    deletedirs = forms.BooleanField(label="Delete BACKUP_DIRS", required=False)
    loadmigrations = forms.BooleanField(label="Load Migration-files", required=False)
    skiptest = forms.BooleanField(label="Skip Unittest", required=False)


class CreateForm(forms.Form):
    compress = forms.BooleanField(label="compress Backup", required=False, initial=True)
    exclude = forms.CharField(label="exclude models", required=False, max_length=10000,
                              widget=forms.TextInput(attrs={'size': '60'}),
                              help_text="</br>example: myapp.model1 myapp.model2")
