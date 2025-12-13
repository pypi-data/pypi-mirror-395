from decimal import ROUND_HALF_UP, Decimal, getcontext
from random import randint, seed


__DecimalPrecision=16
"""
#### Variable used for precision.
"""

getcontext().rounding=ROUND_HALF_UP


def setpr(__p:int)->None:
    """
#### Changes __DecimalPrecision.
- **__p**: The new precision
    """
    try:
        if (__p:=int(__p)) < 0:raise Exception("{} less than 0.".format(__p));
        global __DecimalPrecision;__DecimalPrecision=__p;
    except Exception as e:
        print(e)


def getpr()->int:
    """
#### Get the precision i.e. __DecimalPrecision.
    """
    return __DecimalPrecision;


def deciml(__a:float|int|str|Decimal,__pr:int|None=None)->Decimal:
    '''
#### Get Decimal object.
- **__a**: Value to convert to Decimal
- **__pr**: Precision for the Decimal value
    '''
    try:
        if __pr==None:__pr=getpr();
        if (sa:=str(__a))=='NaN' or sa=='Inf' or sa=='-Inf':return __a;
        def __exp(__a:str)->list:
            match len(a:=__a.split('e')):
                case 1:
                    match len(a:=__a.split('E')):
                        case 1:return a+['0',]; 
                        case 2:return a;
                        case _:return None;
                case 2:return a;
                case _:return None;
        __a=str(__a)
        if __a[0]=='-':a0=__a[0];__a=__a[1:];
        else:a0='';
        if (a1:=__exp(__a)) is None:raise Exception;
        if len(a2:=a2 if (a2:=a1[0].split('.'))[0]!='' else ['0',a2[1]])==1:a2+=['0',];
        # for positive exponential
        if (ia1:=int(a1[1])) > 0:
            if (la2:=len(a2[1])) > 0:
                if int(a2[1]) == 0:
                    a2[1] = ''
                    la2=0
                a2[0]=a2[0]+a2[1][:ia1 if (dd:=la2 - ia1) > 0 else la2]
                if dd < 0:
                    s = ''
                    for i in range(-dd):
                        s+='0'
                a2[0]=a2[0]+('' if dd > 0 else s);a2[1]='0' if dd <= 0 else a2[1][ia1:];a1[1]='0';
        if Decimal(a1[0])==0:return Decimal('0.0');
        if int(a2[0])==0:
            if a2[1][0]=='0':
                c=1
                for i in a2[1][1:]:
                    if i=='0':c+=1;
                    else:break;
                a2[0]=a2[1][c];a2[1]=a2[1][c+1:];a1[1]=str(int(a1[1])-c-1);
        if __pr > 0:
            if len(a2[1]) > 1:
                if len(a2[1])>__pr:
                    a2[1]=a2[1][:__pr+1];del __pr,__a;
                    if int(a2[1][-1])>=5:
                        a2[1] = a2[1][:-1]
                        while len(a2[1])!=0 and a2[1][-1]=='9':a2[1]=a2[1][:-1];
                        if a2[1]=='':a2[0]=str(int(a2[0])+1);
                        else:a2[1]=a2[1][:-1]+str(int(a2[1][-1])+1);
                    else:a2[1]=a2[1][:-1];
            if int(a2[1]) == 0:a2[1]='0'
        else:
            if len(a2[1])>0:
                a2[1]=a2[1][0];del __pr,__a;
                if int(a2[1][0])>=5:a2[0]=a2[0][:-2]+str(int(a2[0][-2:])+1);
                a2[1]='';
        return Decimal(a0+a2[0]+('.'+a2[1] if a2[1]!='' else '')+('E'+a1[1] if a1[1]!='' else ''));
    except:return Decimal('NaN');

# args: (start number,end number), decimal precision, seed
def rint(__i:int,__j:int,__n=1,s=None)->int|tuple[int,...]:
    """
#### Get a random integer or tuple of random integers.
- **__i**: Minimum integer
- **__j**: Maximum integer
- **__n**: Number of numbers
- **s**: Seed *"Positive integer"*
    """
    try:
        if s is not None:seed(s);
        if __n==1:return randint(__i,__j);
        return tuple(map(lambda _:randint(__i,__j),range(__n)))
    except Exception as e:print("Invalid command: rint\n",e);


