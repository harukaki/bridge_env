from bridge_env import Card, Hands, Suit

PBN_HANDS1 = \
    'N:4.KJ32.842.AQ743 JT987.Q876.AK5.2 AK532.T.JT6.T985 Q6.A954.Q973.KJ6'
JSON_HANDS1 = {'N': ['C3', 'C4', 'C7', 'CQ', 'CA', 'D2', 'D4', 'D8', 'H2', 'H3',
                     'HJ', 'HK', 'S4'],
               'E': ['C2', 'D5', 'DK', 'DA', 'H6', 'H7', 'H8', 'HQ', 'S7', 'S8',
                     'S9', 'ST', 'SJ'],
               'S': ['C5', 'C8', 'C9', 'CT', 'D6', 'DT', 'DJ', 'HT', 'S2', 'S3',
                     'S5', 'SK', 'SA'],
               'W': ['C6', 'CJ', 'CK', 'D3', 'D7', 'D9', 'DQ', 'H4', 'H5', 'H9',
                     'HA', 'S6', 'SQ']}
HANDS1 = Hands(north_hand={Card(4, Suit.S), Card(13, Suit.H), Card(11, Suit.H),
                           Card(3, Suit.H), Card(2, Suit.H), Card(8, Suit.D),
                           Card(4, Suit.D), Card(2, Suit.D), Card(14, Suit.C),
                           Card(12, Suit.C), Card(7, Suit.C), Card(4, Suit.C),
                           Card(3, Suit.C)},
               east_hand={Card(11, Suit.S), Card(10, Suit.S), Card(9, Suit.S),
                          Card(8, Suit.S), Card(7, Suit.S), Card(12, Suit.H),
                          Card(8, Suit.H), Card(7, Suit.H), Card(6, Suit.H),
                          Card(14, Suit.D), Card(13, Suit.D), Card(5, Suit.D),
                          Card(2, Suit.C)},
               south_hand={Card(14, Suit.S), Card(13, Suit.S), Card(5, Suit.S),
                           Card(3, Suit.S), Card(2, Suit.S), Card(10, Suit.H),
                           Card(11, Suit.D), Card(10, Suit.D), Card(6, Suit.D),
                           Card(10, Suit.C), Card(9, Suit.C), Card(8, Suit.C),
                           Card(5, Suit.C)},
               west_hand={Card(12, Suit.S), Card(6, Suit.S), Card(14, Suit.H),
                          Card(9, Suit.H), Card(5, Suit.H), Card(4, Suit.H),
                          Card(12, Suit.D), Card(9, Suit.D), Card(7, Suit.D),
                          Card(3, Suit.D), Card(13, Suit.C), Card(11, Suit.C),
                          Card(6, Suit.C)})

PBN_HANDS2 = \
    'E:KQ9752.K74.8742. T.A93.QT93.KJ873 J6.T852.AJ65.QT9 A843.QJ6.K.A6542'
JSON_HANDS2 = {'N': ['C2', 'C4', 'C5', 'C6', 'CA', 'DK', 'H6', 'HJ', 'HQ', 'S3',
                     'S4', 'S8', 'SA'],
               'E': ['D2', 'D4', 'D7', 'D8', 'H4', 'H7', 'HK', 'S2', 'S5', 'S7',
                     'S9', 'SQ', 'SK'],
               'S': ['C3', 'C7', 'C8', 'CJ', 'CK', 'D3', 'D9', 'DT', 'DQ', 'H3',
                     'H9', 'HA', 'ST'],
               'W': ['C9', 'CT', 'CQ', 'D5', 'D6', 'DJ', 'DA', 'H2', 'H5', 'H8',
                     'HT', 'S6', 'SJ']}
HANDS2 = Hands(north_hand={Card(14, Suit.S), Card(8, Suit.S), Card(4, Suit.S),
                           Card(3, Suit.S), Card(12, Suit.H), Card(11, Suit.H),
                           Card(6, Suit.H), Card(13, Suit.D), Card(14, Suit.C),
                           Card(6, Suit.C), Card(5, Suit.C), Card(4, Suit.C),
                           Card(2, Suit.C)},
               east_hand={Card(13, Suit.S), Card(12, Suit.S), Card(9, Suit.S),
                          Card(7, Suit.S), Card(5, Suit.S), Card(2, Suit.S),
                          Card(13, Suit.H), Card(7, Suit.H), Card(4, Suit.H),
                          Card(8, Suit.D), Card(7, Suit.D), Card(4, Suit.D),
                          Card(2, Suit.D)},
               south_hand={Card(10, Suit.S), Card(14, Suit.H), Card(9, Suit.H),
                           Card(3, Suit.H), Card(12, Suit.D), Card(10, Suit.D),
                           Card(9, Suit.D), Card(3, Suit.D), Card(13, Suit.C),
                           Card(11, Suit.C), Card(8, Suit.C), Card(7, Suit.C),
                           Card(3, Suit.C)},
               west_hand={Card(11, Suit.S), Card(6, Suit.S), Card(10, Suit.H),
                          Card(8, Suit.H), Card(5, Suit.H), Card(2, Suit.H),
                          Card(14, Suit.D), Card(11, Suit.D), Card(6, Suit.D),
                          Card(5, Suit.D), Card(12, Suit.C), Card(10, Suit.C),
                          Card(9, Suit.C)})

PBN_HANDS3 = 'W:KQT2.AT.J6542.85 - A8654.KQ5.T.QJT6 -'
HANDS3 = Hands(north_hand=set(),
               east_hand={Card(14, Suit.S), Card(8, Suit.S), Card(6, Suit.S),
                          Card(5, Suit.S), Card(4, Suit.S), Card(13, Suit.H),
                          Card(12, Suit.H), Card(5, Suit.H), Card(10, Suit.D),
                          Card(12, Suit.C), Card(11, Suit.C), Card(10, Suit.C),
                          Card(6, Suit.C)},
               south_hand=set(),
               west_hand={Card(13, Suit.S), Card(12, Suit.S), Card(10, Suit.S),
                          Card(2, Suit.S), Card(14, Suit.H), Card(10, Suit.H),
                          Card(11, Suit.D), Card(6, Suit.D), Card(5, Suit.D),
                          Card(4, Suit.D), Card(2, Suit.D), Card(8, Suit.C),
                          Card(5, Suit.C)})
