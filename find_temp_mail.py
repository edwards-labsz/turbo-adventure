#!/usr/bin/env python3
"""
Geometry Dash Level Uploader
Uploads one level with a configurable name scheme.
"""

import hashlib
import base64
import random
import requests

# ─────────────────────────────────────────────────────────────
# CONFIG — fill in your credentials before running
# ─────────────────────────────────────────────────────────────
ACCOUNT_ID   = 43360728          # your GD account ID (not userID)
USERNAME     = "iQd712r7BL"         # your in-game username
PASSWORD     = "Coolguy1"         # your plain-text GD password

CUSTOM_TITLE = "GIFT Flow CCCXCVI"         # base title (used in modes below)
# TITLE_MODE options:
#   "random"  → random word + roman numeral          (e.g. "Phantom CCXLII")
#   "custom"  → CUSTOM_TITLE exactly                 (e.g. "My Level")
#   "prefix"  → CUSTOM_TITLE + random roman numeral  (e.g. "My Level VIII")
#   "suffix"  → random word + CUSTOM_TITLE           (e.g. "Phantom My Level")
#   "full"    → CUSTOM_TITLE + random word + numeral (e.g. "My Level Phantom CCXLII")
TITLE_MODE   = "custom"

SONG_ID      = 599842     # primary custom song ID
SONG_ID_2    = 1          # secondary custom song ID (0 = none)
SFX_IDS      = "5853,14061"  # comma-separated SFX IDs
# ─────────────────────────────────────────────────────────────

GD_URL = "http://www.boomlings.com/database/uploadGJLevel21.php"

