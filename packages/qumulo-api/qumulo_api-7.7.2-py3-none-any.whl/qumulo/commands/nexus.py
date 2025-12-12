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

import argparse

from dataclasses import asdict

import qumulo.lib.opts

from qumulo.lib.request import pretty_json
from qumulo.rest.nexus import NexusConnectionConfigPatch, NexusRegistrationPut
from qumulo.rest_client import RestClient


class GetNexusConnectionConfigCommand(qumulo.lib.opts.Subcommand):
    NAME = 'nexus_get_config'
    SYNOPSIS = 'Get Nexus connection configuration'

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        print(pretty_json(asdict(rest_client.nexus.get_nexus_connection_config().data)))


class GetNexusRegistrationCommand(qumulo.lib.opts.Subcommand):
    NAME = 'nexus_get_registration'
    SYNOPSIS = 'Get Nexus registration status'

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        print(pretty_json(asdict(rest_client.nexus.get_nexus_registration_status().data)))


class SetNexusConnectionConfigCommand(qumulo.lib.opts.Subcommand):
    NAME = 'nexus_set_config'
    SYNOPSIS = 'Set Nexus connection configuration'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        enable_group = parser.add_mutually_exclusive_group()
        enable_group.add_argument('--enable', action='store_true', help='Enable Nexus connection')
        enable_group.add_argument('--disable', action='store_true', help='Disable Nexus connection')
        parser.add_argument('--nexus-host', type=str, help='Nexus host address')
        parser.add_argument('--nexus-port', type=int, help='Nexus port number')
        parser.add_argument('--nexus-interval', type=int, help='Nexus metrics interval in seconds')
        remote_support_group = parser.add_mutually_exclusive_group()
        remote_support_group.add_argument(
            '--enable-remote-support', action='store_true', help='Enable remote support capability'
        )
        remote_support_group.add_argument(
            '--disable-remote-support',
            action='store_true',
            help='Disable remote support capability',
        )
        sso_group = parser.add_mutually_exclusive_group()
        sso_group.add_argument('--enable-sso', action='store_true', help='Enable SSO capability')
        sso_group.add_argument('--disable-sso', action='store_true', help='Disable SSO capability')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        if args.enable and args.disable:
            raise ValueError('Cannot specify both --enable and --disable')

        config = NexusConnectionConfigPatch()

        if args.enable:
            config.nexus_enabled = True
        elif args.disable:
            config.nexus_enabled = False
        if args.nexus_host is not None:
            config.nexus_host = args.nexus_host
        if args.nexus_port is not None:
            config.nexus_port = args.nexus_port
        if args.nexus_interval is not None:
            config.nexus_interval = args.nexus_interval
        if args.enable_remote_support:
            config.nexus_capability_remote_support = True
        elif args.disable_remote_support:
            config.nexus_capability_remote_support = False
        if args.enable_sso:
            config.nexus_capability_sso = True
        elif args.disable_sso:
            config.nexus_capability_sso = False

        print(pretty_json(asdict(rest_client.nexus.modify_nexus_connection_config(config).data)))


class SetNexusRegistrationCommand(qumulo.lib.opts.Subcommand):
    NAME = 'nexus_set_registration'
    SYNOPSIS = 'Set Nexus registration or delete registration'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '--delete',
            action='store_true',
            help='Delete Nexus registration and forget all registration info',
        )
        group.add_argument('--join-key', type=str, help='Join key for registering with Nexus')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        if args.delete:
            result = rest_client.nexus.delete_nexus_registration()
        elif args.join_key:
            registration = NexusRegistrationPut(join_key=args.join_key)
            result = rest_client.nexus.set_nexus_registration(registration)
        else:
            raise ValueError('Must specify either --delete or --join-key')

        print(pretty_json(asdict(result.data)))
