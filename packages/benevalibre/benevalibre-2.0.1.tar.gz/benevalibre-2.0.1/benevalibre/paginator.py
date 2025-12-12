from django.core.paginator import EmptyPage, PageNotAnInteger
from django.core.paginator import Paginator as BasePaginator


class Paginator(BasePaginator):
    """
    Extend Paginator from Django with a custom `get_elided_page_range()` method.

    Inspired by Wagtail, see:
    https://github.com/wagtail/wagtail/blob/v7.1/wagtail/admin/paginator.py
    """

    """The number of items to return in `get_elided_page_range()`."""
    num_page_buttons = 6

    def get_elided_page_range(self, page_number):
        """
        Provides a range of page numbers where the number of positions
        occupied by page numbers and ellipses is fixed to num_page_buttons.

        For example, if there are 10 pages where num_page_buttons is 6, the
        output will be:
            - at page 1:  1 2 3 4 … 10
            - at page 6:  1 … 6 7 … 10
            - at page 10: 1 … 7 8 9 10

        The paginator will show the current page in the middle (odd number of
        buttons) or to the left side of the middle (even number of buttons).
        """

        try:
            number = self.validate_number(page_number)
        except PageNotAnInteger:
            number = 1
        except EmptyPage:
            number = self.num_pages

        # Provide all page numbers if fewer than num_page_buttons
        if self.num_pages <= self.num_page_buttons:
            yield from self.page_range
            return

        # These thresholds are the maximum number of buttons that can be shown
        # on the start or end of the page range before the middle part of the
        # range expands.
        # For even num_page_buttons values both thresholds are the same.
        # For odd num_page_buttons values the start threshold is one more than
        # the end threshold.
        end_threshold = self.num_page_buttons // 2
        start_threshold = end_threshold + (self.num_page_buttons % 2)

        # Show the first page
        yield 1

        # Show middle pages
        if number <= start_threshold:
            # Result: 1 [ 2 3 4 … ] 10
            yield from range(2, self.num_page_buttons - 1)
            yield self.ELLIPSIS
        elif number < self.num_pages - end_threshold:
            # Result: 1 [ … 5 6* 7 … ] 10
            # 4 spaces are occupied by first/last page numbers and ellipses
            middle_size = self.num_page_buttons - 4
            offset = (middle_size - 1) // 2
            yield self.ELLIPSIS
            yield from range(number - offset, number + middle_size - offset)
            yield self.ELLIPSIS
        else:
            # Result: 1 [ … 7 8 9 ] 10
            yield self.ELLIPSIS
            yield from range(
                self.num_pages - (self.num_page_buttons - 3), self.num_pages
            )

        # Show the last page
        yield self.num_pages
