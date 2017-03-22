#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

RAW_FILE_NAME = os.path.join('scripts', 'leo', 'raw.txt')
HTML_FILES_DIR = os.path.join('static', 'leo')
IMG_FILES_DIR = os.path.join('static', 'leo', 'img')

MONTH_LABEL = '{0}й месяц'

IMG_FILE_NAME = re.compile('^(\d+)_(\d+)_(\d+)_?(\d+)?\.[jpegpnJPEGPN]{3,4}$')

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
      <h1>{0}</h1>
      <div class="row">"""

HTML_FILE_FOOTER = """
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
          <nav aria-label="...">
            <ul class="pager">{0}{1}</ul>
          </nav>
         </div>
       </div>
    </div><!--container-->"""

HTML_END = """
    <script src="js/jquery-1.9.1.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/custom.js"></script>
    <!-- Yandex.Metrika counter -->
    <script type="text/javascript">
    (function (d, w, c) {
    (w[c] = w[c] || []).push(function() {
    try {
    w.yaCounter43063704 = new Ya.Metrika({
    id:43063704,
    clickmap:true,
    trackLinks:true,
    accurateTrackBounce:true,
    webvisor:true,
    trackHash:true
    });
    } catch(e) { }
    });

    var n = d.getElementsByTagName("script")[0],
    s = d.createElement("script"),
    f = function () { n.parentNode.insertBefore(s, n); };
    s.type = "text/javascript";
    s.async = true;
    s.src = "https://mc.yandex.ru/metrika/watch.js";

    if (w.opera == "[object Opera]") {
    d.addEventListener("DOMContentLoaded", f, false);
    } else { f(); }
    })(document, window, "yandex_metrika_callbacks");
    </script>
    <noscript><div><img src="https://mc.yandex.ru/watch/43063704" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
    <!-- /Yandex.Metrika counter -->

    <script>
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

    ga('create', 'UA-92667702-1', 'auto');
    ga('send', 'pageview');
    </script>
  </body>
</html>"""

MAX_MONTH = 0

class ContentType:
    DATE = 'date'
    HTML = 'html'
    TEXT = 'text'
    NEWLINE = 'newline'

def get_file_contents():
    with open(RAW_FILE_NAME) as raw_file:
        return [line.strip() for line in raw_file.readlines()]

def _date_from_regex(match, group_shift):
    return '{dd}.{mm:02d}.{yyyy}'.format(dd=int(match.group(group_shift + 1)),
                                         mm=int(match.group(group_shift + 2)),
                                         yyyy=int(match.group(group_shift + 3)))

def _normalize_date(line):
    return _date_from_regex(PARSED_DATE.match(line), 1)


def _get_image_info(path):
    parsed_date = IMG_FILE_NAME.match(os.path.basename(path))
    if parsed_date:
        card = parsed_date.group(4)
        return {
            'date': _date_from_regex(parsed_date, 0),
            'path': path,
            'card': 1 if card is None else int(card),
        }
    return None


def collect_images():
    images = []
    for dirpath, dirnames, filenames in os.walk(IMG_FILES_DIR):
        images += filter(None, map(_get_image_info, [
            os.path.join(dirpath, filename) for filename in filenames]))
    infos = {}
    for info in images:
        infos[(info['date'], info['card'])] = info['path']
    return infos

def is_date(line):
    required_date = REQUIRED_DATE.match(line)
    if required_date:
        return True
    else:
        possible_date = POSSIBLE_DATE.match(line)
        if possible_date:
            raise RuntimeError('Possible incorrect date: {0}'.format(line))
        return False

def is_html(line):
    global MAX_MONTH
    required_html = REQUIRED_HTML.match(line)
    if required_html:
        MAX_MONTH = int(PARSED_HTML.match(line).group(1))
        return True
    else:
        possible_html = POSSIBLE_HTML.match(line)
        if possible_html:
            raise RuntimeError('Possible incorrect html: {0}'.format(line))
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
    month_label = MONTH_LABEL.format(month)
    if month == 0:
        month_label = 'Лёва родился!'
    return HTML_FILE_HEADER.format(month_label)

def render_footer(file_name):
    HTML_NAME = '{0:02d}.html'
    PREV_LI = ('<li class="previous"><a href="{0}">'
        '<span aria-hidden="true">&larr;</span>{1}</a></li>')
    NEXT_LI = ('<li class="next"><a href="{0}">{1}<span aria-hidden="true">'
        '&rarr;</span></a></li>')
    month = int(PARSED_HTML.match(file_name).group(1))
    prev_li = ''
    next_li = ''
    if month > 0:
        prev_html = HTML_NAME.format(month - 1)
        prev_month = MONTH_LABEL.format(month - 1)
        if month - 1 == 0:
            prev_month = 'Лёва родился!'
        prev_li = PREV_LI.format(prev_html, prev_month)
    if month < MAX_MONTH:
        next_html = HTML_NAME.format(month + 1)
        next_month = MONTH_LABEL.format(month + 1)
        next_li = NEXT_LI.format(next_html, next_month)

    return HTML_FILE_FOOTER.format(prev_li, next_li)

def render_card(card, image_path):
    image = ''
    if image_path:
        url = os.path.relpath(image_path, HTML_FILES_DIR)
        image = """
          <div class="item_img_hr">
            <img src="{0}" onclick="showImg(this);"/>
          </div>""".format(url)
    return """
    <div class="col-xs-12 col-sm-12 col-md-6 col-lg-4">
      <div class="panel item">
        <div class="panel-heading date_pan">
          <h3 class="panel-title date_pan">{0}</h3>
        </div>
        <div class="panel-body">{1}{2}</div>
      </div>
    </div>""".format(card['date'], ' '.join(card['paragraphs']), image)

def get_files(classified_content):
    file_name = None
    cards = []

    def new_card(date=None):
        return  {
            'date': date,
            'paragraphs': [],
        }
    def append_card(card):
        if card['date'] is not None and len(card['paragraphs']) > 0:
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
                card = new_card(date=_normalize_date(content))
        elif content_type == ContentType.NEWLINE:
            append_card(card)
            card = new_card(date=card['date'])
        elif content_type == ContentType.TEXT:
            card['paragraphs'].append(content)

    append_card(card)
    yield file_name, cards

def process_contents(contents, images):
    classified_content = [(classify_content(line), line) for line in contents]
    for file_name, cards in get_files(classified_content):
        with open(os.path.join(HTML_FILES_DIR, file_name), 'wb+') as html:
            html.write(render_header(file_name))
            card_number = 1
            current_date = None
            for card in cards:
                if card['date'] == current_date:
                    card_number = card_number + 1
                else:
                    card_number = 1
                current_date = card['date']

                image_path = images.get((current_date, card_number), None)
                html.write(render_card(card, image_path))
            html.write(render_footer(file_name))
            html.write(HTML_END)

if __name__ == '__main__':
    images = collect_images()
    process_contents(get_file_contents(), images)
