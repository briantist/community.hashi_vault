#!/usr/bin/python
# -*- coding: utf-8 -*-
# (c) 2022, Brian Scholer (@briantist)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
  module: vault_write
  version_added: 1.4.0
  author:
    - Brian Scholer (@briantist)
  short_description: Perform a write operation against HashiCorp Vault
  requirements:
    - C(hvac) (L(Python library,https://hvac.readthedocs.io/en/stable/overview.html))
    - For detailed requirements, see R(the collection requirements page,ansible_collections.community.hashi_vault.docsite.user_guide.requirements).
  description:
    - Performs a generic write operation against a given path in HashiCorp Vault, returning any output.
  notes:
    - The I(data) option is not treated as secret and may be logged. Use the C(no_log) keyword if I(data) contains sensitive values.
  seealso:
    - ref: community.hashi_vault.vault_write lookup <ansible_collections.community.hashi_vault.vault_write_lookup>
      description: The official documentation for the C(community.hashi_vault.vault_write) lookup plugin.
    - module: vault_read
    - ref: community.hashi_vault.vault_read lookup <ansible_collections.community.hashi_vault.vault_read_lookup>
      description: The official documentation for the C(community.hashi_vault.vault_read) lookup plugin.
  extends_documentation_fragment:
    - community.hashi_vault.connection
    - community.hashi_vault.auth
  options:
    path:
      description: Vault path to be written to.
      type: str
      required: True
    data:
      description: A dictionary to be serialized to JSON and then sent as the request body.
      type: dict
      required: false
      default: {}
"""

EXAMPLES = """
- name: Read a kv2 secret from Vault via the remote host with userpass auth
  community.hashi_vault.vault_read:
    url: https://vault:8201
    path: secret/data/hello
    auth_method: userpass
    username: user
    password: '{{ passwd }}'
  register: secret

- name: Display the secret data
  ansible.builtin.debug:
    msg: "{{ secret.data.data.data }}"

- name: Retrieve an approle role ID from Vault via the remote host
  community.hashi_vault.vault_read:
    url: https://vault:8201
    path: auth/approle/role/role-name/role-id
  register: approle_id

- name: Display the role ID
  ansible.builtin.debug:
    msg: "{{ approle_id.data.data.role_id }}"
"""

RETURN = """
data:
  description: The raw result of the write against the given path.
  returned: success
  type: dict
"""

import traceback

from ansible.module_utils._text import to_native
from ansible.module_utils.basic import missing_required_lib

from ansible_collections.community.hashi_vault.plugins.module_utils._hashi_vault_module import HashiVaultModule
from ansible_collections.community.hashi_vault.plugins.module_utils._hashi_vault_common import HashiVaultValueError

try:
    import hvac
except ImportError:
    HAS_HVAC = False
    HVAC_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_HVAC = True


def run_module():
    argspec = HashiVaultModule.generate_argspec(
        path=dict(type='str', required=True),
        data=dict(type='dict', required=False, default={})
    )

    module = HashiVaultModule(
        argument_spec=argspec,
        supports_check_mode=True
    )

    if not HAS_HVAC:
        module.fail_json(
            msg=missing_required_lib('hvac'),
            exception=HVAC_IMPORT_ERROR
        )

    path = module.params.get('path')
    data = module.params.get('data')

    module.connection_options.process_connection_options()
    client_args = module.connection_options.get_hvac_connection_options()
    client = module.helper.get_vault_client(**client_args)

    try:
        module.authenticator.validate()
        module.authenticator.authenticate(client)
    except (NotImplementedError, HashiVaultValueError) as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())

    try:
        response = client.write(path=path, **data)
    except hvac.exceptions.Forbidden:
        module.fail_json(msg="Forbidden: Permission Denied to path '%s'." % path, exception=traceback.format_exc())
    except hvac.exceptions.InvalidPath:
        module.fail_json(msg="The path '%s' doesn't seem to exist." % path, exception=traceback.format_exc())
    except hvac.exceptions.InternalServerError as e:
        module.fail_json(msg="Internal Server Error: %s" % to_native(e), exception=traceback.format_exc())

    # https://github.com/hvac/hvac/issues/797
    # HVAC returns a raw response object when the body is not JSON.
    # That includes 204 responses, which are successful with no body.
    # So we will try to detect that and a act accordingly.
    # A better way may be to implement our own adapter for this
    # collection, but it's a little premature to do that.
    if hasattr(response, 'json') and callable(response.json):
        if response.status_code == 204:
            output = {}
        else:
            module.warn('Vault returned status code %i and an unparsable body.' % response.status_code)
            output = response.content
    else:
        output = response

    module.exit_json(changed=True, data=output)


def main():
    run_module()


if __name__ == '__main__':
    main()
