class InvalidInputsError(Exception):
    """
    Raised during :class:`Service`'s :meth:`service_clean` method.
    Encapsulates both field_errors and non_field_errors into a single
    entity.

    :param dictionary errors: :class:`Services`'s ``errors`` dictionary

    :param dictionary non_field_errors: :class:`Service`'s
        ``non_field_errors`` dictionary
    """
    def __init__(self, errors, non_field_errors):
        self.errors = errors
        self.non_field_errors = non_field_errors

    def __repr__(self):
        return '{}({}, {})'.format(
            type(self).__name__, repr(self.errors), repr(self.non_field_errors))


import sys
import traceback


class Error(Exception):
    """
    Custom exception to handle response body correctly
    Attributes:
        translation_key (optional) -- unique key to use localization for message
        message (optional) -- message for users (will be used in case not found translation by translation_key)
        debug_message (optional) -- message for development team
        details (optional) -- error details, must contains object with next structure (example):
            details = {
                "field_or_key": [
                    {
                        "translation_key": string,
                        "message": string
                    }
                ]
            }
        additional_info (optional) -- non-structured object with valid JSON
                                      representation which contains some specific information
        response_status (optional) -- HTTP response status
        errors_dict (optional) -- dict which used for add errors in service objects

    """

    def __init__(
        self,
        translation_key=None,
        message=None,
        debug_message=None,
        details=None,
        additional_info=None,
        response_status=None,
        errors_dict=None,
    ) -> None:
        self.translation_key = translation_key or self._default_translation_key
        self.message = message or self._default_message
        self.debug_message = debug_message
        self.details = details
        self.additional_info = additional_info
        self.response_status = response_status or self._default_response_status
        self.errors_dict = errors_dict
        super().__init__(self.message)

    @property
    def _default_response_status(self):
        return 500

    @property
    def _default_message(self):
        return "We are sorry but something went wrong"

    @property
    def _default_translation_key(self):
        return "internal_server_error"


class Unauthorized(Error):
    @property
    def _default_response_status(self):
        return 401

    @property
    def _default_message(self):
        return "Authorization is required"

    @property
    def _default_translation_key(self):
        return "unauthorized"


class NotFound(Error):
    @property
    def _default_response_status(self):
        return 404

    @property
    def _default_message(self):
        return "Resource not found"

    @property
    def _default_translation_key(self):
        return "not_found"

    # What for ? (WTF)
    @property
    def code(self):
        return "not_found"


class ValidationError(Error):
    @property
    def _default_response_status(self):
        return 400

    @property
    def _default_message(self):
        return "Invalid request data"

    @property
    def _default_translation_key(self):
        return "invalid_request_data"


class ForbiddenError(Error):
    @property
    def _default_response_status(self):
        return 403

    @property
    def _default_message(self):
        return "Access denied"

    @property
    def _default_translation_key(self):
        return "forbidden"


class SystemError(Error):
    @property
    def _default_response_status(self):
        return 400

    @property
    def _default_message(self):
        return "Invalid requ"

    @property
    def _default_translation_key(self):
        return "system_error"


class ServiceObjectLogicError(ValidationError):
    pass
