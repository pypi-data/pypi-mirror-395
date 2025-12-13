#!/usr/bin/env python3
# ultimateultimateguitar

# Copyright (C) 2018-2025 Salvo "LtWorf" Tomaselli
#
# ultimateultimateguitar is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# author Salvo "LtWorf" Tomaselli <tiposchi@tiscali.it>


import argparse
from enum import Enum
import gzip
import hashlib
import html
import json
import os
from typing import *

import typedload
import termcolor


VERSION = '1.2'


class Cache:
    def __init__(self) -> None:
        cachedir = os.environ.get('XDG_CACHE_HOME', os.path.expanduser('~') + '/.cache')
        if not os.path.exists(cachedir):
            raise FileNotFoundError('No cache directory present: %s' % cachedir)
        uugcache = cachedir + '/ultimateultimateguitar/'
        if not os.path.exists(uugcache):
            os.mkdir(uugcache)
        self._cachedir = uugcache

    @staticmethod
    def sha(key: str) -> str:
        return hashlib.sha256(key.encode('utf8')).hexdigest()

    def get(self, key: str) -> Optional[bytes]:
        fname = self._cachedir + str(self.sha(VERSION + key))
        if not os.path.exists(fname):
            return None
        with gzip.open(fname, 'rb') as f:
            return f.read()

    def set(self, key: str, content: bytes) -> None:
        fname = self._cachedir + str(self.sha(VERSION + key))
        with gzip.open(fname, 'wb') as f:
            f.write(content)


class Chord(str):
    @property
    def diesis(self) -> bool:
        """
        True if the chord has a ♯
        """
        try:
            return self[1] in {'#', '♯'}
        except IndexError:
            return False

    @property
    def bemolle(self) -> bool:
        """
        True if the chord has a ♭
        """
        try:
            return self[1] in {'b', '♭'}
        except IndexError:
            return False

    @property
    def details(self) -> str:
        """
        Returns whatever is left after the dominant of the chord

        eg: m, 7, and so on.
        """
        start = 1
        if self.diesis or self.bemolle:
            start += 1
        return self[start:]

    @property
    def dominant(self) -> int:
        TABLE = {
            'C': 0,
            'D': 2,
            'E': 4,
            'F': 5,
            'G': 7,
            'A': 9,
            'B': 11,
        }
        value = TABLE[self[0].upper()]
        if self.bemolle:
            value -= 1
        elif self.diesis:
            value += 1
        return value % 12

    def transpose(self, semitones: int) -> 'Chord':
        TABLE = [
            'C',
            'C♯',
            'D',
            'D♯',
            'E',
            'F',
            'F♯',
            'G',
            'G♯',
            'A',
            'B♭',
            'B',
        ]
        dominant = TABLE[(self.dominant + semitones) % 12]
        return Chord(dominant + self.details)


class WikiTab(NamedTuple):
    content: str

    def get_tokens(self, transpose: int = 0) -> Iterator[Union[str, Chord]]:
        for i in self.content.split('[ch]'):
            s = i.split('[/ch]', 1)
            if len(s) > 1:
                sep = ''
                for j in s[0].split('/'):
                    yield sep
                    yield Chord(j).transpose(transpose)
                    sep = '/'
                yield s[1]
            else:
                yield s[0]


    def print(self, transpose: int = 0) -> None:
        content = self.content
        for i in self.get_tokens(transpose):
            if isinstance(i, Chord):
                termcolor.cprint(i, 'green', end='')
            else:
                i = i.replace('[tab]', '').replace('[/tab]', '')
                print(i, end='')
        print()


class Meta(NamedTuple):
    capo: int | None = None
    tonality: str | None = None

    def print(self) -> None:
        r = []
        if self.capo:
            r.append(f'Capotasto: {self.capo}')
        if self.tonality:
            r.append(f'Tonality: {self.tonality}')

        if r:
            print(' '.join(r))

    # tuning': {'name': 'Standard', 'value': 'E A D G B E', 'index': 1}}


class TabView(NamedTuple):
    wiki_tab: WikiTab
    meta: Meta | None | list[Meta] = None
    #TODO recommendations
    #TODO applicature


class SearchResultType(Enum):
    CHORDS = 'Chords'
    TABS = 'Tabs'
    UKULELE_CHORDS = 'Ukulele Chords'
    BASS_TABS = 'Bass Tabs'
    PRO = 'Pro'
    DRUM_TABS = 'Drum Tabs'
    POWER = 'Power'
    VIDEO = 'Video'
    OFFICIAL = 'Official'