# A minimal valid GD 2.2 platformer level
LEVEL_STRING = (
    "H4sIAAAAAAAAA62cW4_cthmG_5B2wbNEFLmw3XrrAElRb2IHvhnU2WBb2C6KorCboD--PI1EzoF85OyFZ9arhx8P3yvylajVh3u9TPIgDir80wdl7UHK_KXyV_6lOdzIgztIIcRhPsiDtPFjCYWWg_xfDiCFYiHkFsLnkF8byfciRTSXQ7HUIYa51DmT2qRYnPD_3x_DXIwRix87JEbdsVe7I_aMirsaZufwXu7SviDh108Q5LKCd3ZnfoqWPMnAXtLb9OGZ1JPVt3P8yU4ifrn8ZabwmX-e06cqx_P_5BK_7rXPxyYZPnX6OR14ZtJnPipFhjKlMqYyoeb0SyPy15K_ZP4qBXJElYPpfEyXKt0U225yTJNjGpuL59ab3GCtcwGTv3JndK5d52pDZ-KXLH3KxVVpvMxdCV9_CC3wYdxCC-ykp1ibjTWGtoSPORC3c_h_KHcbjsfii51ULBWKWBXL6ADYeVpSyZNDpj40hXrjWdEgahkiWo6j2CEi_TiKGkdxY0SPETFE5nGQIXFt9PViE2Sr9KlEhahBoeHnIFB1RhpMSkqW9BPSYlJRsmiCkA6TGpOCkjhFOEMkQQsEndwFgjZmEPS6VA0GspAgOYUECS8kEFEmiTALCcReSHACZZKclIXEKUKTx7KTJCJe8DSz4GlmwdPMgqeZBU8zC55mFjzNLHiaWeg0s4xOYalmt61R9aIb3Ip1k03BTCzuTKUMfaXaisRg6TIhNSYdIOedpMe1U9DQujEIRn0WuyKCzuSIpNe0jaVqooyZKiO3Eg8QqbyQuHIitkICsWWyzGyEtJhcKKmxPDRQXCGxQHaQWO-kR5kko1RIMPKFBNnMcwcn-cSF2mlw3w0eTzPOkfdxpZr12J8U0mHS7yP7_qQhu_6kIbv-pCb7_qQhu_6kIbv-pBmlrt9ryK7fa3JEYrp9MVGOHM6RwzlyOEcO58jhHLmxh2zyjkl8cmB9kFRqCrpdEZHgNBacxoLTWHAaC05jwWksOI0Fp7GMNJWR2wXiVPYvVJ0I_13qW6TXFqxMWkwuO8m-UanJ_sJakYPFuib7BqAm-_ajIgf2oyb79rgm-5a7Jvs2viJxinCGSIIsBdUukLRR0V4rPJAKJ0fhhCssIoWFWe9DgPxwkoy7peNu8bhbPO4Wj7vF427xuFs8HVk8xVk8bfJJW-GYCrdTDfvupZnq25Aq7k1uoLh1S2LTD1pOv_zxg_3LDx9sXuritpEHt4QbcrDOJtJgct5JknbWF-WAHPmwihz4sIoc-LCNHPmwihz4sIoc-LCKHPiwjcQpwhkiCTK7QCxiDOKqkTANFqbBwjRYmAYL02BhGixMg4VpsDANFeZ4v7FJOqkb7Dc2JBkjsN9YkyiXYL-xIYnmxvuNeV3adkF2rEu56HZXZHfRzYbsLropf89CmrfO4gNqY7PQoH230KB9u1CjA6_UoH2T2qB9r1ajAwPYoH1X2aB9q9qgff9bozxZPFcoVRqTbh-J2ulw3x0fUMfT5HjyHZeU40Kt7-MiFJ1U9R1nhPJksWlF70VRAzTvluaDpXkKNE-s5nLRXIT13U2EohOmur9JSLAfKQXYmGpQTg6eM2nQ_sMrDdp_IiajUu1F-0_kNA3AZP92cF09J8nwS7svJulROfa07VRYJlJhmeRjfJxY_XZn_Ux7FmsvHxs8YtagXQffov2H4Wp08IRdgyIBWjz9SLUX5WcA65big6V4ChROrADb-O1UxWc11FYBnk1o1xU-WZINUynBTldBleQoeOywQft-pUW7fqVFu36lQft-pUW7fqVFu36lHSzwHM0R7frANlsoqtwZlWVL8mxJni3JsyV5tiTPVn1_CmmAo_x84WIhWZXjjc-29zgm0p8EO-MNivQnwd54ixL9SbA73qJEfxLsj7coEZUc75A3aeUkzyrYjZMK7EAVVAuOgocOWxQ8bHJE-6twjQ7W9gbtO4YG7VuWGh1YlgbtW-wG7Rv3Bu1fDtQoTxbPFUqVoKQa75s1JGmnGu_utbWTAVVgG7JFSfIV2DBtUCRUBbZ2m0ztQJFQBBafwAnQAidAC5wALXACtMAJ0PW2BZqB-VnFplU-ryvwFEKL8rOVbL1JDW4ct-hgYc2ox6gBTzy2KGmrAQ_FNOjIhdXowIXV6MCFVejIhdXowIXV6MCF1ejAhVUoTxbPFUmV9vtIrmpO8trZSeWxULXHQtUeC1V7LFTtsVC1x0LVHgtVeyxU7alQ9XjzshUAqh5sXrYoGiqwedmgLK1g87JFkQTHm5f5GYlqj2338xXV9sz-stvdl_1lN-fyFWX9V5dV9pgqJdaFPYCv__ntx3f3z799uHvzn59__dM3pwVUUyDXFd_TkuqKZkFO93dev_rz68-v7h4-Pjz75jSE9EsE1yguvh_EXA713b15fKNe_uvhxbP_fvfi-W_v3n7_-f2n17-dhpzdbd2wOYZUV0L-wzz-cPfx36GT4m93Pz6-v3uj3r39ctbK-D4fGvJX8_jjp5cihHz-8NPrz6ehtMSt-_6Fefyr8l9-uX_26dXLN1_e3_m_v3tx1tLqTSvNC12Sc6vfyoHfT0HI8if4YBur_EU4_qtjQpY_Hgd3eMrfyJA_5HGY9KDv9d8s4CfdEbk8ZczmeVP8NCMiZ6ql47NL_Pkdhmoqp-PWOd-UZaiiijreCUT3wSVHyanX3IrhV-0MBWffjqitueaGDaFmfK6mUVKTWa1NmMczmd8qsuQ3lgX5hZ-WUK5Mz2a9dxm9m4zFzDZT-7gG6IAu3q-wzgtOwqRInJxcCDkt8_HNaGGcbDjLJzHF96sdX4-WKtBnAWPH1oDyekAbAqrcKmsvBZVKzU2frvRGO6G22vW4O9rHLAgnU1tvYpOjik18ZVj4VKklpUHGx28t04vEnBGdBsnU3aoeG19BNs3x921-1GlRdTzurxw_eeGZWa-lEHfW1DNOw3huzCWNR-zGJMyuPUySvnpkvnrk5nK4LDpl0tG4sKx5VyUfR63F00RJv6p3lZnZ5FPiLMuFOK10giOJkoleK-ln7uonvbwwqkjdOj1PNlZWFo8oJu1FY09zxdWkIG-zWQvfMQnC-HVEVq1XvY2a27jj4JhrgxPxKUwosYzKA1piuwuxdZ5pvJArZyutmsunW1oko--cYjfq1yvK4-sVm4iWRNQo4nzaRAuaeDOOaElEPYoolVvWbjtzMZnmjJNkeMIVjg71KSNm4bcQ82mE6603JxEai3-DX0VGyHwxMCAri3-DXzBDyHwx0CdrO95vZ30xgEgH-l7Z8UGPKjuOSEX6vpnsUY82445IkvfauA-6VLtxhjoqkmLciUaLG2coOJsai01kWjw-QpWkUikWmyi1WGyEKqyr4puJWIsbZyjRgIuvDNZW3aaD612aekE9rtbquFyr8uq_GCl49Fx0vWcEirqkEWOTQVhv54CC3s_XnIXrlDvxDOdd3BYHl9bDdF6kaHGBkcfrjWwIz-40ZatVFWrWu2SdU3jjRPrMRuZ4kzX5Tr-VON4GPMa38UbWu7f2Qxp0kSxpuad2ci00l_Kh82ll9Npsrkc0jUqrotTNdUMye_Ki2atc3Vm-XazaX_V1x3JnEmPlTkUyKFUyvV1eXrparHMSUu6PNrG1oP6ia_FfWYlU1fVcLmjm29OiqxxPrreezpyX61nc9N41xiDenlBmMKyXRvQkbbScK1d80qxnUXWdWn5b3p9-epVYjs7do_GU7h3W_cOuf9h3D8cL7N5h2z-8dA9r2T_cHzTdHzVzZdTMul92emPh_3tB8jAAZAAA"
)

