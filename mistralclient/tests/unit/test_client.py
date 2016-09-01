# Copyright 2015 Huawei Technologies Co., Ltd.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import uuid

import mock
import testtools

from mistralclient.api import client


AUTH_HTTP_URL = 'http://localhost:5000/v3'


class BaseClientTests(testtools.TestCase):
    @mock.patch('keystoneclient.v3.client.Client')
    def test_mistral_url_from_catalog(self, keystone_client_mock):
        keystone_client_instance = keystone_client_mock.return_value
        keystone_client_instance.auth_token = str(uuid.uuid4())
        keystone_client_instance.project_id = str(uuid.uuid4())
        keystone_client_instance.user_id = str(uuid.uuid4())

        get_endpoints = mock.Mock()
        get_endpoints.return_value = {
            'workflowv2': [
                {
                    'url': 'http://mistral_host:8989/v2',
                    'interface': 'public',
                    'region': None,
                    'region_id': None,
                    'id': '446eca511e8d45acae0924aea42a4c9f'
                }
            ]
        }

        keystone_client_instance.service_catalog.get_endpoints = get_endpoints

        mistralclient = client.client(
            username='mistral',
            project_name='mistral',
            auth_url=AUTH_HTTP_URL,
            service_type='workflowv2'
        )

        self.assertEqual(
            'http://mistral_host:8989/v2',
            mistralclient.http_client.base_url
        )

    @mock.patch('keystoneclient.v3.client.Client')
    @mock.patch('mistralclient.api.httpclient.HTTPClient')
    def test_mistral_url_defult(self, mock, keystone_client_mock):
        client.client(username='mistral',
                      project_name='misteal',
                      auth_url="http://localhost:35357/v3")
        self.assertTrue(mock.called)
        params = mock.call_args
        self.assertEqual('http://localhost:8989/v2',
                         params[0][0])