class SearchItem(NamedTuple):
    song_name: str
    artist_name: str
    artist_url: str
    tab_url: str
    type: SearchResultType | None = None


def get_data(url: str) -> Dict[str, Any]:
    """
    From a url of ultimate-guitar, this function returns
    the actual data, which is stored as json.
    """
    lineheader = b'<div class="js-store" data-content="'
    cache = Cache()

    content = cache.get(url)
    if content is not None:
        return json.loads(content)

    from urllib.request import urlopen, Request

    req = Request(url)
    req.headers['DNT'] = '1'
    req.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0'
    req.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    req.headers['Sec-Fetch-Dest'] = 'document'
    req.headers['Sec-Fetch-Mode'] = 'navigate'
    req.headers['Sec-Fetch-Site'] = 'same-site'
    req.headers['TE'] = 'trailers'
    req.headers['Upgrade-Insecure-Requests'] = '1'

    with urlopen(req) as f:
        for i in f:
            i = i.strip()
            if i.startswith(lineheader):
                content = i[len(lineheader):-1].split(b'"',1)[0]
                unescaped = html.unescape(content.decode('utf8'))
                content = unescaped.encode('utf8')
                cache.set(url, content)
                return json.loads(content)

    raise ValueError('Unable to parse song data')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('--transpose', '-t', help='Transposes the chords of n semitones',
                        type=int, default=0)

    parser.add_argument('url', nargs='?')
    args = parser.parse_args()

    if args.url:
        print_tab(args.url, args.transpose)
    else:
        interactive()


def print_tab(url: str, transpose: int) -> None:
    data = get_data(url)

    # Remove useless crap
    data = data['store']['page']['data']['tab_view']

    try:
        a = typedload.load(data, TabView)
    except Exception:
        print(data)
        raise
    if a.meta:
        if isinstance(a.meta, list):
            for i in a.meta:
                i.print()
        else:
            a.meta.print()
    a.wiki_tab.print(transpose)


def search_tabs(query: str, filter: frozenset[SearchResultType]) -> list[SearchItem]:
    from urllib.parse import urlencode
    getparams =urlencode(
        {
            'search_type': 'title',
            'value': query}
    )
    data = get_data(f'https://www.ultimate-guitar.com/search.php?{getparams}')
    # Remove useless crap
    data = data['store']['page']['data']['results']
    songs = []
    for i in data:
        try:
            songs.append(typedload.load(i, SearchItem))
        except Exception:
            print('>>> ERROR', i)
    # Filter just guitar chords, for now
    return [i for i in songs if i.type in filter]


def interactive() -> None:
    commandlist = ['quit', 'search', 'transpose', 'load', 'urlopen']
    import readline
    import atexit

    def completer(text: str, state: int) -> Optional[str]:
        l = [i for i in commandlist if i.startswith(text)]
        try:
            return l[state] + ' '
        except IndexError:
            return None

    histfile = f'{Cache()._cachedir}/.history'

    readline.parse_and_bind('set editing-mode emacs')
    readline.parse_and_bind('tab: complete')
    readline.set_completer(completer)
    readline.set_history_length(1000)

    try:
        readline.read_history_file(histfile)
    except FileNotFoundError:
        pass
    atexit.register(readline.write_history_file, histfile)

    songs: list[SearchItem] = []
    transpose = 0

    while True:
        try:
            line = input('> ').strip()
        except KeyboardInterrupt:
            print('^C')
            continue
        except EOFError:
            print('quit')
            return
        try:
            if ' ' in line:
                cmd, rest = line.split(' ', 1)
                cmd = cmd.strip()
                rest = rest.strip()
            else:
                cmd = line
                rest = ''
        except Exception:
            cmd = 'help'

        match cmd:
            case 'urlopen':
                try:
                    print_tab(rest, transpose)
                except Exception as e:
                    print(e)
            case 'transpose':
                try:
                    transpose = int(rest)
                except Exception as e:
                    print(e)
                if transpose not in range(-12,12):
                    print("That's a weird transpose value!")
            case 'load':
                try:
                    index = int(rest)
                    url = songs[index].tab_url
                except Exception as e:
                    print(f'Unable to load this result: {e}')
                    continue
                print_tab(url, transpose)
            case 'search':
                try:
                    songs = search_tabs(rest, frozenset((SearchResultType.CHORDS, )))
                except Exception as e:
                    print(e)
                    continue
                for i, s in enumerate(songs):
                    print(i, s.song_name, s.artist_name)
            case 'quit':
                print('quit')
                return
            case _:
                print(f'Commands: {" ".join(commandlist)}')

if __name__ == '__main__':
    main()

