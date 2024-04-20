from typing import List, Self
from struct import pack, unpack

def rotl32(a: int, n: int) -> int:
  return ((a << n) | (a >> (32 - n))) % 2 ** 32

def rotr32(a: int, n: int) -> int:
  return ((a >> n) | (a << (32 - n))) % 2 ** 32

class MyCipher:

  AFTER_STRING: bytes = bytes([
    50,  104, 85,  115, 113, 78,  119, 68,  112, 105, 77,  121, 73, 53,
    99,  105, 98,  115, 78,  112, 54,  122, 116, 88,  101, 102, 87, 68,
    105, 57,  106, 82,  65,  116, 84,  109, 118, 74,  104, 79,  53, 97,
    81,  50,  112, 79,  79,  87,  109, 54,  110, 68,  107, 69,  68, 120,
    117, 66,  90,  86,  90,  68,  51,  105, 120, 71,  87,  104
  ])
  SUBKEY_SIZE: int = 16
  ROUNDS: int = 17
  KEY_SIZE: int = 16
  BLOCK_SIZE: int = 16
  SBOX: List[int] = [
      185, 93,  80,  16,  43,  165, 119, 100, 124, 59,  150, 121, 66,  189, 83,
      237, 73,  169, 149, 49,  136, 2,   8,   19,  252, 167, 180, 184, 41,  166,
      116, 148, 209, 126, 7,   230, 159, 104, 65,  160, 158, 79,  191, 186, 140,
      109, 4,   118, 62,  255, 11,  156, 135, 94,  77,  212, 111, 192, 71,  231,
      117, 176, 214, 90,  107, 38,  157, 37,  199, 42,  219, 146, 235, 46,  31,
      204, 223, 52,  206, 108, 3,   222, 75,  208, 14,  181, 179, 202, 211, 95,
      72,  238, 239, 87,  82,  241, 171, 196, 85,  130, 243, 162, 55,  36,  120,
      221, 187, 147, 132, 164, 60,  242, 97,  151, 193, 115, 103, 175, 247, 131,
      44,  110, 198, 234, 254, 173, 25,  145, 18,  58,  142, 122, 92,  217, 98,
      33,  74,  6,   69,  32,  21,  57,  250, 253, 70,  244, 163, 240, 64,  139,
      232, 12,  245, 53,  30,  61,  50,  183, 188, 114, 248, 15,  0,   91,  29,
      155, 143, 152, 86,  251, 200, 233, 127, 170, 51,  67,  22,  141, 47,  182,
      48,  26,  229, 54,  23,  220, 24,  13,  113, 178, 226, 106, 102, 112, 195,
      56,  63,  203, 34,  134, 133, 197, 137, 17,  174, 9,   68,  172, 28,  210,
      194, 89,  27,  213, 1,   39,  215, 123, 216, 161, 125, 207, 228, 5,   225,
      236, 224, 177, 105, 218, 96,  168, 35,  128, 154, 99,  227, 45,  101, 84,
      246, 78,  81,  138, 153, 129, 76,  205, 40,  190, 201, 88,  249, 144, 20,
      10
  ]
  SBOX_INV: List[int] = [
      162, 214, 21,  80,  46,  223, 137, 34,  22,  205, 255, 50,  151, 187, 84,
      161, 3,   203, 128, 23,  254, 140, 176, 184, 186, 126, 181, 212, 208, 164,
      154, 74,  139, 135, 198, 232, 103, 67,  65,  215, 248, 28,  69,  4,   120,
      237, 73,  178, 180, 19,  156, 174, 77,  153, 183, 102, 195, 141, 129, 9,
      110, 155, 48,  196, 148, 38,  12,  175, 206, 138, 144, 58,  90,  16,  136,
      82,  246, 54,  241, 41,  2,   242, 94,  14,  239, 98,  168, 93,  251, 211,
      63,  163, 132, 1,   53,  89,  230, 112, 134, 235, 7,   238, 192, 116, 37,
      228, 191, 64,  79,  45,  121, 56,  193, 188, 159, 115, 30,  60,  47,  6,
      104, 11,  131, 217, 8,   220, 33,  172, 233, 245, 99,  119, 108, 200, 199,
      52,  20,  202, 243, 149, 44,  177, 130, 166, 253, 127, 71,  107, 31,  18,
      10,  113, 167, 244, 234, 165, 51,  66,  40,  36,  39,  219, 101, 146, 109,
      5,   29,  25,  231, 17,  173, 96,  207, 125, 204, 117, 61,  227, 189, 86,
      26,  85,  179, 157, 27,  0,   43,  106, 158, 13,  249, 42,  57,  114, 210,
      194, 97,  201, 122, 68,  170, 250, 87,  197, 75,  247, 78,  221, 83,  32,
      209, 88,  55,  213, 62,  216, 218, 133, 229, 70,  185, 105, 81,  76,  226,
      224, 190, 236, 222, 182, 35,  59,  150, 171, 123, 72,  225, 15,  91,  92,
      147, 95,  111, 100, 145, 152, 240, 118, 160, 252, 142, 169, 24,  143, 124,
      49
  ]

  subkeys: List[List[int]];
  def _xor_block(self: Self, block: List[int], key: List[int]):
    for i in range(self.BLOCK_SIZE // 4):
      block[i] ^= key[i]

  def _linear_transform(self: Self, block: List[int]):
    block[0] = rotl32(block[0], 13);                   
    block[2] = rotl32(block[2], 3);                     
    block[1] = block[1] ^ block[0] ^ block[2];        
    block[3] = (block[3] ^ block[2] ^ (block[0] << 3)) % 2 ** 32; 
    block[1] = rotl32(block[1], 1);                     
    block[3] = rotl32(block[3], 7);                     
    block[0] = block[0] ^ block[1] ^ block[3];        
    block[2] = (block[2] ^ block[3] ^ (block[1] << 7)) % 2 ** 32; 
    block[0] = rotl32(block[0], 5);                     
    block[2] = rotl32(block[2], 22);

  def _linear_transform_inv(self: Self, block: List[int]):
    block[2] = rotr32(block[2], 22);                  
    block[0] = rotr32(block[0] , 5);                    
    block[2] = (block[2] ^ block[3] ^ (block[1] << 7)) % 2 ** 32; 
    block[0] = block[0] ^ block[1] ^ block[3];        
    block[3] = rotr32(block[3], 7);                     
    block[1] = rotr32(block[1], 1);                     
    block[3] = (block[3] ^ block[2] ^ (block[0] << 3)) % 2 ** 32; 
    block[1] = block[1] ^ block[0] ^ block[2];        
    block[2] = rotr32(block[2], 3);                     
    block[0] = rotr32(block[0], 13);                    

  def _apply_sbox(self: Self, block: List[int]):
    for i in range(self.BLOCK_SIZE // 4):
      block[i] = unpack("I", bytes(self.SBOX[b] for b in pack("I", block[i])))[0]

  def _apply_sbox_inv(self: Self, block: List[int]):
    for i in range(self.BLOCK_SIZE // 4):
      block[i] = unpack("I", bytes(self.SBOX_INV[b] for b in pack("I", block[i])))[0]

  def _round(self: Self, block: List[int], key: List[int]):
    self._xor_block(block, key)
    self._apply_sbox(block)
    self._linear_transform(block)
    pass  

  def _round_inv(self: Self, block: List[int], key: List[int]):
    self._linear_transform_inv(block)
    self._apply_sbox_inv(block)
    self._xor_block(block, key)
    pass


  def _keygen(self: Self, key: bytes):

    self.subkeys = [[None] * 4 for _ in range(17)]
    h = 31337;
    for k in key:
        h = ((h * 171717) ^ k) % 2 ** 32

    for i, k in enumerate(self.AFTER_STRING):
      h = ((h * 171717) ^ k) % 2 ** 32
      self.subkeys[i // 4][i % 4] = h;

  def __init__(self: Self, key: bytes):
    assert len(key) == 16
    self._keygen(key)

  def encrypt_block(self: Self, block: bytes) -> bytes:
    block = list(unpack("4I", block))

    for subkey in self.subkeys:
      self._round(block, subkey)

    return pack("4I", *block)

  def decrypt_block(self: Self, block: bytes) -> bytes:
    block = list(unpack("4I", block))

    for subkey in self.subkeys[::-1]:
      self._round_inv(block, subkey)

    return pack("4I", *block)

  def encrypt(self: Self, data: bytes) -> bytes:
    assert len(data) % 16 == 0

    res = b''

    for i in range(0, len(data), 16):
      res += self.encrypt_block(data[i:i + 16])

    return res

  def decrypt(self: Self, data: bytes) -> bytes:
    assert len(data) % 16 == 0

    res = b''

    for i in range(0, len(data), 16):
      res += self.decrypt_block(data[i:i + 16])

    return res
