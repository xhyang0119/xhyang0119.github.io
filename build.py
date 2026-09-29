#!/usr/bin/env python3
"""Build this small, dependency-free static academic site.

Usage: python3 build.py
Edit site.json, run this script, then publish the generated HTML files.
No Python is used by the deployed website. All personal content is escaped.
"""
from __future__ import annotations
import html
import json
from pathlib import Path
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
NAV = [('index.html', 'Home'), ('research.html', 'Research'),
       ('notes.html', 'Notes & Talks'), ('teaching.html', 'Teaching'), ('cv.html', 'CV')]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def text(obj: dict, key: str, default: str = '') -> str:
    value = obj.get(key, default)
    if not isinstance(value, str):
        raise ValueError(f'{key!r} must be a text string.')
    return value.strip()


def sequence(obj: dict, key: str) -> list:
    value = obj.get(key, [])
    if not isinstance(value, list):
        raise ValueError(f'{key!r} must be a list.')
    return value


def safe_url(value: str) -> str:
    if not value or any(ord(c) < 32 for c in value) or '\\' in value:
        raise ValueError(f'Invalid link: {value!r}')
    parsed = urlparse(value)
    if parsed.scheme not in ('', 'https', 'http', 'mailto') or value.startswith('//'):
        raise ValueError(f'Unsupported link protocol: {value!r}')
    return esc(value)


def local_asset(value: str, label: str) -> str:
    if urlparse(value).scheme or value.startswith('/'):
        raise ValueError(f'{label} must be a relative file path, e.g. files/cv.pdf.')
    target = (ROOT / value).resolve()
    if not target.is_relative_to(ROOT) or not target.is_file():
        raise ValueError(f'{label} file is missing or outside the site folder: {value}')
    return safe_url(value)


def paragraphs(values: list) -> str:
    if not all(isinstance(item, str) for item in values):
        raise ValueError('Each paragraph must be a text string.')
    return '\n'.join(f'<p>{esc(item)}</p>' for item in values)


def empty(message: str) -> str:
    return f'<div class="empty-state"><p>{esc(message)}</p></div>'


def section(title: str, body: str, *, bordered: bool = False) -> str:
    classes = 'content-section bordered' if bordered else 'content-section'
    return f'<section class="{classes}"><h2>{esc(title)}</h2>{body}</section>'


def more_link(url: str, label: str) -> str:
    return f'<a class="text-link" href="{safe_url(url)}">{esc(label)}<span class="arrow" aria-hidden="true">→</span></a>'


def entries(items: list) -> str:
    output = []
    for item in items:
        if not isinstance(item, dict) or not text(item, 'title'):
            raise ValueError('Each paper, note, course, or CV entry needs a title.')
        title = text(item, 'title')
        primary = text(item, 'url')
        heading = f'<a href="{safe_url(primary)}">{esc(title)}</a>' if primary else esc(title)
        meta_parts = [text(item, k) for k in ('year', 'authors', 'venue', 'role') if text(item, k)]
        metadata = f'<p class="entry-meta">{esc(" · ".join(meta_parts))}</p>' if meta_parts else ''
        description = text(item, 'description')
        detail = f'<p class="entry-description">{esc(description)}</p>' if description else ''
        links = []
        for link in sequence(item, 'links'):
            if not isinstance(link, dict):
                raise ValueError('Each link must have label and url fields.')
            label, url = text(link, 'label'), text(link, 'url')
            if not label or not url:
                raise ValueError('Each link needs a nonempty label and url.')
            links.append(f'<a href="{safe_url(url)}">{esc(label)}</a>')
        link_html = f'<div class="entry-links">{"".join(links)}</div>' if links else ''
        output.append(f'<li class="entry"><h3>{heading}</h3>{metadata}{detail}{link_html}</li>')
    return f'<ul class="entries">{"".join(output)}</ul>'


