"""
Coding/decoding utilities (e.g. Base64).

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

import base64
import datetime
import enum
import json
import math
import re
from typing import Any, Callable

from .bits import mod_ceil, split_bits, join_bits
from .functools import deprecated

# yes, I know ItsDangerous implements that as well, but remember
# what happened with werkzeug.safe_str_cmp()? 
# see also: https://gitlab.com/wcorrales/quart-csrf/-/issues/1

def want_bytes(s: str | bytes, encoding: str = "utf-8", errors: str = "strict") -> bytes:
    """
    Force a string into its bytes representation.

    By default, UTF-8 encoding is assumed.
    """
    if isinstance(s, str):
        s = s.encode(encoding, errors)
    return s

def want_str(s: str | bytes, encoding: str = "utf-8", errors: str = "strict") -> str:
    """
    Convert a bytestring into a text string.
    
    By default, UTF-8 encoding is assumed.
    """
    if isinstance(s, bytes):
        s = s.decode(encoding, errors)
    return s


BASE64_TO_URLSAFE = str.maketrans('+/', '-_', ' ')

def want_urlsafe(s: str | bytes) -> str:
    """
    Force a Base64 string into its urlsafe representation.

    Behavior is unchecked and undefined with anything else than Base64 strings.
    In particular, this is NOT an URL encoder.

    Used by b64encode() and b64decode().
    """
    return want_str(s).translate(BASE64_TO_URLSAFE)

def want_urlsafe_bytes(s: str | bytes) -> bytes:
    """
    Shorthand for want_bytes(want_urlsafe(s)).
    """
    return want_bytes(want_urlsafe(s))

B32_TO_CROCKFORD = str.maketrans(
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567',
    '0123456789ABCDEFGHJKMNPQRSTVWXYZ',
    '=')

CROCKFORD_TO_B32 = str.maketrans(
    '0123456789ABCDEFGHJKMNPQRSTVWXYZ',
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567',
    '=')


BIP39_WORD_LIST = """
abandon ability able about above absent absorb abstract absurd abuse access accident account accuse achieve acid acoustic acquire across act action
actor actress actual adapt add addict address adjust admit adult advance advice aerobic affair afford afraid again age agent agree ahead aim air airport
aisle alarm album alcohol alert alien all alley allow almost alone alpha already also alter always amateur amazing among amount amused analyst anchor
ancient anger angle angry animal ankle announce annual another answer antenna antique anxiety any apart apology appear apple approve april arch
arctic area arena argue arm armed armor army around arrange arrest arrive arrow art artefact artist artwork ask aspect assault asset assist assume
asthma athlete atom attack attend attitude attract auction audit august aunt author auto autumn average avocado avoid awake aware away awesome
awful awkward axis baby bachelor bacon badge bag balance balcony ball bamboo banana banner bar barely bargain barrel base basic basket battle
beach bean beauty because become beef before begin behave behind believe below belt bench benefit best betray better between beyond bicycle bid
bike bind biology bird birth bitter black blade blame blanket blast bleak bless blind blood blossom blouse blue blur blush board boat body boil bomb
bone bonus book boost border boring borrow boss bottom bounce box boy bracket brain brand brass brave bread breeze brick bridge brief bright bring
brisk broccoli broken bronze broom brother brown brush bubble buddy budget buffalo build bulb bulk bullet bundle bunker burden burger burst bus
business busy butter buyer buzz cabbage cabin cable cactus cage cake call calm camera camp can canal cancel candy cannon canoe canvas canyon
capable capital captain car carbon card cargo carpet carry cart case cash casino castle casual cat catalog catch category cattle caught cause caution
cave ceiling celery cement census century cereal certain chair chalk champion change chaos chapter charge chase chat cheap check cheese chef cherry
chest chicken chief child chimney choice choose chronic chuckle chunk churn cigar cinnamon circle citizen city civil claim clap clarify claw clay clean clerk
clever click client cliff climb clinic clip clock clog close cloth cloud clown club clump cluster clutch coach coast coconut code coffee coil coin collect color
column combine come comfort comic common company concert conduct confirm congress connect consider control convince cook cool copper copy coral
core corn correct cost cotton couch country couple course cousin cover coyote crack cradle craft cram crane crash crater crawl crazy cream credit creek
crew cricket crime crisp critic crop cross crouch crowd crucial cruel cruise crumble crunch crush cry crystal cube culture cup cupboard curious current
curtain curve cushion custom cute cycle dad damage damp dance danger daring dash daughter dawn day deal debate debris decade december decide
decline decorate decrease deer defense define defy degree delay deliver demand demise denial dentist deny depart depend deposit depth deputy derive
describe desert design desk despair destroy detail detect develop device devote diagram dial diamond diary dice diesel diet differ digital dignity dilemma
dinner dinosaur direct dirt disagree discover disease dish dismiss disorder display distance divert divide divorce dizzy doctor document dog doll dolphin
domain donate donkey donor door dose double dove draft dragon drama drastic draw dream dress drift drill drink drip drive drop drum dry duck dumb
dune during dust dutch duty dwarf dynamic eager eagle early earn earth easily east easy echo ecology economy edge edit educate effort egg eight
either elbow elder electric elegant element elephant elevator elite else embark embody embrace emerge emotion employ empower empty enable enact
end endless endorse enemy energy enforce engage engine enhance enjoy enlist enough enrich enroll ensure enter entire entry envelope episode equal
equip era erase erode erosion error erupt escape essay essence estate eternal ethics evidence evil evoke evolve exact example excess exchange excite
exclude excuse execute exercise exhaust exhibit exile exist exit exotic expand expect expire explain expose express extend extra eye eyebrow fabric face
faculty fade faint faith fall false fame family famous fan fancy fantasy farm fashion fat fatal father fatigue fault favorite feature february federal fee
feed feel female fence festival fetch fever few fiber fiction field figure file film filter final find fine finger finish fire firm first fiscal fish fit fitness fix flag
flame flash flat flavor flee flight flip float flock floor flower fluid flush fly foam focus fog foil fold follow food foot force forest forget fork fortune forum
forward fossil foster found fox fragile frame frequent fresh friend fringe frog front frost frown frozen fruit fuel fun funny furnace fury future gadget gain
galaxy gallery game gap garage garbage garden garlic garment gas gasp gate gather gauge gaze general genius genre gentle genuine gesture ghost
giant gift giggle ginger giraffe girl give glad glance glare glass glide glimpse globe gloom glory glove glow glue goat goddess gold good goose gorilla
gospel gossip govern gown grab grace grain grant grape grass gravity great green grid grief grit grocery group grow grunt guard guess guide guilt
guitar gun gym habit hair half hammer hamster hand happy harbor hard harsh harvest hat have hawk hazard head health heart heavy hedgehog height
hello helmet help hen hero hidden high hill hint hip hire history hobby hockey hold hole holiday hollow home honey hood hope horn horror horse hospital
host hotel hour hover hub huge human humble humor hundred hungry hunt hurdle hurry hurt husband hybrid ice icon idea identify idle ignore ill illegal
illness image imitate immense immune impact impose improve impulse inch include income increase index indicate indoor industry infant inflict inform
inhale inherit initial inject injury inmate inner innocent input inquiry insane insect inside inspire install intact interest into invest invite involve iron island
isolate issue item ivory jacket jaguar jar jazz jealous jeans jelly jewel job join joke journey joy judge juice jump jungle junior junk just kangaroo keen
keep ketchup key kick kid kidney kind kingdom kiss kit kitchen kite kitten kiwi knee knife knock know lab label labor ladder lady lake lamp language
laptop large later latin laugh laundry lava law lawn lawsuit layer lazy leader leaf learn leave lecture left leg legal legend leisure lemon lend length lens
leopard lesson letter level liar liberty library license life lift light like limb limit link lion liquid list little live lizard load loan lobster local lock logic lonely
long loop lottery loud lounge love loyal lucky luggage lumber lunar lunch luxury lyrics machine mad magic magnet maid mail main major make mammal
man manage mandate mango mansion manual maple marble march margin marine market marriage mask mass master match material math matrix
matter maximum maze meadow mean measure meat mechanic medal media melody melt member memory mention menu mercy merge merit merry mesh
message metal method middle midnight milk million mimic mind minimum minor minute miracle mirror misery miss mistake mix mixed mixture mobile
model modify mom moment monitor monkey monster month moon moral more morning mosquito mother motion motor mountain mouse move movie
much muffin mule multiply muscle museum mushroom music must mutual myself mystery myth naive name napkin narrow nasty nation nature near neck
need negative neglect neither nephew nerve nest net network neutral never news next nice night noble noise nominee noodle normal north nose notable
note nothing notice novel now nuclear number nurse nut oak obey object oblige obscure observe obtain obvious occur ocean october odor off offer office
often oil okay old olive olympic omit once one onion online only open opera opinion oppose option orange orbit orchard order ordinary organ orient
original orphan ostrich other outdoor outer output outside oval oven over own owner oxygen oyster ozone pact paddle page pair palace palm panda
panel panic panther paper parade parent park parrot party pass patch path patient patrol pattern pause pave payment peace peanut pear peasant pelican
pen penalty pencil people pepper perfect permit person pet phone photo phrase physical piano picnic picture piece pig pigeon pill pilot pink pioneer pipe
pistol pitch pizza place planet plastic plate play please pledge pluck plug plunge poem poet point polar pole police pond pony pool popular portion
position possible post potato pottery poverty powder power practice praise predict prefer prepare present pretty prevent price pride primary print
priority prison private prize problem process produce profit program project promote proof property prosper protect proud provide public pudding pull
pulp pulse pumpkin punch pupil puppy purchase purity purpose purse push put puzzle pyramid quality quantum quarter question quick quit quiz quote
rabbit raccoon race rack radar radio rail rain raise rally ramp ranch random range rapid rare rate rather raven raw razor ready real reason rebel
rebuild recall receive recipe record recycle reduce reflect reform refuse region regret regular reject relax release relief rely remain remember remind
remove render renew rent reopen repair repeat replace report require rescue resemble resist resource response result retire retreat return reunion
reveal review reward rhythm rib ribbon rice rich ride ridge rifle right rigid ring riot ripple risk ritual rival river road roast robot robust rocket romance
roof rookie room rose rotate rough round route royal rubber rude rug rule run runway rural sad saddle sadness safe sail salad salmon salon salt salute
same sample sand satisfy satoshi sauce sausage save say scale scan scare scatter scene scheme school science scissors scorpion scout scrap screen
script scrub sea search season seat second secret section security seed seek segment select sell seminar senior sense sentence series service session
settle setup seven shadow shaft shallow share shed shell sheriff shield shift shine ship shiver shock shoe shoot shop short shoulder shove shrimp shrug
shuffle shy sibling sick side siege sight sign silent silk silly silver similar simple since sing siren sister situate six size skate sketch ski skill skin skirt
skull slab slam sleep slender slice slide slight slim slogan slot slow slush small smart smile smoke smooth snack snake snap sniff snow soap soccer
social sock soda soft solar soldier solid solution solve someone song soon sorry sort soul sound soup source south space spare spatial spawn speak
special speed spell spend sphere spice spider spike spin spirit split spoil sponsor spoon sport spot spray spread spring spy square squeeze squirrel
stable stadium staff stage stairs stamp stand start state stay steak steel stem step stereo stick still sting stock stomach stone stool story stove
strategy street strike strong struggle student stuff stumble style subject submit subway success such sudden suffer sugar suggest suit summer sun
sunny sunset super supply supreme sure surface surge surprise surround survey suspect sustain swallow swamp swap swarm swear sweet swift swim
swing switch sword symbol symptom syrup system table tackle tag tail talent talk tank tape target task taste tattoo taxi teach team tell ten tenant
tennis tent term test text thank that theme then theory there they thing this thought three thrive throw thumb thunder ticket tide tiger tilt timber time
tiny tip tired tissue title toast tobacco today toddler toe together toilet token tomato tomorrow tone tongue tonight tool tooth top topic topple torch
tornado tortoise toss total tourist toward tower town toy track trade traffic tragic train transfer trap trash travel tray treat tree trend trial tribe trick
trigger trim trip trophy trouble truck true truly trumpet trust truth try tube tuition tumble tuna tunnel turkey turn turtle twelve twenty twice twin twist
two type typical ugly umbrella unable unaware uncle uncover under undo unfair unfold unhappy uniform unique unit universe unknown unlock until
unusual unveil update upgrade uphold upon upper upset urban urge usage use used useful useless usual utility vacant vacuum vague valid valley valve
van vanish vapor various vast vault vehicle velvet vendor venture venue verb verify version very vessel veteran viable vibrant vicious victory video view
village vintage violin virtual virus visa visit visual vital vivid vocal voice void volcano volume vote voyage wage wagon wait walk wall walnut want
warfare warm warrior wash wasp waste water wave way wealth weapon wear weasel weather web wedding weekend weird welcome west wet whale
what wheat wheel when where whip whisper wide width wife wild will win window wine wing wink winner winter wire wisdom wise wish witness wolf
woman wonder wood wool word work world worry worth wrap wreck wrestle wrist write wrong yard year yellow you young youth zebra zero zone zoo
""".split()

BIP39_DECODE_MATRIX = {v[:4]: i for i, v in enumerate(BIP39_WORD_LIST)}

def cb32encode(val: bytes) -> str:
    '''
    Encode bytes in Crockford Base32.
    '''
    return want_str(base64.b32encode(val)).translate(B32_TO_CROCKFORD)

def cb32lencode(val: bytes) -> str:
    '''
    Encode bytes in Crockford Base32, lowercased.
    '''
    return want_str(base64.b32encode(val)).translate(B32_TO_CROCKFORD).lower()

def cb32decode(val: bytes | str) -> bytes:
    '''
    Decode bytes from Crockford Base32.
    '''
    return base64.b32decode(want_bytes(val).upper().translate(CROCKFORD_TO_B32) + b'=' * ((8 - len(val) % 8) % 8))

def b32lencode(val: bytes) -> str:
    '''
    Encode bytes as a lowercase base32 string, with trailing '=' stripped.
    '''
    return want_str(base64.b32encode(val)).rstrip('=').lower()

def b32ldecode(val: bytes | str) -> bytes:
    '''
    Decode a lowercase base32 encoded byte sequence. Padding is managed automatically.
    '''
    return base64.b32decode(want_bytes(val).upper() + b'=' * ((8 - len(val) % 8) % 8))

def b64encode(val: bytes, *, strip: bool = True) -> str:
    '''
    Wrapper around base64.urlsafe_b64encode() which also strips trailing '='.
    '''
    b = want_str(base64.urlsafe_b64encode(val))
    return b.rstrip('=') if strip else b

def b64decode(val: bytes | str) -> bytes:
    '''
    Wrapper around base64.urlsafe_b64decode() which deals with padding.
    '''
    val = want_urlsafe(val)
    return base64.urlsafe_b64decode(val.ljust(mod_ceil(len(val), 4), '='))

def rb64encode(val: bytes, *, strip: bool = True) -> str:
    '''
    Call base64.urlsafe_b64encode() with null bytes i.e. '\\0' padding to the start. Leading 'A' are stripped from result.
    '''
    b = want_str(base64.urlsafe_b64encode(val.rjust(mod_ceil(len(val), 3), '\0')))
    return b.lstrip('A') if strip else b

def rb64decode(val: bytes | str) -> bytes:
    '''
    Wrapper around base64.urlsafe_b64decode() which deals with padding.
    '''
    val = want_urlsafe(val)
    return base64.urlsafe_b64decode(val.rjust(mod_ceil(len(val), 4), 'A'))


B85_TO_Z85 = str.maketrans(
    '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~',
    '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#'
)
Z85_TO_B85 = str.maketrans(
    '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#',
    '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~'
)

if hasattr(base64, 'z85encode'):
    # Python >=3.13
    def z85encode(val: bytes) -> str:
        return want_str(base64.z85encode(val))
    z85decode = base64.z85decode
else:
    # Python <=3.12
    def z85encode(val: bytes) -> str:
        return want_str(base64.b85encode(val)).translate(B85_TO_Z85)
    def z85decode(val: bytes | str) -> bytes:
        return base64.b85decode(want_str(val).translate(Z85_TO_B85))

def b2048encode(val: bytes) -> str:
    '''
    Encode a bytestring using the BIP-39 wordlist.
    '''
    return ' '.join(BIP39_WORD_LIST[x] for x in split_bits(val, 11))


def b2048decode(val: bytes | str, *, strip = True) -> bytes:
    """
    Decode a BIP-39 encoded string into bytes.
    """
    try:
        words = [BIP39_DECODE_MATRIX[x[:4]] for x in re.sub(r'[^a-z]+', ' ', want_str(val).lower()).split()]
    except KeyError:
        raise ValueError('illegal character')
    b = join_bits(words, 11)
    if strip:
        assert b[math.ceil(len(words) * 11 / 8):].rstrip(b'\0') == b''
        b = b[:math.ceil(len(words) * 11 / 8)]
    return b
    

def _json_default(func = None) -> Callable[Any, str | list | dict]:
    def default_converter(obj: Any) -> str | list | dict:
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif callable(func):
            return func(obj)
        else:
            raise TypeError
    return default_converter

def jsonencode(obj: dict, *, skipkeys: bool = True, separators: tuple[str, str] = (',', ':'), default: Callable | None = None, **kwargs) -> str:
    '''
    json.dumps() but with stricter and smarter defaults, i.e. no whitespace in separators, and encoding dates as ISO strings.
    '''
    return json.dumps(obj, skipkeys=skipkeys, separators=separators, default=_json_default(default), **kwargs)

jsondecode: Callable[Any, dict] = deprecated('just use json.loads()')(json.loads)

def ssv_list(s: str, *, sep_chars = ',;') -> list[str]:
    """
    Parse values from a Space Separated Values (SSV) string.

    By default, values are split on spaces, commas (,) and semicolons (;), configurable
    with sepchars= argument.

    Double quotes (") can be used to allow spaces, commas etc. in values. Doubled double
    quotes ("") are parsed as literal double quotes.

    Useful for environment variables: pass it to ConfigValue() as the cast= argument.
    """
    sep_re = r'\s+|\s*[' + re.escape(sep_chars) + r']\s*'
    parts = s.split('"')
    parts[::2] = [re.split(sep_re, x) for x in parts[::2]]
    l: list[str] = parts[0].copy()
    for i in range(1, len(parts), 2):
        p0, *pt = parts[i+1]
        # two "strings" sandwiching each other case
        if i < len(parts)-2 and parts[i] and parts[i+2] and not p0 and not pt:
            p0 = '"'
        l[-1] += ('"' if parts[i] == '' else parts[i]) + p0
        l.extend(pt)
    if l and l[0] == '':
        l.pop(0)
    if l and l[-1] == '':
        l.pop()
    return l

def twocolon_list(s: str | None) -> list[str]:
    """
    Parse a string on a single line as multiple lines, each line separated by double colon (::).

    Returns a list.
    """
    if not s:
        return []
    return [x.strip() for x in s.split('::')]

def quote_css_string(s):
    """Quotes a string as CSS string literal.
    
    Source: libsass==0.23.0"""
    return "'" + ''.join(('\\%06x' % ord(c)) for c in s) + "'"

class StringCase(enum.Enum):
    """
    Enum values used by regex validators and storage converters.

    AS_IS = case sensitive
    LOWER = case insensitive, force lowercase
    UPPER = case insensitive, force uppercase
    IGNORE = case insensitive, leave as is, use lowercase in comparison
    IGNORE_UPPER = same as above, but use uppercase in comparison
    """
    AS_IS = 0
    LOWER = FORCE_LOWER = 1
    UPPER = FORCE_UPPER = 2
    ## difference between above and below is in storage and representation
    IGNORE_LOWER = IGNORE = 3
    IGNORE_UPPER = 4

    def transform(self, s: str) -> str:
        match self:
            case self.AS_IS:
                return s
            case self.LOWER | self.IGNORE_LOWER:
                return s.lower()
            case self.UPPER | self.IGNORE_UPPER:
                return s.upper()

    def compile(self, exp: str) -> re.Pattern:
        r_flags = 0
        if self in (self.IGNORE, self.IGNORE_UPPER):
            r_flags |= re.IGNORECASE
        return re.compile(exp, r_flags)
        

__all__ = (
    'cb32encode', 'cb32decode', 'b32lencode', 'b32ldecode', 'b64encode', 'b64decode', 'jsonencode'
    'StringCase', 'want_bytes', 'want_str', 'jsondecode', 'ssv_list', 'twocolon_list', 'want_urlsafe', 'want_urlsafe_bytes',
    'z85encode', 'z85decode'
)