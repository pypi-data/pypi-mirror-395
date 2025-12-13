from atelier.invlib import setup_from_tasks

# docs are currently not maintained. To restart mataining them, uncomment the
# ``doc_trees=[]`` below. Last error message was "Handler <function analyze at
# ...> for event 'builder-inited' threw an exception (exception: Expecting
# value: line 1 column 1 (char 0))"

ns = setup_from_tasks(
    globals(), "lino_react",
    languages="en de fr et".split(),
    # doc_trees=[],
    # tolerate_sphinx_warnings=True,
    blogref_url='https://luc.lino-framework.org',
    revision_control_system='git',
    locale_dir='lino_react/react/locale',
    cleanable_files=['docs/api/lino_react.*'])