def sidebar(profile: dict) -> str:
    name, photo = text(profile, 'name'), text(profile, 'photo')
    if photo:
        visual = f'<img class="profile-photo" src="{local_asset(photo, "photo")}" alt="{esc(name)}" decoding="async">'
    else:
        visual = (f'<div class="monogram" aria-hidden="true">'
                  f'<span class="monogram-initials">{esc(text(profile, "initials"))}</span></div>')
    affiliation = ''.join(f'<span>{esc(text(profile, key))}</span>' for key in ('department', 'university'))
    location = text(profile, 'location')
    location_html = f'<p class="location">{esc(location)}</p>' if location else ''
    blocks = f'<section class="sidebar-block"><h2>Affiliation</h2><address>{affiliation}</address>{location_html}</section>'
    email, office = text(profile, 'email'), text(profile, 'office')
    if email:
        if '@' not in email or any(c.isspace() for c in email) or any(c in email for c in '?&#'):
            raise ValueError('email should contain only a plain email address, or be empty.')
        blocks += f'<section class="sidebar-block"><h2>Contact</h2><p><a href="{safe_url("mailto:" + email)}">{esc(email)}</a></p></section>'
    if office:
        blocks += f'<section class="sidebar-block"><h2>Office</h2><p>{esc(office)}</p></section>'
    social = []
    for key, label in [('github_url', 'GitHub'), ('orcid_url', 'ORCID')]:
        if text(profile, key):
            social.append(f'<a href="{safe_url(text(profile, key))}">{label}</a>')
    if social:
        blocks += f'<section class="sidebar-block"><h2>Elsewhere</h2><p class="sidebar-links">{"".join(social)}</p></section>'
    return (f'<aside class="sidebar" aria-label="Profile and contact information">'
            f'<div class="profile-visual">{visual}</div>'
            f'<p class="sidebar-name">{esc(name)}</p>'
            f'<p class="sidebar-role">{esc(text(profile, "role"))}</p>{blocks}</aside>')


def render(filename: str, page_title: str, content: str, data: dict) -> str:
    profile, site = data['profile'], data['site']
    name = text(profile, 'name')
    chinese_name = text(profile, 'chinese_name')
    chinese_html = f'<span class="chinese-name" lang="zh-Hans">{esc(chinese_name)}</span>' if chinese_name else ''
    navigation = ''.join(f'<a href="{url}"' + (' aria-current="page"' if url == filename else '') + f'>{esc(label)}</a>' for url, label in NAV)
    title = f'{name} | Mathematics' if filename == 'index.html' else f'{page_title} | {name}'
    description = f'{name} — {text(profile, "role")}, {text(profile, "university")}. {text(site, "tagline")}.'
    updated = text(site, 'updated')
    updated_html = f'<p>Last updated: {esc(updated)}</p>' if updated else ''
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{esc(description)}">
  <meta name="author" content="{esc(name)}">
  <meta name="theme-color" content="#176f73">
  <meta name="color-scheme" content="light">
  <title>{esc(title)}</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
  <header class="masthead wrapper">
    <div class="brand-row">
      <div>
        <p class="eyebrow">Mathematics · {esc(text(profile, 'university'))}</p>
        <p class="site-name"><a href="index.html">{esc(name)}{chinese_html}</a></p>
      </div>
      <p class="tagline">{esc(text(site, 'tagline'))}</p>
    </div>
    <nav class="site-nav" aria-label="Main navigation">{navigation}</nav>
  </header>
  <div class="layout wrapper">
    <!-- Page content. Prefer editing site.json and running python3 build.py. -->
    <main id="main-content" tabindex="-1">{content}</main>
    {sidebar(profile)}
  </div>
  <footer class="site-footer wrapper">
    <p>© {esc(text(site, 'copyright_year'))} {esc(name)}</p>
    {updated_html}
  </footer>
