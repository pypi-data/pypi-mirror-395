#include "builtin.hpp"
#include "array.hpp"
#include "re.hpp"
#include "struct.hpp"
#include "socket.hpp"
#include "itertools.hpp"
#include "26.hpp"

namespace __26__ {

str *const_0, *const_1, *const_2, *const_3, *const_4, *const_5;


str *__0, *__name__, *aa, *c;
lambda0 a;
lambda3 l;
__ss_int __1, mm;
meh *m;


static inline __ss_int __lambda1__(__ss_int a, __ss_int b, __ss_int c);
static inline void *__lambda2__(void *a);
static inline void *__lambda3__(void *a, void *b);

static inline __ss_int __lambda1__(__ss_int a, __ss_int b, __ss_int c) {
    return ((a+b)+c);
}

static inline void *__lambda2__(void *a) {
    return a;
}

static inline void *__lambda3__(void *a, void *b) {
    return (a)->__add__(b);
}

/**
class meh
*/

class_ *cl_meh;

void *meh::hop() {
    return NULL;
}

void __init() {
    const_0 = new str("pat");
    const_1 = new str("str");
    const_2 = new str("huhp");
    const_3 = __char_cache[120];
    const_4 = __char_cache[98];
    const_5 = new str("ntohuntaehu");

    __name__ = new str("__main__");

    print(__power(__ss_int(9), (-__ss_int(2))));
    a = ((lambda0)(__ss_int(1)));
    a = __lambda0__;
    __re__::findall(const_0, const_1, __ss_int(0));
    ((new __socket__::socket(__socket__::default_0, __socket__::default_1, __ss_int(0))))->gettimeout();
    map(3, False, __lambda1__, range(__ss_int(2)), range(__ss_int(3)), range(__ss_int(4)));
    __itertools__::zip_longest(2, ((void *)(NULL)), range(__ss_int(2)), range(__ss_int(3)));
    c = const_2;
    (new __array__::array<void *>(const_3));
    (new __array__::array<void *>(__26__::c));
    l = ((lambda3)(__lambda2__));
    l = __lambda3__;
    __26__::l());
    aa = const_4;
    __0 = const_5;
    __1 = 0;
    mm = __struct__::unpack_int('@', 'b', 1, __0, &__1);
    cl_meh = new class_("__main__.meh");
    m = (new meh());
    __26__::m->hop();
}

} // module namespace

int main(int, char **) {
    __shedskin__::__init();
    __re__::__init();
    __socket__::__init();
    __itertools__::__init();
    __array__::__init();
    __struct__::__init();
    __shedskin__::__start(__26__::__init);
}
