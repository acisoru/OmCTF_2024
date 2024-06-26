# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: clone_market.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x63lone_market.proto\x12\x0c\x63lone_market\"L\n\x15GetCloneByUUIDRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05token\x18\x02 \x01(\t\x12\x18\n\x10url_encoded_uuid\x18\x03 \x01(\t\"\'\n\x16GetCloneByUUIDResponse\x12\r\n\x05\x63lone\x18\x01 \x01(\t\"3\n\rSignInRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"\x1b\n\x0bPingRequest\x12\x0c\n\x04pong\x18\x01 \x01(\t\"\x1c\n\x0cPingResponse\x12\x0c\n\x04pong\x18\x01 \x01(\t\"+\n\x0eSignInResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05token\x18\x02 \x01(\t\"+\n\x0eSignOutRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05token\x18\x02 \x01(\t\"7\n\x0fSignOutResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x13\n\x0bserver_resp\x18\x02 \x01(\t\"3\n\rSignUpRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"1\n\x0eSignUpResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x13\n\x0bserver_resp\x18\x02 \x01(\t\"A\n\x10GetClonesRequest\x12\r\n\x05my_id\x18\x01 \x01(\x05\x12\x0f\n\x07user_id\x18\x02 \x01(\x05\x12\r\n\x05token\x18\x03 \x01(\t\"#\n\x11GetClonesResponse\x12\x0e\n\x06\x63lones\x18\x01 \x03(\t\"W\n\x12\x43reateCloneRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05token\x18\x02 \x01(\t\x12\x11\n\tcloneUUID\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\";\n\x13\x43reateCloneResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x13\n\x0bserver_resp\x18\x02 \x01(\t\"C\n\x19\x43reateCloneFromURLRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05token\x18\x02 \x01(\t\x12\x0b\n\x03url\x18\x03 \x01(\t\"B\n\x1a\x43reateCloneFromURLResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x13\n\x0bserver_resp\x18\x02 \x01(\t2\x96\x05\n\x0b\x43loneMarket\x12\x45\n\x06SignIn\x12\x1b.clone_market.SignInRequest\x1a\x1c.clone_market.SignInResponse\"\x00\x12H\n\x07SignOut\x12\x1c.clone_market.SignOutRequest\x1a\x1d.clone_market.SignOutResponse\"\x00\x12\x45\n\x06SignUp\x12\x1b.clone_market.SignUpRequest\x1a\x1c.clone_market.SignUpResponse\"\x00\x12N\n\tGetClones\x12\x1e.clone_market.GetClonesRequest\x1a\x1f.clone_market.GetClonesResponse\"\x00\x12T\n\x0b\x43reateClone\x12 .clone_market.CreateCloneRequest\x1a!.clone_market.CreateCloneResponse\"\x00\x12i\n\x12\x43reateCloneFromURL\x12\'.clone_market.CreateCloneFromURLRequest\x1a(.clone_market.CreateCloneFromURLResponse\"\x00\x12?\n\x04Ping\x12\x19.clone_market.PingRequest\x1a\x1a.clone_market.PingResponse\"\x00\x12]\n\x0eGetCloneByUUID\x12#.clone_market.GetCloneByUUIDRequest\x1a$.clone_market.GetCloneByUUIDResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'clone_market_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_GETCLONEBYUUIDREQUEST']._serialized_start=36
  _globals['_GETCLONEBYUUIDREQUEST']._serialized_end=112
  _globals['_GETCLONEBYUUIDRESPONSE']._serialized_start=114
  _globals['_GETCLONEBYUUIDRESPONSE']._serialized_end=153
  _globals['_SIGNINREQUEST']._serialized_start=155
  _globals['_SIGNINREQUEST']._serialized_end=206
  _globals['_PINGREQUEST']._serialized_start=208
  _globals['_PINGREQUEST']._serialized_end=235
  _globals['_PINGRESPONSE']._serialized_start=237
  _globals['_PINGRESPONSE']._serialized_end=265
  _globals['_SIGNINRESPONSE']._serialized_start=267
  _globals['_SIGNINRESPONSE']._serialized_end=310
  _globals['_SIGNOUTREQUEST']._serialized_start=312
  _globals['_SIGNOUTREQUEST']._serialized_end=355
  _globals['_SIGNOUTRESPONSE']._serialized_start=357
  _globals['_SIGNOUTRESPONSE']._serialized_end=412
  _globals['_SIGNUPREQUEST']._serialized_start=414
  _globals['_SIGNUPREQUEST']._serialized_end=465
  _globals['_SIGNUPRESPONSE']._serialized_start=467
  _globals['_SIGNUPRESPONSE']._serialized_end=516
  _globals['_GETCLONESREQUEST']._serialized_start=518
  _globals['_GETCLONESREQUEST']._serialized_end=583
  _globals['_GETCLONESRESPONSE']._serialized_start=585
  _globals['_GETCLONESRESPONSE']._serialized_end=620
  _globals['_CREATECLONEREQUEST']._serialized_start=622
  _globals['_CREATECLONEREQUEST']._serialized_end=709
  _globals['_CREATECLONERESPONSE']._serialized_start=711
  _globals['_CREATECLONERESPONSE']._serialized_end=770
  _globals['_CREATECLONEFROMURLREQUEST']._serialized_start=772
  _globals['_CREATECLONEFROMURLREQUEST']._serialized_end=839
  _globals['_CREATECLONEFROMURLRESPONSE']._serialized_start=841
  _globals['_CREATECLONEFROMURLRESPONSE']._serialized_end=907
  _globals['_CLONEMARKET']._serialized_start=910
  _globals['_CLONEMARKET']._serialized_end=1572
# @@protoc_insertion_point(module_scope)
