"""
This module provides a class to parse movie and series information from raw subtitle names.
"""
import re

# Dictionary to map Chinese numerals to integers
CHINESE_NUMERALS = {
    '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
    '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15, '十六': 16, '十七': 17, '十八': 18, '十九': 19, '二十': 20,
}

def chinese_to_arabic(s: str) -> int | None:
    """将中文数字字符串转换为整数。"""
    return CHINESE_NUMERALS.get(s)

def contains_cjk(str):
    """检查字符串是否包含中日韩字符。"""
    """
    主要CJK区块：

    CJK统一汉字：U+4E00-U+9FFF
    CJK统一汉字扩展A：U+3400-U+4DBF
    CJK统一汉字扩展B：U+20000-U+2A6DF
    CJK统一汉字扩展C：U+2A700-U+2B73F
    CJK统一汉字扩展D：U+2B740-U+2B81F
    CJK统一汉字扩展E：U+2B820-U+2CEAF

    韩文（한글/Hangul）专用区块：

    韩文字母：U+1100-U+11FF
    韩文兼容字母：U+3130-U+318F
    韩文音节：U+AC00-U+D7AF
    """
    return re.search(r'[\u4e00-\u9fa5\u3041-\u30fc\uAC00-\uD7AF]', str)

def split_by_language_boundary(text: str) -> list[str]:
    """
    在语言边界（例如英语和中日韩字符之间）分割字符串。

    该函数使用正则表达式查找两种模式：
    1. 可以由空格、冒号、点或连字符分隔的英文单词/数字序列（例如，“The Runarounds”，“Season 1”）。
    2. 中日韩字符序列（例如，“第一季”）。

    Args:
        text: 要分割的输入字符串。

    Returns:
        根据规则分割的字符串列表。
    """
    # 正则表达式：匹配一个英文词组（允许内部有空格和部分标点）且后面不跟中文，或者匹配一个非空格的词
    # pattern = r'[a-zA-Z0-9]+(?:[\s.:-]+[a-zA-Z0-9]+)*|[\u4e00-\u9fa5\u3041-\u30fc]+'
    pattern = r"[a-zA-Z0-9]+(?:[\s.:-]+[a-zA-Z0-9']+)*\b(?![\u4E00–\u9Fa5：，！.])|[^\s丨|\-/]+"
    
    return re.findall(pattern, text)

def split_by_isolate_space(text):
    """依空格分段，要求空格前非冒号、连字符或逗号。"""
    return re.split(r'(?<![:\-,])[\s]', text)

def contains_eng_word(str):
    """检查字符串是否包含至少两个字母的英文单词, 且单词前不紧邻中字。"""
    return re.search(r'(?<![一-鿆：，])[a-zA-Z]{2,}\b', str)

