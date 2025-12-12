#include "builtin.hpp"
#include "45.hpp"

namespace __45__ {

str *const_0, *const_2;
bytes *const_1;


str *__name__;
pyobj *a, *c;
bytes *b;



void __init() {
    const_0 = new str("hoi");
    const_1 = new bytes("hoi");
    const_2 = new str("uh");

    __name__ = new str("__main__");

    a = const_0;
    a = const_1;
    b = const_1;
    b = __bytearray(__45__::b);
    c = const_2;
    c = __bytearray(__45__::b);
}

} // module namespace

int main(int, char **) {
    __shedskin__::__init();
    __shedskin__::__start(__45__::__init);
}
