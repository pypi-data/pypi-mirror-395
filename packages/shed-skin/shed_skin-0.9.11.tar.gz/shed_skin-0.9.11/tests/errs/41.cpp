#include "builtin.hpp"
#include "41.hpp"

namespace __41__ {


str *__name__;



/**
class X
*/

class_ *cl_X;

void *X::__init__() {
    this->x = __ss_int(5);
    return NULL;
}

__ss_int X::x;

void X::__static__() {
    x = __ss_int(4);
}

void __init() {
    __name__ = new str("__main__");

    cl_X = new class_("__main__.X");
    X::__static__();
    (new X(1));
}

} // module namespace

int main(int, char **) {
    __shedskin__::__init();
    __shedskin__::__start(__41__::__init);
}
