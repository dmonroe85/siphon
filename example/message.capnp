@0xe93247769f9754de;

struct Message {
  user_id @0 :UInt32;
  first_name @1 :Text;
  union {
    favorite_serializer @2 :Text;
    favorite_serializer_null @3 :Void;
  }
}
