#include "builtin.hpp"
#include "24.hpp"

namespace __24__ {


str *__name__;
void *a, *myset2;



void __init() {
    __name__ = new str("__main__");

    a = True;
}

} // module namespace

int main(int, char **) {
    __shedskin__::__init();
    __shedskin__::__start(__24__::__init);
}
