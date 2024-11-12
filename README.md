# mpc_der

## Requirements
- Python 3.12
- Pipenv

You can install Pipenv with `pip3 install Pipenv --user`.

## Scripts
Run the scripts from the workspace root.

Once Pipenv is installed, run the setup script first with `./scripts/setup`.

## Running the Program
To collect data, run:
```shell
python ./src/collect_video_data.py
```
This will read configuration information from `./config/config_collect_data.json`.

Output files will appear in: `./output/collect_video_data/`
