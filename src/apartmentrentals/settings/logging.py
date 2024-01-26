# Django logging settings
# Customize according to your needs, take into account when the project runs in a Docker container
#
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "verbose": {
#             "format": "{levelname} {asctime} {name} {message}",
#             "style": "{",
#         },
#     },
#     "handlers": {
#         "django_file": {
#             "level": "ERROR",
#             "class": "logging.FileHandler",
#             "filename": "django_error.log",  # File for logging Django errors
#         },
#         "console": {
#             "level": "ERROR",
#             "class": "logging.StreamHandler",
#         },
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["django_file", "console"],
#             "level": "ERROR",
#             "propagate": True,
#         },
#     },
# }
