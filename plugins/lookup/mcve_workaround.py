from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
  lookup: mcve_workaround
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
            collection_name: community.hashi_vault
            plugin_name: mcve_workaround
      ini:
        - section: fake
          key: fake
          deprecated:
            why: u kno y
            version: 2.1212
            alternatives: 'Get a job'
            collection_name: community.hashi_vault
            plugin_name: mcve_workaround
"""

EXAMPLES = """
"""

RETURN = """
"""

from ansible import constants as C

from ansible.plugins.lookup import LookupBase

from ansible.utils.display import Display
display = Display()


def deprecate(plugin_name='mcve_workaround'):

    # nicked directly from cli/__init__.py
    # with slight customization to help filter out relevant messages
    # (must add `plugin_name:` to the `deprecation:` dict)

    # warn about deprecated config options

    for deprecated in list(C.config.DEPRECATED):
        name = deprecated[0]
        why = deprecated[1]['why']
        if deprecated[1].get('plugin_name') != plugin_name:
            continue

        if 'alternatives' in deprecated[1]:
            alt = ', use %s instead' % deprecated[1]['alternatives']
        else:
            alt = ''
        ver = deprecated[1].get('version')
        date = deprecated[1].get('date')
        collection_name = deprecated[1].get('collection_name')
        display.deprecated("%s option, %s%s" % (name, why, alt), version=ver, date=date, collection_name=collection_name)

        # remove this item from the list so it won't get processed again by something else
        C.config.DEPRECATED.remove(deprecated)


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options()
        deprecate()

        # don't actually need to use self.get_option()
        # self.set_options() is enough to populate the deprecations
        return ['q']
