import re
from json import JsonSerializable, PropertyJsonSerializer

class SegueError(JsonSerializable, Exception):
    code = 400

    def __init__(self, *args, **kw):
        self.code   = self.__class__.code
        super(SegueError, self).__init__(*args, **kw)

    def to_json(self):
        return { 'args': self.args }

class SegueValidationError(SegueError):
    recognizers = []

    code = 422

    @staticmethod
    def register_recognizer(recognizer):
        SegueValidationError.recognizers.append(recognizer)

    def __init__(self, errors):
        self.errors = errors
        super(SegueValidationError, self).__init__()

    def to_json(self):
        result = []
        for error in self.errors:
            for recognizer_class in SegueValidationError.recognizers:
                if recognizer_class.recognize(error):
                    result.append(recognizer_class.emit_error(error))
                    break
        return result

class InvalidLogin(SegueError):
    def to_json(self):
        return [ 'bad login' ]

class SegueFieldError(SegueError):
    def __init__(self, field=None, label=None, message=None):
        self.field   = field   or getattr(self, 'FIELD', None)
        self.label   = label   or getattr(self, 'LABEL', None)
        self.message = message or getattr(self, 'MESSAGE', None)

    def to_json(self):
        return self.__dict__

class EmailAlreadyInUse(SegueFieldError):
    FIELD = 'email'
    LABEL = 'already_in_use'
    MESSAGE = 'this e-mail address is already registered'

class GenericFieldErrorRecognizer():
    def __init__(self, validator_name, failure_label):
        self.validator_name = validator_name
        self.failure_label = failure_label

    def recognize(self, error):
        return error.validator == self.validator_name

    def emit_error(self, error):
        return SegueFieldError(error.relative_path.pop(), self.failure_label, error.message)


class FieldRequiredErrorRecognizer(GenericFieldErrorRecognizer):
    def emit_error(self, error):
        match = re.match(r"'(.*)' is a required property", error.message)
        return SegueFieldError(match.group(1), self.failure_label, error.message)

class UnknownErrorRecognizer(GenericFieldErrorRecognizer):
    def __init__(self):
        pass
    def recognize(self, error):
        return True
    def emit_error(self, error):
        return SegueError(error.message)


SegueValidationError.register_recognizer(GenericFieldErrorRecognizer('minLength', 'string_length_short'))
SegueValidationError.register_recognizer(GenericFieldErrorRecognizer('maxLength', 'string_length_long'))
SegueValidationError.register_recognizer(GenericFieldErrorRecognizer('pattern',   'string_pattern'))
SegueValidationError.register_recognizer(GenericFieldErrorRecognizer('format',    'invalid_format'))
SegueValidationError.register_recognizer(GenericFieldErrorRecognizer('type',      'invalid_type'))
SegueValidationError.register_recognizer(FieldRequiredErrorRecognizer('required', 'object_required'))
SegueValidationError.register_recognizer(UnknownErrorRecognizer())
