#include "builtin.hpp"
#include "44.hpp"

namespace __44__ {


str *__name__;
yo *y;



/**
class yo
*/

class_ *cl_yo;

void __init() {
    __name__ = new str("__main__");

    cl_yo = new class_("__main__.yo");
    y = (new yo());
    __44__::y->woep;
}

} // module namespace

int main(int, char **) {
    __shedskin__::__init();
    __shedskin__::__start(__44__::__init);
}
