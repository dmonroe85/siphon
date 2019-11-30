@0x9ea95743155ea393;

struct Test {
    a @0 :Float32;
    b @1 :Text;
    union {
        c @2 :Text;
        cNull @3 :Void;
    }
    d @4 :List(UInt8);
    e :group {
        f @5 :UInt8;
    }
}
