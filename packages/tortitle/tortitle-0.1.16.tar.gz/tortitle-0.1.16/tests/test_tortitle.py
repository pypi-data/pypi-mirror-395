import pytest

from tortitle import TorTitle

# Test cases formatted as a list of (input_string, expected_dictionary)
TEST_CASES = [
    (
        "The.Matrix.1999.1080p.BluRay.x264-GROUP",
        {
            "title": "The Matrix",
            "year": "1999",
            "type": "movie",
            "resolution": "1080p",
            "media_source": "encode",
            "group": "GROUP",
        },
    ),
    (
        "Breaking.Bad.S01E01.720p.BluRay.x264-GROUP",
        {
            "title": "Breaking Bad",
            "year": "",
            "type": "tv",
            "season": "S01",
            "episode": "E01",
            "seasons": [1],
            "episodes": [1],
            "resolution": "720p",
            "media_source": "encode",
            "group": "GROUP",
        },
    ),
    (
        "Inception.2010.1080p.BluRay.x264-GROUP",
        {"title": "Inception", "year": "2010", "type": "movie"},
    ),
    (
        "【囧妈】Lost.in.Russia.2020.WEB-DL.1080p.H264.AAC-CMCTV",
        {
            "title": "Lost in Russia",
            "cntitle": "",
            "year": "2020",
            "resolution": "1080p",
            "media_source": "webdl",
            "group": "CMCTV",
        },
    ),
    (
        "[The.Mandalorian].S01E01-E05.(2019).1080p.WEB-DL-GROUP",
        {
            "title": "The Mandalorian",
            "year": "2019",
            "type": "tv",
            "season": "S01",
            "episode": "E01-E05",
            "seasons": [1],
            "episodes": [1,2,3,4,5],
        },
    ),
    (
        "She's Got No Name 2025 2160p WEB-DL H265 DTS5.1-CHDWEB",
        {
            "title": "She's Got No Name",
            "year": "2025",
            "type": "movie",
            "audio": "DTS5.1",
        },
    ),
    (
        "[大陆][绝世天医][Jue Shi Tian Yi 2025 S01 1080p WEB-DL H.264 AAC-GodDramas]",
        {
            "title": "Jue Shi Tian Yi",
            "cntitle": "绝世天医",
            "year": "2025",
            "type": "tv",
            "season": "S01",
            "seasons": [1],
            "episode": "",
            "resolution": "1080p",
            "media_source": "webdl",
            "group": "GodDramas",
        },
    ),
    (
        "[TV][jsum@U2][我独自升级 第二季 -起于暗影-][Ore dake Level Up na Ken Season 2: Arise from the Shadow][1080p][TV 01-13(13-25) Fin+SP][MKV/BDRip][2025年01月]",
        {
            "title": "Ore dake Level Up na Ken", 
            "type": "tv",
            "seasons": [2]
        },
    ),
    (
        "[The.Movie.2023][1080p][BluRay]",
        {
            "title": "The Movie",
            "year": "2023",
            "resolution": "1080p",
            "media_source": "bluray",
        },
    ),
    (
        "[美剧][古战场传奇 第八季][Outlander.Blood.of.My.Blood.S08E03.School.of.the.Moon.2160p.STAN.WEB-DL.DDP5.1.HDR.H.265-NTb]",
        {
            "title": "Outlander Blood of My Blood",
            "cntitle": "古战场传奇",
            "year": "",
            "type": "tv",
            "season": "S08",
            "seasons": [8],
            "episode": "E03",
            "episodes": [3],
            "resolution": "2160p",
            "media_source": "webdl",
            "group": "NTb",
        },
    ),
    (
        "[瑞典][克拉克][Clark.S01.2160p.NF.WEB-DL.DD+5.1.H.265-playWEB]",
        {"title": "Clark", "cntitle": "克拉克", "year": ""},
    ),
    (
        "[大陆][光·渊][Justice.in.The.Dark.2023.S01.Complete.1080p.WOWOW.WEB-DL.H.264.AAC-UBWEB]",
        {
            "title": "Justice in The Dark",
            "cntitle": "光·渊",
            "year": "2023",
            "type": "tv",
            "season": "S01",
            "full_season": True,
            "episode": "",
            "resolution": "1080p",
            "media_source": "webdl",
            "group": "UBWEB",
        },
    ),
    # Standard Movie
    (
        "Iron.Man.2008.BluRay.1080p.x264.DTS-WiKi",
        {
            "title": "Iron Man",
            "cntitle": "",
            "year": "2008",
            "type": "movie",
            "season": "",
            "episode": "",
        },
    ),
    # Movie with Chinese Title
    (
        "[钢铁侠].Iron.Man.2008.BluRay.1080p.x264.DTS-WiKi",
        {
            "title": "Iron Man",
            "cntitle": "钢铁侠",
            "year": "2008",
            "type": "movie",
            "season": "",
            "episode": "",
        },
    ),
    # Standard TV Show
    (
        "The.Mandalorian.S01E01.2019.1080p.WEB-DL.DDP5.1.H264-NTb",
        {
            "title": "The Mandalorian",
            "cntitle": "",
            "year": "2019",
            "type": "tv",
            "season": "S01",
            "episode": "E01",
        },
    ),
    # TV Show with Chinese Title
    (
        "[曼达洛人].The.Mandalorian.E01-05.2019.1080p.WEB-DL.DDP5.1.H264-NTb",
        {
            "title": "The Mandalorian",
            "cntitle": "曼达洛人",
            "year": "2019",
            "type": "tv",
            "season": "S01",
            "episode": "E01-05",
            "episodes": [1,2,3,4,5]
        },
    ),
    # TV Show with Season only
    (
        "The.Terminal.List.S01.2022.1080p.AMZN.WEB-DL.DDP5.1.H.264-BlackTV",
        {
            "title": "The Terminal List",
            "cntitle": "",
            "year": "2022",
            "type": "tv",
            "season": "S01",
            "episode": "",
        },
    ),
    # Movie with long name and dots
    (
        "The.Lord.of.the.Rings.The.Fellowship.of.the.Ring.2001.EXTENDED.1080p.BluRay.x264-FSiHD",
        {
            "title": "The Lord of the Rings The Fellowship of the Ring",
            "cntitle": "",
            "year": "2001",
            "type": "movie",
            "season": "",
            "episode": "",
        },
    ),
    # Movie with year at the end
    (
        "1917.2019.1080p.BluRay.x264-SPARKS",
        {
            "title": "1917",
            "cntitle": "",
            "year": "2019",
            "type": "movie",
            "season": "",
            "episode": "",
        },
    ),
    # Movie with no clear year (should not find one)
    (
        "Top.Gun.Maverick.1080p.BluRay.x264-SPARKS",
        {
            "title": "Top Gun Maverick",
            "cntitle": "",
            "year": "",
            "type": "movie",
            "season": "",
            "episode": "",
        },
    ),
    # TV Show with Chinese title and season
    (
        "[终极名单].The.Terminal.List.S01.2022.1080p.AMZN.WEB-DL.DDP5.1.H.264-BlackTV",
        {
            "title": "The Terminal List",
            "cntitle": "终极名单",
            "year": "2022",
            "type": "tv",
            "season": "S01",
            "episode": "",
        },
    ),
    # Movie with brackets in title
    (
        "Zack.Snyders.Justice.League.2021.2160p.WEB-DL.DDP5.1.Atmos.DV.HEVC-CMRG",
        {
            "title": "Zack Snyders Justice League",
            "cntitle": "",
            "year": "2021",
            "type": "movie",
            "season": "",
            "episode": "",
        },
    ),
    # Another TV show format
    (
        "Game.of.Thrones.Season.1.Complete.1080p.BluRay.x264-CiNEFiLE",
        {
            "title": "Game of Thrones",
            "cntitle": "",
            "year": "",
            "type": "tv",
            "full_season": True,
            "season": "S01",
            "episode": "",
        },
    ),
    (
        "半暖时光.The.Memory.About.You.S01.2021.2160p.WEB-DL.AAC.H265-HDSWEB",
        {
            "title": "The Memory About You",
            "cntitle": "半暖时光",
            "year": "2021",
            "type": "tv",
            "season": "S01",
            "episode": "",
        },
    ),
    (
        "不惑之旅.To.the.Oak.S01.2021.2160p.WEB-DL.AAC.H265-HDSWEB",
        {
            "title": "To the Oak",
            "cntitle": "不惑之旅",
            "year": "2021",
            "type": "tv",
            "season": "S01",
            "episode": "",
        },
    ),
    (
        "Dinotrux S03E02 1080p Netflix WEB-DL DD 5.1 H.264-AJP69.mkv",
        {
            "title": "Dinotrux",
            "cntitle": "",
            "year": "",
            "type": "tv",
            "season": "S03",
            "seasons": [3],
            "episode": "E02",
            "episodes": [2]
        },
    ),
    (
        "排球女将.Moero.Attack.1979.Complete.WEB-DL.1080p.H264.DDP.MP3.Mandarin&Japanese-OPS",
        {
            "title": "Moero Attack",
            "cntitle": "排球女将",
            "year": "1979",
            "type": "tv",
            "full_season": True
        },
    ),
    (
        "【红钻级收藏版】蜘蛛侠：英雄归来.全特效+内封三版字幕.Spider-Man.Homecoming.2017.2160P.BluRay.X265.10bit.HDR.DHD.MA.TrueHD.7.1.Atmos.English&Mandarin-GYT.strm",
        {
            "title": "Spider Man Homecoming",
            "cntitle": "蜘蛛侠：英雄归来",
            "year": "2017",
            "type": "movie",
            "season": "",
            "episode": "",
        },
    ),
    (
        "21座桥-英语.21.Bridges.2019.BluRay.2160p.x265.10bit.HDR.mUHD-FRDS",
        {
            "title": "21 Bridges",
            "cntitle": "21座桥",
            "year": "2019",
            "type": "movie",
            "season": "",
            "episode": "",
        },
    ),
    (
        "13.Going.on.30.2004.Bluray.1080p.DTS.x264-CHD.strm",
        {
            "title": "13 Going on 30",
            "cntitle": "",
            "year": "2004",
            "type": "movie",
            "season": "",
            "episode": "",
        },
    ),
    (
        "X档案.第一季.1993.中英字幕￡CMCT梦幻",
        {
            "title": "X档案",
            "cntitle": "X档案",
            "year": "1993",
            "type": "tv",
            "season": "S01",
            "episode": "",
        },
    ),
    (
        "Taxi.4.Director's.Cut.2007.Bluray.1080p.x264.DD5.1-wwhhyy@Pter.mkv",
        {
            "title": "Taxi 4",
            "cntitle": "",
            "year": "2007",
            "type": "movie",
            "season": "",
            "episode": "",
        },
    ),
    (
        "豹.1963.JPN.1080p.意大利语中字￡CMCT风潇潇",
        {
            "title": "豹",
            "cntitle": "豹",
            "year": "1963",
            "type": "movie",
            "season": "",
            "episode": "",
        },
    ),
    (
        "金刚狼3殊死一战.Logan.2017.BluRay.1080p.x265.10bit.MNHD-FRDS",
        {
            "title": "Logan",
            "cntitle": "金刚狼3殊死一战",
            "year": "2017",
            "type": "movie",
            "season": "",
            "episode": "",
        },
    ),
    (
        "人工智能4K REMUX (2001)",
        {
            "title": "人工智能",
            "cntitle": "人工智能",
            "year": "2001",
            "type": "movie",
            "season": "",
            "episode": "",
        },
    ),
    (
        "1988 骗徒臭事多 Dirty Rotten Scoundrels 豆瓣：8.2（美国）",
        {
            "title": "Dirty Rotten Scoundrels",
            "cntitle": "骗徒臭事多",
            "year": "1988",
            "type": "movie",
            "season": "",
            "episode": "",
        },
    ),
    (
        "蝙蝠侠前传：黑暗骑士崛起4K REMUX（2012）",
        {
            "title": "蝙蝠侠前传：黑暗骑士崛起",
            "cntitle": "蝙蝠侠前传：黑暗骑士崛起",
            "year": "2012",
            "type": "movie",
            "season": "",
            "episode": "",
        },
    ),
    (
        "2001太空漫游4K REMUX",
        {
            "title": "2001太空漫游",
            "cntitle": "2001太空漫游",
            "year": "",
            "type": "movie",
            "season": "",
            "episode": "",
        },
    ),
    (
        "代号47 4K REMUX (2015)",
        {
            "title": "代号47",
            "cntitle": "代号47",
            "year": "2015",
            "type": "movie",
        },
    ),
    (
        "[日剧][高岭之花][Takanenohana][全10集][720p][国语][中文字幕]",
        {
            "title": "Takanenohana",
            "cntitle": "高岭之花",
            "type": "tv",
            "full_season": True
        }
    ),
    (
        "[大陆][沸腾的群山][The.Rise.of.Wanshan.2024.S01E18-E19.2160p.WEB-DL.HEVC.DDP.2Audios-QHstudIo]",
        {
            "title": "The Rise of Wanshan",
            "cntitle": "沸腾的群山",
            "type": "tv",
            "episode": "E18-E19",
            "episodes": [18, 19]
        }
        
    ),
    (
        "Jade Journey To Guangdong From East To North EP03 20250806 HDTV 1080i H264-HDHTV",
        {
            "title": "Journey To Guangdong From East To North",
            "type": "tv",
            "episode": "EP03",
            "episodes": [3],
            "full_season": False
        }
    ),
    (
        "[加拿大/美国/爱尔兰][爱尔兰之血][Irish.Blood.S01E04.Father.Al.1080p.AMZN.WEB-DL.DDP5.1.H.264-RAWR]",
        {
            "title": "Irish Blood",
            "cntitle": "爱尔兰之血",
            "type": "tv",
            "season": "S01",
            "seasons": [1],
            "episode": "E04",
            "episodes": [4],
            "full_season": False
        }
    ),
    (
        "1980.Star.Wars.Episode.V-.The.Empire.Strikes.Back.1920x816.BDRip.x264.DTS-HD.MA.strm",
        {
            "title": "1980 Star Wars Episode V The Empire Strikes Back",
            "year": "1980"
        }
    ),
    (
        "1979.Alien.1920x816.BDRip.x264.DTS-HD.MA.strm",
        {
            "title": "1979 Alien",
            "year": "1979"
        }
    ),
    (
        "Anpan.S01.1080p.KKTV.WEB-DL.AAC2.0.H.264-CHDWEB",
        {
            "title": "Anpan"
        }
    ),
    (
        "CCTV4.National.Memory.2018.HDTV.Subbed.MiniSD-TLF",
        {
            "title": "National Memory",
            "year": "2018"
        }
    ),
    (
        "CCTV6 The Hobbit An Unexpected Journey 2012 HDTV 1080i H264-HDSTV",
        {
            "title": "The Hobbit An Unexpected Journey",
            "year": "2012"
        }
    ),
    (
        "GDTV3 Formula 1 Heineken Dutch Grand Prix 2025 1080i HDTV H264 MP2-HDHTV",
        {
            "title": "Formula 1 Heineken Dutch Grand Prix",
            "year": "2025"
        }
    ),
    (
        "「 Resolution: Native 4K 」Interstellar 2014 IMAX 2160p BluRay x265 10bit TrueHD5.1-WiKi 星际穿越/ 星际启示录(港)/ 星际效应(台)/「马修·麦康纳 安妮·海瑟薇」*克里斯托弗·诺兰导演作品 *国英双语 *官译简繁英",
        {
            "title": "Interstellar",
            "year": '2014'
        }
    ),
    (
        "CCTV-4K Commemorating the 80th Anniversary of the Victory in the Chinese People's War of Resistance against Japanese Aggression and the World Anti-Fascist War 20250903 2160p 50fps UHDTV HEVC 10bit HLG DD5.1-QHstudIo",
        {
            "title": "Commemorating the 80th Anniversary of the Victory in the Chinese People's War of Resistance against Japanese Aggression and the World Anti Fascist War",
        }
    ),
    (
        "CCTV-8K CMG 2025 Spring Festival Gala 20250128 4320p 50fps UHDTV HEVC 10bit HLG MPEG-QHstudIo",
        {
            "title": "CMG 2025 Spring Festival Gala",
        }
    ),
    (
        "生化危机123合集 2002-2007",
        {
            "title": "生化危机123合集",
        }
    ),
    (
        "Tale.of.Tales.AKA.Il.racconto.dei.racconti.2015.1080p.USA.Blu-ray.AVC.DTS-HD.MA.5.1-CONSORTiUM",
        {
            "title": "Tale of Tales",
            "media_source": "bluray",
        }
    ),
    (
        "The.Coordinate.2025.S01.Complete.2160p.WEB-DL.HEVC.AAC-QHstudIo",
        {
            "title": "The Coordinate",
            "media_source": "webdl",
            "type": "tv",
            "full_season": True
        }
    ),
    (
        "KBS1 100 People Appraisal Show The Signature Live 20250806 HDTV 1080i AC3 MP2-TPTV",
        {
            "title": "100 People Appraisal Show The Signature Live",
        }
    ),
    (
        "除暴安良 (1977)",
        {
            "title": "除暴安良",
            "year": "1977",
        }
    ),
    (
        "新世界（2020）",
        {
            "title": "新世界",
            "cntitle": "新世界",
            "year": "2020",
            "type": "movie",
            "season": "",
            "episode": "",
        },
    ),
]


