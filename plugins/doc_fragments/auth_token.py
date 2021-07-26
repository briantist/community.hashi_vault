# -*- coding: utf-8 -*-

# Copyright: (c) 2012, Brian Scholer (@briantist)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    DOCUMENTATION = r'''
    options:
      token:
        description:
          - Vault token. Token may be specified explicitly, through the listed [env] vars, and also through the C(VAULT_TOKEN) env var.
          - If no token is supplied, explicitly or through env, then the plugin will check for a token file, as determined by I(token_path) and I(token_file).
          - The order of token loading (first found wins) is C(token param -> ansible var -> ANSIBLE_HASHI_VAULT_TOKEN -> VAULT_TOKEN -> token file).
        env:
          - name: ANSIBLE_HASHI_VAULT_TOKEN
            version_added: '0.2.0'
        vars:
          - name: ansible_hashi_vault_token
            version_added: '1.2.0'
      token_path:
        description: If no token is specified, will try to read the I(token_file) from this path.
        env:
          - name: VAULT_TOKEN_PATH
            deprecated:
              why: standardizing environment variables
              version: 2.0.0
              collection_name: community.hashi_vault
              alternatives: ANSIBLE_HASHI_VAULT_TOKEN_PATH
          - name: ANSIBLE_HASHI_VAULT_TOKEN_PATH
            version_added: '0.2.0'
        ini:
          - section: lookup_hashi_vault
            key: token_path
        vars:
          - name: ansible_hashi_vault_token_path
            version_added: '1.2.0'
      token_file:
        description: If no token is specified, will try to read the token from this file in I(token_path).
        env:
          - name: VAULT_TOKEN_FILE
            deprecated:
              why: standardizing environment variables
              version: 2.0.0
              collection_name: community.hashi_vault
              alternatives: ANSIBLE_HASHI_VAULT_TOKEN_FILE
          - name: ANSIBLE_HASHI_VAULT_TOKEN_FILE
            version_added: '0.2.0'
        ini:
          - section: lookup_hashi_vault
            key: token_file
        vars:
          - name: ansible_hashi_vault_token_file
            version_added: '1.2.0'
        default: '.vault-token'
      token_validate:
        description:
          - For token auth, will perform a C(lookup-self) operation to determine the token's validity before using it.
          - Disable if your token doesn't have the C(lookup-self) capability.
        env:
          - name: ANSIBLE_HASHI_VAULT_TOKEN_VALIDATE
        ini:
          - section: lookup_hashi_vault
            key: token_validate
        vars:
          - name: ansible_hashi_vault_token_validate
            version_added: '1.2.0'
        type: boolean
        default: true
        version_added: 0.2.0
    '''