# rdeciml(num1,num2,precision)
# rdeciml.random(n,seed)
# .cgpr(new precision)
class rdeciml:
    """
#### Object to generate random numbers
- **__a, __b**: Range extremities
- **__pr**: Precision for random numbers
    """
    
    def __init__(self,__a:int|float|Decimal|str,__b:int|float|Decimal|str,__pr:int|None=None)->None:
        try:
            if __pr==None:__pr=getpr();
            __a=str(__a);__b=str(__b);
            def __exp(__a)->list:
                match len(a1:=__a.split('E')):
                    case 1:
                        match len(a2:=__a.split('e')):
                            case 1:return a2+[0,];
                            case 2:return a2;
                            case _:return None;
                    case 2:return a1;
                    case _:return None;
            def __dtd(__a)->list:
                match len(a1:=__a.split('.')):
                    case 1:return a1+['',];
                    case 2:
                        if a1[0]=='':a1[0]='0';
                        return a1;
                    case _:return None;
            def __etd(__a)->list:
                __a,a1=__a
                if (i1a:=int(__a[1]))>=0:
                    if (la1:=len(a1[1]))<i1a:
                        z=''
                        for _ in range(i1a-la1):z+='0';
                        return [a1[0]+a1[1]+z,'0'];
                    elif la1>=i1a:
                        return [a1[0]+a1[1][:(da:=i1a-la1)],a1[1][da:]]
                    else:return None
                else:
                    if (la0:=len(a1[0]))<(ni1a:=-i1a):
                        z=''
                        for _ in range(ni1a-la0):z+='0';
                        return ['0',z+a1[0]+__a[1]]
                    elif la0>=ni1a:
                        return [a1[0][:(da:=la0-ni1a)],a1[1][da:]+a1[0]]
                    else:return None
            __a,__b=tuple(map(__exp,(__a,__b)))
            if __a is None or __b is None:raise Exception;
            a1,b1=tuple(map(__dtd,(__a[0],__b[0])));
            if a1 is None or b1 is None:raise Exception;
            __a,__b=tuple(map(__etd,((__a,a1),(__b,b1))))
            if __a is None or __b is None:raise Exception;
            self.__oa=__a;self.__ob=__b;del a1,b1;__a,__b=map(self.__dtip,((__a,__pr),(__b,__pr)));
            self.__a=__a;self.__b=__b;self.__pr=__pr;del __a,__b,__pr;self.random=lambda __n,__s=None:self.__frandom(self.__pr,__n,__s);
            """
#### Get a tuple of random numbers in Decimal.
- **__n**: Number of random numbers to generate
- **__s**: Seed for generating random numbers
            """
        except Exception as e:print("Invalid command: rdeciml\n",e);

    def __dtip(self,__apr)->int:
        __a,__pr=__apr
        if (la:=len(__a[1]))<__pr:
            for _ in range(__pr-la):__a[1]+='0';
        return int(__a[0]+__a[1][:__pr]);

    def __frandom(self,__pr,__n,__s)->list:
        def rint(__a,__b,__pr):
            (z:=[__a,__b]).sort();__a,__b=z;del z;r=str(randint(__a,__b));
            if (r1:=len(r)-__pr)>0:
                return r[:r1]+'.'+r[r1:];
            else:
                z=''
                for _ in range(-r1):z+='0';
                return '0.'+z+r
        seed(__s);return tuple(Decimal(rint(self.__a,self.__b,__pr)) for _ in range(__n));
    
    def cgpr(self,__pr: int)->None:
        """
#### Change precision for random numbers
- __pr: New precision
        """
        try:
            if __pr < 0:raise Exception("{} less than 0.".format(__pr))
            self.__pr=__pr;del __pr;self.__a,self.__b=map(self.__dtip,((self.__oa,self.__pr),(self.__ob,self.__pr)));print("New precision: "+str(self.__pr));
        except Exception as e:print("Invalid command: rdeciml.cgpr\n",e);


_Pi='3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679';
"""
#### Variable that stores the value of Pi.
"""
_EulersNumber='2.7182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274';
"""
#### Variable that stores the value of e.
"""

class constant:
    """
### Get values of constants.
    """
    
    @staticmethod
    def e(pr:int|None=None)->Decimal|None:
        """
#### Get value of Euler's number as Decimal.
- **pr**: Precision *"not more than 100"*
        """
        try:
            if pr==None:pr=getpr();
            if pr>100:raise Exception;
            global _EulersNumber;return Decimal(_EulersNumber[:pr+2]);
        except:print("Invalid argument: pr -> < 100");

    def pi(pr:int|None=None)->Decimal|None:
        """
#### Get value of Pi as Decimal.
- **pr**: Precision *"not more than 100"*
        """
        try:
            if pr==None:pr=getpr();
            if pr>100:raise Exception;
            global _Pi;return Decimal(_Pi[:pr+2]);
        except:print("Invalid argument: pr -> < 100");


def abs(__a:float|int|str|Decimal)->Decimal|None:
    """
#### Get the absolute value in Decimal.
- **__a**: Value to convert to it's absolute value
    """
    a=Decimal(str(__a))
    if (a1:=str(a))=='NaN' or a1=='Inf' or a1=='-Inf':return None;
    elif a<0:return Decimal(a1[1:]);
    else:return a;

def deciml_sort(__a:list[float]|list[int]|list[str]|list[Decimal],__pr:int|None=None)->list[Decimal]:
    '''
#### Returns a new sorted list in Decimal.
- **__a**: List to convert to Decimal and sort
- **__pr**: Precison for Decimal
    '''
    try:
        if __pr==None:__pr=getpr();
        lis=list(map(lambda i:deciml(i,__pr),__a));lis.sort();return lis;
    except Exception as e:print(e);return None;

