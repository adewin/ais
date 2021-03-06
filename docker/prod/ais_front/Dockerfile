FROM elixir:slim AS build

# install build dependencies
RUN apt-get update \
    && apt-get install -y curl \
    && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install -y nodejs

# prepare build dir
WORKDIR /app

# install hex + rebar
RUN mix local.hex --force && \
    mix local.rebar --force

# set build ENV
ENV MIX_ENV=prod

# install mix dependencies
COPY ais_front/mix.exs ais_front/mix.lock ./
COPY ais_front/config config
RUN mix do deps.get, deps.compile

# build assets
COPY ais_front/assets/package.json ais_front/assets/package-lock.json ./assets/
RUN npm --prefix ./assets ci --progress=false --no-audit

COPY ais_front/priv priv
COPY ais_front/assets assets
RUN npm run --prefix ./assets deploy
RUN mix phx.digest

# compile and build release
COPY ais_front/lib lib
# uncomment COPY if rel/ exists
# COPY rel rel
RUN mix do compile, release

FROM elixir:slim AS app

RUN apt-get update \
    && apt-get install -y locales \
    && echo 'fr_FR.UTF-8 UTF-8' > /etc/locale.gen \
    && echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen \
    && locale-gen
ENV LANG fr_FR.UTF-8
ENV LC_ALL fr_FR.UTF-8

RUN apt-get install -y netcat

WORKDIR /app

RUN chown nobody:nogroup /app

COPY --from=build --chown=nobody:nogroup /app/_build/prod/rel/ais_front ./

ENV HOME=/app

COPY ./docker/prod/ais_front/init.sh /init.d/init.sh
COPY ./docker/common/init.d/*.sh /init.d/
RUN chmod +x /init.d/*.sh

USER nobody:nogroup

CMD ["/init.d/init.sh"]
