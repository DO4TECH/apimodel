# apimodeler
I am a big fan of the expressiveness provided by [Python type hints](https://docs.python.org/3.9/library/typing.html) combined with the use of [FastApi](https://github.com/tiangolo/fastapi). To benefit simply of this expressiveness for all my projects using OpenAPI, I developed this little tool

## Build docker image
```bash
$ git clone https://github.com/DO4TECH/apimodeler.git
$ cd apimodeler/docker && docker build -t apimodeler . && cd ..
```

## Usage
The use of apimodeler is very simple. Just create a Python file containing your API model and use the docker image to generate the corresponding OpenAPI json description.
```bash
$ docker run --rm -v $(pwd):/data apimodeler test_api.py > test_api.json
```
To view the documentation simply run
```bash
$ docker run --rm -v $(pwd):/data apimodeler -p 8000:8000 test_api.py
```
and open your browser to http://localhost:8000/docs.

The cli is made with [Typer](https://github.com/tiangolo/typer), by the way, to access the documentation use
```bash
$ docker run --rm apimodeler --help
```
## Advanced usage
If your model is big and thus can be slow to generate you can increase the timeout by setting RETRY (default is 3) or/and BACKOFF_FACTOR (default is 1) env variables in the docker command.

For more information see [urllib3](https://urllib3.readthedocs.io/en/stable/) Retry [documentation](https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html).