class algbra:

    @staticmethod
    def add(*__a:float|int|str|Decimal,pr:int|None=None)->Decimal:
        '''
#### Get the addition of numbers in Decimal.
- **\\*__a**: Numbers to add
- **pr**: Precision for returned Decimal
        '''
        try:
            if pr==None:pr=getpr();
            p=pr+2
            def __add(__a:str,__b:str)->Decimal:
                try:
                    def __exp(__a)->list:
                        match len(a1:=__a.split('E')):
                            case 1:
                                match len(a2:=__a.split('e')):
                                    case 1:return a2+['0',];
                                    case 2:return a2;
                                    case _:return None;
                            case 2:return a1;
                            case _:return None;
                    a,b=map(__exp,(__a,__b))
                    if a is None or b is None:raise Exception
                    an=a[0].lstrip('-').split('.')[0];bn=b[0].lstrip('-').split('.')[0];d1=len(an)+int(a[1]);d2=len(bn)+int(b[1]);
                    if d1>d2:
                        if d1>0:getcontext().prec=p+d1;
                        else:getcontext().prec=p;
                    else:
                        if d2>0:getcontext().prec=p+d2;
                        else:getcontext().prec=p;
                    return str(Decimal(__a)+Decimal(__b))
                except:return None;
            r=str(__a[0])
            for i in __a[1:]:
                r=str(__add(r,str(i)))
                if r=='None':raise Exception;
            return deciml(r,pr)
        except:return Decimal('NaN');

    @staticmethod
    def sub(*__a:float|int|str|Decimal,pr:int|None=None)->Decimal:
        '''
#### Get the subtraction of numbers in Decimal.
- **\\*__a**: Numbers to subtract (Next arguments subtracted from the first number)
- **pr**: Precision for returned Decimal
        '''
        try:
            if pr==None:pr=getpr();
            p=pr+2
            def __sub(__a:str,__b:str)->Decimal:
                try:
                    def __exp(__a)->list:
                        match len(a1:=__a.split('E')):
                            case 1:
                                match len(a2:=__a.split('e')):
                                    case 1:return a2+['0',];
                                    case 2:return a2;
                                    case _:return None;
                            case 2:return a1;
                            case _:return None;
                    a,b=map(__exp,(__a,__b))
                    if a is None or b is None:raise Exception
                    an=a[0].lstrip('-').split('.')[0];bn=b[0].lstrip('-').split('.')[0];d1=len(an)+int(a[1]);d2=len(bn)+int(b[1]);
                    if d1>d2:
                        if d1>0:getcontext().prec=p+d1;
                        else:getcontext().prec=p;
                    else:
                        if d2>0:getcontext().prec=p+d2;
                        else:getcontext().prec=p;
                    return str(Decimal(__a)-Decimal(__b))
                except:return None
            r=str(__a[0])
            for i in __a[1:]:
                r=str(__sub(r,str(i)))
                if r=='None':raise Exception;
            return deciml(r,pr)
        except:return Decimal('NaN');

    @staticmethod
    def mul(*__a:float|int|str|Decimal,pr:int|None=None)->Decimal:
        '''
#### Get the multiplication of numbers in Decimal.
- **\\*__a**: Numbers to multiply
- **pr**: Precision for returned Decimal
        '''
        try:
            if pr==None:pr=getpr();
            p=pr+2
            def __mul(__a:str,__b:str)->Decimal:
                try:
                    def __exp(__a)->list:
                        match len(a1:=__a.split('E')):
                            case 1:
                                match len(a2:=__a.split('e')):
                                    case 1:return a2+['0',];
                                    case 2:return a2;
                                    case _:return None;
                            case 2:return a1;
                            case _:return None;
                    a,b=map(__exp,(__a,__b))
                    if a is None or b is None:raise Exception
                    an=a[0].lstrip('-').split('.')[0];bn=b[0].lstrip('-').split('.')[0];
                    if (p1:=int(a[1])+int(b[1])+len(an)+len(bn))>0:getcontext().prec=p1+p;
                    else:getcontext().prec=p;
                    return str(Decimal(__a)*Decimal(__b))
                except:return None;
            r=str(__a[0])
            for i in __a[1:]:
                r=str(__mul(r,str(i)))
                if r=='None':raise Exception;
            return deciml(r,pr)
        except:return Decimal('NaN');

    @staticmethod
    def div(__a:float|int|str|Decimal,__b:float|int|str|Decimal,__pr:int|None=None)->Decimal:
        '''
#### Get the division of numbers in Decimal.
- **__a**: Numerator
- **__b**: Denominator
- **__pr**: Precision for returned Decimal
        '''
        try:
            if __pr==None:__pr=getpr();
            p=__pr+2
            def __exp(__a)->list:
                match len(a1:=__a.split('E')):
                    case 1:
                        match len(a2:=__a.split('e')):
                            case 1:return a2+['0',];
                            case 2:return a2;
                            case _:return None;
                    case 2:return a1;
                    case _:return None;
            a,b=map(__exp,(str(__a),str(__b)))
            if a is None or b is None:raise Exception
            an=a[0].lstrip('-').split('.')[0];bn=b[0].lstrip('-').split('.')[0];
            if (p1:=int(a[1])-int(b[1])+len(an)-len(bn))>0:getcontext().prec=p1+p;
            else:getcontext().prec=p;
            return deciml(Decimal(__a)/Decimal(__b),__pr)
        except:return Decimal('NaN');
    
    @classmethod
    def log(cls,__a:float|int|str|Decimal,__b=constant.e(),__pr:int|None=None)->Decimal:
        '''
#### Get the logarithm of number in Decimal.
- **__a**: Number
- **__b**: Base
- **__pr**: Precision for returned Decimal
        '''
        try:
            if __pr==None:__pr=getpr();
            p=__pr+2
            a=Decimal(str(__a));b=Decimal(str(__b));c=0;
            if a==0:raise Exception()
            getcontext().prec=p;
            if b>=1:
                if a>=1:
                    while a>=b:a=cls.div(a,b,p);c+=1;
                    return deciml(str(c)+"."+(s[2:] if (s := str(a.ln()/b.ln()))[1] != 'E' and s[2] != 'E' else '0'),__pr);
                if a<1:
                    while a<1:a=cls.mul(a,b,pr=p);c+=1;
                    return deciml(str(-c)+"."+(s[2:] if (s := str(a.ln()/b.ln()))[1] != 'E' and s[2] != 'E' else '0'),__pr);
            if b<1:
                if a>b:
                    while a>1:a=cls.mul(a,b,pr=p);c+=1;
                    return deciml(str(-c)+"."+(s[2:] if (s := str(a.ln()/b.ln()))[1] != 'E' and s[2] != 'E' else '0'),__pr);
                if a<=b:
                    while a<=b:a=cls.div(a,b,p);c+=1;
                    return deciml(str(c)+"."+(s[2:] if (s := str(a.ln()/b.ln()))[1] != 'E' and s[2] != 'E' else '0'),__pr);
        except:return Decimal('NaN');

    @classmethod
    def pwr(cls,__a:float|int|Decimal|str,__b:float|int|Decimal|str,__pr:int|None=None)->Decimal:
        '''
#### Get the Decimal after exponentiation.
- **__a**: Number to exponent
- **__b**: Exponent
- **__pr**: Precision for returned Decimal
        '''
        try:
            if __pr==None:__pr=getpr();
            a=Decimal(str(__a));c=0;p=__pr+2;
            if (b:=Decimal(str(__b)))==(ib:=int(b)):
                r=1
                if b<0:
                    for _ in range(-ib):r=cls.mul(r,a,pr=p);
                    r=cls.div(1,r,p)
                else:
                    for _ in range(ib):r=cls.mul(r,a,pr=p);
                return deciml(r,__pr)
            elif a<0:raise Exception;
            elif b==0:return Decimal('1');
            elif a==0:return Decimal('0');
            if a>=1:
                if b>=0:
                    while a>1:a=cls.div(a,10,p);c+=1;
                    getcontext().prec=int((p1:=cls.mul(c, b, pr=p)))+p;return deciml((10**p1)*(a**b),__pr);
                if b<0:getcontext().prec=p;return deciml(a**b,__pr);
            if a<1:
                if b>=0:
                    getcontext().prec=p;return deciml(a**b,__pr);
                if b<0:
                    while a<1:a=cls.mul(a,10,pr=p);c+=1;
                    getcontext().prec=int((p1:=cls.mul(-c, b, pr=p)))+p;return deciml((10**p1)*(a**b),__pr);
        except:return Decimal('NaN');


