from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from dal.autocomplete import ModelSelect2
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Profile, Recommendation, User


class CaptchaForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV3, label=False)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'name',
            'institution',
            'country',
            'contact_email',
            'webpage',
            'position',
            'grad_month',
            'grad_year',
            'brain_structure',
            'modalities',
            'methods',
            'domains',
            'keywords',
        )

    def save(self, user=None):
        user_profile = super(UserProfileForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile


class UserDeleteForm(forms.Form):
    confirm = forms.BooleanField(
        widget=forms.HiddenInput(),
        required=True,
        initial=True
    )


class CreateUserForm(CaptchaForm, UserCreationForm):
    email = forms.EmailField(required=True)

    def save(self, commit=True):

        user = super().save(commit=False)
        user.is_active = False

        if commit:
            user.save()

        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)
        labels = {
            'email': _('Email Address'),
        }
        help_texts = {
            'email': _('We will use this address only when we need to '
                       'communicate with you about this website - it will not '
                       'be displayed to anyone else. It is recommended to enter '
                       'an email address that is not likely to change in the future.'),
        }


# class CreateProfileModelForm(CaptchaForm, forms.ModelForm):
class CreateProfileModelForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Profile
        fields = (
            'name',
            'institution',
            'country',
            'contact_email',
            'webpage',
            'position',
            'grad_month',
            'grad_year',
            'brain_structure',
            'modalities',
            'methods',
            'domains',
            'keywords',
        )
        labels = {
            'name': _('Full Name'),
            'institution': _('Institution/Company'),
            'contact_email': _('Email Address'),
            'webpage': _('Linked In or web page'),
            'grad_month': _('Date PhD was obtained: Month'),
            'grad_year': _('Year'),
            'brain_structure': _('Field of Research - Brain Structure'),
            'modalities': _('Field of Research - Modalities'),
            'methods': _('Field of Research - Methods'),
            'domains': _('Field of Research - Domain'),
            'keywords': _('Field of Research - Keywords'),
        }
        help_texts = {
            'contact_email': _('Email Address that will be shown to the people '
                               'who look at your profile.'),
            'country': _('Country of the institution'),
            'webpage': _('Make sure people can look you up easily by '
                         'providing a link to a personal website, profile '
                         'or institution site.'),
            'position': _('Please choose your \'highest\' title from the '
                          'proposed options to ease future searches.'),
            'grad_month': _('Leave empty if no PhD (yet).'),
            'grad_year': _('Please enter the full year (4 digits).'),
            'domains': _('There are free keywords at the end of the '
                         'questionnaire to input further information.'),
            'keywords': _('Optionally you can add some more specific terms '
                          'to describe your field of research, separated '
                          'by commas.'),
        }
        widgets = {
            'country': ModelSelect2(
                url='profiles:countries_autocomplete',
                attrs={
                    # 'data-minimum-input-length': 2,
                    'data-placeholder': 'Search Country...',
                },
            )
        }

    def clean_contact_email(self):
        email = self.cleaned_data['contact_email']
        if email and Profile.objects.filter(contact_email=email).exists():
            raise forms.ValidationError(_('This email address is already taken'),
                                        code='duplicate_email')

        return email


class RecommendModelForm(CaptchaForm, forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Recommendation

        fields = (
            'profile',
            'reviewer_name',
            'reviewer_institution',
            'reviewer_position',
            'seen_at_conf',
            'comment',
        )

        labels = {
            'profile': _('Recommended Person'),
            'reviewer_name': _('Your full name'),
            'reviewer_institution': _('Your Institution/Company'),
            'reviewer_position': _('Your Position'),
            'seen_at_conf': _('I saw one of her talks'),
            'comment': _('')
        }

        help_texts = {
            'profile': _('Name of the person you would like to recommend'),
            'reviewer_position': _('Please choose the \'closest\' title from '
                                   'the proposed options.'),
            'comment': _('Describe here why you recommend this person for '
                         'conference invitations or collaborations. If you '
                         'attended one of her talks, add details on the event '
                         '(year, event name). Please also mention potential '
                         'conflicts of interest, like personal or '
                         'professional relationships '
                         '(friends, colleagues, former PI, ...)'),
        }

        widgets = {
            'profile': ModelSelect2(
                url='profiles:profiles_autocomplete',
                attrs={
                    'data-minimum-input-length': 3,
                    'data-placeholder': 'Search Profile...',
                },
            )
        }

    def clean(self):
        cleaned_data = super(RecommendModelForm, self).clean()
        profile = cleaned_data.get('profile')
        reviewer_name = cleaned_data.get('reviewer_name')

        if profile \
           and reviewer_name \
           and Recommendation.objects \
                             .filter(profile=profile,
                                     reviewer_name=reviewer_name) \
                             .exists():
            raise forms.ValidationError(_('You have already recommended that '
                                          'person!'),
                                        code='aready_recommended')

        return cleaned_data
