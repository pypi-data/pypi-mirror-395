#include "builtin.hpp"
#include "11.hpp"

namespace __11__ {

str *const_0;


str *__name__;
list<void *> *P, *S;
list<list<__ss_int> *> *P2, *r;
list<list<str *> *> *S2;
list<__ss_int> *wa;
list<__ss_float> *x;
list<list<__ss_float> *> *c;
list<__ss_bool> *bp;



list<__ss_float> *woef() {
    list<void *> *P;

    P = (new list<void *>());
    return (new list<__ss_float>(1,__ss_float(1.0)));
    return P;
}

void __init() {
    const_0 = __char_cache[115];

    __name__ = new str("__main__");

    P = (new list<void *>());
    ((True)?((new list<__ss_int>(1,__ss_int(1)))):(__11__::P));
    print(___bool(__eq((new list<__ss_int>(1,__ss_int(1))), __11__::P)));
    P2 = (new list<list<__ss_int> *>(2,(new list<__ss_int>(1,__ss_int(1))),__11__::P));
    S = (new list<void *>(1,NULL));
    S2 = (new list<list<str *> *>(2,(new list<str *>(1,const_0)),((list<str *> *)(__11__::S))));
    woef();
    wa = (new list<__ss_int>(1,__ss_int(1)));
    x = (new list<__ss_float>(1,__ss_float(1.0)));
    x = (new list<__ss_float>(1,((__ss_float)(__ss_int(1)))));
    x = __11__::wa;
    r = (new list<list<__ss_int> *>(1,(new list<__ss_int>(1,__ss_int(1)))));
    c = (new list<list<__ss_float> *>(1,(new list<__ss_float>(1,__ss_float(1.0)))));
    c = (new list<list<__ss_float> *>(1,(new list<__ss_float>(1,((__ss_float)(__ss_int(1)))))));
    c = __11__::r;
    bp = (new list<__ss_bool>(1,True));
    print(___bool(__eq((new list<__ss_int>(1,__ss_int(1))), __11__::bp)));
}

} // module namespace

int main(int, char **) {
    __shedskin__::__init();
    __shedskin__::__start(__11__::__init);
}
