// Full lexer coverage file for pygramm lexer.
// This is intentionally not a semantically valid JS program in all engines;
// it is designed to exercise every keyword/operator token your lexer supports.

{
  (a);
  b.c, d;

  x = 1;
  x == 1;
  x != 2;
  !x;

  x < 10;
  x <= 10;
  x > 0;
  x >= 0;

  x + 1;
  x += 2;
  x - 1;
  x -= 2;
  x * 3;
  x *= 4;
  x / 2;
  x /= 2;

  flagA && flagB;
  flagA & flagB;
  flagA || flagB;
  flagA | flagB;

  identifier_1;
  123;
  45.67;
  "double-quoted string";

  // keyword coverage
  await;
  break;
  case;
  catch;
  class;
  const;
  continue;
  debugger;
  default;
  delete;
  do;
  else;
  enum;
  export;
  extends;
  false;
  finally;
  for;
  function;
  if;
  implements;
  import;
  in;
  instanceof;
  interface;
  let;
  new;
  null;
  package;
  private;
  protected;
  public;
  return;
  super;
  switch;
  static;
  this;
  throw;
  try;
  true;
  typeof;
  var;
  void;
  while;
  with;
  yield;
}
