#include "builtin.hpp"
#include "46.hpp"

namespace __46__ {


str *__name__;



void *hop(void *a, void *b) {
    return NULL;
}

void __init() {
    __name__ = new str("__main__");

    hop(__ss_int(1), __ss_int(2));
}

} // module namespace

int main(int, char **) {
    __shedskin__::__init();
    __shedskin__::__start(__46__::__init);
}
