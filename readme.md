# **Still In Production**

# Usage:
1. clone repository with `git clone https://github.com/08Aristodemus24/sandigan-backend.git`
2. navigate to directory with manage.py file and requirements.txt file
3. run command; `conda create -n <name of env e.g. sandigan-backend> python=3.9.12`. Note that 3.9.12 must be the python version otherwise packages to be installed would not be compatible with a different python version e.g. simplejwt, django_rest_framework, etc. 
4. once environment is created activate it by running command `conda activate`
5. then run `conda activate sandigan-backend`
6. check if pip is installed by running `conda list -e`
7. if it is there then move to step 8, if not then install `pip` by typing `conda install pip`
8. if `pip` exists or install is done run `pip install -r requirements.txt` in the directory you are currently in
9. once done installing you can run server by `python manage.py runserver`

# This is the backend where phil-jurisprudence-recsys will be integrated, apart from being integrated in another web app which will be deployed. This is but a web app to personally integrate phil-jurisprudence-recsys to

# Database Tasks
## creating database for django:
**Prerequisites to do:**
1. https://console.firebase.google.com/ > "new project" > "<web icon>" > enter web app name > select add firebase as sdk "as npm install" > copy node.js code >
```
// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: os.environ['FIREBASE_API_KEY']
  authDomain: os.environ['FIREBASE_AUTH_DOMAIN']
  projectId: os.environ['FIREBASE_PROJECT_ID']
  storageBucket: os.environ['FIREBASE_STORAGE_BUCKET']
  messagingSenderId: os.environ['FIREBASE_MESSAGING_SENDER_ID']
  appId: os.environ['FIREBASE_APP_ID']
  measurementId: os.environ['FIREBASE_MEASUREMENT_ID']
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
```

1. ... > F5 (refresh) > "see all build features" > "Realtime Database" > "Create Database" > select "United States (us-central1)" as default > next > select "Start in test mode" > "Enable" > 

2. to create dummy data: hover over link below the link > "+" > enter key (name of key e.g. meta-data)  > "Add" > hover over meta-data > "+" > enter key (name of key e.g. app-name) & enter value (value e.g. sandigan-backend) > "Add" > hover over meta-data > "+" > enter key (name of key e.g. owner) & enter value (value e.g. LoneVagabond)

**Articles**
https://www.section.io/engineering-education/integrating-firebase-database-in-django/


## configuring database for django:
**Prerequisites to do:**
1. 

**To do:**
1. activate environment by `conda activate sandigan-backend` 
2. once in environment enter command `pip install pyrebase`
3. in `<base directory>` enter command python manage.py startapp <name of app e.g. phil_juris_api>
3. in `<base directory>/sandigan/settings.py` add string `'phil_juris_api'` in `INSTALLED_APPS` array
4. in `<base directory>/phil_juris_api/models.py` add the ff:
```
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
"""
This block defines custom users and modifying the user models and user manager models
"""
class AdvocateManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Advocate(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = AdvocateManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["date_of_birth"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    


"""
This block defines normal models to be interacted with by users
and does not modify any model via inheritance
"""
```

5. in `<base directory>/phil_juris_api/admin.py` add the ff:
```
from django.contrib import admin

from .models import Advocate
from .forms import AdvocateCreationForm, AdvocateChangeForm

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# define custom admin class to now depend on new user
class AdvocateAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = AdvocateChangeForm
    add_form = AdvocateCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "date_of_birth", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["date_of_birth"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "date_of_birth", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []



# Register your models here.
admin.site.register(Advocate, AdvocateAdmin)
```
6. create `forms.py` in `<base directory>/phil_juris_api/` directory
7. in `<base directory>/phil_juris_api/forms.py` add the ff:
```
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import Advocate

"""
following forms are for admin page
"""

class AdvocateCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = Advocate
        fields = ["email", "date_of_birth"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AdvocateChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Advocate
        fields = ["email", "password", "date_of_birth", "is_active", "is_admin"]



"""
for the users outside the access of the admin page place custom forms here
"""
```
7. in `<base directory>/sandigan/urls.py` add the a `path()` object with the arguments `"phil_juris_api/"` and `include('phil_juris_api.added_urls')` to the `urlpatterns` list. `path("phil_juris_api/", include('phil_juris_api.added_urls'))`
8. in this file add the import: `from django.urls import include`
9. in `<base directory>/phil_juris_api/views.py` add the ff:
```
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("<h1>Philippine Jurisprudence API<h1>")
```
10. 
9. create `added_urls.py` in `<base directory>/phil_juris_api/` directory
10. in the newly created `added_urls.py` add the ff:
```
from django.urls import path
from . import views

app_name = 'phil_juris_api'

urlpatterns = [
    path('', views.index, name='test_index')
]
```





**Articles**
1. https://www.section.io/engineering-education/integrating-firebase-database-in-django/
2. https://docs.djangoproject.com/en/4.2/topics/auth/customizing/ *important*

