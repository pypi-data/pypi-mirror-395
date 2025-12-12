[![Scanned by Frogbot](https://raw.github.com/jfrog/frogbot/master/images/frogbot-badge.svg)](https://docs.jfrog-applications.jfrog.io/jfrog-applications/frogbot)

# ps-cli
The Password Safe CLI Application is an efficient Command Line Interface (CLI) tool specifically crafted to interface with the Beyond Insight and Password Safe APIs (version 24.3). This application allows users to access various API resources, including safes, folders, secrets, managed accounts, and more. It offers a user-friendly interface that simplifies command parsing, ensures input validation, and delivers detailed output.


# Available environment variables

## Required:
- **PSCLI_API_URL**: Beyond Insight and Password Safe API URL. This can also be set in the settings file.
- **PSCLI_CLIENT_ID**: Client ID to use when requesting data from the API. This can also be set in the settings file.
- **PSCLI_CLIENT_SECRET**: Client secret to use when requesting data from the API. This can also be set in the settings file.

## Optional:
- **PSCLI_SETTINGS_PATH**: Custom settings path to use for `ps-cli`. By default, the settings file is created in the user's home directory (~).
- **PSCLI_AUTH_RETRIES**: The number of times `ps-cli` should attempt to authenticate in case of an error.
- **PSCLI_TIMEOUT_CONNECTION**: How long to wait for the server to connect and send data before giving up. Integer value defined in seconds, by default 30 seconds.
- **PSCLI_TIMEOUT_REQUEST**: How long to wait for each request made to the API. Defined in seconds, by default 30 seconds.
- **PSCLI_VERIFY_CA**: Set to `false` to disable SSL certificate verification (useful for self-signed certificates). By default, SSL verification is enabled for secure connections.


# Prerequisites

- Python 3.12+
- Password Safe version 24.3


# Getting started

- Install `ps-cli` (package name: `beyondtrust-bips-cli`)

```sh
pip install beyondtrust-bips-cli
```

- Check that `ps-cli` is properly installed:

```sh
ps-cli -h
# Output usage instructions:
usage: ps-cli [-h] [-v] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--format {json,csv,tsv}] [--delimiter {,,;,   ,|, }]
              [-av {3.0,3.1}]
              {safes,folders,secrets,settings} ...
```


- Create the settings file using:

By default, the settings file is created in the user's home directory (~). If you would like to specify a custom path for the settings, you can achieve this by setting the **PSCLI_SETTINGS_PATH** environment variable. If you're using the custom settings path (PSCLI_SETTINGS_PATH), set it before running the settings initialization command:

```sh
ps-cli settings initialize-settings
```

After creating the settings file, proceed to edit it and configure the **api_url**, **client_id**, and **client_secret**, in case you did not define this configuration using the available environment variables (PSCLI_API_URL, PSCLI_CLIENT_ID and PSCLI_CLIENT_SECRET).


You can find more details on `ps-cli` official [documentation](https://docs.beyondtrust.com/).
