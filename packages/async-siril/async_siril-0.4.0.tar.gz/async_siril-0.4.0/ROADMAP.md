## Roadmap

### Immediate
* [x] smart source the siril cli
* [x] setup logging correctly
* [x] async examples with cappa
* [x] full on command listing
* [x] automated command coverage checking
* [x] review all python commands and their types (see "TODO:")
* [x] pytest setup for common commands
* [x] updated examples with how to
* [x] make flats cli example
* [x] add type check with `ty` tool
* [x] make linear stack cli example
* [x] logging cleanup and namespaces
* [x] updated readme with how to
* [x] How to contribute
* [x] Confirm Linux & Windows support
* [x] Updated LICENSE
* [x] Gitops / CI / CD
* [x] publish step to PyPI (and update docs to install)

### Future
* [x] exposing cgroup aware startup (for support in containerized environments)
* [x] developer docs
* [x] base container image usage with Siril pre-installed (started)
* [x] More test coverage and coverage reporting
* [x] clean up core siril imports to hide internals for library
* [ ] multi process support (named pipes need to be dynamic, only available on Linux)
* [ ] multi process examples (ex. stack by filter in parallel by process)
* [ ] make rgb cli example
* [ ] clean up the command & types import signatures to be less verbose
* [ ] multiple siril version support (how to with generated commands)
* [ ] additional composit helpers or commands to reduce boilerplate repetition and provide best practices
* [ ] can `await siril.{some_command}(...)` be made as a convience to `await siril.some_command(...)`?
