# Wilson Docker Runtime

**Author and owner:** Destiny Machwaya  
**Copyright:** © 2015–2026 Destiny Machwaya

This container packages the existing `wilson-demo` command-line runtime from
`wilson-open-middleware` version `0.1.1rc3`. It does not add an HTTP server,
public API, new acceptance threshold, or substitute operation.

Tensor P2 is immutable. Its canonical traversal is:

`3,3 / 0,0 / 0,1 / 1,2 / 2,1 / 1,0 / 0,0 / Delay(200)`

Operatively, this is the same Tensor P2 expressed through quantum gates as:

`H–CX–CX–CX–CX–H–Delay`

These are not different constructions. The gate operation is the operative
expression of the same immutable Tensor P2.

## Build

From the release directory:

```bash
docker build -t wilson-open-middleware:0.1.1rc3 .
```

## Run

Supply the required interaction text followed by optional runtime arguments:

```bash
docker run --rm wilson-open-middleware:0.1.1rc3 \
  "Review this input through the released Wilson runtime." \
  --shots 1024 \
  --noise 0.1
```

The container writes the existing JSON result to standard output and exits.
It is therefore suitable for a batch execution or IBM Code Engine job. It is
not an HTTP application and does not listen on a network port.

## IBM Code Engine job

After selecting an IBM Code Engine project, create a job from the local source:

```bash
ibmcloud ce job create \
  --name wilson \
  --build-source . \
  --argument "Review this input through the released Wilson runtime." \
  --argument=--shots \
  --argument=1024 \
  --argument=--noise \
  --argument=0.1
```

Run the configured job:

```bash
ibmcloud ce jobrun submit --job wilson
```

This Docker layer packages the released software. It does not define, divide,
modify, adapt, replace, or supersede Tensor P2.

