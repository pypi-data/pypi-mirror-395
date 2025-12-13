from importlib.metadata import version

# Domain configuration - Earnix Elevate service endpoints follow this pattern
# Legacy suffix for servers not using the new e2- prefix scheme
DOMAIN_SUFFIX_LEGACY = ".e2.earnix.com"
# New suffix for servers using the e2- prefix scheme
DOMAIN_SUFFIX_NEW = ".earnix.com"
# Prefix indicating new DNS scheme (e2 zone becomes prefix instead of subdomain)
E2_PREFIX = "e2-"

PACKAGE_VERSION = version("earnix_elevate")

# User agent identifies SDK version to help with support and debugging
USER_AGENT = f"Earnix-Elevate-SDK-Python/{PACKAGE_VERSION}"

# Authentication constants - OAuth2-style bearer token authentication
AUTH_HEADER_NAME = "Authorization"
AUTH_HEADER_PREFIX = "Bearer"
AUTH_EXCHANGE_ROUTE = "/exchange-auth-code"
AUTH_EXCHANGE_METHOD = "POST"
AUTH_RESPONSE_KEY = "accessToken"
CONTENT_TYPE_JSON = "application/json"
ACCEPT_JSON = "application/json"

# JWT decode options - Skip signature verification to avoid key management complexity
JWT_DECODE_OPTIONS = {"verify_signature": False, "verify_exp": True}

# DNS compliance constants - Prevent DNS resolution failures and ensure valid URLs
DNS_LABEL_MAX_LENGTH = 63  # RFC 1035 limit prevents DNS server rejection
DNS_FQDN_MAX_LENGTH = 253  # RFC 1035 limit prevents URL construction failures

# Server name validation - Prevent injection attacks and ensure secure URL construction
DANGEROUS_PATTERNS = [
    ("{}", "template injection"),
    ("://", "protocol injection"),
    (" ", "spaces"),
    ("\t", "tabs"),
    ("\n", "newlines"),
    ("\r", "carriage returns"),
    ("%", "URL encoding"),
    ("&", "query parameters"),
    ("?", "query start"),
    ("#", "fragment"),
    ("@", "user info"),
    ("[", "IPv6 brackets"),
    ("]", "IPv6 brackets"),
    ("\\", "backslashes"),
    ("/", "forward slashes"),
    (";", "command separator"),
    ("|", "pipe"),
    ("`", "command substitution"),
    ("$", "variable expansion"),
    ("(", "command substitution"),
    (")", "command substitution"),
    ("<", "redirection"),
    (">", "redirection"),
]
