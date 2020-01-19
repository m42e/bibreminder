# Bib Reminder for Munich public library

This automatically sending pushover messages when a lent item is about to be returned, while also extending the period of the lending if possible.

It will remind you 20 and 15 days before you have to return the media And if there are only 10 or less days left, it gets pretty annoying and bothers you each and every day, till you return it.

It's not much code nor is it complicated, but maybe it prevents someone else from paying for books kept to long.

Configure the docker container with the following variables.

## Docker Config

The container by default keeps running. It sleeps till it is time to check again. But you can configure it to be a one shot.
It does not keep any track of any data.

### Required
- `PUSHOVER_KEY` Your pushover API Key
- `PUSHOVER_CLIENTS` A comma seperated list of pushover client ids. All the notifications will be sent to this ids
- `BIB_USERS` A comma seperated list of combinations of <USER>:<PWD> combinations to check and extend lent items.


### Optional:
- `LIBRARY_URL` The url of the OPAC entry page of your library, defaults to the one of Stadtbibliothek München
- `RUN_AT_HOUR` Check at hour, default 6
- `RUN_AT_MINUTE` Check at minute, default 0
- `HEALTHCHECK_URL` OPTIONAL url for performing a healthcheck (see healthckeck.io for details)
- `NOTIFY_USERS` A coma separated list of <USER>:<pushover client id> tulles to send pushover messages selectivly
- `RUN_FOREVER` If set to `False` (mind the capitalization) the container will only perform a one time check. This way you could trigger it externally e.g. using cron.

### Example:

```
PUSHOVER_KEY=abcdef1234567890abcdef12345678
HEALTHCHECK_URL=https://healthcheck.io/ping/0000000-0000-0000-0000-000000000000
BIB_USERS=400001234567:password,40000987654:drowssap
NOTIFY_USERS=400001234567:12345678abcdef1234567890abcdef,40000987654:12345678abcdef1234567890abcdef
```
