"""
This module provides the TorTitle class for parsing torrent names.
"""

import re
import os
from typing import List, Tuple, Dict, Any, Optional, Match

def cut_ext(torrent_name: str) -> str:
    """Removes the file extension from a torrent name."""
    if not torrent_name:
        return ''
    tortup = os.path.splitext(torrent_name)
    torext = tortup[1].lower()
    mvext = ['.strm', '.mkv', '.ts', '.m2ts', '.vob', '.mpg', '.mp4', '.3gp', '.mov', '.tp', '.zip', '.pdf', '.iso', '.ass', '.srt', '.7z', '.rar']
    if torext.lower() in mvext:
        return tortup[0].strip()
    else:
        return torrent_name

def delimer_to_space(input_string: str) -> str:
    """Replaces various delimiters in a string with spaces."""
    # add Chinese parentheses and full-width brackets to delimiters so they won't remain
    delimiters = ['[', ']', '.', '{', '}', '_', ',', '(', ')', '「', '」', '（', '）', '【', '】']
    for dchar in delimiters:
        input_string = input_string.replace(dchar, ' ')
    return input_string

def hyphen_to_space(input_string: str) -> str:
    """Replaces hyphens in a string with spaces."""
    return input_string.replace('-', ' ')

def contains_cjk(input_string: str) -> Optional[Match[str]]:
    """Checks if a string contains CJK characters."""
    return re.search(r'[\u4e00-\u9fa5\u3041-\u30fc]', input_string)

def cut_aka(title_string: str) -> str:
    """Cuts the 'AKA' part from a title string."""
    m = re.search(r'\s(/|AKA)\s', title_string, re.I)
    if m:
        title_string = title_string.split(m.group(0))[0]
    return title_string.strip()

def try_int(input_string: str) -> int:
    """Tries to convert a string to an integer, handling Chinese numerals."""
    cndigit = '一二三四五六七八九十'
    if input_string and input_string[0] in cndigit and len(input_string) == 1:
        return cndigit.index(input_string[0]) + 1
    try:
        return int(input_string)
    except (ValueError, TypeError):
        return 0

