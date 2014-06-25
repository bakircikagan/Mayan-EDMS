# {{{ http://code.activestate.com/recipes/578272/ (r1)
def toposort2(data):
    """Dependencies are expressed as a dictionary whose keys are items
    and whose values are a set of dependent items. Output is a list of
    sets in topological order. The first set consists of items with no
    dependences, each subsequent set consists of items that depend upon
    items in the preceeding sets.

    >>> print '\\n'.join(repr(sorted(x)) for x in toposort2({
    ...     2: set([11]),
    ...     9: set([11,8]),
    ...     10: set([11,3]),
    ...     11: set([7,5]),
    ...     8: set([7,3]),
    ...     }) )
    [3, 5, 7]
    [8, 11]
    [2, 9, 10]

    """

    from functools import reduce

    # Ignore self dependencies.
    for k, v in data.items():
        v.discard(k)
    # Find all items that don't depend on anything.
    extra_items_in_deps = reduce(set.union, data.itervalues()) - set(data.iterkeys())
    # Add empty dependences where needed
    for item in extra_items_in_deps:
        data[item] = set()
    while True:
        ordered = set(item for item, dep in data.iteritems() if not dep)
        if not ordered:
            break
        yield ordered
        data = {}
        for item, dep in data.iteritems():
            if item not in ordered:
                data[item] = dep - ordered
    assert not data, "Cyclic dependencies exist among these items:\n%s" % '\n'.join(repr(x) for x in data.iteritems())
# end of http://code.activestate.com/recipes/578272/ }}}
