# BatteryHorse
Encode and decode text as English sentences. The name is inspired by this [xkcd comic](https://www.xkcd.com/936/).

## API
The batteryhorse module exposes three functions:

### encode_data(data: bytes) -> str
Encode the given data into one or more English phrases/sentences. Uses [Wordnet](https://wordnet.princeton.edu/) from the [NLTK](http://www.nltk.org/) library to create sentences in the following format: VERB NOUN ADJECTIVE CONJUNCTION ADJECTIVE. If the bytes can be encoded into fewer parts of speech then the rest will be truncated.

### decode_data(data: str, length: int) -> bytes
Decode a string of sentences or phrases back into the original bytes. Also requires the size of the output bytes

### create_secret(size=3: int) -> bytes
Creates a random passphrase by using random words from the Wordnet. Size specifies the number of words to use

## Examples
A basic example that encodes some data
```python
>>> import batteryhorse
>>> batteryhorse.encode_data(b'TEST')
'Unitise annum abasic'
```

An example showing encoding and decoding data
```python
>>> from hashlib import sha1
>>> import batteryhorse
>>> 
>>> digest = sha1('test'.encode('utf-8')).digest()
>>> 
>>> batteryhorse.encode_data(digest)
'Birdnest vara lobed or orthoptic. Wow fencing orthogonal yet anthropomorphic. Scranch rifadin anosmatic'
>>> 
>>> batteryhorse.decode_data('Birdnest vara lobed or orthoptic. Wow fencing orthogonal yet anthropomorphic. Scranch rifadin anosmatic', len(digest))
b'\xa9J\x8f\xe5\xcc\xb1\x9b\xa6\x1cL\x08s\xd3\x91\xe9\x87\x98/\xbb\xd3'
>>> print(digest)
b'\xa9J\x8f\xe5\xcc\xb1\x9b\xa6\x1cL\x08s\xd3\x91\xe9\x87\x98/\xbb\xd3'
```

## Command Line
BatteryHorse is also available on the command line.
```
  --encode         Accept data to be encoded from STDIN
  --decode         Accept data to be decoded from STDIN
  --generate       Generate a random secret
  --length LENGTH  Specify the length of secret or data to be decoded
```

And as an example
```bash
$ echo "TEST" | python -m batteryhorse --encode
Bare gyrostabilizer amygdaloidal
```

## Uses
The original intention of this library was to create a new way of sharing fingerprints of public keys.

## Limitations
Although Batteryhorse can encode data of arbitary lengths it does no padding of the data beforehand resulting in some sentences that may not be complete.

Additionally, since the length of the original data is not encoded the decode function must take the length as a parameter.