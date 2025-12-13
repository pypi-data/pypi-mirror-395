import logging

# Avoid "No handler" warnings when host apps have not configured logging.
logging.getLogger(__name__).addHandler(logging.NullHandler())