# ── word list ──────────────────────────────────────────────────
WORDS = [
    "able","about","above","act","add","age","air","all","also","and","any","are","art",
    "ask","back","bad","ball","band","bank","base","bear","beat","been","bell","best",
    "bird","black","blue","boat","body","bone","book","born","both","break","bring","brown",
    "burn","call","calm","came","camp","card","care","case","cast","cave","city","clam",
    "clan","clay","clip","coal","coat","code","coil","cold","come","cool","core","corn",
    "cost","cozy","crew","crop","crow","cure","dark","dash","date","dawn","days","dead",
    "deal","deep","deer","dell","deny","dew","diet","dirt","disk","dive","dock","does",
    "done","door","dote","down","draw","dream","drop","drum","dune","dusk","dust","duty",
    "each","earl","earn","east","edge","else","emit","even","ever","evil","exam","face",
    "fact","fade","fail","fair","fall","fame","farm","fast","fate","fear","feel","fell",
    "felt","fern","fill","film","find","fine","fire","firm","fish","fist","five","flag",
    "flat","flew","flip","flow","foam","foes","fold","folk","fond","font","food","fool",
    "foot","ford","form","fort","foul","four","free","from","fuel","full","fume","fund",
    "fury","fuse","gain","gale","game","gave","gaze","gear","gems","give","glee","glow",
    "glue","gnaw","goal","goes","gold","golf","gone","good","gore","grim","grip","grow",
    "gulf","hail","half","hall","hand","hang","hard","hare","harm","harp","have","hawk",
    "heal","heap","heat","heel","heir","held","helm","help","here","hero","hide","high",
    "hill","hint","hire","hold","hole","home","hope","horn","howl","huge","hull","hum",
    "hunt","hurl","hurt","icon","idea","idle","inch","into","iris","isle","jade","jail",
    "jeer","jest","join","jump","just","keen","kept","keys","kind","king","knew","know",
    "lace","lack","lake","land","lane","lark","last","late","lava","laws","lead","leaf",
    "lean","left","lend","lens","less","life","lift","like","limb","line","link","list",
    "live","loft","lone","long","look","loop","lore","lose","lost","loud","love","luck",
    "lush","made","mail","main","make","many","mark","mars","mast","maze","melt","mine",
    "mint","mist","mode","moon","more","moss","most","move","much","muse","must","name",
    "navy","near","neck","need","next","nice","nigh","nine","node","note","null","oath",
    "once","open","orbs","over","page","pale","palm","part","past","path","peak","peel",
    "peer","pine","pipe","plan","play","plot","plow","plum","poem","poll","pond","pool",
    "port","pour","prey","pull","pure","push","rack","raid","rail","rain","rank","rare",
    "rays","read","real","reed","reel","rely","rest","rich","ride","rift","ring","rise",
    "risk","road","roam","roar","robe","rock","rode","role","roll","roof","root","rose",
    "ruin","rule","rush","rust","safe","sage","sail","salt","sand","sang","sank","seal",
    "seam","seen","self","send","sent","sera","shed","ship","shoe","shot","show","side",
    "sign","silk","silt","sing","sink","site","size","skin","skip","slab","slow","smog",
    "snow","soar","soft","soil","sole","some","song","soul","span","spin","spit","spur",
    "star","stay","stem","step","stir","stop","strap","such","suit","sunlit","swap","tale",
    "tall","task","team","tear","tell","tend","tent","term","test","than","that","them",
    "then","they","thin","this","thorn","tide","till","time","tiny","toll","tomb","tone",
    "took","torn","town","trap","tree","trek","true","tune","turn","twin","upon","urge",
    "vale","vast","veil","very","view","vile","vine","void","volt","wade","wage","wait",
    "wake","walk","wall","wand","warm","warp","wash","wave","weld","well","went","were",
    "west","what","when","whip","wide","wild","will","wind","wing","wise","wish","with",
    "woke","wolf","wood","word","work","worn","wrap","writ","yard","year","yell","your",
    "zone","ember","azure","blaze","cascade","cobalt","crest","crimson","crystal","dusk",
    "eclipse","echo","epoch","fable","flare","flux","forge","fury","gale","glyph",
    "grace","grove","haven","hollow","hue","hymn","ink","ivory","jade","karma","knell",
    "lore","lotus","lumens","lunar","mantle","marble","mauve","mirror","mirage","monolith",
    "mural","myth","nexus","nimbus","novan","obsidian","omen","onyx","opus","orbit","origin",
    "ozone","paragon","petal","phantom","pillar","pinnacle","prism","pyre","quartz",
    "radiance","realm","relic","remnant","rift","rogue","rune","sable","sage","sanctum",
    "scarlet","shard","shiver","silo","slate","solace","sorrow","sovereign","specter",
    "spiral","spire","storm","stratum","surge","sylph","thorn","titan","tome","totem",
    "tower","trace","trance","transit","tundra","twilight","umbra","vault","vector",
    "verdant","verge","vessel","vigil","viper","virtue","vista","vivid","vortex","warden",
    "watcher","wavelet","whisper","wrath","wraith","zenith","zephyr",
]

