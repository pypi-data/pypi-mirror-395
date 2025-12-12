import warnings

# Explicitly ignore SyntaxWarning: invalid escape sequence '\*', caused by comments
# in cerberus module. Need to check if newer versions of cerberus fix this.
# Cerberus is used in secrets_safe_library, which is a dependency of this project.
warnings.filterwarnings("ignore", category=SyntaxWarning)
