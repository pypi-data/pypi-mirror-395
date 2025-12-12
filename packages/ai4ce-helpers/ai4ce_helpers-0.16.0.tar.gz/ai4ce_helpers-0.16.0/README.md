# AI4CE Helpers
A set of tools to help interact with the AI4CE backend.

For mor information, please refer to the [AI4CE Project](https://gitlab.com/ai4ce/public-info).

# How to Publush
``` bash
poetry install
poetry shell
poetry config pypi-token.pypi <your-api-token>

poetry version minor  # vX.Y.Z --> vX.Y+1.Z
# or
poetry version patch  # vX.Y.Z --> vX.Y.Z+1

poetry publish --build
```
