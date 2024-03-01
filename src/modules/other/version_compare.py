try:
    from rpm import labelCompare as _compare_rpm_labels
except ImportError:
    import re

    # Emulate RPM field comparisons
    #
    # * Search each string for alphabetic fields [a-zA-Z]+ and
    #   numeric fields [0-9]+ separated by junk [^a-zA-Z0-9]*.
    # * Successive fields in each string are compared to each other.
    # * Alphabetic sections are compared lexicographically, and the
    #   numeric sections are compared numerically.
    # * In the case of a mismatch where one field is numeric and one is
    #   alphabetic, the numeric field is always considered greater (newer).
    # * In the case where one string runs out of fields, the other is always
    #   considered greater (newer).
    try:
        from itertools import zip_longest
    except ImportError:
        from itertools import izip_longest as zip_longest

    _subfield_pattern = re.compile(
        r"(?P<junk>[^a-zA-Z0-9]*)((?P<text>[a-zA-Z]+)|(?P<num>[0-9]+))"
    )

    def _iter_rpm_subfields(field):
        """Yield subfields as 2-tuples that sort in the desired order

        Text subfields are yielded as (0, text_value)
        Numeric subfields are yielded as (1, int_value)
        """
        for subfield in _subfield_pattern.finditer(field):
            text = subfield.group("text")
            if text is not None:
                yield (0, text)
            else:
                yield (1, int(subfield.group("num")))

    def _compare_rpm_field(lhs, rhs):
        # Short circuit for exact matches (including both being None)
        if lhs == rhs:
            return 0
        # Otherwise assume both inputs are strings
        lhs_subfields = _iter_rpm_subfields(lhs)
        rhs_subfields = _iter_rpm_subfields(rhs)
        for lhs_sf, rhs_sf in zip_longest(lhs_subfields, rhs_subfields):
            if lhs_sf == rhs_sf:
                # When both subfields are the same, move to next subfield
                continue
            if lhs_sf is None:
                # Fewer subfields in LHS, so it's less than/older than RHS
                return -1
            if rhs_sf is None:
                # More subfields in LHS, so it's greater than/newer than RHS
                return 1
            # Found a differing subfield, so it determines the relative order
            return -1 if lhs_sf < rhs_sf else 1
        # No relevant differences found between LHS and RHS
        return 0

    def _compare_rpm_labels(lhs, rhs):
        lhs_epoch, lhs_version, lhs_release = lhs
        rhs_epoch, rhs_version, rhs_release = rhs
        result = _compare_rpm_field(str(lhs_epoch), str(rhs_epoch))
        if result:
            return result
        result = _compare_rpm_field(str(lhs_version), str(rhs_version))
        if result:
            return result
        return _compare_rpm_field(str(lhs_release), str(rhs_release))
