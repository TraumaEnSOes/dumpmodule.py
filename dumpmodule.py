#!/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import inspect
import importlib

class dummyClass( object ):
  dummyValue = 1;

  def __init__( self ):
    super( dummyClass, self ).__init__( self )

def mywrite( text, *args ):
  sys.stdout.write( text )
  for val in args:
    sys.stdout.write( val )

def dumpFunctionArgs( item ):
  try:
    sign = inspect.signature( item )
  except ValueError:
    mywrite( 'NOT INTROSPECTION INFO )\n' )
    return

  notFirst = 0

  for k, v in sign.parameters.items( ):
    if notFirst:
      mywrite( ', ' )

    mywrite( v.name )
    if v.default != inspect.Parameter.empty:
      mywrite( ' = ', str( v.default ) )

    notFirst = 1
  mywrite( ' )' )

  if sign.return_annotation != inspect.Signature.empty:
    mywrite( ' -> ' + sign.return_annotation )

  mywrite( '\n' )

def dumpScope( item, level = 1 ):
  for v in dir( item ):
    if v.startswith( '_' ):
      continue

    attr = getattr( item, v )
    attrType = type( attr )

    mywrite( ' ' * level )

    if ( attrType == TYPEOF_FUNCTION ) or ( attrType == TYPEOF_INTERNAL ):
      mywrite( v, ': function( ' )
      dumpFunctionArgs( attr )
    elif( attrType == TYPEOF_CLASS ):
      mywrite( 'class ', v, ':\n' )
      dumpScope( attr, level + 1 )
    elif( attrType == TYPEOF_MODULE ):
      global VisitedYet

      if v in VisitedYet:
        continue;

      VisitedYet[v] = True
      mywrite( 'module ', v, ':\n' )
      dumpScope( attr, level + 1 )
    else:
      mywrite( v, ': ', attrType.__name__, '\n' )

    sys.stdout.flush( )

TYPEOF_FUNCTION = type( dumpScope )
TYPEOF_INTERNAL = type( print )
TYPEOF_CLASS = type( dummyClass )
TYPEOF_MODULE = type( os )
VisitedYet = { 'os': True }

if len( sys.argv ) == 2:
  if sys.argv[1].startswith( 'gi.' ):
    print( 'PENDIENTE' )
  else:
    todump = importlib.import_module( sys.argv[1] )
    mywrite( 'module ', sys.argv[1], ':\n' )
    dumpScope( todump )
else:
  print( 'Usage: dumpmodule NOMBRE_MODULO' )
