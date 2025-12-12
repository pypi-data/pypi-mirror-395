# Copyright (c) 2025 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Mapping, Optional

from dataclasses_json import config as dc_config

import qumulo.lib.request as request

from qumulo.lib.rest_util import dataclass_to_dict_omit_none_fields

NEXUS_CONNECTION_URI = '/v1/nexus/connection'
NEXUS_REGISTRATION_URI = '/v1/nexus/registration'
NEXUS_REGISTRATION_ROTATE_URI = '/v1/nexus/registration/rotate'


def ExcludeIfNone(*v: object) -> bool:
    return v[0] is None


@dataclass
class NexusConnectionConfig:
    nexus_enabled: bool
    nexus_host: str
    nexus_port: int
    nexus_interval: int
    nexus_capability_remote_support: bool
    nexus_capability_sso: bool

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'NexusConnectionConfig':
        return NexusConnectionConfig(
            nexus_enabled=data['nexus_enabled'],
            nexus_host=data['nexus_host'],
            nexus_port=data['nexus_port'],
            nexus_interval=data['nexus_interval'],
            nexus_capability_remote_support=data['nexus_capability_remote_support'],
            nexus_capability_sso=data['nexus_capability_sso'],
        )


@dataclass
class NexusConnectionConfigPatch:
    nexus_enabled: Optional[bool] = field(default=None, metadata=dc_config(exclude=ExcludeIfNone))
    nexus_host: Optional[str] = field(default=None, metadata=dc_config(exclude=ExcludeIfNone))
    nexus_port: Optional[int] = field(default=None, metadata=dc_config(exclude=ExcludeIfNone))
    nexus_interval: Optional[int] = field(default=None, metadata=dc_config(exclude=ExcludeIfNone))
    nexus_capability_remote_support: Optional[bool] = field(
        default=None, metadata=dc_config(exclude=ExcludeIfNone)
    )
    nexus_capability_sso: Optional[bool] = field(
        default=None, metadata=dc_config(exclude=ExcludeIfNone)
    )

    def to_dict(self) -> Mapping[str, Any]:
        return dataclass_to_dict_omit_none_fields(self)


class NexusRegistrationStatusEnum(str, Enum):
    NONE = 'NONE'
    PENDING_REGISTRATION = 'PENDING_REGISTRATION'
    ERROR_REGISTERING = 'ERROR_REGISTERING'
    REGISTERED = 'REGISTERED'


@dataclass
class NexusRegistrationStatus:
    nexus_enabled: bool
    registration_status: NexusRegistrationStatusEnum
    secret_created_at: Optional[str]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'NexusRegistrationStatus':
        return NexusRegistrationStatus(
            nexus_enabled=data['nexus_enabled'],
            registration_status=NexusRegistrationStatusEnum(data['registration_status']),
            secret_created_at=data.get('secret_created_at'),
        )


@dataclass
class NexusRegistrationPut:
    join_key: str


class Nexus:
    def __init__(self, client: request.SendRequestObject):
        self.client = client

    def get_nexus_connection_config(self) -> request.ResponseWithEtag[NexusConnectionConfig]:
        response = self.client.send_request('GET', NEXUS_CONNECTION_URI)
        assert response.etag is not None
        return request.ResponseWithEtag(
            NexusConnectionConfig.from_dict(response.data), response.etag
        )

    def modify_nexus_connection_config(
        self, config: NexusConnectionConfigPatch, if_match: Optional[str] = None
    ) -> request.ResponseWithEtag[NexusConnectionConfig]:
        response = self.client.send_request(
            'PATCH', NEXUS_CONNECTION_URI, body=config.to_dict(), if_match=if_match
        )
        assert response.etag is not None
        return request.ResponseWithEtag(
            NexusConnectionConfig.from_dict(response.data), response.etag
        )

    def get_nexus_registration_status(self) -> request.ResponseWithEtag[NexusRegistrationStatus]:
        response = self.client.send_request('GET', NEXUS_REGISTRATION_URI)
        assert response.etag is not None
        return request.ResponseWithEtag(
            NexusRegistrationStatus.from_dict(response.data), response.etag
        )

    def set_nexus_registration(
        self, registration: NexusRegistrationPut, if_match: Optional[str] = None
    ) -> request.ResponseWithEtag[NexusRegistrationStatus]:
        response = self.client.send_request(
            'PUT',
            NEXUS_REGISTRATION_URI,
            body={'join_key': registration.join_key},
            if_match=if_match,
        )
        assert response.etag is not None
        return request.ResponseWithEtag(
            NexusRegistrationStatus.from_dict(response.data), response.etag
        )

    def delete_nexus_registration(
        self, if_match: Optional[str] = None
    ) -> request.ResponseWithEtag[NexusRegistrationStatus]:
        response = self.client.send_request('DELETE', NEXUS_REGISTRATION_URI, if_match=if_match)
        assert response.etag is not None
        return request.ResponseWithEtag(
            NexusRegistrationStatus.from_dict(response.data), response.etag
        )

    def rotate_nexus_secret(self) -> str:
        response = self.client.send_request('POST', NEXUS_REGISTRATION_ROTATE_URI)
        return response.data['monitor_uri']
