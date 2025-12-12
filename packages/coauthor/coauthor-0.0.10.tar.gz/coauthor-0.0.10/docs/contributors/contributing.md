# Contributing

Welcome to the Coauthor developer docs!
We're excited you're here and want to contribute. ✨

Please discuss new features in an issue before submitting a PR
to make sure that the feature is wanted and will be merged.

<!-- Below are the basic development steps,
and for further information also see the
[EBP organisation guidelines](https://github.com/executablebooks/.github/blob/master/CONTRIBUTING.md).
-->

## Clone the repository

Clone the repository:

```bash
git clone git@gitlab.com:c2platform/c2/coauthor.git
```

Or, using HTTPS:

```bash
git clone https://gitlab.com/c2platform/c2/coauthor.git
```

## Create `.env`

To run Pytest tests create a file `.env` with environment variables. At a minimum you need:

```text
OPENAI_API_URL=https://api.openai.com/v1
OPENAI_API_KEY=<your-api-key>
OPENAI_API_BASE=https://api.openai.com/v1
```

If you want to use LangSmith / LangChain tracing, you will also need:

```text
LANGCHAIN_PROJECT=coauthor-dev
LANGCHAIN_API_KEY=<your-api-key>
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://eu.api.smith.langchain.com"
```

## Setup Python Virtual Environment

```bash
virtualenv ~/.virtualenv/c2d -p python3
source ~/.virtualenv/c2d/bin/activate
```

```bash
python3 -m pip install --upgrade build
pip install .
python -m build
```

You can now also use
[Flit](https://flit.pypa.io/en/stable/)
to create a build, publish etc:

```bash
flit build
```

Install Pytest and Pytest dependencies:

```bash
pip install -r tests/requirements.txt
```

You can now use `pytest` to run tests:

```bash
pytest .
```

## Build and Pip Install Test

```bash
cd ~/git/gitlab/c2/c2/coauthor
rm -rf ~/.virtualenv/whatever | true
virtualenv ~/.virtualenv/whatever -p python3
source ~/.virtualenv/whatever/bin/activate
pip install ~/git/gitlab/c2/c2/coauthor/dist/coauthor-*.tar.gz
```
