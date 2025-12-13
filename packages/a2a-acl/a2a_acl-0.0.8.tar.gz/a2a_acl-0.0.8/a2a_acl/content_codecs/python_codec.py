import ast

from a2a_acl.content_codecs.common import BadFormat, Codec, python_codec_id


class PythonCodec(Codec):

    def __init__(self):
        super().__init__(python_codec_id)

    def extract_entry_point(self, s: str):
        (a, b) = self.decode(s)
        return a

    def decode(self, s: str):
        try:
            if "(" in s:
                (a, b) = s.split("(", 1)
                c = b.removesuffix(")")
                d = ast.literal_eval(c)
                return (a, d)
            else:
                return (s, None)
        except Exception:
            print("Failed to decode " + s)
            raise BadFormat


codec_object = PythonCodec()
