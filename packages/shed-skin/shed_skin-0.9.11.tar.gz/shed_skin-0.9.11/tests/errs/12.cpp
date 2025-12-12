#include "builtin.hpp"
#include "12.hpp"

namespace __12__ {

str *const_0, *const_1, *const_2;


str *__name__;
file *f;
A *a;
lambda0 azo;



/**
class A
*/

class_ *cl_A;

void A::__static__() {
}

void *blah(lambda1 b) {
    return NULL;
}

void *hoep(__ss_int a, __ss_int b, __ss_int c) {
    return NULL;
}

void __init() {
    const_0 = new str("meuh");
    const_1 = __char_cache[119];
    const_2 = new str("woef");

    __name__ = new str("__main__");

    f = (new file(const_0, const_1));
    cl_A = new class_("__main__.A");
    A::__static__();
    a = (new A());
    __12__::a->b = const_2;
    azo = ((lambda0)(__ss_int(1)));
    azo = __lambda0__;
    blah(((lambda1)(__ss_int(1))));
    blah(blah);
    if (False) {
        hoep(__ss_int(1), __ss_int(4));
        hoep(__ss_int(1), __ss_int(2), __ss_int(4));
        hoep(__ss_int(1), __ss_int(2), __ss_int(3));
        hoep(__ss_int(1), __ss_int(2), __ss_int(3));
    }
}

} // module namespace

int main(int, char **) {
    __shedskin__::__init();
    __shedskin__::__start(__12__::__init);
}
