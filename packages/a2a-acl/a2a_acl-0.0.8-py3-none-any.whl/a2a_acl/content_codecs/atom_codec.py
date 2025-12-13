from a2a_acl.content_codecs.python_codec import PythonCodec

"""Atom codec is for literals reduced to a word, such as 'ping', or 'build'. 
Two agents using this codec to dialogue can be implemented in different languages.
 In the Python implementation of BDI agents, we use the 'Python Codec' to implement the Atom codec. """

codec_object = PythonCodec()
