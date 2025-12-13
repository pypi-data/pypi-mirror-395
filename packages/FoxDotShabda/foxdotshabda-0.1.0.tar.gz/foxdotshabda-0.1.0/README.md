# FoxDotShabda - Interface with shabda for audio samples and text speech

## Instalation

``` shell
pip install FoxDotShabda
# or
pip install git+https://codeberg.org/FoxDotExtensions/FoxDotShabda
```

## Usage

Import lib

``` python
from FoxDot.lib.Extensions.Shabda import samples, speech
```

### `samples(definition: str)`

Fetch random samples from [freesound](https://freesound.org/)

Any word can be a pack definition. If you want more than one sample,
separate words by a comma: `"blue,red"`

You can define how many variations of a sample to assemble by adding a colon
and a number.
e.g. blue,red:3,yellow:2 will produce one 'blue' sample, three 'red' samples
and two 'yellow' sample.

``` python
samples('bass:4,hihat:4,rimshot:2')
```

will print in the terminal when finished downloading

``` python
s1 >> loop('bass', dur=PDur(3,8), sample=2)
s2 >> loop('hihat', dur=10, sus=2)
s3 >> loop('rimshot', dur=PDur(7,9)*8, sample=2)
```

### `speech(words: str, language: str = 'en-GB', gender: str = 'f')`

Generate Text-to-Speech samples.

If you want more than one sample, separate words by a comma: `"hello,bye"`
If you want a sentence, separate it with `_`: `"eita_carai,oi"`

By default the language is `en-GB` but you can change this.

The gender of the voice unfortunately can be `f` and `m`.

If you only want to change the gender, use the following syntax

``` python
speech('baby', gender='m')
```

``` python
speech('what')
speech('voa,ai','pt-BR')
speech('eita_carai,continua','pt-BR','m')
```

will print in the terminal when finished downloading

``` python
v1 >> loop('eita_carai', dur=4, pan=[-5,0,1,0])
v2 >> loop('voa', dur=PDur(3,8), pan=[0,1,0,-5])
v3 >> loop('ai', dur=4, pan=[1,0,-5,0])
v4 >> loop('continua', dur=var([PDur(3,8), 6], [7,1]), pan=[0,1,0,-5])
v5 >> loop('what', dur=8, sus=2, pan=[0,1,0,-5])
```
