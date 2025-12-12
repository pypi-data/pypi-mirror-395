# Copyright 2024 Liu Siyao
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
from io import StringIO
from typing import List

from filetype import filetype
from pymultirole_plugins.v1.schema import Document, Sentence, AltText
from rapidfuzz import fuzz

from .types import ConversionConfig, ElementType, ParsedPresentation, SlideType, TextRun
from .utils import rgb_to_hex


def guess_kind(base64_src):
    kind = None
    img_regex = r"data:(image/[^;]+);base64"
    matches = re.search(img_regex, base64_src)
    if matches:
        mime = matches.group(1)
        kind = filetype.get_type(mime)
    return kind


class Formatter:

    def __init__(self, config: ConversionConfig, include_image_base64_as_links: bool, include_image_base64_as_altTexts: bool):
        self.ofile = StringIO()
        self.last_start = 0
        self.segments = []
        self.images = {}
        self.config = config
        self.include_image_base64_as_links = include_image_base64_as_links
        self.include_image_base64_as_altTexts = include_image_base64_as_altTexts

    def output(self, presentation_data: ParsedPresentation, identifier):
        self.put_header()

        last_element = None
        last_title = None
        for slide_idx, slide in enumerate(presentation_data.slides):
            all_elements = []
            if slide.type == SlideType.General:
                all_elements = slide.elements
            elif slide.type == SlideType.MultiColumn:
                all_elements = slide.preface + slide.columns

            for element in all_elements:
                if last_element and last_element.type == ElementType.ListItem and element.type != ElementType.ListItem:
                    self.put_list_footer()

                if element.type == ElementType.Title:
                    element.content = element.content.strip()
                    if element.content:
                        if last_title and last_title.level == element.level and fuzz.ratio(
                                last_title.content, element.content, score_cutoff=92):
                            # skip if the title is the same as the last one
                            # Allow for repeated slide titles - One or more - Add (cont.) to the title
                            if self.config.keep_similar_titles:
                                self.put_title(f'{element.content} (cont.)', element.level)
                        else:
                            self.put_title(element.content, element.level)
                        last_title = element
                elif element.type == ElementType.ListItem:
                    if not (last_element and last_element.type == ElementType.ListItem):
                        self.put_list_header()
                    self.put_list(self.get_formatted_runs(element.content), element.level)
                elif element.type == ElementType.Paragraph:
                    self.put_para(self.get_formatted_runs(element.content))
                elif element.type == ElementType.Image:
                    self.put_image(element.path, element.alt_text)
                    if self.include_image_base64_as_altTexts:
                        self.images[element.path] = element.alt_text
                elif element.type == ElementType.Table:
                    self.put_table([[self.get_formatted_runs(cell) for cell in row] for row in element.content])
                else:
                    last_element = element

            if not self.config.disable_notes and slide.notes:
                self.put_para('---')
                for note in slide.notes:
                    self.put_para(note)

            if slide_idx < len(presentation_data.slides) - 1 and self.config.enable_slides:
                self.add_segment()
                self.put_para("\n---\n")
        altTexts = []
        for m_id, m_url in self.images.items():
            kind = guess_kind(m_url)
            if kind is not None and kind.mime.startswith("image"):
                altTexts.append(AltText(name=m_id, text=m_url, properties={'mime-type': kind.mime}))

        doc = Document(identifier=identifier, text=self.val(), altTexts=altTexts,
                       sentences=[Sentence(start=s[0], end=s[1]) for s in self.segments])
        self.close()
        return doc

    def put_header(self):
        pass

    def put_title(self, text, level):
        pass

    def put_list(self, text, level):
        pass

    def put_list_header(self):
        self.put_para('')

    def put_list_footer(self):
        self.put_para('')

    def get_formatted_runs(self, runs: List[TextRun]):
        res = ''
        for run in runs:
            text = run.text
            if text == '':
                continue

            if not self.config.disable_escaping:
                text = self.get_escaped(text)

            if run.style.hyperlink:
                text = self.get_hyperlink(text, run.style.hyperlink)
            if run.style.is_accent:
                text = self.get_accent(text)
            elif run.style.is_strong:
                text = self.get_strong(text)
            if run.style.color_rgb and not self.config.disable_color:
                text = self.get_colored(text, run.style.color_rgb)

            res += text
        return res.strip()

    def put_para(self, text):
        pass

    def add_segment(self):
        end = len(self.ofile.getvalue())
        self.segments.append((self.last_start, end))
        self.last_start = end

    def put_image(self, path, max_width):
        pass

    def put_table(self, table):
        pass

    def get_accent(self, text):
        pass

    def get_strong(self, text):
        pass

    def get_colored(self, text, rgb):
        pass

    def get_hyperlink(self, text, url):
        pass

    def get_escaped(self, text):
        pass

    def write(self, text):
        self.ofile.write(text)

    def flush(self):
        self.ofile.flush()

    def close(self):
        self.ofile.close()

    def val(self):
        return self.ofile.getvalue()


