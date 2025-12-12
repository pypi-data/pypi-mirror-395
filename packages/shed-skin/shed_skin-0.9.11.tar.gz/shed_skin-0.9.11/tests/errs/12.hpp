#ifndef __12_HPP
#define __12_HPP

using namespace __shedskin__;
namespace __12__ {

extern str *const_0, *const_1, *const_2;

class A;

typedef void *(*lambda0)(void *);
typedef void *(*lambda1)(lambda1);

extern str *__name__;
extern file *f;
extern A *a;
extern lambda0 azo;


extern class_ *cl_A;
class A : public pyobj {
public:
    str *b;

    A() { this->__class__ = cl_A; }
    static void __static__();
};

void *blah(lambda1 b);
void *hoep(__ss_int a, __ss_int b, __ss_int c);

} // module namespace
#endif
