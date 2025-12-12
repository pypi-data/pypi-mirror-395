# Imports of the required python modules and libraries
######################################################
from django import forms
from django.contrib.auth.models import Permission as Permissions
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, HTML, Submit
from crispy_forms.bootstrap import FormActions
from PIL import Image
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

User = get_user_model()

# Custom User Creation form layout
class CustomUserCreationForm(UserCreationForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permissions.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="الصلاحيات"
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "first_name", "last_name", "phone", "occupation", "is_staff", "permissions", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["username"].label = "اسم المستخدم"
        self.fields["email"].label = "البريد الإلكتروني"
        self.fields["first_name"].label = "الاسم"
        self.fields["last_name"].label = "اللقب"
        self.fields["is_staff"].label = "صلاحيات انشاء و تعديل المستخدمين"
        self.fields["password1"].label = "كلمة المرور"
        self.fields["password2"].label = "تأكيد كلمة المرور"
        self.fields["is_active"].label = "تفعيل الحساب"

        # Help Texts
        self.fields["username"].help_text = "اسم المستخدم يجب أن يكون فريدًا، 50 حرفًا أو أقل. فقط حروف، أرقام و @ . + - _"
        self.fields["email"].help_text = "أدخل عنوان البريد الإلكتروني الصحيح"
        self.fields["is_staff"].help_text = "يحدد ما إذا كان بإمكان المستخدم الوصول إلى قسم ادارة المستخدمين."
        self.fields["is_active"].help_text = "يحدد ما إذا كان يجب اعتبار هذا الحساب نشطًا."
        self.fields["password1"].help_text = "كلمة المرور يجب ألا تكون مشابهة لمعلوماتك الشخصية، وأن تحتوي على 8 أحرف على الأقل، وألا تكون شائعة أو رقمية بالكامل.."
        self.fields["password2"].help_text = "أدخل نفس كلمة المرور السابقة للتحقق."

        # Split permissions queryset into two parts for 2 columns
        permissions_list = list(Permissions.objects.exclude(
            Q(codename__regex=r'^(delete_)') |
            Q(content_type__app_label__in=[
                'admin',
                'auth',
                'contenttypes',
                'sessions',
                'django_celery_beat',
                'users'
            ])
        ))
        mid_point = len(permissions_list) // 2
        permissions_right = permissions_list[:mid_point]
        permissions_left = permissions_list[mid_point:]

        # Create two fields with only one column of permissions each
        self.fields["permissions_right"] = forms.ModelMultipleChoiceField(
            queryset=Permissions.objects.filter(id__in=[p.id for p in permissions_right]),
            required=False,
            widget=forms.CheckboxSelectMultiple,
            label="الصلاحيـــات"
        )
        self.fields["permissions_left"] = forms.ModelMultipleChoiceField(
            queryset=Permissions.objects.filter(id__in=[p.id for p in permissions_left]),
            required=False,
            widget=forms.CheckboxSelectMultiple,
            label=""
        )

        # Use Crispy Forms Layout helper
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "username",
            "email",
            "password1",
            "password2",
            HTML("<hr>"),
            Div(
                Div(Field("first_name", css_class="col-md-6"), css_class="col-md-6"),
                Div(Field("last_name", css_class="col-md-6"), css_class="col-md-6"),
                css_class="row"
            ),
            Div(
                Div(Field("phone", css_class="col-md-6"), css_class="col-md-6"),
                Div(Field("occupation", css_class="col-md-6"), css_class="col-md-6"),
                css_class="row"
            ),
            HTML("<hr>"),
            Div(
                Div(Field("permissions_right", css_class="col-md-6"), css_class="col-md-6"),
                Div(Field("permissions_left", css_class="col-md-6"), css_class="col-md-6"),
                css_class="row"
            ),
            "is_staff",
            "is_active",
            FormActions(
                HTML(
                    """
                    <button type="submit" class="btn btn-success">
                        <i class="bi bi-person-plus-fill text-light me-1 h4"></i>
                        إضافة
                    </button>
                    """
                ),
                HTML(
                    """
                    <a href="{% url 'manage_users' %}" class="btn btn-secondary">
                        <i class="bi bi-arrow-return-left text-light me-1 h4"></i> إلغـــاء
                    </a>
                    """
                )
            )
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        # Manually set permissions from both fields
        user.user_permissions.set(self.cleaned_data["permissions_left"] | self.cleaned_data["permissions_right"])
        return user


# Custom User Editing form layout
class CustomUserChangeForm(UserChangeForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permissions.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="الصلاحيات"
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "phone", "occupation", "is_staff",  "permissions", "is_active"]

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        
        # Labels
        self.fields["username"].label = "اسم المستخدم"
        self.fields["email"].label = "البريد الإلكتروني"
        self.fields["first_name"].label = "الاسم الاول"
        self.fields["last_name"].label = "اللقب"
        self.fields["is_staff"].label = "صلاحيات انشاء و تعديل المستخدمين"
        self.fields["is_active"].label = "الحساب مفعل"
        
        # Help Texts
        self.fields["username"].help_text = "اسم المستخدم يجب أن يكون فريدًا، 50 حرفًا أو أقل. فقط حروف، أرقام و @ . + - _"
        self.fields["email"].help_text = "أدخل عنوان البريد الإلكتروني الصحيح"
        self.fields["is_staff"].help_text = "يحدد ما إذا كان بإمكان المستخدم الوصول إلى قسم ادارة المستخدمين."
        self.fields["is_active"].help_text = "يحدد ما إذا كان يجب اعتبار هذا الحساب نشطًا. قم بإلغاء تحديد هذا الخيار بدلاً من الحذف."
        
        # Split permissions queryset into two parts for 2 columns
        permissions_list = list(Permissions.objects.exclude(
            Q(codename__regex=r'^(delete_)') |
            Q(content_type__app_label__in=[
                'admin',
                'auth',
                'contenttypes',
                'sessions',
                'django_celery_beat',
                'users'
            ])
        ))
        mid_point = len(permissions_list) // 2
        self.permissions_right = permissions_list[:mid_point]
        self.permissions_left = permissions_list[mid_point:]

        # Get user's current permissions
        if user:
            user_permissions = set(user.user_permissions.all())

            # Set initial values based on user's existing permissions
            initial_right = [p.id for p in self.permissions_right if p in user_permissions]
            initial_left = [p.id for p in self.permissions_left if p in user_permissions]
        else:
            initial_right = []
            initial_left = []

        # Create two fields with only one column of permissions each
        self.fields["permissions_right"] = forms.ModelMultipleChoiceField(
            queryset=Permissions.objects.filter(id__in=[p.id for p in self.permissions_right]),
            required=False,
            widget=forms.CheckboxSelectMultiple,
            label="الصلاحيـــات",
            initial=initial_right
        )
        self.fields["permissions_left"] = forms.ModelMultipleChoiceField(
            queryset=Permissions.objects.filter(id__in=[p.id for p in self.permissions_left]),
            required=False,
            widget=forms.CheckboxSelectMultiple,
            label="",
            initial=initial_left
        )

        # Use Crispy Forms Layout helper
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "username",
            "email",
            HTML("<hr>"),
            Div(
                Div(Field("first_name", css_class="col-md-6"), css_class="col-md-6"),
                Div(Field("last_name", css_class="col-md-6"), css_class="col-md-6"),
                css_class="row"
            ),
            Div(
                Div(Field("phone", css_class="col-md-6"), css_class="col-md-6"),
                Div(Field("occupation", css_class="col-md-6"), css_class="col-md-6"),
                css_class="row"
            ),
            HTML("<hr>"),
            Div(
                Div(Field("permissions_right", css_class="col-md-6"), css_class="col-md-6"),
                Div(Field("permissions_left", css_class="col-md-6"), css_class="col-md-6"),
                css_class="row"
            ),
            "is_staff",
            "is_active",
            FormActions(
                HTML(
                    """
                    <button type="submit" class="btn btn-success">
                        <i class="bi bi-person-plus-fill text-light me-1 h4"></i>
                        تحديث
                    </button>
                    """
                ),
                HTML(
                    """
                    <a href="{% url 'manage_users' %}" class="btn btn-secondary">
                        <i class="bi bi-arrow-return-left text-light me-1 h4"></i> إلغـــاء
                    </a>
                    """
                ),
                HTML(
                    """
                    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#resetPasswordModal">
                        <i class="bi bi-key-fill text-light me-1 h4"></i> إعادة تعيين كلمة المرور
                    </button>
                    """
                )
            )
        )


    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        # Manually set permissions from both fields
        user.user_permissions.set(self.cleaned_data["permissions_left"] | self.cleaned_data["permissions_right"])
        return user


