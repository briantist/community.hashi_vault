from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
  lookup: mcve
  author:
    - Brian Scholer (@briantist)
  short_description: Retrieve secrets from HashiCorp's Vault
  description:
    - Retrieve secrets from HashiCorp's Vault.
  options:
    fake_one:
      description: fake one
      required: True
      env:
        - name: ANSIBLE_FAKE
          deprecated:
            why: snot real
            version: 2.12
            alternatives: 'ANSIBLE_REAL'
"""

EXAMPLES = """
"""

RETURN = """
"""

#import os

#from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
#from ansible.utils.display import Display
#from ansible.module_utils.parsing.convert_bool import boolean

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
      self.set_options()

      return [self.get_option('fake_one')]
