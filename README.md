# TNTW

## About

There's nothing to watch!
An API to search movies, special only to myself.

## Backstory

I've been asked to build an API to search for movies, by using an old API
as seeding. So I just decided to make something out of it.

There must be a better way! :smile:

## Roadmap

- [x] Initial setup
  - [ ] Dockerize Elasticsearch
  - [ ] Dockerize FastAPI
  - [ ] Dockerize Tests?
- [ ] Add seeding endpoint
  - [ ] Build the seeding API crawler
  - [ ] Define Elasticsearch Index schema
  - [ ] Bulk upload to Elasticsearch
- [ ] Add search endpoint
  - [ ] No parameter behavior (full pagination?)
  - [ ] Add year filter
  - [ ] Add title filter
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

[open-issues]: https://github.com/nramirezuy/tntw/issues
