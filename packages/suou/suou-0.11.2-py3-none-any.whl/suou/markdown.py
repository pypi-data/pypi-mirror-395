"""
Plugins for markdown.

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

import re
import markdown
from markdown.inlinepatterns import InlineProcessor, SimpleTagInlineProcessor
import xml.etree.ElementTree as etree

class StrikethroughExtension(markdown.extensions.Extension):
    """
    Turn ~~crossed out~~ (with double tilde) text into HTML strikethrough

    well, markdown-strikethrough is a trivial dependency lol
    """
    def extendMarkdown(self, md: markdown.Markdown, md_globals=None):
        postprocessor = StrikethroughPostprocessor(md)
        md.postprocessors.register(postprocessor, 'strikethrough', 0)

class StrikethroughPostprocessor(markdown.postprocessors.Postprocessor):
    PATTERN = re.compile(r"~~(((?!~~).)+)~~", re.DOTALL)

    def run(self, html):
        return re.sub(self.PATTERN, self.convert, html)

    def convert(self, match: re.Match):
        return '<del>' + match.group(1) + '</del>'


class SpoilerExtension(markdown.extensions.Extension):
    """
    Add spoiler tags to text, using >!Reddit syntax!<.

    If blockquotes interfer with rendered markup, you might want to call
    SpoilerExtension.patch_blockquote_processor() to clear conflicts with
    the blockquote processor and allow spoiler tags to start at beginning of line.
    """
    def extendMarkdown(self, md: markdown.Markdown, md_globals=None):
        md.inlinePatterns.register(SimpleTagInlineProcessor(r'()>!(.*?)!<', 'span class="spoiler"'), 'spoiler', 14)

    @classmethod
    def patch_blockquote_processor(cls):
        """Patch BlockquoteProcessor to make Spoiler prevail over blockquotes."""
        from markdown.blockprocessors import BlockQuoteProcessor
        BlockQuoteProcessor.RE = re.compile(r'(^|\n)[ ]{0,3}>(?!!)[ ]?(.*)')


class MentionPattern(InlineProcessor):
    def __init__(self, regex, url_prefix: str):
        super().__init__(regex)
        self.url_prefix = url_prefix
    def handleMatch(self, m, data):
        el = etree.Element('a')
        el.attrib['href'] = self.url_prefix + m.group(1)
        el.text = m.group(0)
        return el, m.start(0), m.end(0)

class PingExtension(markdown.extensions.Extension):
    """
    Convert @mentions into profile links.

    Customizable by passing a dict as mappings= argument, where
    the key is the first character, and the value is the URL prefix.
    """
    mappings: dict[str, str]
    DEFAULT_MAPPINGS = {'@': '/@'}
    CHARACTERS = r'[a-zA-Z0-9_-]{2,32}'

    def __init__(self, /, mappings: dict | None = None, **kwargs):
        super().__init__(**kwargs)
        self.mappings = mappings or self.DEFAULT_MAPPINGS.copy()
    def extendMarkdown(self, md: markdown.Markdown, md_globals=None):
        for at, url_prefix in self.mappings.items():
            md.inlinePatterns.register(MentionPattern(re.escape(at) + r'(' + self.CHARACTERS + ')', url_prefix), 'ping_mention', 14)


__all__ = ('PingExtension', 'SpoilerExtension', 'StrikethroughExtension')