class MarkdownFormatter(Formatter):
    # write outputs to markdown
    def __init__(self, config: ConversionConfig, include_image_base64_as_links: bool, include_image_base64_as_altTexts: bool):
        super().__init__(config, include_image_base64_as_links, include_image_base64_as_altTexts)
        self.esc_re1 = re.compile(r'([\\\*`!_\{\}\[\]\(\)#\+-\.])')
        self.esc_re2 = re.compile(r'(<[^>]+>)')

    def put_title(self, text, level):
        self.ofile.write('#' * level + ' ' + text + '\n\n')

    def put_list(self, text, level):
        self.ofile.write('  ' * level + '* ' + text.strip() + '\n')

    def put_para(self, text):
        self.ofile.write(text + '\n\n')

    def put_image(self, path, alt, max_width=None):
        if self.include_image_base64_as_links:
            self.ofile.write(f'![{path}]({alt})\n')
        else:
            self.ofile.write(f'![{path}]({path})\n')

    def put_table(self, table):
        def gen_table_row(row):
            return '| ' + ' | '.join([c.replace('\n', '<br />') for c in row]) + ' |'
        self.ofile.write(gen_table_row(table[0]) + '\n')
        self.ofile.write(gen_table_row([':-:' for _ in table[0]]) + '\n')
        self.ofile.write('\n'.join([gen_table_row(row) for row in table[1:]]) + '\n\n')

    def get_accent(self, text):
        return ' _' + text.strip() + '_ '

    def get_strong(self, text):
        return ' __' + text.strip() + '__ '

    def get_colored(self, text, rgb):
        return ' <span style="color:%s">%s</span> ' % (rgb_to_hex(rgb), text)

    def get_hyperlink(self, text, url):
        return '[' + text + '](' + url + ')'

    def esc_repl(self, match):
        return '\\' + match.group(0)

    def get_escaped(self, text):
        text = re.sub(self.esc_re1, self.esc_repl, text)
        text = re.sub(self.esc_re2, self.esc_repl, text)
        return text


class WikiFormatter(Formatter):
    # write outputs to wikitext
    def __init__(self, config: ConversionConfig):
        super().__init__(config)
        self.esc_re = re.compile(r'<([^>]+)>')

    def put_title(self, text, level):
        self.ofile.write('!' * level + ' ' + text + '\n\n')

    def put_list(self, text, level):
        self.ofile.write('*' * (level + 1) + ' ' + text.strip() + '\n')

    def put_para(self, text):
        self.ofile.write(text + '\n\n')

    def put_image(self, path, max_width):
        if max_width is None:
            self.ofile.write(f'<img src="{path}" />\n\n')
        else:
            self.ofile.write(f'<img src="{path}" width={max_width}px />\n\n')

    def get_accent(self, text):
        return ' __' + text + '__ '

    def get_strong(self, text):
        return ' \'\'' + text + '\'\' '

    def get_colored(self, text, rgb):
        return ' @@color:%s; %s @@ ' % (rgb_to_hex(rgb), text)

    def get_hyperlink(self, text, url):
        return '[[' + text + '|' + url + ']]'

    def esc_repl(self, match):
        return "''''" + match.group(0)

    def get_escaped(self, text):
        text = re.sub(self.esc_re, self.esc_repl, text)
        return text


class MadokoFormatter(Formatter):
    # write outputs to madoko markdown
    def __init__(self, config: ConversionConfig):
        super().__init__(config)
        self.ofile.write('[TOC]\n\n')
        self.esc_re1 = re.compile(r'([\\\*`!_\{\}\[\]\(\)#\+-\.])')
        self.esc_re2 = re.compile(r'(<[^>]+>)')

    def put_title(self, text, level):
        self.ofile.write('#' * level + ' ' + text + '\n\n')

    def put_list(self, text, level):
        self.ofile.write('  ' * level + '* ' + text.strip() + '\n')

    def put_para(self, text):
        self.ofile.write(text + '\n\n')

    def put_image(self, path, max_width):
        if max_width is None:
            self.ofile.write(f'<img src="{path}" />\n\n')
        elif max_width < 500:
            self.ofile.write(f'<img src="{path}" width={max_width}px />\n\n')
        else:
            self.ofile.write('~ Figure {caption: image caption}\n')
            self.ofile.write('![](%s){width:%spx;}\n' % (path, max_width))
            self.ofile.write('~\n\n')

    def get_accent(self, text):
        return ' _' + text + '_ '

    def get_strong(self, text):
        return ' __' + text + '__ '

    def get_colored(self, text, rgb):
        return ' <span style="color:%s">%s</span> ' % (rgb_to_hex(rgb), text)

    def get_hyperlink(self, text, url):
        return '[' + text + '](' + url + ')'

    def esc_repl(self, match):
        return '\\' + match.group(0)

    def get_escaped(self, text):
        text = re.sub(self.esc_re1, self.esc_repl, text)
        text = re.sub(self.esc_re2, self.esc_repl, text)
        return text
