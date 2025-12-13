# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

project = 'generic_exporters'
copyright = '2024, BobTheBuidler'
author = 'BobTheBuidler'

_pony_private_members = "_access_rules_,_adict_,_all_bases_,_attrnames_cache_,_attrs_,_base_attrs_,_batchload_sql_cache_,_cached_max_id_sql_,_composite_keys_,_database_,_default_genexpr_,_default_iter_name_,_delete_sql_cache_,_direct_bases_,_discriminator_,_discriminator_attr_,_find_sql_cache_,_id_,_indexes_"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'a_sync.sphinx.ext',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

intersphinx_mapping = {
    'a_sync': ('https://bobthebuidler.github.io/ez-a-sync', None),
    'aiohttp': ('https://docs.aiohttp.org/', None),
    'bqplot': ('https://bqplot.github.io/bqplot/', None),
    'msgspec': ('https://jcristharif.com/msgspec/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/', None),
    'pony': ('https://docs.ponyorm.org/', None),
    'python': ('https://docs.python.org/3', None),
    'typing_extensions': ('https://typing-extensions.readthedocs.io/en/latest/', None),
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

autodoc_default_options = {
    'private-members': True,
    # sort these modules by source order, not alphabet
    'bysource': 'metric',
    # hide private methods that aren't relevant to us here
    'exclude-members': f'{_pony_private_members},_abc_impl,_prune_running,_ConstantSingletonMeta__instances,_ConstantSingletonMeta__lock,_do_math,_coros',
}
automodule_generate_module_stub = True

sys.path.insert(0, os.path.abspath('./generic_exporters'))