class TorTitle:
    """
    Parses a torrent name to extract details like title, year, season, episode, etc.
    """
    def __init__(self, name: str):
        self.raw_name: str = name or ""
        self.title: str = name or ""
        self.cntitle: str = ''
        self.year: str = ''
        self.type: str = 'movie'
        self.season: str = ''
        self.episode: str = ''
        self.seasons: List[int] = []
        self.episodes: List[int] = []
        self.media_source: str = ''
        self.group: str = ''
        self.resolution: str = ''
        self.video: str = ''
        self.audio: str = ''
        self.full_season: bool = False
        self.failsafe_title: str = self.title
        self.parse()

    def parse(self) -> None:
        """
        The main parsing logic to extract information from the torrent name.
        """
        self.raw_name = self.title.strip()

        self.resolution = self._parse_resolution(self.raw_name)
        self.media_source, self.video, self.audio = self._parse_media_info(self.raw_name)
        if not self.resolution and not self.video:
            self.type, match = self._check_non_media_type(self.raw_name)
            if match:
                return

        self._check_movie_tv_type(delimer_to_space(self.raw_name))

        self.title, self.cntitle = self._handle_bracket_title(self.title)
        self.title = self._prepare_title(self.title)

        self.group = self._parse_group(self.title)
        year_pos, self.year = self._extract_year(self.title)
        se_pos = self._extract_season_episode(self.title)
        self.failsafe_title = self.title
        self.title = self._cut_year_season(self.title, year_pos, se_pos)
        self.title = self._cut_keywords(self.title)

        if not self.cntitle:
            self.title, self.cntitle = self._extract_cn_title(self.title)
        self._polish_title()

    def _parse_media_info(self, torrent_name: str) -> Tuple[str, str, str]:
        """Parses media source, video and audio info from the torrent name."""
        media_source, video, audio = '', '', ''
        if m := re.search(r"(?<=(1080p|2160p)\s)(((\w+)\s+)?WEB(-DL)?)|\bWEB(-DL)?\b|\bHDTV\b|((UHD )?(BluRay|Blu-ray))", torrent_name, re.I):
            m0 = m[0].strip()
            if re.search(r'WEB[-]?(DL)?', m0, re.I):
                media_source = 'webdl'
            elif re.search(r'BLURAY|BLU-RAY', m0, re.I):
                if re.search(r'x26[45]', torrent_name, re.I):
                    media_source = 'encode'
                elif re.search(r'remux', torrent_name, re.I):
                    media_source = 'remux'
                else:
                    media_source = 'bluray'
            else:
                media_source = m0
        if m := re.search(r"AVC|HEVC(\s(DV|HDR))?|H\.?26[456](\s(HDR|DV))?|x26[45]\s?(10bit)?(HDR)?|DoVi (HDR(10)?)? (HEVC)?", torrent_name, re.I):
            video = m[0].strip()
        if m := re.search(r"DTS-HD MA \d.\d|LPCM\s?\d.\d|TrueHD\s?\d\.\d( Atmos)?|DDP[\s\.]*\d\.\d( Atmos)?|(AAC|FLAC)(\s*\d\.\d)?( Atmos)?|DTS(\s?\d\.\d)?|DD\+? \d\.\d", torrent_name, re.I):
            audio = m[0].strip()
        return media_source, video, audio

    def _parse_resolution(self, torrent_name: str) -> str:
        """Parses the resolution from the torrent name."""
        match = re.search(r'\b(4K|2160p|1080[pi]|720p|576p|480p)\b', torrent_name, re.A | re.I)
        if match:
            r = match.group(0).strip().lower()
            if r == '4k':
                r = '2160p'
            return r
        return ''

    def _parse_group(self, torrent_name: str) -> Optional[str]:
        """Parses the release group from the torrent name."""
        sstr = cut_ext(torrent_name)
        match = re.search(r'[@\-￡]\s?(\w+)(?!.*[@\-￡].*)$', sstr, re.I)
        return match.group(1).strip() if match else ''

    def _prepare_title(self, processing_title: str) -> str:
        """Prepares the title for further parsing."""
        processing_title = cut_ext(processing_title)
        processing_title = re.sub(r'^[「【][^】」]*[】」]', '', processing_title, flags=re.I).strip()
        processing_title = re.sub(r'^\w+TV-?(\d+)?([48]K)?\b', '', processing_title, flags=re.I).strip()
        processing_title = delimer_to_space(processing_title)
        return processing_title

    def _handle_bracket_title(self, processing_title: str) -> Tuple[str, str]:
        """Handles titles enclosed in brackets."""
        cn_title = ""
        if processing_title.startswith('[') and processing_title.endswith(']'):
            parts = [part.strip() for part in processing_title[1:-1].split('][') if part.strip()]
            keyword_pattern = r'1080p|2160p|4K|Web-?DL|720p|H\.?26[45]|x26[45]|全.{1,4}集'
            
            main_part = ''
            keyword_idx = -1
            for idx, part in enumerate(parts):
                if re.search(keyword_pattern, part, re.I):
                    keyword_idx = idx
                    main_part = part
                    break
            
            if main_part:
                if re.match(r'^' + keyword_pattern + '$', main_part, flags=re.I):
                    if keyword_idx > 0:
                        keyword_idx = keyword_idx - 1
                        processing_title = parts[keyword_idx]
                else:
                    processing_title = main_part
                if keyword_idx > 0 and contains_cjk(parts[keyword_idx-1]):
                    full_cn_title = parts[keyword_idx-1]
                    full_cn_title = re.sub(r'大陆|港台', '', full_cn_title, flags=re.I)
                    cn_title = full_cn_title.split(' ')[0].strip()
        return processing_title, cn_title

    def _extract_year(self, processing_title: str) -> Tuple[int, str]:
        """Extracts the year from the title."""
        _year_pos = 0
        year = ""
        potential_years = re.findall(r'(?<!\d{4}-)(19\d{2}|20\d{2})(?:\d{4})?\b', processing_title)
        if potential_years:
            year = potential_years[-1]
            _year_pos = processing_title.rfind(year)
        return _year_pos, year

    patterns = {
        's_e': r'\b(S(\d+))\s*(E(\d+)(-Ep?(\d+))?)\b',
        'season_only': r'(?<![a-zA-Z])(S(\d+)([\-\+]S?(\d+))?)\b(?!.*\bS\d+)',
        'season_word': r'\bSeason (\d+)\b',
        'ep_only': r'\bEp?(\d+)(-E?p?(\d+))?\b',
        'cn_season': r'第([一二三四五六七八九十]|\d+)季',
        'cn_episode': r'第([一二三四五六七八九十]+|\d+)集',
        'full_season': r'[全]\w{,4}\s*[集季]|\d+\s*集全|\d{4}\s*(S\d+\s*)?complete'
    }
    def _match_season(self, processing_title: str, match_key: Optional[str] = None) -> Any:
        """Matches season and episode patterns."""
        if match_key:
            return re.search(self.patterns[match_key], processing_title)
        
        for key, pattern in self.patterns.items():
            match = re.search(pattern, processing_title, flags=re.IGNORECASE)
            if match:
                return key, match
        return None, None

    def _check_movie_tv_type(self, processing_title: str) -> str:
        """Checks if the title is a TV show."""
        key, match = self._match_season(processing_title)
        self.type = 'tv' if match else 'movie'
        if self.type == 'tv':
            if key == 'full_season':
                self.full_season = True
            if re.search(r'complete', processing_title[match.span(0)[1]:], flags=re.I):
                self.full_season = True
        return self.type

    def _extract_season_episode(self, processing_title: str) -> int:
        """Extracts season and episode numbers."""
        se_pos = 0
        key, match = self._match_season(processing_title)
        if match:
            if key in ['s_e']:
                self.season = match.group(1)
                self.episode = match.group(3)
                self.seasons = [int(match.group(2))]
                if match.group(6):
                    self.episodes = list(range(int(match.group(4)), int(match.group(6)) + 1))
                    self.episode = match.group(3)
                else:
                    self.episodes = [int(match.group(4))]
            elif key == 'season_only':
                self.season = match.group(0)
                if match.group(4):
                    self.seasons = list(range(int(match.group(2)), int(match.group(4)) + 1))
                else:
                    self.seasons = [int(match.group(2))]
            elif key in ['season_word', 'cn_season']:
                season_int = try_int(match.group(1))
                self.seasons = [season_int]
                self.season = 'S' + str(season_int).zfill(2) if season_int else ''
            elif key in ['cn_episode', 'ep_only']:
                self.season = 'S01'
                self.seasons = [1]
                if match.group(3):
                    self.episodes = list(range(try_int(match.group(1)), try_int(match.group(3)) + 1))
                    self.episode = match.group(0)
                else:
                    self.episodes = [try_int(match.group(1))]
                    self.episode = match.group(0)
            elif key == 'full_season':
                self.full_season = True
    
            self.full_season = self.full_season or (self.season and not self.episode)
            se_pos = match.span(0)[0]
        return se_pos


    def _check_non_media_type(self, processing_title: str) -> str:
        """Checks if the title is a music or others."""
        patterns_ebook = [
            r'(pdf|epub|mobi|txt|chm|azw3|eBook-\w{4,8}|mobi|doc|docx).?$',
            r'(上下册|全.{1,4}册|精装版|修订版|第\d版|共\d本|文集|新修版|PDF版|课本|课件|出版社)',
        ]
        patterns_music = [
            r'(\b\d+ ?CD|(\[|\()\s*(16|24)\b|\-(44\.1|88.2|48|192)|24Bit|44\s*\]|FLAC.*(16|24|48|CUE|WEB|Album)|WAV.*CUE|CD.*FLAC|(\[|\()\s*FLAC)', 
            r'(\bVarious Artists|\bMQA\b|整轨|\b分轨|\b分軌|\b无损|\bLPCD|\bSACD|\bMP3|XRCD\d{1,3})',
            r'(\b|_)(FLAC.{0,3}|DSF.{0,3}|DSD(\d{1,3})?)$',
            r'\bVolume.*[\(\[]\d+[\)\]]$',
            r'\w+Music$', r'HDSCD$', r'Hi-?Res'
        ]
        pattern_game = [
            r'\b(PC|PS4|PS5|Switch|WiiU|XBOXONE|XBOX360|XBOXSeriesX|PSVita|PS3|PS2|PSP|3DS|DS)\b',
            r'\b(\w*Game|GOG|DINOByTES|RAZOR|TiNYiSO|RUNE|VACE|P2P|5play|\w*Know|KaOs|TENOKE|FitGirl)$'
        ]
        patterns_other = [
            r'(zip|7z|rar).?$',
        ]
        for pattern in patterns_ebook:
            match = re.search(pattern, processing_title, flags=re.IGNORECASE)
            if match:
                return 'ebook', match
        for pattern in patterns_music:
            match = re.search(pattern, processing_title, flags=re.IGNORECASE)
            if match:
                return 'music', match
        for pattern in pattern_game:
            match = re.search(pattern, processing_title, flags=re.IGNORECASE)
            if match:
                return 'game', match
        for pattern in patterns_other:
            match = re.search(pattern, processing_title, flags=re.IGNORECASE)
            if match:
                return 'other', match
        return '', None

    def _cut_year_season(self, processing_title: str, year_pos: int, se_pos: int) -> str:
        """Cuts the year and season part from the title."""
        positions = [p for p in [year_pos, se_pos] if p > 0]
        if not positions:
            if try_match := re.search(r"(\d+x\d+|BDRip|.26[45])", processing_title, flags=re.I):
                positions = [try_match.span(0)[0]]
        if positions:
            cut_pos = min(positions)
            processing_title = processing_title[:cut_pos]
            # remove trailing noise including ASCII and CJK parentheses/brackets and common separators
            processing_title = re.sub(r'[\s\._\-\(\)\（\）\[\]\{\}]+$', '', processing_title)
        return processing_title.strip()

    def _cut_keywords(self, processing_title: str) -> str:
        """Cuts keywords like resolution, source, etc. from the title."""
        tags = [
            '2160p', '1080p', '720p', '480p', 'BluRay', r'(4K)?\s*Remux',
            r'WEB-?(DL)?', r'(?<![a-z])4K', r'(?<=\w\s)BDMV',
        ]
        pattern = r'(' + '|'.join(tag for tag in tags) + r')\b.*$'
        processing_title = re.sub(pattern, '', processing_title, flags=re.IGNORECASE)
        return processing_title.strip()

    def _extract_cn_title(self, processing_title: str) -> Tuple[str, str]:
        """Extracts the Chinese title from the string."""
        cn_title = ""
        if contains_cjk(processing_title):
            cn_title = processing_title
            if m := re.search(r"([一-鿆]+[\-0-9a-zA-Z]*)[ :：]+([^一-鿆]+\b)", processing_title, flags=re.I):
                cn_title = cn_title[:m.span(1)[1]]
                processing_title = m.group(2)

            if m1 := re.match(r'^([^一-鿆]*)[\s\(\[]+[一-鿆]', cn_title, flags=re.I):
                cn_title = cn_title.replace(m1.group(1), '').strip()

            if cn_title:
                match = re.match(r'^([^ \-\(\[]*)', cn_title)
                if match:
                    cn_title = match.group()

        return processing_title.strip(), cn_title

    def _has_english_chars(self, str) -> bool:
        """Checks if the title contains English characters."""
        return bool(re.search('[a-zA-Z]', str))

    def _polish_title(self) -> None:
        """Polishes the final title by removing noise."""
        self.title = re.sub(r'[\._\+]', ' ', self.title)
        tags = [
            r'^Jade\b', r'^(KBS|SBS)\d*\b', r'^TVBClassic', r'CCTV\s*\d+(HD|\+)?', r'Top\s*\d+',
            r'\b\w+版', r'[全共]\d+集', 'BDMV',
            'COMPLETE', 'REPACK', 'PROPER', r'REMASTER\w*',
            'iNTERNAL', 'LIMITED', 'EXTENDED', 'UNRATED',
            r"Direct.{1,5}Cut"
        ]
        pattern = r'\b(' + '|'.join(tag for tag in tags) + r')\b'
        self.title = re.sub(pattern, '', self.title, flags=re.IGNORECASE)
        self.title = self.title.strip()

        self.title = hyphen_to_space(self.title)
        self.title = cut_aka(self.title)
        self.title = re.sub(r'\s+', ' ', self.title)

        if len(self.title) < 1: 
            self.title = self.failsafe_title
            if not self._has_english_chars(self.title) and self.cntitle:
                self.title = self.cntitle

    def to_dict(self) -> Dict[str, Any]:
        """Returns the parsed data as a dictionary."""
        return {
            'title': self.title,
            'cntitle': self.cntitle,
            'year': self.year,
            'type': self.type,
            'season': self.season,
            'episode': self.episode,
            'seasons': self.seasons,
            'episodes': self.episodes,
            'media_source': self.media_source,
            'group': self.group,
            'resolution': self.resolution,
            'video': self.video,
            'audio': self.audio,
            'full_season': self.full_season,
        }

def parse_tor_name(name: str) -> TorTitle:
    """
    Parses a torrent name and returns a TorTitle object.
    This is a convenience function.
    """
    return TorTitle(name)
