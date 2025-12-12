#ifndef __41_HPP
#define __41_HPP

using namespace __shedskin__;
namespace __41__ {

class X;


extern str *__name__;


extern class_ *cl_X;
class X : public pyobj {
public:
    static __ss_int x;

    __ss_int x;

    X() {}
    X(int __ss_init) {
        this->__class__ = cl_X;
        __init__();
    }
    static void __static__();
    void *__init__();
};


} // module namespace
#endif
