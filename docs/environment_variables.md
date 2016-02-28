# Environment Variables

Jeev can be configured with a python file, or directly from environment variables. This document lists all of the 
configuration options that can be set to configure Jeev.

## Dissonance Core

* `DISSONANCE_STORAGE`: The storage backend to use to serialize module data via `module.data`.
    * Builtin options: `shelve`, `redis`
    * Default: `shelve`
    
* `DISSONANCE_MODULES`: A comma seperated list of modules to load.
    * Default: ``
    * Example: `facts,eightball`

## Jeev Web-Server

* `DISSONANCE_WEB`: Should Jeev run it's built in web-server, that will allow modules to define web endpoints?
    * Default: `FALSE`
    * Possible Values: `FALSE`, `TRUE`
    
* `DISSONANCE_WEB_LISTEN_HOST`: The host that the built in web-server will bind to.
    * **REQUIRED** if `DISSONANCE_WEB == TRUE`.
    * Example: `0.0.0.0` (to listen on all interfaces), `127.0.0.1` (to only listen on localhost)
    
* `DISSONANCE_WEB_LISTEN_PORT`: The port taht the built in web-server will bind to.
    * **REQUIRED** if `DISSONANCE_WEB == TRUE`
    * Example: `8000` (note that if you are using the Slack adapter, by default port 8080 will already be in use)

## Storage Options

* `DISSONANCE_STORAGE_SYNC_INTERVAL`: How often to periodically sync the storage in seconds.
    * Default: `600`

### `jeev.storage.shelve`

* `DISSONANCE_STORAGE_SHELVE_DATA_PATH`: Where shelve stores it's database files.
    * **REQUIRED**
    * Example: `./shelve`
    
### `jeev.storage.redis`

* `DISSONANCE_STORAGE_REDIS_KEY_PREFIX`: What to prefix all the redis keys with in the database
    * Default: `` (empty string, keys won't be prefixed)

* `DISSONANCE_STORAGE_REDIS_URL`: The redis URL to connect to
    * Default: `redis://127.0.0.1:6379/0`

If you don't want to use a URL, you can set the connection kwargs for the `StrictRedis` connection by using 
`DISSONANCE_STORAGE_REDIS_{KEY}`, where `{KEY}` is one of: `HOST`, `PORT`, `DB`, `PASSWORD`, `SOCKET_TIMEOUT`,
`SOCKET_CONNECT_TIMEOUT`, `SOCKET_KEEPALIVE`, `SOCKET_KEEPALIVE_OPTIONS`, `CONNECTION_POOL`, `UNIX_SOCKET_PATH`, 
`ENCODING`, `ENCODING_ERRORS`, `ERRORS`, `DECODE_RESPONSES`, `RETRY_ON_TIMEOUT`, `SSL`, `SSL_KEYFILE`, `SSL_CERTFILE`, 
`SSL_CERT_REQS`, `SSL_CA_CERTS`. See https://github.com/andymccurdy/redis-py for more details.