</body>
</html>
'''


def build() -> None:
    data = json.loads((ROOT / 'site.json').read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError('site.json must contain a JSON object.')
    for required in ('profile', 'site', 'home', 'research', 'notes', 'teaching', 'cv'):
        if not isinstance(data.get(required), dict):
            raise ValueError(f'{required} must be an object in site.json.')
    if not text(data['profile'], 'name'):
        raise ValueError('profile.name cannot be empty.')
    p, home, research = data['profile'], data['home'], data['research']
    topics = sequence(research, 'topics')
    for topic in topics:
        if not isinstance(topic, dict) or not text(topic, 'title'):
            raise ValueError('Each research topic needs a title.')
    topic_list = '<ul class="research-list">' + ''.join(
        f'<li class="research-item"><h3><a href="research.html#topic-{i}">{esc(text(t, "title"))}</a></h3>'
        f'<p>{esc(text(t, "summary"))}</p></li>' for i, t in enumerate(topics, 1)) + '</ul>'
    home_html = '<h1>About me</h1><div class="intro">' + paragraphs(sequence(home, 'about')) + '</div>'
    if topics:
        home_html += section('Research interests', topic_list + more_link('research.html', 'More on my research'))
    notes_html = f'<p class="quiet-note">{esc(text(home, "notes_intro"))}</p>' + more_link('notes.html', 'Notes & talks')
    home_html += section('Notes & talks', notes_html, bordered=True)

    research_html = f'<h1>Research</h1><p class="intro">{esc(text(research, "intro"))}</p>'
    topic_detail = ''.join(f'<section class="topic" id="topic-{i}"><h3>{esc(text(t, "title"))}</h3>'
                           f'<p>{esc(text(t, "summary"))}</p></section>' for i, t in enumerate(topics, 1))
    if topics:
        research_html += section('Mathematical interests', topic_detail)
    papers = sequence(research, 'papers')
    research_html += section('Papers & preprints', entries(papers) if papers else empty('No papers are listed on this page yet.'), bordered=True)

    notes = data['notes']
    notes_page = f'<h1>Notes & talks</h1><p class="intro">{esc(text(notes, "intro"))}</p>'
    note_items = sequence(notes, 'items')
    notes_page += section('Materials', entries(note_items) if note_items else empty('No notes or slides have been posted here yet.'), bordered=True)

    teaching = data['teaching']
    teaching_page = f'<h1>Teaching</h1><p class="intro">{esc(text(teaching, "intro"))}</p>'
    teaching_items = sequence(teaching, 'items')
    teaching_page += section('Courses', entries(teaching_items) if teaching_items else empty('Teaching information has not been posted here yet.'), bordered=True)

    cv = data['cv']
    cv_page = f'<h1>Curriculum vitae</h1><p class="intro">{esc(text(cv, "intro"))}</p>'
    pdf = text(p, 'cv_pdf')
    if pdf:
        cv_page += f'<p><a class="download-link" href="{local_asset(pdf, "CV PDF")}">Download CV (PDF)<span class="arrow" aria-hidden="true">↓</span></a></p>'
    summary = '<dl class="cv-summary">'
    for label, values in [('Position', [text(p, 'role')]), ('Affiliation', [text(p, 'department'), text(p, 'university')]),
                          ('Interests', [text(topic, 'title') for topic in topics])]:
        summary += f'<dt>{label}</dt><dd>' + ''.join(f'<span>{esc(v)}</span>' for v in values) + '</dd>'
    summary += '</dl>'
    cv_page += section('Academic profile', summary, bordered=True)
    for cv_section in sequence(cv, 'sections'):
        if not isinstance(cv_section, dict) or not text(cv_section, 'title'):
            raise ValueError('Each CV section needs a title.')
        cv_page += section(text(cv_section, 'title'), entries(sequence(cv_section, 'items')), bordered=True)

    pages = [('index.html', 'Home', home_html), ('research.html', 'Research', research_html),
             ('notes.html', 'Notes & Talks', notes_page), ('teaching.html', 'Teaching', teaching_page), ('cv.html', 'CV', cv_page)]
    # Render and validate every page before writing any files.
    outputs = [(filename, render(filename, title, content, data)) for filename, title, content in pages]
    outputs.append(('404.html', '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page not found</title>
<style>body{font-family:Georgia,serif;color:#293a3b;max-width:620px;margin:12vh auto;padding:24px;line-height:1.8}h1,a{color:#176f73}</style></head>
<body><h1>Page not found</h1><p>This page may have moved, or the address may be incorrect.</p>
<p>Return to the site's homepage using its main address.</p></body></html>'''))
    for filename, result in outputs:
        (ROOT / filename).write_text(result, encoding='utf-8')
    (ROOT / '.nojekyll').touch()
    print(f'Built {len(outputs)} static pages in {ROOT}')
    print('Preview: open index.html in a browser. No server or dependencies required.')


if __name__ == '__main__':
    try:
        build()
    except (OSError, json.JSONDecodeError, ValueError, TypeError, KeyError) as error:
        print(f'Build failed: {error}', file=sys.stderr)
        raise SystemExit(1)
