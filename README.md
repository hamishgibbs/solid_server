# solid_server

![GitHub Actions (Tests)](https://github.com/hamishgibbs/solid_server/workflows/Tests/badge.svg)

An example [Solid](https://solidproject.org/) resource server implemented in Python.

## See Also

This library is being developed alongside example implementations of:

* [Solid Identity Provider (IdP)](https://github.com/hamishgibbs/solid_idp).
* [Solid Client](https://github.com/hamishgibbs/solid_client).

### Installation

**From a clone:**

To develop this project locally, clone it onto your machine:

```shell
git clone https://github.com/hamishgibbs/solid_server.git
```

Enter the project directory:

```shell
cd solid_server
```

Install the package with:

```shell
pip install .
```

**From GitHub:**

To install the package directly from GitHub run:

```shell
pip install git+https://github.com/hamishgibbs/solid_server.git
```

## Usage

The API is configured in `solid_server/main.py`. To start the development server, initiate the server with `uvicorn`.

``` shell
uvicorn solid_server.main:app --reload --port 8002
```

The current implementation assumes that the IdP is available at http://127.0.0.1:8000/, the Client is available at http://127.0.0.1:8001/, and the RS is available at http://127.0.0.1:8002/.

## Contributions

This library is in the early stages of development and is intended to demonstrate the flow of Solid client authentication. Review, contributions, and discussion are welcome.

## Acknowledgements

This library relies on draft SOLID specifications authored by the [Solid Project](https://solidproject.org/).
