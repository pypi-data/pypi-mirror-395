# Development Setup

## Installation

For local development:

```bash
uv sync --frozen --extra dev
```

## Testing in another project

To test the package in another project without publishing to PyPI, you can use `uv add` to install

```bash
cd ~
git clone git@github.com:pascal-pfeiffer/ilulab-client.git

# From another project directory:
uv add ~/ilulab-client
```

### Upload to PyPI

#### Create PyPI accounts and API tokens

You'll need to create accounts and generate API tokens:

- TestPyPI (for testing): <https://test.pypi.org/account/register/>
- PyPI (production): <https://pypi.org/account/register/>

For each, go to Account Settings → API tokens → Add API token. Create tokens scoped to "Entire account" initially (you can scope to specific project after first upload).

#### Store tokens securely

Create a ~/.pypirc file (NOT in the repo):

```sh
cp .pypirc.example ~/.pypirc
```

And add your tokens. Then secure it:

```sh
chmod 600 ~/.pypirc
```

#### Test on TestPyPI first

Once you have the token, run:

```bash
make publish-test
```

Then test installation:

```bash
pip install --index-url https://test.pypi.org/simple/ ilulab
```

#### Upload to real PyPI

If TestPyPI works:

```bash
uv run python -m twine upload dist/*
```