class galgbra:

    @staticmethod
    def add(*__a:list[Decimal]|tuple[Decimal,...],pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the numbers after addition for lists or tuples.
##### (a, b, c) + [A, B, C] + ... = (a+A+..., b+B+..., c+C+...)
- **\\*__a**: Lists or tuples to perform addition
- **pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda x:algbra.add(*x,pr=pr),zip(*__a)));
        except Exception as e:print("Invalid command: galgra.add\n",e);return None;
    
    @staticmethod
    def sub(*__a:list[Decimal]|tuple[Decimal,...],pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the numbers after subtraction for lists or tuples.
##### (a, b, c) - [A, B, C] - ... = (a-A-..., b-B-..., c-C-...)
- **\\*__a**: Lists or tuples to perform subtraction
- **pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda x:algbra.sub(*x,pr=pr),zip(*__a)));
        except Exception as e:print("Invalid command: galgra.sub\n",e);return None;
    
    @staticmethod
    def mul(*__a:list[Decimal]|tuple[Decimal,...],pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the numbers after multiplication for lists or tuples.
##### (a, b, c) x [A, B, C] x ... = (a\\*A\\*..., b\\*B\\*..., c\\*C\\*...)
- **\\*__a**: Lists or tuples to perform mutiplication
- **pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda x:algbra.mul(*x,pr=pr),zip(*__a)));
        except Exception as e:print("Invalid command: galgra.mul\n",e);return None;
    
    @staticmethod
    def div(__a:list[Decimal]|tuple[Decimal,...],__b:list[Decimal]|tuple[Decimal,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the numbers after division for lists or tuples.
##### (a, b, c, ...) / [A, B, C, ...] = (a/A, b/B, c/C, ...)
- **__a**: List or tuple with numerators
- **__b**: List or tuple with denominators
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda x:algbra.div(*x,__pr),zip(__a,__b)));
        except Exception as e:print("Invalid command: galgra.div\n",e);return None;
    
    @staticmethod
    def pwr(__a:list[Decimal]|tuple[Decimal,...],__b:list[Decimal]|tuple[Decimal,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the numbers after exponentiation.
##### (a, b, c, ...) ^ (A, B, C, ...) = (a^A, b^B, c^C, ...)
- **__a**: List or tuple with numbers
- **__b**: List or tuple of exponents
- **__pr**: Precision for returned Decimal numbers

        '''
        try:
            return tuple(map(lambda x:algbra.pwr(*x,__pr),zip(__a,__b)));
        except Exception as e:print("Invalid command: galgra.pwr\n",e);return None;
    
    @staticmethod
    def log(__a:list[Decimal]|tuple[Decimal,...],__b:list[Decimal]|tuple[Decimal,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the logarithm of numbers.
##### (a, b, c), (A, B, C) = (log_a(A), log_b(B), log_c(C))
- **__a**: List or tuple with numbers
- **__b**: List or tuple with base values
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda x:algbra.log(*x,__pr),zip(__a,__b)));
        except Exception as e:print("Invalid command: galgra.log\n",e);return None;
    
    @staticmethod
    def addsg(__a:Decimal,__b:list[Decimal]|tuple[Decimal,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the numbers after addition.
##### N + (A, B, C, ...) = (N+A, N+B, N+C, ...)
- **__a**: Number to add
- **__b**: List or tuple with numbers for addition
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            __a=str(__a);return tuple(map(lambda x:algbra.add(__a,x,pr=__pr),__b));
        except Exception as e:print("Invalid command: galgra.addsg\n",e);return None;
    
    @staticmethod
    def subgs(__a:list[Decimal]|tuple[Decimal,...],__b:Decimal,__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the numbers after subtraction.
##### (A, B, C, ...) - N = (A-N, B-N, C-N, ...)
- **__a**: List or tuple with numbers
- **__b**: Number to subtract
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            __b=str(__b);return tuple(map(lambda x:algbra.sub(x,__b,pr=__pr),__a));
        except Exception as e:print("Invalid command: galgra.subgs\n",e);return None;
    
    @staticmethod
    def subsg(__a:Decimal,__b:list[Decimal]|tuple[Decimal,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the numbers after subtraction.
##### N - (A, B, C, ...) = (N-A, N-B, N-C, ...)
- **__a**: Number
- **__b**: List or tuple with numbers to subtract
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            __a=str(__a);return tuple(map(lambda x:algbra.sub(__a,x,pr=__pr),__b));
        except Exception as e:print("Invalid command: galgra.subsg\n",e);return None;

    @staticmethod
    def mulsg(__a:Decimal,__b:list[Decimal]|tuple[Decimal,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the numbers after multiplication.
##### N x (A, B, C, ...) = (N*A, N*B, N*C, ...)
- **__a**: Number
- **__b**: List or tuple with numbers to multiply
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            __a=str(__a);return tuple(map(lambda x:algbra.mul(__a,x,pr=__pr),__b));
        except Exception as e:print("Invalid command: galgra.mulsg\n",e);return None;

    @staticmethod
    def divgs(__a:list[Decimal]|tuple[Decimal,...],__b:Decimal,__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the numbers after division.
##### (A, B, C, ...) / N = (A/N, B/N, C/N, ...)
- **__a**: List or tuple with numerators
- **__b**: Denominator
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            __b=str(__b);return tuple(map(lambda x:algbra.div(x,__b,__pr),__a));
        except Exception as e:print("Invalid command: galgra.divgs\n",e);return None;
    
    @staticmethod
    def divsg(__a:Decimal,__b:list[Decimal]|tuple[Decimal,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the numbers after division.
##### N / (A, B, C, ...) = (N/A, N/B, N/C, ...)
- **__a**: Numerator
- **__b**: List or tuple with numbers to denominators
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            __a=str(__a);return tuple(map(lambda x:algbra.div(__a,x,__pr),__b));
        except Exception as e:print("Invalid command: galgra.divsg\n",e);return None;

    @staticmethod
    def pwrgs(__a:list[Decimal]|tuple[Decimal,...],__b:Decimal,__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the numbers after exponentiation.
##### (A, B, C, ...) ^ N = (A^N, B^N, B^N, ...)
- **__a**: List or tuple with numbers
- **__b**: Exponent
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            __b=str(__b);return tuple(map(lambda x:algbra.pwr(x,__b,__pr),__a));
        except Exception as e:print("Invalid command: galgra.pwrgs\n",e);return None;
    
    @staticmethod
    def pwrsg(__a:Decimal,__b:list[Decimal]|tuple[Decimal,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the numbers after exponentiation.
##### N ^ (A, B, C, ...) = (N^A, N^B, N^C, ...)
- **__a**: Number
- **__b**: List or tuple with exponents
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            __a=str(__a);return tuple(map(lambda x:algbra.pwr(__a,x,__pr),__b));
        except Exception as e:print("Invalid command: galgra.pwrsg\n",e);return None;
    
    @staticmethod
    def loggs(__a:list[Decimal]|tuple[Decimal,...],__b:Decimal,__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the logarithm of numbers.
##### (A, B, C, ...), N = (log_N(A), log_N(B), log_N(C), ...)
- **__a**: List or tuple of numbers
- **__b**: Base of logarithm
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            __b=str(__b);return tuple(map(lambda x:algbra.log(x,__b,__pr),__a));
        except Exception as e:print("Invalid command: galgra.loggs\n",e);return None;
    
    @staticmethod
    def logsg(__a:Decimal,__b:list[Decimal]|tuple[Decimal,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the logarithm of numbers.
##### N, (A, B, C, ...) = (log_A(N), log_B(N), log_C(N), ...)
- **__a**: Number
- **__a**: List or tuple with bases of logarithms
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            __a=str(__a);return tuple(map(lambda x:algbra.log(__a,x,__pr),__b));
        except Exception as e:print("Invalid command: galgra.logsg\n",e);return None;


class trig:

    @staticmethod
    def sin(__a:Decimal|int|float|str,__pr:int|None=None)->Decimal:
        """
#### Get the sine in Decimal.
- **__a**: Number
- **__pr**: Precision for returned Decimal number
        """
        try:
            if __pr==None:__pr=getpr();
            pr=__pr+2
            if (a:=Decimal(str(__a)))>(p:=algbra.mul(constant.pi(pr),'2',pr=pr)):a='0.'+str(algbra.div(a,p,pr+1)).split('.')[1];a=algbra.mul(a,p,pr=pr);
            elif a<algbra.mul('-1',p,pr=pr):a='-0.'+str(algbra.div(a,p,pr+1)).split('.')[1];a=algbra.mul(a,p,pr=pr);
            rp=None;n=a;d=1;c=1;a1=algbra.pwr(a,'2',pr+1);r=algbra.div(n,d,pr+1);
            while r!=rp:rp=r;r=algbra.add(r,algbra.div((n:=algbra.mul(n,a1,'-1',pr=pr+2)),(d:=d*(c+1)*((c:=c+2))),pr+1),pr=pr);
            return deciml(r,__pr);
        except Exception as e:print("Invalid command: trig.sin\n",e);return Decimal('NaN');

    @staticmethod
    def cos(__a:Decimal|int|float|str,__pr:int|None=None)->Decimal:
        '''
#### Get the cosine in Decimal.
- **__a**: Number
- **__pr**: Precision for returned Decimal number
        '''
        try:
            if __pr==None:__pr=getpr();
            pr=__pr+2
            if (a:=Decimal(str(__a)))>(p:=algbra.mul(constant.pi(pr),'2',pr=pr)):a='0.'+str(algbra.div(a,p,pr+1)).split('.')[1];a=algbra.mul(a,p,pr=pr);
            elif a<algbra.mul('-1',p,pr=pr):a='-0.'+str(algbra.div(a,p,pr+1)).split('.')[1];a=algbra.mul(a,p,pr=pr);
            rp=0;n=1;d=1;c=0;r=1;a1=algbra.pwr(a,'2',pr);
            while r!=rp:rp=r;r=algbra.add(r,algbra.div((n:=algbra.mul(n,a1,'-1',pr=pr+2)),(d:=d*(c+1)*((c:=c+2))),pr+1),pr=pr);
            return deciml(r,__pr);
        except Exception as e:print("Invalid command: trig.cos\n",e);return Decimal('NaN');

    @classmethod
    def tan(cls,__a:Decimal|int|float|str,__pr:int|None=None)->Decimal:
        '''
#### Get the tan in Decimal.
- **__a**: Number
- **__pr**: Precision for returned Decimal number
        '''
        try:
            if __pr==None:__pr=getpr();
            pr=__pr+2
            if (a:=Decimal(str(__a)))>(p:=algbra.mul(constant.pi(pr),'2',pr=pr)):a='0.'+str(algbra.div(a,p,pr+1)).split('.')[1];a=algbra.mul(a,p,pr=pr);
            elif a<algbra.mul('-1',p,pr=pr):a='-0.'+str(algbra.div(a,p,pr+1)).split('.')[1];a=algbra.mul(a,p,pr=pr);
            r=algbra.div(cls.sin(a,pr+1),cls.cos(a,pr+1),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: trig.tan\n",e);return Decimal('NaN');

    @classmethod
    def cosec(cls,__a:Decimal|int|float|str,__pr:int|None=None)->Decimal:
        '''
#### Get the cosec in Decimal.
- **__a**: Number
- **__pr**: Precision for returned Decimal number
        '''
        try:
            if __pr==None:__pr=getpr();
            pr=__pr+2;r=algbra.div(1,cls.sin(__a,pr+1),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: trig.cosec\n",e);return Decimal('NaN');

    @classmethod
    def sec(cls,__a:Decimal|int|float|str,__pr:int|None=None)->Decimal:
        '''
#### Get the sec in Decimal.
- **__a**: Number
- **__pr**: Precision for returned Decimal number
        '''
        try:
            if __pr==None:__pr=getpr();
            pr=__pr+2;r=algbra.div(1,cls.cos(__a,pr+1),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: trig.sec\n",e);return Decimal('NaN');

    @classmethod
    def cot(cls,__a:Decimal|int|float|str,__pr:int|None=None)->Decimal:
        '''
#### Get the cot in Decimal.
- **__a**: Number
- **__pr**: Precision for returned Decimal number
        '''
        try:
            if __pr==None:__pr=getpr();
            pr=__pr+2;r=algbra.div(cls.cos(__a,pr+1),cls.sin(__a,pr+1),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: trig.cot\n",e);return Decimal('NaN');

    # [-pi/2, pi/2]
    @classmethod
    def asin(cls,__a:Decimal|int|float|str,__pr:int|None=None)->Decimal:
        '''
#### Get the sine<sup>-1</sup> in Decimal.
##### Note - Return bounds are -*pi/2* and *pi/2*.
- **__a**: Number
- **__pr**: Precision for returned Decimal number
        '''
        try:
            if __pr==None:__pr=getpr();
            pr=__pr+2;a=Decimal(str(__a));
            if a<-1 or a>1:raise Exception;
            if a>(a1:=algbra.pwr('2','-0.5',pr)):r=cls.acos(algbra.pwr(algbra.sub(1,algbra.pwr(a,'2',pr),pr=pr),'0.5',pr),pr);
            elif a<Decimal('-'+str(a1)):r=algbra.mul('-1',cls.acos(algbra.pwr(algbra.sub('1',algbra.pwr(a,'2',pr),pr=pr),'0.5',pr),pr),pr=pr);
            else:
                i=0;r=(n:=a);rn=None;a1=algbra.pwr(a,'2',pr);d1=1;d2=1;d3=1;
                while r!=rn:rn=r;i+=1;r=algbra.add(r,algbra.div((n:=algbra.mul(n,(q:=2*i),(q-1),a1,pr=pr)),(d1:=d1*4)*((d2:=d2*i)**2)*(d3:=d3+2),pr),pr=pr);
            return deciml(r,__pr)
        except Exception as e:print("Invalid command: trig.asin\n",e);return Decimal('NaN');

    # [0, pi]
    @classmethod
    def acos(cls,__a:Decimal|int|float|str,__pr:int|None=None)->Decimal:
        '''
#### Get the cosine<sup>-1</sup> in Decimal.
##### Note - Return bounds are *0* and *pi*.
- **__a**: Number
- **__pr**: Precision for returned Decimal number
        '''
        try:
            if __pr==None:__pr=getpr();
            pr=__pr+2;a=Decimal(str(__a));
            if a<-1 or a>1:raise Exception;
            if a>(a1:=algbra.pwr('2','-0.5',pr)):r=cls.asin(algbra.pwr(algbra.sub(1,algbra.pwr(a,'2',pr),pr=pr),'0.5',pr),pr);
            elif a<Decimal('-'+str(a1)):r=algbra.add(algbra.mul('-1',cls.asin(a,pr),pr=pr),algbra.div(constant.pi(pr),'2',pr),pr=pr);
            else:
                i=0;r=algbra.sub(algbra.div(constant.pi(pr),'2',pr),(n:=a),pr=pr);
                rn=None;a1=algbra.pwr(a,'2',pr);d1=1;d2=1;d3=1;
                while r!=rn:rn=r;i+=1;r=algbra.sub(r,algbra.div((n:=algbra.mul(n,(q:=2*i),(q-1),a1,pr=pr)),(d1:=d1*4)*((d2:=d2*i)**2)*(d3:=d3+2),pr),pr=pr);
            return deciml(r,__pr)
        except Exception as e:print("Invalid command: trig.acos\n",e);return Decimal('NaN');

    # [-pi/2, pi/2]
    @classmethod
    def atan(cls,__a:Decimal|int|float|str,__pr:int|None=None)->Decimal:
        '''
#### Get the tan<sup>-1</sup> in Decimal.
##### Note - Return bounds are *-pi/2* and *pi/2*.
- **__a**: Number
- **__pr**: Precision for returned Decimal number
        '''
        try:
            if __pr==None:__pr=getpr();
            pr=__pr+2
            if (a:=Decimal(str(__a)))<0:r=algbra.mul('-1',cls.asec(algbra.pwr(algbra.add(algbra.pwr(a,'2',pr),'1',pr=pr),'0.5',pr),pr),pr=pr);
            else:r=cls.asec(algbra.pwr(algbra.add(algbra.pwr(a,'2',pr),'1',pr=pr),'0.5',pr),pr);
            return deciml(r,__pr);
        except Exception as e:print("Invalid command: trig.atan\n",e);return Decimal('NaN');

    # [-pi/2, pi/2]
    @classmethod
    def acosec(cls,__a:Decimal|int|float|str,__pr:int|None=None)->Decimal:
        '''
#### Get the cosec<sup>-1</sup> in Decimal.
##### Note - Return bounds are *-pi/2* and *pi/2*.
- **__a**: Number
- **__pr**: Precision for returned Decimal number
        '''
        try:
            if __pr==None:__pr=getpr();
            pr=__pr+2;r=cls.asin(algbra.div('1',__a,pr),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: trig.acosec\n",e);return Decimal('NaN');

    # [0, pi]
    @classmethod
    def asec(cls,__a:Decimal|int|float|str,__pr:int|None=None)->Decimal:
        '''
#### Get the sec<sup>-1</sup> in Decimal.
##### Note - Return bounds are *0* and *pi*.
- **__a**: Number
- **__pr**: Precision for returned Decimal number
        '''
        try:
            if __pr==None:__pr=getpr();
            pr=__pr+2;r=cls.acos(algbra.div('1',__a,pr),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: trig.asec\n",e);return Decimal('NaN');

    # [-pi/2, pi/2]
    @classmethod
    def acot(cls,__a:Decimal|int|float|str,__pr:int|None=None)->Decimal:
        '''
#### Get the cot<sup>-1</sup> in Decimal.
##### Note - Return bounds are *-pi/2* and *pi/2*.
- **__a**: Number
- **__pr**: Precision for returned Decimal number
        '''
        try:
            if __pr==None:__pr=getpr();
            pr=__pr+2;r=cls.atan(algbra.div('1',__a,pr),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: trig.acot\n",e);return Decimal('NaN');

class gtrig:

    @staticmethod
    def sine(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the sine for list or tuple as tuple with Decimal.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda i:trig.sin(i, __pr),__a))
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def cosine(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the cosine for list or tuple as tuple with Decimal.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda i:trig.cos(i, __pr),__a))
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def tan(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the tan for list or tuple as tuple with Decimal.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda i:trig.tan(i, __pr),__a))
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def cot(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...], __pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the cot for list or tuple as tuple with Decimal.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda i:trig.cot(i, __pr),__a))
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def sec(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...], __pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the sec for list or tuple as tuple with Decimal.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda i:trig.sec(i, __pr),__a))
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def cosec(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the cosec for list or tuple as tuple with Decimal.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda i:trig.cosec(i, __pr),__a))
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def asine(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the sine<sup>-1</sup> for list or tuple as tuple with Decimal.
##### Return bounds are *-pi/2* and *pi/2*.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda i:trig.asin(i, __pr),__a))
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def acosine(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the cosine<sup>-1</sup> for list or tuple as tuple with Decimal.
##### Return bounds are *0* and *pi*.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda i:trig.acos(i, __pr),__a))
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def atan(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the tan<sup>-1</sup> for list or tuple as tuple with Decimal.
##### Return bounds are *-pi/2* and *pi/2*.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda i:trig.tan(i, __pr),__a))
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def acot(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the cot<sup>-1</sup> for list or tuple as tuple with Decimal.
##### Return bounds are *-pi/2* and *pi/2*.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda i:trig.acot(i, __pr),__a))
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def asec(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the sec<sup>-1</sup> for list or tuple as tuple with Decimal.
##### Return bounds are *0* and *pi*.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda i:trig.asec(i, __pr),__a))
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def acosec(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the cosec<sup>-1</sup> for list or tuple as tuple with Decimal.
##### Return bounds are *-pi/2* and *pi/2*.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda i:trig.acosec(i, __pr),__a))
        except Exception as e:
            print(e)
            return None

class htrig:

    @staticmethod
    def sinh(__a:Decimal|int|float|str,__pr:int|None=None)->Decimal:
        '''
#### Get the sinh in Decimal.
- **__a**: Number
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            if __pr==None:__pr=getpr();
            pr=__pr+2;r=__a;rn=None;n=__a;d=1;c=1;a1=algbra.pwr(__a,'2',pr);
            while r!=rn:rn=r;r=algbra.add(r,algbra.div((n:=algbra.mul(n,a1,pr=pr)),(d:=d*(c+1)*((c:=c+2))),pr),pr=pr);
            return deciml(r,__pr)
        except Exception as e:print("Invalid command: htrig.sinh\n",e);return Decimal('NaN');
    
    @staticmethod
    def cosh(__a:Decimal|int|float|str,__pr:int|None=None)->Decimal:
        '''
#### Get the cosh in Decimal.
- **__a**: Number
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            if __pr==None:__pr=getpr();
            pr=__pr+2;r=1;rn=None;n=1;d=1;c=0;a1=algbra.pwr(__a,'2',pr);
            while r!=rn:rn=r;r=algbra.add(r,algbra.div((n:=algbra.mul(n,a1,pr=pr)),(d:=d*(c+1)*((c:=c+2))),pr),pr=pr);
            return deciml(r,__pr);
        except Exception as e:print("Invalid command: htrig.cosh\n",e);return Decimal('NaN');
    
    @classmethod
    def tanh(cls,__a:Decimal|int|float|str,__pr:int|None=None)->Decimal:
        '''
#### Get the tanh in Decimal.
- **__a**: Number
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            if __pr==None:__pr=getpr();
            pr=__pr+2;r=algbra.div(cls.sinh(__a,pr),cls.cosh(__a,pr),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: htrig.tanh\n",e);return Decimal('NaN');
    
    @classmethod
    def cosech(cls,__a:Decimal|int|float|str,__pr:int|None=None)->Decimal:
        '''
#### Get the cosech in Decimal.
- **__a**: Number
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            if __pr==None:__pr=getpr();
            pr=__pr+2;r=algbra.div(1,cls.sinh(__a),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: htrig.cosech\n",e);return Decimal('NaN');
    
    @classmethod
    def sech(cls,__a:Decimal|int|float|str,__pr:int|None=None)->Decimal:
        '''
#### Get the sech in Decimal.
- **__a**: Number
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            if __pr==None:__pr=getpr();
            pr=__pr+2;r=algbra.div(1,cls.cosh(__a),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: htrig.sech\n",e);return Decimal('NaN');
    
    @classmethod
    def coth(cls,__a:Decimal|int|float|str,__pr:int|None=None)->Decimal:
        '''
#### Get the coth in Decimal.
- **__a**: Number
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            if __pr==None:__pr=getpr();
            pr=__pr+2
            if deciml(__a)==0:raise Exception;
            r=algbra.div(cls.cosh(__a),cls.sinh(__a),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: htrig.coth\n",e);return Decimal('NaN');
    
class ghtrig:

    @staticmethod
    def sinh(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the sinh for list or tuple as tuple with Decimal.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda i:htrig.sinh(i,__pr),__a))
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def cosh(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the cosh for list or tuple as tuple with Decimal.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda i:htrig.cosh(i,__pr),__a))
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def tanh(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the tanh for list or tuple as tuple with Decimal.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda i:htrig.tanh(i,__pr),__a))
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def coth(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the coth for list or tuple as tuple with Decimal.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda i:htrig.coth(i,__pr),__a))
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def sech(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the sech for list or tuple as tuple with Decimal.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda i:htrig.sech(i,__pr),__a))
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def cosech(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->tuple[Decimal,...]|None:
        '''
#### Get the cosech for list or tuple as tuple with Decimal.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal numbers
        '''
        try:
            return tuple(map(lambda i:htrig.cosech(i,__pr),__a))
        except Exception as e:
            print(e)
            return None

class stat:

    @staticmethod
    def amean(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->Decimal|None:
        '''
#### Get the arithmatic mean of numbers.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal
        '''
        try:
            if __pr==None:__pr=getpr();
            return algbra.div(algbra.add(*__a,pr=__pr+1),len(__a),__pr)
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def gmean(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->Decimal|None:
        '''
#### Get the geometric mean of numbers.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal
        '''
        try:
            if __pr==None:__pr=getpr();
            return algbra.pwr(algbra.mul(*__a, pr=__pr+1),algbra.div('1',len(__a),__pr+1),__pr)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def hmean(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->Decimal|None:
        '''
#### Get the harmonic mean of numbers.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal
        '''
        try:
            if __pr==None:__pr=getpr();
            return algbra.div('1', algbra.add(*tuple(map(lambda i:algbra.div('1',i,__pr+2),__a)),pr=__pr+1),__pr)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def qmean(__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->Decimal|None:
        '''
        '''
        try:
            if __pr==None:__pr=getpr();
            return algbra.pwr(algbra.div(algbra.add(*galgbra.pwrgs(__a,'2',__pr+3),pr=__pr+2),len(__a),__pr+1),'0.5',__pr)
        except Exception as e:
            print(e)
            return None

    @classmethod
    def pvar(cls,__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->Decimal|None:
        '''
#### Get the population variance of numbers.
##### Note: For large sample.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal
        '''
        try:
            if __pr==None:__pr=getpr();
            return algbra.div(algbra.add(*galgbra.pwrgs(galgbra.subgs(__a,cls.amean(__a,__pr+4),__pr+3),'2',__pr+2),pr=__pr+1),len(__a),__pr)
        except Exception as e:
            print(e)
            return None
    
    @classmethod
    def svar(cls,__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->Decimal|None:
        '''
#### Get the sample variance of numbers.
##### Note: For small sample.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal
        '''
        try:
            if __pr==None:__pr=getpr();
            return algbra.div(algbra.add(*galgbra.pwrgs(galgbra.subgs(__a,cls.amean(__a,__pr+4),__pr+3),'2',__pr+2),pr=__pr+1),len(__a)-1,__pr)
        except Exception as e:
            print(e)
            return None

    @classmethod
    def pstd_dev(cls,__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->Decimal|None:
        '''
#### Get the poulation standard deviation of numbers.
##### Note: For large sample.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal
        '''
        try:
            if __pr==None:__pr=getpr();
            return algbra.pwr(cls.pvar(__a,__pr+1),'0.5',__pr)
        except Exception as e:
            print(e)
            return None

    @classmethod
    def sstd_dev(cls,__a:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->Decimal|None:
        '''
#### Get the sample standard deviation of numbers.
##### Note: For small sample.
- **__a**: List or tuple of numbers
- **__pr**: Precision for returned Decimal
        '''
        try:
            if __pr==None:__pr=getpr();
            return algbra.pwr(cls.svar(__a,__pr+1),'0.5',__pr)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def median(__x:list[Decimal|str|float]|tuple[Decimal|str|float,...],__pr:int|None=None)->Decimal|None:
        '''
#### Get the median of numbers.
- **__x**: List or tuple of numbers
- **__pr**: Precision for returned Decimal
        '''
        try:
            if __pr==None:__pr=getpr();
            lm=algbra.div(len(__x),'2',1);x=deciml_sort(__x,__pr+2);
            if (i:=int(lm))<lm:return x[i];
            else:return(algbra.div(algbra.add(x[i-1],x[i],pr=__pr+1),'2',__pr));
        except Exception as e:print("Invalid command: stat.median\n",e);return None;
    
    @staticmethod
    def mode(__x:list[Decimal|str|float]|tuple[Decimal|str|float,...])->dict["values":tuple[Decimal,...],"mode":int]|None:
        '''
#### Get the mode of numbers as dict with keys - values and mode.
##### Note: Values are the numbers with mode occurrences.
- **__x**: List or tuple of numbers

        '''
        try:
            d=dict();r=list();
            for i in __x:d[i]=d.setdefault(i,0)+1;
            c=max(d.values())
            for i in d.items():
                if i[1]==c:r.append(i[0]);
            return {"values":tuple(r),"mode":c}
        except Exception as e:print("Invalid command: stat.mode\n",e);return None;



# print(deciml(22.01234485145124641E+42), deciml(0.000015646541E+100))
# print(algbra.add(0.1234567156461254845148546554, '1.1234567'), algbra.add(1.2646515484544556546, 1, 2, 5), algbra.add(1.0123456789E-5, 1.234567890E-5), algbra.add(0.000010123456789, 0.00001234567890))
# print(algbra.add(0.1234567156461254845148546554, 1.1234567), algbra.add(1.2646515484544556546, 1, 2, 5), algbra.mul(-2,-4), algbra.mul(-2.123, 1.123), algbra.mul(2E+1,-1.123), algbra.mul(12.5467E-1, 25), algbra.div(4E-1,2), algbra.div(2E+1,4), algbra.div(2.5E+1, 7.5), algbra.div(-7.5E-1, -2.5), algbra.div(7.5, -2), algbra.div(-2, 7.5))
# print(Decimal(str(2 ** 0.5)))
# a=algbra.log(0.9395227492140118E-100, 2E-11)
# print(a, len(str(a)))
# print(trig.cos(trig.acos(0)), len(str(trig.cos(trig.acos(0)))))
# print(algbra.pwr(2, 3), algbra.pwr(2, -3.5), algbra.div(constant.pi(), 1), trig.sin(trig.asin(-0.8)), trig.cos(trig.acos(-0.8)), trig.tan(trig.atan(111111111111)), trig.tan(1.5707963267947966))
# print(htrig.sinh(-10), htrig.cosh(-10))

# print(trig.asin(-1.0), trig.asin(1.0))
# print(constant.pi()/2)
# print(trig.acos(-1.0), trig.acos(1.0))
# print(trig.acot(0.0000001), trig.acot(-0.0000001))
# print(trig.asec(-1.0), trig.asec(1.0))

# r=rdeciml('.111111e-1',5E-20)
# print(r.random(5))
# setpr(5)
# print(deciml('.454245424'))

# a=stat.median([1,2,3,4,5,3,2,1,2,3])
# print(a)
# a=stat.mode(['1','2','3','4','5','3','2','1','2','3'])
# print(a)
# print(deciml('000.00000000000000000045'))
# print(algbra.log('1', '10'))
# print(deciml_sort(['2.42153154E3', 2.852582, 5.52582], 4))
# print(deciml('2.42153154E+10', 0))
# print(algbra.div(1, '2.4215315E-30', 1))
# print(algbra.div(1, '24215315.0E-37', 1))

# print(algbra.div('0.0', '-5.00'))

# setpr(3)
# print(deciml('12.000000000000000'))
print("Imported deciml...")
