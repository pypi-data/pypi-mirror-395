import asyncio
import json
import logging
import os
from pathlib import Path
from sys import argv

import yaml

from .util.lti import generate as generate_lti_url
from . import Moodle, ResourceActivity, LTIActivity


async def main():
    # check environment variables
    if 'MOODLE_URL' not in os.environ:
        raise ValueError('MOODLE_URL environment variable not set')
    if 'MOODLE_USERNAME' not in os.environ:
        raise ValueError('MOODLE_USERNAME environment variable not set')
    if 'MOODLE_PASSWORD' not in os.environ:
        raise ValueError('MOODLE_PASSWORD environment variable not set')

    MOODLE_URL = os.environ['MOODLE_URL']
    MOODLE_USERNAME = os.environ['MOODLE_USERNAME']
    MOODLE_PASSWORD = os.environ['MOODLE_PASSWORD']
    MOODLE_IDP = os.environ.get('MOODLE_IDP', None)
    MOODLE_REQUEST_WAIT_TIME = float(os.environ.get('MOODLE_REQUEST_WAIT_TIME', '1.0'))

    # read mapping
    if len(argv) != 2:
        raise ValueError('Usage: python -m moodle_api path/to/mapping.[yaml|json]')
    mapping_path = argv[1]

    if mapping_path.endswith(('.yml', '.yaml')):
        logging.warning(f'read yaml mapping from "{mapping_path}"')
        with open(mapping_path, 'r', encoding='utf-8') as mapping_file:
            mapping_source = yaml.load(mapping_file, Loader=yaml.Loader)
    elif mapping_path.endswith('.json'):
        logging.warning(f'read json mapping from "{mapping_path}"')
        with open(mapping_path, 'r', encoding='utf-8') as mapping_file:
            mapping_source = json.load(mapping_file)

    # convert mapping
    mapping: dict[int, dict] = {}

    for activity, options in mapping_source.items():
        if options is None or len(options) == 0:
            logging.warning(f'skip empty activity "{activity}"')
            continue

        if isinstance(activity, int):
            key = activity
        elif isinstance(activity, str) and activity.isnumeric():
            key = int(activity)
        elif isinstance(activity, str) and activity.startswith(MOODLE_URL):
            key = int(activity.rsplit('id=', 1)[-1])
        else:
            raise ValueError(f'unknown activity "{activity}"')

        if not isinstance(options, dict):
            raise ValueError(f'unknown options type "{type(options)}" for activity {activity}')

        value = {}
        for k, v in options.items():
            match k:
                case 'name':
                    if not isinstance(v, str):
                        raise ValueError(f'invalid type "{type(v)}" for {k} in activity {activity}')

                    value[k] = v

                case 'description':
                    if not isinstance(v, str):
                        raise ValueError(f'invalid type "{type(v)}" for {k} in activity {activity}')

                    value[k] = v

                case 'file':
                    if isinstance(v, str):
                        path = Path(v)
                        value[k] = {
                            'clear': False,
                            'path': path,
                            'name': v.split('/')[-1],
                            'author': ''
                        }
                    elif isinstance(v, dict):
                        if 'path' not in v:
                            raise ValueError(f'missing path for file update in activity {activity}')

                        for l in v:
                            if l not in ('clear', 'path', 'name', 'author'):
                                raise ValueError(f'unknown option "{l}" for file update in activity {activity}')

                        path = Path(v['path'])
                        value[k] = {
                            'clear': v.get('clear', False),
                            'path': path,
                            'name': v.get('name', v['path'].split('/')[-1]),
                            'author': v.get('author', '')
                        }
                    else:
                        raise ValueError(f'invalid type "{type(v)}" for {k} in activity {activity}')

                    if not path.exists():
                        raise ValueError(f'invalid path "{path}" for file update in {activity}')

                case 'lti':
                    value[k] = generate_lti_url(
                        v['hub'],
                        v['image'],
                        v['git']['repository'], v['git']['branch'], v['git']['target'],
                        v['start']
                    )

                case _:
                    raise ValueError(f'unknown option "{key}" for activity {activity}')

        mapping[key] = value

    # create moodle
    async with Moodle(MOODLE_URL, MOODLE_REQUEST_WAIT_TIME) as moodle:
        # login
        if MOODLE_IDP is None:
            logging.warning(f'login to "{MOODLE_URL}" as "{MOODLE_USERNAME}"')
            await moodle.login(MOODLE_USERNAME, MOODLE_PASSWORD)
        else:
            logging.warning(f'login to "{MOODLE_URL}" as "{MOODLE_USERNAME}" using IDP "{MOODLE_IDP}"')
            await moodle.shibboleth_login(MOODLE_USERNAME, MOODLE_PASSWORD, MOODLE_IDP)

        # update activities
        for activity_id, options in mapping.items():
            logging.warning(f'processing activity {activity_id}')
            activity = await moodle.activity(activity_id).fetch()

            for option, value in options.items():
                match option:
                    case 'name':
                        logging.info(f'set name="{value}" for activity {activity_id}')
                        await activity.set_name(value)

                    case 'description':
                        logging.info(f'set description="{value}" for activity {activity_id}')
                        await activity.set_description(value)

                    case 'file':
                        if not isinstance(activity, ResourceActivity):
                            raise ValueError(f'invalid type "{type(activity)}" for activity {activity_id}')

                        logging.info(f'receive files for activity {activity_id}')
                        resource_list = await activity.resource_list()

                        if value['clear']:
                            logging.info(f'clear files for activity {activity_id}')

                            for folder in resource_list.children:
                                await folder.delete()
                            for file in resource_list.files:
                                await file.delete()

                        with open(value['path'], 'rb') as file:
                            logging.info(f'upload "{value["path"]}" for activity {activity_id}')
                            await resource_list.upload(file, value['name'], value['author'])

                    case 'lti':
                        if not isinstance(activity, LTIActivity):
                            raise ValueError(f'invalid type "{type(activity)}" for activity {activity_id}')

                        logging.info(f'set lti="{value}" for activity {activity_id}')
                        await activity.set_tool_url(value)

            await activity.set()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
