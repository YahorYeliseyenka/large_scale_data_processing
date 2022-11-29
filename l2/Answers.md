## Why we use a broker?
    Do odbierania wiadomości

## Why there is no broker URL defined in code?
``` yaml
# URL brokera jest zdefiniowany w pliku *docker-compose.yaml*:
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672
```

## How the broker URL is build (what is guest etc.)
https://en.wikipedia.org/wiki/Advanced_Message_Queuing_Protocol

    - amqp:// - otwarty standard protokołu warstwy aplikacji dla oprogramowania pośredniczącego zorientowanego komunikatowo. Cechy określające AMQP to zorientowanie komunikatowe, kolejkowanie, trasowanie, niezawodność i bezpieczeństwo.
    - guest:guest - username:password
    - rabbitmq:5672 - host:port (może być localhost)

## Change RabitMQ logs to appropriate severity (warning)
https://github.com/docker-library/rabbitmq/issues/118

https://www.rabbitmq.com/logging.html

https://github.com/docker-library/rabbitmq/issues/225

    RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS="-rabbit log_levels [{connection,warning}]"

## Do tasks need to return results?
https://docs.celeryproject.org/en/latest/userguide/tasks.html

    Nie

## Can we schedule periodical tasks?
https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#entries

    -> Entries

## Why the worker is logging twice? can we fix that?
https://stackoverflow.com/questions/45340837/prevent-duplicate-celery-logging

## Why we can see celery errors at the beginning?
    Ponieważ rabbitmq server jeszcze się nie uruchomił. Czasami można tego błędu nie dostać. Zdarza się to kiedy czas uruchomienia grafana jest odpowiednio długi.

## What is the context of docker image building process defined in docker-compose file?
https://docs.docker.com/engine/reference/commandline/build/#:~:text=The%20docker%20build%20command%20builds,a%20file%20in%20the%20context.
    
    build: .
    all the files in the local directory sent to docker daemon

## Can we somehow exclude some files from docker image building context?
    Tak, do folderu projektowego można dodać plik .dockerignore. Jest podobny do .gitignore

---------------
http://0.0.0.0:8088/metrics

http://localhost:9090/graph?g0.range_input=1h&g0.stacked=1&g0.expr=bodys_counter_total&g0.tab=0&g1.range_input=1h&g1.stacked=1&g1.expr=fetching_time_bucket&g1.tab=0&g2.range_input=1h&g2.stacked=1&g2.expr=titles_length_bucket&g2.tab=0&g3.range_input=1h&g3.end_input=2020-11-24%2020%3A06&g3.stacked=1&g3.expr=publications_hours_bucket&g3.tab=0

http://localhost:9090/metrics

http://localhost:3000/d/gtHwGiAGk/publications-hours?orgId=1&from=now-24h&to=now