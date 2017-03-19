#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

RAW_FILE_NAME = 'raw.txt'

PARSED_HTML = re.compile('^(\d{2})\.html$')
REQUIRED_HTML = re.compile('^(\d{2}\.html)$')
POSSIBLE_HTML = re.compile('^(.*html)$')

PARSED_DATE = re.compile('^((\d+)\.(\d+)\.(2016|2017))$')
REQUIRED_DATE = re.compile('^(\d+\.\d+\.(2016|2017))$')
POSSIBLE_DATE = re.compile('^(\d+\.\d+\.\d+)$')

HTML_FILE_HEADER = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Leo</title>
    <link href="css/bootstrap.css" rel="stylesheet">
    <link href="css/custom.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Lobster|Neucha|Pangolin"
        rel="stylesheet">
    <link rel="shortcut icon" href="img/favicon.ico.png" type="image/x-icon">
 </head>
 <body>
   <div class="back" onclick="window.location='main.html'">
     <ol class="breadcrumb"><li>Главная</li></ol>
   </div>
   <div class="container">
     <div class="alert alert-warning alert-dismissible" role="alert"
         id="photo_popup">
       <div class="close" onclick="hideImg();">
         <span class="glyphicon glyphicon-remove"></span>
       </div>
       <div class="photo_large"></div>
     </div>
     <h1>{} месяц</h1>
     <div class="row">"""

HTML_FILE_FOOTER = """
     </div>
     <div class="row">
       <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
         <nav aria-label="...">
           <ul class="pager">
             {}
             {}
           </ul>
         </nav>
        </div>
      </div>
   </div><!--container-->
   <script src="js/jquery-1.9.1.min.js"></script>
   <script src="js/bootstrap.min.js"></script>
   <script src="js/custom.js"></script>
  </body>
</html>"""

class ContentType:
    DATE = 'date'
    HTML = 'html'
    TEXT = 'text'
    NEWLINE = 'newline'


def get_file_contents():
    with open(RAW_FILE_NAME) as raw_file:
        return [line.strip() for line in raw_file.readlines()]

def _normalize_date(line):
    parsed_date = PARSED_DATE.match(line)
    return '{}.{}.{}'.format(int(parsed_date.group(2)),
                             int(parsed_date.group(3)),
                             int(parsed_date.group(4)))


def is_date(line):
    required_date = REQUIRED_DATE.match(line)
    if required_date:
        return True
    else:
        possible_date = POSSIBLE_DATE.match(line)
        if possible_date:
            raise RuntimeError('Possible incorrect date: {}'.format(line))
        return False

def is_html(line):
    required_html = REQUIRED_HTML.match(line)
    if required_html:
        return True
    else:
        possible_html = POSSIBLE_HTML.match(line)
        if possible_html:
            raise RuntimeError('Possible incorrect html: {}'.format(line))
        return False

def classify_content(line):
    if is_date(line):
        return ContentType.DATE
    elif is_html(line):
        return ContentType.HTML
    elif line:
        return ContentType.TEXT
    else:
        return ContentType.NEWLINE

def render_header(file_name):
    month = int(PARSED_HTML.match(file_name).group(1))
    return HTML_FILE_HEADER.format(month + 1)

def render_footer(file_name):
    MONTH_LABEL = '{} месяц'
    HTML_NAME = '{}.html'
    PREV_LI = ('<li class="previous"><a href="{}">'
        '<span aria-hidden="true">&larr;</span>{}</a></li>')
    NEXT_LI = ('<li class="next"><a href="{}">{}<span aria-hidden="true">'
        '&rarr;</span></a></li>')
    month = int(PARSED_HTML.match(file_name).group(1))
    prev_li = ''
    next_li = ''
    if month > 0:
        prev_html = HTML_NAME.format(month - 1)
        prev_month = MONTH_LABEL.format(month - 1)
        prev_li = PREV_LI.format(prev_html, prev_month)
    if month < 11:
        next_html = HTML_NAME.format(month + 1)
        next_month = MONTH_LABEL.format(month + 1)
        next_li = NEXT_LI.format(next_html, next_month)

    return HTML_FILE_FOOTER.format(prev_li, next_li)

def render_body(paragraphs):
    body = ''
    for paragraph in paragraphs:
        if len(paragraph) == 0:
           continue
        body += '<hr/>'
        body += paragraph[0]
    return body[5:]  # Skip first '<hr/>'

def render_card(card):
    return """
    <div class="col-xs-12 col-sm-12 col-md-6 col-lg-4">
      <div class="panel item">
        <div class="panel-heading date_pan">
          <h3 class="panel-title date_pan">{}</h3>
        </div>
        <div class="panel-body">{}</div>
      </div>
    </div>""".format(card['date'], render_body(card['paragraphs']))

def get_files(classified_content):
    file_name = None
    cards = []

    def new_card():
        return  {
            'date': None,
            'paragraphs': [],
        }
    def append_card(card):
        if card['date'] is not None:
            cards.append(card)
    card = new_card()
    for content_type, content in classified_content:
        if content_type == ContentType.HTML:
            if file_name is None:
                file_name = content
            else:
                append_card(card)
                card = new_card()
                yield file_name, cards
                file_name = content
                cards = []
        elif content_type == ContentType.DATE:
            if card['date'] is None:
                card['date'] = _normalize_date(content)
            else:
                append_card(card)
                card = new_card()
                card['date'] = _normalize_date(content)
        elif content_type == ContentType.NEWLINE:
            if len(card['paragraphs']) > 0:
                card['paragraphs'].append([])
        elif content_type == ContentType.TEXT:
            if len(card['paragraphs']) > 0:
                card['paragraphs'][-1].append(content)
            else:
                card['paragraphs'].append([content])

    append_card(card)
    yield file_name, cards

def process_contents(contents):
    classified_content = [(classify_content(line), line) for line in contents]
    for file_name, cards in get_files(classified_content):
        with open(file_name, 'wb+') as html:
            html.write(render_header(file_name))
            for card in cards:
                html.write(render_card(card))
            html.write(render_footer(file_name))

if __name__ == '__main__':
    process_contents(get_file_contents())
