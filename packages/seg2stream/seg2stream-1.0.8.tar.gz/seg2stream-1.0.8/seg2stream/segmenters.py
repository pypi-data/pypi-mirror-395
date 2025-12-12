import re
from typing import Literal


class JioNLPSentenceSegmenter:
    """Copied from https://github.com/dongrixinyu/JioNLP."""

    def __init__(self, is_coarse=True):
        if is_coarse:
            self.puncts = {"。", "！", "？", "\n", "“", "”", "‘", "’"}
            self.split_pattern = re.compile("([。“”！？\n])")
        else:
            self.puncts = {
                "……",
                "\r\n",
                "，",
                "。",
                ";",
                "；",
                "…",
                "！",
                "!",
                "?",
                "？",
                "\r",
                "\n",
                "“",
                "”",
                "‘",
                "’",
                "：",
            }
            self.split_pattern = re.compile("([，：。;“”；…！!?？\r\n])")
        self.front_quote_list = {"“", "‘"}
        self.back_quote_list = {"”", "’"}

    def segment(self, text):
        tmp_list = self.split_pattern.split(text)
        final_sentences = []
        quote_flag = False

        for sent in tmp_list:
            if sent == "":
                continue

            if sent in self.puncts:
                if len(final_sentences) == 0:  # 文本起始字符是标点
                    if sent in self.front_quote_list:  # 起始字符是前引号
                        quote_flag = True
                    final_sentences.append(sent)
                    continue

                # 确保当前标点前必然有文本且非空字符串
                # 前引号较为特殊，其后的一句需要与前引号合并，而不与其前一句合并
                if sent in self.front_quote_list:
                    if final_sentences[-1][-1] in self.puncts:
                        # 前引号前有标点如句号、引号等，另起一句
                        final_sentences.append(sent)
                    else:
                        # 前引号之前无任何终止标点，与前一句合并
                        final_sentences[-1] = final_sentences[-1] + sent
                    quote_flag = True
                else:  # 非前引号，则与前一句合并
                    final_sentences[-1] = final_sentences[-1] + sent
                continue

            if len(final_sentences) == 0:  # 起始句且非标点
                final_sentences.append(sent)
                continue

            if quote_flag:  # 当前句子之前有前引号，须与前引号合并
                final_sentences[-1] = final_sentences[-1] + sent
                quote_flag = False
            else:
                if final_sentences[-1][-1] in self.back_quote_list:
                    # 此句之前是后引号，需要考察有无其他终止符，用来判断是否和前句合并
                    if len(final_sentences[-1]) <= 1:
                        # 前句仅一个字符，则合并
                        final_sentences[-1] = final_sentences[-1] + sent
                    else:  # 前句有多个字符
                        if final_sentences[-1][-2] in self.puncts:
                            # 有逗号等，则需要另起一句，该判断不合语文规范，但须考虑此情况
                            final_sentences.append(sent)
                        else:  # 前句无句号，则需要与前句合并
                            final_sentences[-1] = final_sentences[-1] + sent
                else:
                    final_sentences.append(sent)

        return final_sentences


def get_sentence_segmenter(
    method_name: Literal["jionlp", "pysbd", "stanza"] = "jionlp",
):
    try:
        match method_name:
            case "pysbd":
                import pysbd

                segmenter = pysbd.Segmenter(language="zh", clean=False)
                return lambda text: segmenter.segment(text)
            case "stanza":
                import stanza

                stanza.download("zh")
                segmenter = stanza.Pipeline(
                    "zh", processors="tokenize", download_method=None
                )
                return lambda text: [s.text for s in segmenter(text).sentences]
            case _:
                raise
    except:
        segmenter = JioNLPSentenceSegmenter(is_coarse=True)
        return lambda text: segmenter.segment(text)


def get_phrase_segmenter(
    method_name: Literal["jionlp", "regex"] = "regex",
):
    match method_name:
        case "jionlp":
            segmenter = JioNLPSentenceSegmenter(is_coarse=False)
            return lambda text: segmenter.segment(text)
        case _:
            seg_puncts = re.escape("。？！，；：.?!,;:")
            patern = re.compile(rf"^[\S\s]*?[{seg_puncts}]")

            def segment_fn(text):
                phrases = []
                while True:
                    match = patern.search(text)
                    if match is None:
                        break
                    phrases.append(match.group())
                    text = text[match.span()[1] :]
                if len(text) > 0:
                    phrases.append(text)
                return phrases

            return segment_fn


def get_rhythm_segmenter(model_path):
    try:
        from paddlespeech.t2s.frontend.zh_frontend import RhyPredictor

        detector = RhyPredictor(model_path)

        def segment_fn(text):
            rhythms = []
            pred = detector.get_prediction(text)
            bounds = re.sub("[%`~]", "", pred).split("$")[:-1]
            pi, last_s = 0, 0
            for idx, rhy in enumerate(bounds):
                for ci, char in enumerate(rhy):
                    pi = text.find(char, pi)
                    if idx >= 1 and ci == 0:
                        rhythms.append(text[last_s:pi])
                        last_s = pi
                    pi += 1
            rhythms.append(text[last_s:])
            return rhythms

        return segment_fn
    except:
        return None
