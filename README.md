# TNTW

## About

There's nothing to watch!
An API to search movies, special only to myself.

## Backstory

I've been asked to build an API to search for movies, by using an old API
as seeding. So I just decided to make something out of it.

There must be a better way! :smile:

## Usage

Everything is dockerized:

```sh
docker-compose up --build --detach
```

Then go to `http://localhost:8000`

## Roadmap

- [x] Initial setup
  - [x] Dockerize Elasticsearch
  - [x] Dockerize FastAPI
  - [ ] Dockerize Tests?
- [x] Add seeding endpoint
  - [x] Build the seeding API crawler
  - [x] Define Elasticsearch Index schema
  - [x] Bulk upload to Elasticsearch
- [ ] Add search endpoint
  - [ ] No parameter behavior (full pagination?)
  - [ ] Add year filter
  - [ ] Add title filter
- [ ] Snapshot testing
- [ ] What next?

See the [open issues][open-issues] for a full list of
proposed features (and known issues).

## Contributing

Contributions are what make the open source community such an amazing place
to learn, inspire, and create.
Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork
the reposiotry and create a pull request. You can also simply open
an issue with the tag "enhancement".

Things to keep in mind:

- We use pre-commit, so don't forget to run `pre-commit install`

### How to test

First install the poetry environment:

```sh
poetry install
```

Some tests may require Elasticsearch to be running, these tests are
marked with `needs_elasticsearch`:

```sh
docker-compose up --build --detach --renew-anon-volumes
pytest
```

If you want to test something that does not require Elasticsearch:

```sh
pytest -m "not needs_elasticsearch"
```

[open-issues]: https://github.com/nramirezuy/tntw/issues