class TorSubtitle:
    """
    解析原始字幕字符串以提取标题、季和集信息。
    """
    def __init__(self, raw_name: str):
        """
        初始化 TorSubtitle 对象并解析原始名称。

        Args:
            raw_name: 来自字幕文件名或种子标题的原始字符串。
        """
        self.raw_name = raw_name  or  ""
        self.extitle = ""
        self.season = ""
        self.season_pos = 0
        self.episode = ""
        self.episode_pos = 0
        self.total_episodes = 0
        self.full_season = False
        self.tags = []
        self._parse()
        self.istv = self.season or self.episode or (self.total_episodes > 0)

    def _parse_season(self, name: str):
        # “第三季”、“Season 4”的模式
        season_pattern = r'(?:第([一二三四五六七八九十]+|[0-9]+)季|Season\s*([0-9]+))'
        match = re.search(season_pattern, name, re.IGNORECASE)
        if match:
            self.season_pos = match.span(0)[0]
            season_str = match.group(1) or match.group(2)
            if season_str.isdigit():
                self.season = int(season_str)
            else:
                self.season = chinese_to_arabic(season_str)

    def _parse_episode(self, name: str):
        # “第01集”、“第1-2集”、“第1-10集”、“全10集”的模式
        episode_pattern = r'(?:第?([0-9]+(?:-[0-9]+)?)[集回]|[全共]([0-9]+)[集回])'
        match = re.search(episode_pattern, name)
        if match:
            self.episode_pos = match.span(0)[0]
            episode_str = ""
            if match.group(1):  # “第1-2集”或“第1集”
                episode_str = match.group(1)
            elif match.group(2):  # “全10集”
                self.total_episodes = int(match.group(2))
                self.full_season = True
                # episode_str = f"1-{self.total_episodes}"

            if '-' in episode_str:
                parts = episode_str.split('-')
                start = parts[0].zfill(2)
                end = parts[1].zfill(2)
                self.episode = f"E{start}-E{end}"
            elif episode_str:
                self.episode = f"E{episode_str.zfill(2)}"

    def _parse_tags(self):
        if re.search(r"中字|\b简繁|[中简繁多][\w\||\\]*字幕|官译", self.raw_name):
            self.tags.append("中字")
        if re.search(r"特字\b|特效字幕", self.raw_name):
            self.tags.append("特效")
        if re.search(r"国[语語]|[中国粤]配|普通话|国\w*音轨", self.raw_name):
            self.tags.append("国语")

    def _part_clean(self, part_title: str) -> str:
        return part_title.strip()

    def _parse_extitle(self, name: str):
        self.extitle = ""
        processed_name = name.strip()

        # 包含这些的，直接跳过
        NOT_MOVIETV_PATTERN = r"0day破解|\[FLAC\]|\b无损\b|MQA编码|破解版\b|^剩余时间"
        if re.search(NOT_MOVIETV_PATTERN, processed_name, flags=re.I):
            return
        
        # 片名应在这些之前出现
        AFTER_NAME_PATTERN = r"\b([全共第].{1,5}[季集回]|导演|主演\b).*"
        processed_name = re.sub(AFTER_NAME_PATTERN, "", processed_name, flags=re.I).strip()
        if not processed_name:
            return

        # 开头的一些明确pattern，带上分隔符一起删
        PRE_CUT_PATTERN_LIST =[
            r"(\d+\s*年\s*\d+\s*月\s*\w*(番|\w漫)[\:：\s/\|]?|[陸港][剧劇]:?\s*经典台|^\w+高清频道|台湾\(区\)|\(新\)|^[\:：])",
             r"\b(\w{1,4}[剧劇]|\w*[日国动]漫|动画|片名|纪录片?|国创|\w+剧集|韩综|港綜)[\:：]",
        ]
        processed_name = re.sub("|".join(PRE_CUT_PATTERN_LIST), "", processed_name)
        # 开头的官方国语中字
        processed_name = re.sub(r"^(?:官方\s*|首发\s*|禁转\s*|独占\s*|限转\s*|国语\s*|中字\s*|特效\s*|DIY\s*)+\b", "", processed_name, flags=re.I).strip()

        # 分段后包含以下pattern，整段删
        SEG_REJECT_PATTERN_CN = [
            r"^(?:(\w+TV(\d+)?|Jade|TVB\w*|点播|翡翠台|\w*卫视|央视|电影|韩综)+)\b", r"[中央]\w+频道", r"\w+频道", r"\w+TV\w*高清", r"CHC高清\w+",
            r"点播\b", r"\w+字幕", r"简繁(\w+)?", 
            r"[\u2700-\u27BF]", # Unicode Block “Dingbats”
            r"\b(\w语|[中美英法德俄韩泰]国|南韩|印度|日本|瑞士|瑞典|挪威|大陆|香港|港台|新加坡|加拿大|爱尔兰|墨西哥|西班牙)\b", 
            r"\b(\w{1,2}[剧劇]|纪录片?)$",
            r"\b(热门|其他|正片|特辑|完结|无损)\b", 
            r"\b(杜比视界|\w{2}双语|中字|原盘|应求)", 
            r"\b(专辑|综艺|动画|国创|[日国动]漫|DIY)\b", 
            r"类[别型][:：]",
            r"(原盘|连载|赛季)\b", r"\b优惠剩余", "发种大赛", "蓝光大赏", "電影系列",
        ]
        SEG_REJECT_PATTERN_EN = [
            r"PTP Gold.*?corn", r"\bDIY\b", "\bChecked by ", r"(1080p|2160p|720p|4K\b|Max\b)", r"S\d+"
        ]
        reject_pattern_list = SEG_REJECT_PATTERN_CN + SEG_REJECT_PATTERN_EN
        reject_pattern = re.compile("|".join(reject_pattern_list), re.IGNORECASE)
        eng_pattern = re.compile("|".join(SEG_REJECT_PATTERN_EN), re.IGNORECASE)

        PART_CUT_PATTERN_LIST = [
            # r"\b(\w{1,3}剧|\w*[日国动]漫|动画|纪录片?|国创|澳大利亚剧|马来西亚剧|哥伦比亚剧|\w+剧集|韩综|港綜)[\:：]",
            # r"\b(\w{1,4}剧|\w*[日国动]漫|动画|纪录片?|国创|\w+剧集|韩综|港綜)[\:：]",
            # r"剧场版",
        ]
        part_clean_pattern = re.compile("|".join(PART_CUT_PATTERN_LIST), re.IGNORECASE)

        # 【】「」方括号内有特征词，则整个方括号不要了
        bracket_blocks = re.findall(r'[「【][^】」]*[】」]', processed_name)
        for block in bracket_blocks:
            if not re.search(r"[丨|]", block) and reject_pattern.search(block):
                processed_name = processed_name.replace(block, "", 1)

        # 以 特殊标点符 或 中英文段落 分 segments
        if re.search(r'[「」【】\[\]丨｜|/]', processed_name):
            segments = re.split(r'[「」【】\[\]丨｜|/]', processed_name)
        else:
            segments = split_by_language_boundary(processed_name)
        # clear empty segments
        segments = [p for p in segments if p.strip()]
        candidate_list = []
        # 3 段之内要见到 title，否则不要了
        for segment in segments[:3]:
            # 这一segment以此开头，就没戏了
            if re.match(r"^类型|类别|完结|导演|主演", segment.strip() ):
                # 保留英文标题
                if candidate_list:
                    self.extitle = candidate_list[0].strip()
                return 
            if contains_cjk(segment):
                # 分隔化为空格，再将空格合并
                segment = re.sub(r"[\)\(）（]", " ", segment)
                segment = re.sub(r"\s+", " ", segment).strip()
                if contains_eng_word(segment):
                    sub_parts = split_by_language_boundary(segment)
                else:
                    sub_parts = split_by_isolate_space(segment)
                    # sub_parts = re.split(r" ", segment)
                for spart in sub_parts[:3]:
                    # 包含 reject_pattern 的，跳过
                    spart = part_clean_pattern.sub("", spart)
                    if reject_pattern.search(spart.strip()):
                        continue
                    if not contains_cjk(spart) or spart.endswith(":"):
                        # 全英文，以 : 结尾的，等待最后再考虑
                        candidate_list.append(spart)
                        continue
                    self.extitle = spart.strip()
                    return
            else:
                # 一段[丨|/]分隔的仅包括英文的，
                if not eng_pattern.search(segment):
                        candidate_list.append(segment)

        # 保留英文标题
        if candidate_list:
            self.extitle = candidate_list[0].strip()
        return 

    def _parse(self):
        self._parse_season(self.raw_name)
        self._parse_episode(self.raw_name)
        process_name = self.raw_name
        positions = [p for p in [self.season_pos, self.episode_pos] if p > 0]
        if positions:
            cut_pos = min(positions)
            process_name = self.raw_name[:cut_pos]
        if contains_cjk(process_name):
            self._parse_extitle(process_name)
            self._parse_tags()

    def to_dict(self):
        return {
            "extitle": self.extitle,
            "season": self.season,
            "episode": self.episode,
            "total_episodes": self.total_episodes,
            "full_season": self.full_season,
        }

# For backward compatibility, we can keep a function that uses the class.
def parse_subtitle(name: str) -> str:
    return TorSubtitle(name).extitle
