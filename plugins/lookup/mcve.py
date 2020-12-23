from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
  lookup: mcve
  author:
    - Brian Scholer (@briantist)
  short_description: None
  description:
    - None
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

from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options()

        return [self.get_option('fake_one')]
