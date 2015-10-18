from ChaCha import ChaCha


def test_chacha_permute():
    chacha12 = ChaCha(rounds=12)
    vector = bytes([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
                    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
                    0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f,
                    0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27,
                    0x28, 0x29, 0x2a, 0x2b, 0x2c, 0x2d, 0x2e, 0x2f,
                    0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37,
                    0x38, 0x39, 0x3a, 0x3b, 0x3c, 0x3d, 0x3e, 0x3f])
    result = bytes([0xb3, 0x1a, 0xfb, 0x8e, 0xc3, 0x53, 0x1e, 0x35,
                    0x95, 0xb5, 0xd6, 0xff, 0x90, 0x29, 0x36, 0xa5,
                    0xf5, 0xb0, 0xaf, 0x5a, 0x32, 0xed, 0x4c, 0xca,
                    0xc6, 0xc2, 0x12, 0x04, 0x75, 0xe9, 0x4b, 0xef,
                    0x99, 0x15, 0x39, 0xb2, 0x95, 0x93, 0xc6, 0x52,
                    0xdf, 0x7f, 0x8e, 0x8f, 0x1d, 0xa7, 0x24, 0x8d,
                    0x39, 0x41, 0xb0, 0x23, 0xce, 0x1a, 0x31, 0x10,
                    0x35, 0x3e, 0xbc, 0x80, 0x47, 0x2e, 0xab, 0x09])
    assert result == chacha12.permuted(vector)


def test_chacha_TCs():
    """Checks test functions for the ChaCha permutation

    This function partially implements the test vectors that have been
    specified in the Internet-Draft 'draft-strombergson-chacha-test-vectors-01'
    """
    TCs = [{'key':     bytes([0xc4, 0x6e, 0xc1, 0xb1, 0x8c, 0xe8, 0xa8, 0x78,
                              0x72, 0x5a, 0x37, 0xe7, 0x80, 0xdf, 0xb7, 0x35]),
            'iv':      bytes([0x1a, 0xda, 0x31, 0xd5, 0xcf, 0x68, 0x82, 0x21]),
            'state':         [0x61707865, 0x3120646e,
                              0x79622d36, 0x6b206574,
                              0xb1c16ec4, 0x78a8e88c,
                              0xe7375a72, 0x35b7df80,
                              0xb1c16ec4, 0x78a8e88c,
                              0xe7375a72, 0x35b7df80,
                              0x00000000, 0x00000000,
                              0xd531da1a, 0x218268cf],
            'stream': [bytes([0xb0, 0x2b, 0xd8, 0x1e, 0xb5, 0x5c, 0x8f, 0x68,
                              0xb5, 0xe9, 0xca, 0x4e, 0x30, 0x70, 0x79, 0xbc,
                              0x22, 0x5b, 0xd2, 0x20, 0x07, 0xed, 0xdc, 0x67,
                              0x02, 0x80, 0x18, 0x20, 0x70, 0x9c, 0xe0, 0x98,
                              0x07, 0x04, 0x6a, 0x0d, 0x2a, 0xa5, 0x52, 0xbf,
                              0xdb, 0xb4, 0x94, 0x66, 0x17, 0x6d, 0x56, 0xe3,
                              0x2d, 0x51, 0x9e, 0x10, 0xf5, 0xad, 0x5f, 0x27,
                              0x46, 0xe2, 0x41, 0xe0, 0x9b, 0xdf, 0x99, 0x59]),
                       bytes([0x17, 0xbe, 0x08, 0x73, 0xed, 0xde, 0x9a, 0xf5,
                              0xb8, 0x62, 0x46, 0x44, 0x1c, 0xe4, 0x10, 0x19,
                              0x5b, 0xae, 0xde, 0x41, 0xf8, 0xbd, 0xab, 0x6a,
                              0xd2, 0x53, 0x22, 0x63, 0x82, 0xee, 0x38, 0x3e,
                              0x34, 0x72, 0xf9, 0x45, 0xa5, 0xe6, 0xbd, 0x62,
                              0x8c, 0x7a, 0x58, 0x2b, 0xcf, 0x8f, 0x89, 0x98,
                              0x70, 0x59, 0x6a, 0x58, 0xda, 0xb8, 0x3b, 0x51,
                              0xa5, 0x0c, 0x7d, 0xbb, 0x4f, 0x3e, 0x6e, 0x76])
                       ],
            'rounds': 12,
            },
           ]
    for tc in TCs:
        chacha = ChaCha(tc['key'], tc['iv'], tc['rounds'])
        assert tc['state'] == chacha.state
        assert all(block == chacha.keystream() for block in tc['stream'])


def test_streamblocks():
    chacha = ChaCha()
    stream1024 = b''.join([chacha.keystream(64) for _ in range(16)])
    assert ChaCha().keystream(1024) == stream1024


def test_halfblock():
    assert ChaCha().keystream(37) == ChaCha().keystream(64)[:37]
