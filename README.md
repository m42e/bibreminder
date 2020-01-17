# Bib Reminder for Munich public library

This automatically sending pushover messages when a lent item is about to be returned, while also extending the period if possible.

Configure the docker container with the following variables.

## Docker Config

### Required

- `PUSHOVER_KEY` Your pushover API Key
- `PUSHOVER_CLIENTS` A comma seperated list of pushover client ids.
- `HEALTHCHECK_URL` An url for performing a healthcheck (see healthckeck.io for details)
- `BIB_USERS` A comma seperated list of combinations of <USER>:<PWD> combinations to check and extend lent items.
- `LIBRARY_URL` The url of the OPAC entry page of your library

Example:

```
PUSHOVER_KEY=abcdef1234567890abcdef12345678
HEALTHCHECK_URL=https://healthcheck.io/ping/0000000-0000-0000-0000-000000000000
BIB_USERS=400001234567:password,40000987654:drowssap
NOTIFY_USERS=	400001234567:12345678abcdef1234567890abcdef,40000987654:12345678abcdef1234567890abcdef
```