# Custom User Reset Password form layout
class ResetPasswordForm(SetPasswordForm):
    username = forms.CharField(label="اسم المستخدم", widget=forms.TextInput(attrs={"readonly": "readonly"}))

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['username'].initial = user.username
        self.helper = FormHelper()
        self.fields["new_password1"].label = "كلمة المرور الجديدة"
        self.fields["new_password2"].label = "تأكيد كلمة المرور"
        self.helper.layout = Layout(
            Div(
                Field('username', css_class='col-md-12'),
                Field('new_password1', css_class='col-md-12'),
                Field('new_password2', css_class='col-md-12'),
                css_class='row'
            ),
            Submit('submit', 'تغيير كلمة المرور', css_class='btn btn-primary'),
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'occupation', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True  # Prevent the user from changing their username
        self.fields['email'].label = "البريد الالكتروني"  # Prevent the user from changing their email
        self.fields['first_name'].label = "الاسم الاول"
        self.fields['last_name'].label = "اللقب"
        self.fields['phone'].label = "رقم الهاتف"
        self.fields['occupation'].label = "جهة العمل"
        self.fields['profile_picture'].label = "الصورة الشخصية"

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')

        # Check if the uploaded file is a valid image
        if profile_picture:
            try:
                img = Image.open(profile_picture)
                img.verify()  # Verify the image is not corrupt
                # Check if the image size is within the limits
                if img.width > 600 or img.height > 600:
                    raise ValidationError("The image must not exceed 600x600 pixels.")
            except Exception as e:
                raise ValidationError("Invalid image file.")
        return profile_picture


class ArabicPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_('كلمة المرور القديمة'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'dir': 'rtl'}),
    )
    new_password1 = forms.CharField(
        label=_('كلمة المرور الجديدة'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'dir': 'rtl'}),
    )
    new_password2 = forms.CharField(
        label=_('تأكيد كلمة المرور الجديدة'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'dir': 'rtl'}),
    )