# ── helpers ────────────────────────────────────────────────────

def to_roman(n: int) -> str:
    """Convert 0-1000 to Roman numeral (0 → 'N')."""
    if n == 0:
        return "N"
    val = [1000,900,500,400,100,90,50,40,10,9,5,4,1]
    sym = ["M","CM","D","CD","C","XC","L","XL","X","IX","V","IV","I"]
    result = ""
    for i, v in enumerate(val):
        while n >= v:
            result += sym[i]
            n -= v
    return result

def random_level_name() -> str:
    return f"{random.choice(WORDS).capitalize()} {to_roman(random.randint(0, 1000))}"

def build_level_name() -> str:
    if TITLE_MODE == "custom":
        return CUSTOM_TITLE or random_level_name()
    elif TITLE_MODE == "prefix":
        return f"{CUSTOM_TITLE} {to_roman(random.randint(0, 1000))}"
    elif TITLE_MODE == "suffix":
        return f"{random.choice(WORDS).capitalize()} {CUSTOM_TITLE}"
    elif TITLE_MODE == "full":
        return f"{CUSTOM_TITLE} {random_level_name()}"
    else:  # "random"
        return random_level_name()

def generate_gjp2(password: str) -> str:
    return hashlib.sha1((password + "mI29fmAnxgTs").encode()).hexdigest()

