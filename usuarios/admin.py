from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import Usuario

class UsuarioCreationForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nombre', 'email', 'password', 'suspendido')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UsuarioChangeForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nombre', 'email', 'password', 'suspendido', 'is_active', 'is_staff', 'is_superuser')

class UsuarioAdmin(UserAdmin):
    add_form = UsuarioCreationForm
    form = UsuarioChangeForm
    model = Usuario
    list_display = ['id', 'email', 'nombre', 'suspendido', 'is_active', 'is_staff']  # email primero
    fieldsets = (
        (None, {'fields': ('email', 'nombre', 'password', 'suspendido')}),  # email primero
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'password', 'suspendido', 'is_active', 'is_staff', 'is_superuser')}  # email primero
        ),
    )
    search_fields = ('email', 'nombre')  # email primero
    ordering = ('email',)  # ordenar por email
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(Usuario, UsuarioAdmin)
