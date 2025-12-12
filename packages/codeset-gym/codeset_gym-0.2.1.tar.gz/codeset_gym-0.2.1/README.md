# Codeset Gym

A Python package for testing code patches in Docker containers.

## Installation

```bash
uv sync
```

## Usage

```bash
docker login -u <USER> -p <PASSWORD> <REPOSITORY>
python -m codeset_gym <huggingface_dataset> <instance_id> <image_name>
```

### Example

```bash
python -m codeset_gym codeset/codeset-gym-python-new matiasb__python-unidiff-19 europe-docker.pkg.dev/decoded-bulwark-461711-b2/codeset/codeset-platform.codeset-gym-python.matiasb__python-unidiff-19:latest
```

## Build and Publich

```bash
export UV_PUBLISH_TOKEN=pypi-your-token-here
uv build
uv publish
```

## License

MIT
