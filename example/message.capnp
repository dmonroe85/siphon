@0xe93247769f9754de;

struct Message {
  userId @0 :UInt32;
  firstName @1 :Text;
  union {
    favoriteSerializer @2 :Text;
    favoriteSerializerNull @3 :Void;
  }
}