def xor_cipher(text: str, key: str) -> str:
    return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))

def generate_chk(values: list, key: str, salt: str = "") -> str:
    combined = "".join(str(v) for v in values) + salt
    hashed   = hashlib.sha1(combined.encode()).hexdigest()
    xored    = xor_cipher(hashed, key)
    return base64.urlsafe_b64encode(xored.encode()).decode()

def generate_upload_seed(data: str, chars: int = 50) -> str:
    if len(data) < chars:
        return data
    return data[::len(data) // chars][:chars]

# ── main ───────────────────────────────────────────────────────

def upload_level():
    if not ACCOUNT_ID or not USERNAME or not PASSWORD:
        print("⚠  Fill in ACCOUNT_ID, USERNAME, and PASSWORD at the top of the script first.")
        return

    level_name = build_level_name()
    print(f"📛  Level name : {level_name}")
    print(f"🎵  Song ID    : {SONG_ID}" + (f"  |  Song ID 2: {SONG_ID_2}" if SONG_ID_2 else ""))

    gjp2  = generate_gjp2(PASSWORD)
    seed  = generate_upload_seed(LEVEL_STRING)
    seed2 = generate_chk(values=[seed], key="41274", salt="xI25fpAapCQg")

    data = {
        "gameVersion":    22,
        "binaryVersion":  47,
        "accountID":      ACCOUNT_ID,
        "gjp2":           gjp2,
        "userName":       USERNAME,
        "levelID":        0,
        "levelName":      level_name,
        "levelVersion":   1,
        "levelLength":    5,        # Platformer
        "audioTrack":     0,        # 0 = custom song
        "auto":           0,
        "password":       1,
        "original":       145282824,
        "twoPlayer":      0,
        "songID":         SONG_ID,
        "objects":        555,
        "coins":          0,
        "requestedStars": 1,
        "unlisted":       0,
        "ldm":            0,
        "levelString":    LEVEL_STRING,
        "seed2":          seed2,
        "secret":         "Wmfd2893gb7",
        "wt":             0,
        "wt2":            0,
    }

    # Always send SFX; add second song only if set
    data["sfxIDs"] = SFX_IDS
    if SONG_ID_2:
        data["songIDs"] = f"{SONG_ID},{SONG_ID_2}"

    headers = {"User-Agent": ""}

    print("🚀  Uploading…")
    try:
        resp = requests.post(GD_URL, data=data, headers=headers, timeout=15)
        text = resp.text.strip()
        if text == "-1":
            print("❌  Server rejected the request (-1). Check your credentials and level string.")
        elif text.lstrip("-").isdigit() and int(text) > 0:
            print(f"✅  Level uploaded! Level ID: {text}")
        else:
            print(f"⚠  Unexpected response: {text}")
    except requests.RequestException as e:
        print(f"🔌  Request failed: {e}")

if __name__ == "__main__":
    upload_level()
