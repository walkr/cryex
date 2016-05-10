POLONIEX_REPAIRS = {
    "1cr": "1CR",
    "aby": "ABY",
    "adn": "ADN",
    "amp": "AMP",
    "arch": "ARCH",
    "bbr": "BBR",
    "bcn": "BCN",
    "bcy": "BCY",
    "bela": "BELA",
    "bitcny": "BITCNY",
    "bits": "BITS",
    "bitusd": "BITUSD",
    "blk": "BLK",
    "block": "BLOCK",
    "btcd": "BTCD",
    "btm": "BTM",
    "bts": "BTS",
    "burst": "BURST",
    "c2": "C2",
    "cga": "CGA",
    "clam": "CLAM",
    "cnmt": "CNMT",
    "cure": "CURE",
    "dash": "DASH",
    "dgb": "DGB",
    "diem": "DIEM",
    "doge": "DOGE",
    "emc2": "EMC2",
    "eth": "ETH",
    "exe": "EXE",
    "exp": "EXP",
    "fct": "FCT",
    "fibre": "FIBRE",
    "fldc": "FLDC",
    "flo": "FLO",
    "flt": "FLT",
    "gap": "GAP",
    "gemz": "GEMZ",
    "geo": "GEO",
    "gmc": "GMC",
    "grc": "GRC",
    "grs": "GRS",
    "huc": "HUC",
    "hyp": "HYP",
    "hz": "HZ",
    "index": "INDEX",
    "ioc": "IOC",
    "lqd": "LQD",
    "ltbc": "LTBC",
    "ltc": "LTC",
    "maid": "MAID",
    "mcn": "MCN",
    "mil": "MIL",
    "mint": "MINT",
    "mmc": "MMC",
    "mmnxt": "MMNXT",
    "mrs": "MRS",
    "myr": "MYR",
    "naut": "NAUT",
    "nav": "NAV",
    "nbt": "NBT",
    "neos": "NEOS",
    "nmc": "NMC",
    "nobl": "NOBL",
    "note": "NOTE",
    "noxt": "NOXT",
    "nsr": "NSR",
    "nxt": "NXT",
    "omni": "OMNI",
    "piggy": "PIGGY",
    "pink": "PINK",
    "pot": "POT",
    "ppc": "PPC",
    "pts": "PTS",
    "qbk": "QBK",
    "qora": "QORA",
    "qtl": "QTL",
    "rads": "RADS",
    "rby": "RBY",
    "rdd": "RDD",
    "ric": "RIC",
    "sc": "SC",
    "sdc": "SDC",
    "silk": "SILK",
    "sjcx": "SJCX",
    "str": "STR",
    "swarm": "SWARM",
    "sync": "SYNC",
    "sys": "SYS",
    "unity": "UNITY",
    "via": "VIA",
    "vrc": "VRC",
    "vtc": "VTC",
    "wdc": "WDC",
    "xbc": "XBC",
    "xc": "XC",
    "xch": "XCH",
    "xcn": "XCN",
    "xcp": "XCP",
    "xcr": "XCR",
    "xdn": "XDN",
    "xdp": "XDP",
    "xem": "XEM",
    "xmg": "XMG",
    "xmr": "XMR",
    "xpb": "XPB",
    "xpm": "XPM",
    "xrp": "XRP",
    "xst": "XST",
    "xvc": "XVC",
    "yacc": "YACC",
}


def update():
    new_pairs = {}

    # Add *_BTC pair
    for down, up in POLONIEX_REPAIRS.items():
        new_key = '_'.join((down, 'btc'))
        new_value = '_'.join(('BTC', up))
        new_pairs[new_key] = new_value

    # Add *_USD pair
    for down in ['btc', 'eth', 'ltc', 'xmr', 'dash', 'xrp', 'nxt', 'str']:
        up = down.upper()
        new_key = '_'.join((down, 'usd'))
        new_value = '_'.join(('USDT', up))
        new_pairs[new_key] = new_value

    POLONIEX_REPAIRS.update(new_pairs)

update()
