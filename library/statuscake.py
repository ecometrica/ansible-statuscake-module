#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import urllib

# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *


ARGUMENT_SPEC = dict(
    username=dict(required=True),
    api_key=dict(required=True, no_log=True),
    name=dict(required=True),
    pause=dict(default='yes', type='bool'),
    # StatusCake requires an http agent, and the ansible fetch_url
    # function picks it up from here.
    http_agent=dict(default='Mozilla 4.0', no_log=True)
)


class StatusCakeError(Exception):
    pass


class StatusCakeAPI(object):
    URL_ALL_TESTS = u"https://app.statuscake.com/API/Tests/"
    URL_UPDATE_TEST = u"https://app.statuscake.com/API/Tests/Update"

    TEST_NAME_KEY = u'WebsiteName'
    PAUSED_KEY = u'Paused'
    TEST_ID_KEY = u'TestID'

    def __init__(self, module, username, api_key):
        self.module = module
        self.username = username
        self.api_key = api_key

        self.tests = {}
        data = self.get(self.URL_ALL_TESTS)

        for test in data:
            self.tests[test[self.TEST_NAME_KEY]] = test

    def is_test_paused(self, name):
        return self.get_test(name)[self.PAUSED_KEY]

    def set_paused(self, name, paused):
        test_id = self.get_test(name)[self.TEST_ID_KEY]
        resp = self.put(
            self.URL_UPDATE_TEST,
            {
                self.TEST_ID_KEY: test_id,
                self.PAUSED_KEY: 1 if paused else 0
            },
        )
        if not resp.get('Success'):
            raise StatusCakeError(resp['Message'])

    def get_test(self, name):
        try:
            return self.tests[name]
        except KeyError:
            raise StatusCakeError(
                "Test with name %r does not exist." % name
            )

    def auth_headers(self):
        return {
            'API': self.api_key,
            'Username': self.username
        }

    def decode_json(self, response, info):
        if info['status'] != 200:
            if 'body' in info:
                error_text = info['body']
            elif 'msg' in info:
                error_text = info['msg']
                raise StatusCakeError(info['msg'])
            else:
                error_text = u"Status code %r, no body" % info['status']
            raise StatusCakeError(error_text)

        content = response.read()
        try:
            return json.loads(content)
        except ValueError:
            # json.loads will throw up a ValueError
            raise StatusCakeError(
                "Cannot decode expected json data %r" % content
            )

    def get(self, url):
        headers = self.auth_headers()
        resp, info = fetch_url(
            self.module, url, headers=headers, method='GET'
        )
        return self.decode_json(resp, info)

    def put(self, url, data):
        headers = self.auth_headers()
        data = urllib.urlencode(data)

        resp, info = fetch_url(
            self.module, url, data=data, headers=headers, method='PUT'
        )
        return self.decode_json(resp, info)


def main():
    module = AnsibleModule(
        argument_spec=ARGUMENT_SPEC,
        check_invalid_arguments=False,
    )

    username = module.params['username']
    api_key = module.params['api_key']
    name = module.params['name']
    pause = module.params['pause']

    try:
        cake = StatusCakeAPI(module, username, api_key)
        is_paused = cake.is_test_paused(name)

        if bool(is_paused) == bool(pause):
            module.exit_json(
                stdout="skipped, since %s is already %s" % (
                    name, 'paused' if pause else 'unpaused'
                ),
                changed=False
            )
            return

        cake.set_paused(name, pause)
        module.exit_json(changed=True)
    except StatusCakeError as sce:
        module.fail_json(msg=str(sce))


if __name__ == '__main__':
    main()

