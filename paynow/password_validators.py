import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class NumericPasswordValidator(object):
    def validate(self, password, user=None):
        if re.match("^[0-9]{6,6}$", password):
            return
        else:
            raise ValidationError(
                _("The password must contain only numbers of lenght 6"),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _(
            "Your password must be 6 digits"
        )