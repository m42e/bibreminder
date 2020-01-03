# Bib Reminder for Munich public library

This automatically sending pushover messages when a lent item is about to be returned, while also extending the period if possible.

Configure the docker container with the following variables.

## Docker Config

### Required

`PUSHOVER_KEY` Your pushover API Key
`PUSHOVER_CLIENTS` A comma seperated list of pushover client ids.
`HEALTHCHECK_URL` An url for performing a healthcheck (see healthckeck.io for details)
`BIB_USERS` A comma seperated list of combinations of <USER>:<PWD> combinations to check and extend lent items.
