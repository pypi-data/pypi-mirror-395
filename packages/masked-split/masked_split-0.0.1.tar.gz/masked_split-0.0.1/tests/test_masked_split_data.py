get_delim_locations = [
        ['Hello, how are you? I\'m doing great! Thank you.', ['.', '!', '?'], [[18, '?'], [35, '!'], [46, '.']]],
        ]

filter_out_nodes = [
        [[18, 35, 46], [[24, 39]], [18, 46]],
        [[0, 18, 35, 46], [[10, 18], [40, 47]], [0, 35]],
        ]

get_mask_locations = [
        ['\"Thank you!\" Josh said. \"But no thank you!\"', [['\"', '\"']], [[0, 11], [24, 42]]],
        ]

masked_split = [
        ['\"Thank you!\" Josh said. But he was still pissed. \"But no thank you!\"', [['\"', '\"']], ['.'], 'left', False, True, ['\"Thank you!\" Josh said.', ' But he was still pissed.', ' \"But no thank you!\"']],
        ['\"Thank yocdu!\" Josh scdaid. \"But no thcdank you!\"', [['\"', '\"'], ['\'', '\'']], ['.', '!', '?', 'cd'], 'left', False, True, ['\"Thank yocdu!\" Josh scd', 'aid.', ' \"But no thcdank you!\"']],
        ['\"Thank you!\" Josh said. \"But no thank you!\"', [['\"', '\"'], ['\'', '\'']], ['.', '!', '?'], 'left', False, True, ['\"Thank you!\" Josh said.', ' \"But no thank you!\"']],
        ['\"Thank yocdu!\" Josh scdaid. \"But no thcdank you!\"', [['\"', '\"'], ['\'', '\'']], ['.', '!', '?', 'cd'], 'independent', False, True, ['\"Thank yocdu!\" Josh s', 'cd', 'aid', '.', ' \"But no thcdank you!\"']],
        ['\"Thank yocdu!\" Josh scdaid. \"But no thcdank you!\"', [['\"', '\"'], ['\'', '\'']], ['.', '!', '?', 'cd'], 'right', False, True, ['\"Thank yocdu!\" Josh s', 'cdaid', '. \"But no thcdank you!\"']],
        ['\"Thank yocdu!\" Josh scdaid. \"But no thcdank you!\"', [['\"', '\"'], ['\'', '\'']], ['.', '!', '?', 'cd'], 'none', False, True, ['\"Thank yocdu!\" Josh s', 'aid', ' \"But no thcdank you!\"']],
        ['\"Thank you!\" Josh said. But he was still pissed. \"But no thank you!\"', [['\"', '\"']], ['.'], 'left', True, True, ['\"Thank you!\" Josh said.', 'But he was still pissed.', '\"But no thank you!\"']],
        ['\"Thank yocdu!\" Josh scdaid. \"But no thcdank you!\"', [['\"', '\"'], ['\'', '\'']], ['.', '!', '?', 'cd'], 'left', True, True, ['\"Thank yocdu!\" Josh scd', 'aid.', '\"But no thcdank you!\"']],
        ['\"Thank you!\" Josh said. \"But no thank you!\"', [['\"', '\"'], ['\'', '\'']], ['.', '!', '?'], 'left', True, True, ['\"Thank you!\" Josh said.', '\"But no thank you!\"']],
        ['\"Thank yocdu!\" Josh scdaid. \"But no thcdank you!\"', [['\"', '\"'], ['\'', '\'']], ['.', '!', '?', 'cd'], 'independent', True, True, ['\"Thank yocdu!\" Josh s', 'cd', 'aid', '.', '\"But no thcdank you!\"']],
        ['\"Thank yocdu!\" Josh scdaid. \"But no thcdank you!\"', [['\"', '\"'], ['\'', '\'']], ['.', '!', '?', 'cd'], 'right', True, True, ['\"Thank yocdu!\" Josh s', 'cdaid', '. \"But no thcdank you!\"']],
        ['\"Thank yocdu!\" Josh scdaid. \"But no thcdank you!\"', [['\"', '\"'], ['\'', '\'']], ['.', '!', '?', 'cd'], 'none', True, True, ['\"Thank yocdu!\" Josh s', 'aid', '\"But no thcdank you!\"']],
        ["{?PLAYER.GENDER}Sister{?}Brother{\\?}{}... It's been three days", [['\"', '\"'], ['\'', '\''], ['{', '}'], ], ['...', '.', '!', '?'], 'left', False, True, ['{?PLAYER.GENDER}Sister{?}Brother{\\?}{}...', ' It\'s been three days']],
        ["{?PLAYER.GENDER}Sister{?}Brother{\\?}... It's been three days", [['\"', '\"'], ['\'', '\''], ['{', '}']], ['...', '.', '!', '?'], 'left', False, True, ['{?PLAYER.GENDER}Sister{?}Brother{\\?}...', ' It\'s been three days']],
        ["\"I'm Bob.\" He said. \"I'm Jill.\" She replied.", [['\"', '\"'], ['{', '}']], ['...', '.', '!', '?'], 'left', False, True, ["\"I'm Bob.\" He said.", " \"I'm Jill.\" She replied."]],
        ["\"I'm Bob.\" He said. \"Okay, I'm Jill!?\" She replied.", [['\"', '\"'], ['{', '}']], ['...', '.', '!', '?'], 'left', False, True, ["\"I'm Bob.\" He said.", " \"Okay, I'm Jill!?\" She replied."]],
        ['As you leave the village, a merchant who clearly wants your approval shouts out, "{LOCAL_KING} has slain his thousands, but {PLAYER} his tens of thousands!"', [['\"', '\"'], ['{', '}']], ['...', '.', '!', '?'], 'left', True, True, ['As you leave the village, a merchant who clearly wants your approval shouts out, "{LOCAL_KING} has slain his thousands, but {PLAYER} his tens of thousands!"']],
        ["Calradia is a land full of peril - but also opportunities. To face the challenges that await, you will need to build up your clan.Your brother told you that there are many ways to go about this but that none forego coin.", [['\"', '\"'], ['{', '}']], ['...', '.', '!', '?'], 'left', False, True, ["Calradia is a land full of peril - but also opportunities.", " To face the challenges that await, you will need to build up your clan.", "Your brother told you that there are many ways to go about this but that none forego coin."]],
        ["Calradia is a land full of peril - but also opportunities. To face the challenges that await, you will need to build up your clan.Your brother told you that there are many ways to go about this but that none forego coin.", [['\"', '\"'], ['{', '}']], ['...', '.', '!', '?'], 'left', True, True, ["Calradia is a land full of peril - but also opportunities.", "To face the challenges that await, you will need to build up your clan.", "Your brother told you that there are many ways to go about this but that none forego coin."]],
        ["Calradia is a land full of peril - but also opportunities. To face the challenges that await, you will need to build up your clan.{newline}Your brother told you that there are many ways to go about this but that none forego coin.", [['\"', '\"'], ['{', '}']], ['...', '.', '!', '?'], 'left', False, True, ["Calradia is a land full of peril - but also opportunities.", " To face the challenges that await, you will need to build up your clan.", "{newline}Your brother told you that there are many ways to go about this but that none forego coin."]],
        ["delim", [], ['delim'], 'none', False, True, ['']],
        ]
