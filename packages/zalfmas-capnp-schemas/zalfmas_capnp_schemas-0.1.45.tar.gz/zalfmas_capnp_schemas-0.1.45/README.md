# zalfmas-capnp-schemas

Containerized Cap'n Proto schema compiler with C++ and Go (capnpc-go) support.

## Build image

```bash
docker build -t capnp-gen .
```

Optional build arguments:

- CAPNP_VERSION (default 1.2.0)
- JOBS (parallel make jobs, default 6)
- CAPNPC_GO_PKG (Go plugin module path)
- CAPNPC_GO_VERSION (default latest)

Example:

```bash
docker build --build-arg CAPNP_VERSION=1.2.0 --build-arg JOBS=12 -t capnp-gen .
```

## Basic usage

The image ENTRYPOINT is: python3 capnp_compile.py
Default CMD: --lang c++ go

```bash
docker run --rm -u $(id -u):$(id -g) \
  -v "$(pwd)":/workspace -w /workspace capnp-gen
```

Explicit (C++ + Go):

```bash
docker run --rm -u $(id -u):$(id -g) \
  -v "$(pwd)":/workspace -w /workspace capnp-gen --lang c++ go
```

## Notes

- Schemas must be available inside the mounted workspace (default: current directory).
- Generated code is written relative to /workspace (your mounted directory).
- capnpc-go is on PATH (installed in /usr/local/bin).
- Adjust UID/GID mapping with -u to avoid root-owned outputs.

## Updating Go plugin only

Rebuild with a different CAPNPC_GO_VERSION:

```bash
docker build --build-arg CAPNPC_GO_VERSION=v3.0.0 -t capnp-gen .
```
