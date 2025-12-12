#include "builtin.hpp"
#include "30.hpp"

namespace __30__ {


str *__name__;



void __init() {
    __name__ = new str("__main__");

}

} // module namespace

int main(int, char **) {
    __shedskin__::__init();
    __shedskin__::__start(__30__::__init);
}