@pytest.mark.parametrize("input_string, expected_dict", TEST_CASES)
def test_title_parsing(input_string, expected_dict):
    """Tests that various torrent titles are parsed correctly."""
    tor_title = TorTitle(input_string)
    for key, value in expected_dict.items():
        assert (
            getattr(tor_title, key) == value
        ), f"Failed on key '{key}' for input '{input_string}'"

NON_MEDIA_TEST_CASES = [
    ("MyBook.epub", "ebook"),
    ("Another.Book.2023.pdf", "ebook"),
    ("[精装版]Some.Book.mobi", "ebook"),
    ("Some.Course.课件.zip", "ebook"),
    ("Artist - Album [FLAC] [24Bit-48kHz]", "music"),
    ("Some.Album.1999.CD.FLAC.cue", "music"),
    ("VA-Greatest.Hits.2024.MP3-GROUP", "music"),
    ("Artist - Album (2023) [SACD]", "music"),
    ("My.Archive.2023.rar", "other"),
    ("Another.File.zip", "other"),
    ("Backup.7z", "other"),
    ('Michael Jackson - The Mystery Of HIstory (1997) [FLAC]', 'music'),
    ('VA-Kill_Bill_Vol_2-(9362-48676-2)-CD-FLAC-2004', 'music'),
    ('Commodores - Caught In The Act (1975) [FLAC] {24-192 HDTracks}', 'music'),
    ('Aimer - DAWN (2015) {24bit, WEB} [FLAC]', 'music'),
    ("The.Matrix.1999.1080p.BluRay.x264-GROUP", "movie"),
    ('Dana Zemtsov & Anna Fedorova - Silhouettes 2020 DSF', 'music'),
    ('2002 - In Violet Light - \'15 Hi-Res @ 24~96 (flac)', 'music'),
    ('Lucile Boulanger - Bach & Abel_ Solo [FLAC 192kHz-24bit]', 'music'),
    ("[Some.Movie].2024.1080p.WEB-DL.mkv", "movie"),
    ('Sonata Arctica - Acoustic Adventures  - Volume One (2022)', 'music'),
    ('Mikhail Zemtsov, Hanna Shybayeva - Complete Works for Viola - Vol. 1 (2025) FLAC-CHDMusic', 'music'),
    ('Dog Trumpet - Shadowland - 2022 - FLAC分轨', 'music'),
    ('刘德华 - 暖暖柔情粤语精选 1992 WAV分轨 cjm4495@HDSCD', 'music'),
    ('Paul Weller - Modern Classics - The Greatest Hits 1998 - FLAC 分轨 - nbarock', 'music'),
    ("Private Tutor to the Duke's Daughter S01E10 2025 1080p CR WEB-DL H.264 AAC-FROGWeb", "tv"), 
    # ('Sara K.-No Cover-Chesky-0196', 'music'),
]

@pytest.mark.parametrize("input_string, expected_type", NON_MEDIA_TEST_CASES)
def test_non_media_type(input_string, expected_type):
    """Tests that non-media types are correctly identified."""
    tor_title = TorTitle(input_string)
    assert tor_title.type == expected_type, f"Failed on input '{input_string}'"