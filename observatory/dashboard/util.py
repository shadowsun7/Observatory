# Copyright (c) 2010, Nate Stedman <natesm@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import datetime
from collections import defaultdict
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from HTMLParser import HTMLParser
from urllib import urlopen

# adds a "pages" method to paginator, which returns a list of the pages
class ListPaginator(Paginator):
  def pages(self):
    return [self.page(i) for i in range(1, self.num_pages + 1)]

# fuzzies up time spans into nice simple numbers of time units ago
def time_ago(date, time = datetime.datetime.now()):
  delta = time - date

  def plural(number, descriptor):
    if number == 1:
      return "{0} {1} ago".format(number, descriptor)
    else:
      return "{0} {1}s ago".format(number, descriptor)

  if delta.days >= 7:
    return plural(int(delta.days / 7), "week")
  if delta.days > 0:
    return plural(delta.days, "day")
  if delta.seconds >= 60 * 60:
    return plural(int(delta.seconds / (60 * 60)), "hour")
  if delta.seconds >= 60:
    return plural(int(delta.seconds / 60), "minute")
  return plural(delta.seconds, "second")