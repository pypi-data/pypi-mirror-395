from compare.cmpr import tmatx, eqval, tdeciml, eqllen, tint, ttup, tslice
from terminate import retrn
from deciml_maths import *
from decimal import Decimal
from html import escape

try:
    from IPython.display import display, HTML

    display(HTML("""
    <style>
    .output_scroll {
        overflow: hidden !important;
    }
    .jp-OutputArea {
        overflow: hidden !important;
    }
    </style>
    """))
except:
    pass

class matx:
    
    def __init__(self,li:list[Decimal|str|float]|tuple[Decimal|str|float]|list[list[Decimal|str|float]]|tuple[tuple[Decimal|str|float,...]],chk:bool=True,ret:str='a')->None:
        '''
#### 2-D Matrix object.
- **li**: List or tuple of lists or tuples of numbers
- **chk**: Check and convert elements to Decimal for set precision
- **ret**: Exit type
        '''
        try:
            if (tli:=li.__class__.__name__)=='matx':self.__matx=li.matx;self.__collen=li.collen;self.__rowlen=li.rowlen;self.__sqmatx=li.sqmatx;self.__dnant=None;self.__invse=None;self.__invsednant=None;self.__cofacm=None;self.__adjnt=None;self.__tpose=None;
            else:
                match chk:
                    case True:
                        if tli=='list' or tli=='tuple':
                            if (tli0:=li[0].__class__.__name__)=='tuple' or tli0=='list':
                                if eqllen(li) is None:raise Exception("Invalid argument: li - Row lengths not equal.");
                            else:li=li,;
                            if (li:=tdeciml.dall(li,getpr())) is None:raise Exception("Invalid argument: li - Cannot convert elements to Decimal.");
                        else:raise Exception("Invalid argument: li => list/tuple/matx, got {}".format(tli));
                    case False:
                        if not ttup(li):raise Exception("Invalid argument: li => tuple/matx")
                        if li[0].__class__.__name__=="Decimal":li=li,
                        for i in li:
                            for j in i:
                                if j.__class__.__name__!='Decimal':raise Exception(str(j)+" is not Decimal");
                    case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
                lc=len(li);lr=len(li[0]);
                if lr==lc:sq=True;
                else:sq=False;
                self.__matx: tuple[tuple[Decimal,...]]=li;self.__collen=lc;self.__rowlen=lr;self.__sqmatx=sq;self.__dnant=None;self.__invse=None;self.__invsednant=None;self.__cofacm=None;self.__adjnt=None;self.__tpose=None;
        except Exception as e:print("Invalid command: matx()");retrn(ret,e);

    @property
    def matx(self)->tuple:
        '''
#### Get and set the 2-D matrix.
        '''
        return self.__matx;
    
    @matx.setter
    def matx(self,li:list|tuple)->None:
        try:
            if (tli:=li.__class__.__name__)=='matx':self.__matx=li.matx;self.__collen=li.collen;self.__rowlen=li.rowlen;self.__sqmatx=li.sqmatx;self.__dnant=None;self.__invse=None;self.__invsednant=None;self.__cofacm=None;self.__adjnt=None;self.__tpose=None;
            elif tli=='list' or tli=='tuple':
                if (tli0:=li[0].__class__.__name__)=='tuple' or tli0=='list':
                    if eqllen(li) is None:raise Exception("Invalid argument: li - Row lengths not equal.");
                else:li=li,;
                if (li:=tdeciml.dall(li,getpr())) is None:raise Exception("Invalid argument: li - Cannot convert elements to Decimal");
                lc=len(li);lr=len(li[0]);
                if lr==lc:sq=True;
                else:sq=False;
                self.__matx=li;self.__collen=lc;self.__rowlen=lr;self.__sqmatx=sq;self.__dnant=None;self.__invse=None;self.__invsednant=None;self.__cofacm=None;self.__adjnt=None;self.__tpose=None;
            else:raise Exception("Invalid argument: li => list/tuple/matx, got {}".format(tli));
        except Exception as e:print("Invalid command: matx()");retrn('a',e);
    
    @property
    def collen(self)->int:
        '''
#### Get the column length.
        '''
        return self.__collen;
    
    @property
    def rowlen(self)->int:
        '''
#### Get the row length.
        '''
        return self.__rowlen;
    
    @property
    def sqmatx(self)->bool:
        '''
#### Get True if square matrix, otherwise False.
        '''
        return self.__sqmatx;
    
    # prints the value of matx object
    @matx.getter
    def pmatx(self)->tuple[tuple[Decimal,...]]:
        '''
#### Print the matrix.
        '''
        max_in_col=tuple(map(lambda i:max(tuple(map(lambda j:len(str(j)),i))),tuple(zip(*self.__matx))))
        print("matx(")
        scl=len(str(self.__collen))
        row=0
        s=str()
        for _ in range(scl):s+="_"
        s+="____|"
        for i in range(self.__rowlen):
            spaces=str()
            for _ in range(int(abs(max_in_col[i]-len(str(i))))):spaces+="_"
            s+=spaces[:(len(spaces)//2)]+"_["+str(i)+"]"+spaces[len(spaces)//2:]+"_|"
            if max_in_col[i] < len(str(i)):max_in_col[i]=len(str(i))
        print(s)
        for k in [[str(j) for j in i] for i in self.__matx]:
            spaces=str()
            for _ in range(scl-len(str(row))):spaces+=" "
            s=" ("+str(row)+")"+spaces+" |"
            row+=1
            for index,l in enumerate(k):
                spaces=str();
                for _ in range(max_in_col[index]-len(l)):spaces+=" "
                s+=spaces+" '"+l+"'"+" |"
            print(s)
        print(')\n')

    def __str__(self):
        max_in_col=tuple(map(lambda i:max(tuple(map(lambda j:len(str(j)),i))),tuple(zip(*self.__matx))))
        ret="matx(\n"
        scl=len(str(self.__collen))
        row=0
        s=str()
        for _ in range(scl):s+="_"
        s+="____|"
        for i in range(self.__rowlen):
            spaces=str()
            for _ in range(int(abs(max_in_col[i]-len(str(i))))):spaces+="_"
            s+=spaces[:(len(spaces)//2)]+"_["+str(i)+"]"+spaces[len(spaces)//2:]+"_|"
            if max_in_col[i] < len(str(i)):max_in_col[i]=len(str(i))
        ret+=s+"\n"
        for k in [[str(j) for j in i] for i in self.__matx]:
            spaces=str()
            for _ in range(scl-len(str(row))):spaces+=" "
            s=" ("+str(row)+")"+spaces+" |"
            row+=1
            for index,l in enumerate(k):
                spaces=str();
                for _ in range(max_in_col[index]-len(l)):spaces+=" "
                s+=spaces+" '"+l+"'"+" |"
            ret+=s+"\n"
        ret+=')\n'
        return ret

    def __repr__(self):
        max_in_col=tuple(map(lambda i:max(tuple(map(lambda j:len(str(j)),i))),tuple(zip(*self.__matx))))
        ret="matx(\n"
        scl=len(str(self.__collen))
        row=0
        s=str()
        for _ in range(scl):s+="_"
        s+="____|"
        for i in range(self.__rowlen):
            spaces=str()
            for _ in range(int(abs(max_in_col[i]-len(str(i))))):spaces+="_"
            s+=spaces[:(len(spaces)//2)]+"_["+str(i)+"]"+spaces[len(spaces)//2:]+"_|"
            if max_in_col[i] < len(str(i)):max_in_col[i]=len(str(i))
        ret+=s+"\n"
        for k in [[str(j) for j in i] for i in self.__matx]:
            spaces=str()
            for _ in range(scl-len(str(row))):spaces+=" "
            s=" ("+str(row)+")"+spaces+" |"
            row+=1
            for index,l in enumerate(k):
                spaces=str();
                for _ in range(max_in_col[index]-len(l)):spaces+=" "
                s+=spaces+" '"+l+"'"+" |"
            ret+=s+"\n"
        ret+=')\n'
        return ret
    
    def _repr_html_(self):
        max_in_col=tuple(map(lambda i:max(tuple(map(lambda j:len(str(j)),i))),tuple(zip(*self.__matx))))
        scl=len(str(self.__collen))
        s=str()
        for _ in range(scl):s+="_"
        s+="____|"
        for i in range(self.__rowlen):
            spaces=str()
            for _ in range(int(abs(max_in_col[i]-len(str(i))))):spaces+="_"
            s+=spaces[:(len(spaces)//2)]+"_["+str(i)+"]"+spaces[len(spaces)//2:]+"_|"
            if max_in_col[i] < len(str(i)):max_in_col[i]=len(str(i))
        lnth=len(s)
        ret="matx(\n".format(len(s)+3)
        row=0
        ret+=s+"\n"
        for k in [[str(j) for j in i] for i in self.__matx]:
            spaces=str()
            for _ in range(scl-len(str(row))):spaces+=" "
            s=" ("+str(row)+")"+spaces+" |"
            row+=1
            for index,l in enumerate(k):
                spaces=str();
                for _ in range(max_in_col[index]-len(l)):spaces+=" "
                s+=spaces+" '"+l+"'"+" |"
            ret+=s+"\n"
        ret+=')'
        return "<pre style='max-height:45vh;min-width:{}ch'>{}</pre>".format(lnth+10, escape(ret))


    def __getitem__(self, index:slice|int|tuple[int|slice,int|slice]):
        try:
            if (ti:=index.__class__.__name__)=='tuple':
                if len(index)!=2:raise IndexError("Expected 2 slices got {}".format(len(index)))
                else:
                    if (ti0:=index[0].__class__.__name__)=='int' and index[1].__class__.__name__=='int':return self.__matx[index[0]][index[1]]
                    elif ti0=='int' and (index[1].__class__.__name__=='slice' or index[1].__class__.__name__=='int'):
                        return matx(self.__matx[index[0]][index[1]])
                    elif tslice(index[0]):
                        if index[1].__class__.__name__=='slice':
                            return matx([i[index[1]] for i in self.__matx[index[0]]])
                        if index[1].__class__.__name__=='int':
                            return matx([[i[index[1]],] for i in self.__matx[index[0]]])
                    else:raise IndexError("Expected slice or int got {} and {}".format(index[0].__class__.__name__, index[1].__class__.__name__))
            elif ti=='slice' or ti=='int':return matx(self.__matx[index])
            else:raise IndexError("Expected slice got {}".format(ti))
        except Exception as e:retrn('a', e);
    
    def dnant(self)->Decimal:
        '''
#### Get the determinant of matrix.
        '''
        if self.__dnant is None and self.__sqmatx is True:self.__dnant=matutils.dnant(matx(self.__matx,False,'c'),False,'w');return self.__dnant;
        else:return self.__dnant;

    def invsednant(self)->Decimal:
        '''
#### Get the determinant of the inverse matrix.
        '''
        if self.__invsednant is None and self.__sqmatx is True:self.__invsednant=matutils.invsednant(matx(self.__matx,False,'c'),False,'w');return self.__invsednant;
        else:return self.__invsednant;
    
    def invse(self):
        '''
#### Get the inverse matrix of the matrix.
        '''
        if self.__invse is None and self.sqmatx is True and self.dnant()!=0:self.__invse=matutils.invse(matx(self.__matx,False,'c'),False,'w');return self.__invse;
        else:return self.__invse;
    
    def adjnt(self):
        '''
#### Get the adjoint matrix of the matrix.
        '''
        if self.__adjnt is None and self.__sqmatx is True:self.__adjnt=matutils.adjnt(matx(self.__matx,False,'c'),False,'w');return self.__adjnt;
        else:return self.__adjnt;

    def tpose(self):
        '''
#### Get the transpose of the matrix.
        '''
        if self.__tpose is None:self.__tpose=matutils.tpose(matx(self.__matx,False,'c'),False,'w');return self.__tpose;
        else:return self.__tpose;
    
    def cofacm(self):
        '''
#### Get the cofactor matrix of the matrix.
        '''
        if self.__cofacm is None:self.__cofacm=matx(tuple([tuple([matutils.cofac(matx(self.__matx,False,'c'),i,j,False,'c') for j in range(self.__rowlen)]) for i in range(self.__collen)]),False,'w');return self.__cofacm;
        else:return self.__cofacm;

    # returns matx as a list
    def matxl(self)->list:
        '''
#### Get the matrix as a list of lists.
        '''
        return [list(i) for i in self.__matx];
    
    def pop(self,i:int,r:bool=True,chk:bool=True,ret:str='a')->tuple[Decimal,...]:
        '''
#### Pop a row or column of the matrix.
- **i**: Row or column index
- **r**: True for row and False for column
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if (i:=tint.ele(i,self.__collen)) is None:raise Exception;
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            match r:
                case True:m=list(self.__matx);p=m.pop(i);self.__matx=tuple(m);self.__collen=self.__collen-1;
                case False:
                    m=self.matxl();p=list();
                    for j in range(self.__collen):p.append(m[j].pop(i));m[j]=tuple(m[j]);
                    self.__matx=tuple(m);self.__rowlen=self.__rowlen-1;
                case _:raise Exception("Invalid argument: r => bool, got {}".format(r.__class__.__name__))
            del m
            if self.__collen==self.__rowlen:self.__sqmatx=True;
            else: self.__sqmatx=False;
            return tuple(p)
        except Exception as e:print("Invalid command: matx.pop()");retrn(ret,e);

    # return element at i,j of matrix
    def mele(self,i:int,j:int,chk:bool=True,ret:str='a')->Decimal:
        '''
#### Get an element of matrix.
- **i**: Row index
- **j**: Column index
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:return self.__matx[i][j];
                case True:
                    if (i:=tint.ele(i,self.__collen)) is None or (j:=tint.ele(j,self.__rowlen)) is None:raise Exception;
                    return self.__matx[i][j]
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
        except Exception as e:print("Invalid command: matx.mele()");retrn(ret,e);

    # return tuple of i'th row
    def mrow(self,i:int,chk:bool=True,ret:str='a')->tuple[Decimal,...]:
        '''
#### Get a row of matrix.
- **i**: Row index
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:return self.__matx[i];
                case True:
                    if (i:=tint.ele(i,self.__collen)) is None:raise Exception;
                    return self.__matx[i]
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
        except Exception as e:print("Invalid command: matx.mrow()");retrn(ret,e);

    # returns tuple of i'th column
    def mcol(self,j:int,chk:bool=True,ret:str='a')->tuple[Decimal,...]:
        '''
#### Get the column of matrix.
- **j**: Column index
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:return tuple([self.__matx[i][j] for i in range(self.__collen)]);
                case True:
                    if (j:=tint.ele(j,self.__rowlen)) is None:raise Exception;
                    return tuple([self.__matx[i][j] for i in range(self.__collen)])
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
        except Exception as e:print("Invalid command: matx.mcol()");retrn(ret,e);
    
    def gele(self,a:list|tuple,r:bool=False,chk:bool=True,ret:str='a')->tuple[tuple[Decimal,...],...]:
        '''
#### Get the rows or columns of the matrix.
- **a**: List or tuple of row or column indexes
- **r**: True for row and False for column
- **chk**: Check argument
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if a is None:raise Exception;
                    match r:
                        case True:a=tint.ele(a,self.__collen,True);
                        case False:a=tint.ele(a,self.__rowlen,True);
                        case _:raise Exception("Invalid argument: r => bool, {}".format(r.__class__.__name__));
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            match r:
                case True:return tuple([self.__matx[i] for i in a]);
                case False:
                    r=self.__matx[0];r=[[r[i],] for i in a];a=tuple(enumerate(a));
                    for i in self.__matx[1:]:
                        for j in a:r[j[0]].append(i[j[1]]);
                    return tuple([tuple(i) for i in r])
                case _:raise Exception("Invalid argument: r => bool, got {}".format(r.__class__.__name__));
        except Exception as e:print("Invalid command: matx.gele()");retrn(ret,e);

class matutils:

    # returns scalar matrix of size nxn
    @staticmethod
    def sclrm(n:int,el:Decimal,chk:bool=True,ret:str='a')->matx:
        '''
#### Get a scalar matrix as a matx object.
- **n**: Number of rows for square matrix
- **el**: Value for the diagonal elements
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if (n:=tint.intn(n)) is None or str(el:=deciml(str(el)))=='NaN':raise Exception;
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            m=list()
            for i in range(n):
                l1=list()
                for j in range(n):
                    if i==j:l1.append(el);
                    else:l1.append(Decimal('0.0'));
                m.append(tuple(l1))
            return matx(tuple(m),False,'c')
        except Exception as e:print("Invalid command: matutils.sclrm()");retrn(ret,e);

    # returns matrix of size mxn with equal elements
    @staticmethod
    def eqelm(m:int,n:int,i:Decimal,chk:bool=True,ret:str='a')->matx:
        '''
#### Get a matrix of equal elements as a matx object.
- **m**: Number of rows
- **n**: Number of columns
- **i**: Value for elements
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:return matx(tuple([tuple([i for _ in range(n)]) for _ in range(m)]),False,'c');
                case True:
                    if (n:=tint.intn(n)) is None or (m:=tint.intn(m)) is None or str(i:=deciml(i))=='NaN':raise Exception;
                    return matx(tuple([tuple([i for _ in range(n)]) for _ in range(m)]),False,'c')
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__))
        except Exception as e:print("Invalid command: matutils.eqelm()");retrn(ret,e);

    @staticmethod
    def addmatx(a:matx,*b:matx,r:bool=False,chk:bool=True,ret:str='a')->matx:
        '''
#### Get a matrix for matrices in matx objects after appending along row or column direction.
- **a**: matx object
- **\\*b**: matx objects
- **r**: True for row and False for column
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx((a,)+b,True) is None:raise Exception;
                    match r:
                        case False:
                            for i in b:
                                if eqval(i.collen,a.collen) is None:raise Exception;
                        case True:
                            for i in b:
                                if eqval(i.rowlen,a.rowlen) is None:raise Exception;
                        case _:raise Exception("Invalid argument: r => bool, got {}".format(r.__class__.__name__));
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            match r:
                case False:
                    a=list(a.matx)
                    for i in b:
                        l=0
                        for j in i.matx:a[l]=a[l]+j;l+=1;
                    return matx(tuple(a), True if chk else False,'c')
                case True:
                    r=a.matx
                    for i in b:r+=i.matx;
                    return matx(r,True if chk else False,'c')
                case _:raise Exception("Invalid argument: r => bool, got {}".format(r.__class__.__name__));
        except Exception as e:print("Invalid command: matutils.addmatx()");retrn(ret,e);

    @classmethod
    def maddval(cls,a:matx,x:Decimal,chk:bool=True,ret:str='a')->matx:
        '''
#### Get a matrix as a matx object with a number added to all matrix rows at the first index.
- **a**: matx object
- **x**: Number
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:return cls.addmatx(cls.eqelm(a.collen,1,x,False,'c'),a,r=False,chk=False,ret='c');
                case True:
                    if tmatx(a) is None or str(x:=deciml(str(x),getpr()))=='NaN':raise Exception;
                    return cls.addmatx(cls.eqelm(a.collen,1,x,False,'c'),matx(a,True,'c'),r=False,chk=False,ret='c')
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
        except Exception as e:print("Invalid command: matutils.maddval()");retrn(ret,e);

    # convert list x to x
    @staticmethod
    def matlxtox(a:matx,chk:bool=True,ret:str='a')->tuple:
        '''
#### Get the rows of matrix as matx objects.
- **a**: matx object
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:return tuple([matx(i,False,'c') for i in a.matx]);
                case True:
                    if tmatx(a) is None:raise Exception;
                    return tuple([matx(i,True,'c') for i in a.matx])
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
        except Exception as e:print("Invalid command: matutils.matlxtox()");retrn(ret,e);

    @staticmethod
    def matxtolx(a:tuple[matx,...]|list,chk:bool=True,ret:str='a')->matx:
        '''
#### Get a matrix from row matrices as a matx object.
- **a**: matx object
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            x=list()
            match chk:
                case False:return matx(tuple([i.matx[0] for i in a]),False,'c');
                case True:
                    if tmatx(a,True) is None:raise Exception;
                    ar=a[0].rowlen
                    for i in a:
                        if eqval(i.collen,1) is None or eqval(i.rowlen,ar) is None:raise Exception;
                        x.append(i.matx[0])
                    return matx(tuple(x),True,'c')
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
        except Exception as e:print("Invalid command: matutils.matxtolx()");retrn(ret,e);

    # returns row or column elements of the matrix
    @staticmethod
    def gele(a:matx,b:list,r:bool=False,chk:bool=True,ret:str='a')->matx:
        '''
#### Get the rows or columns of a matrix as a matx object of matrix.
- **a**: matx object
- **b**: List or tuple with indexes of rows or columns
- **r**: True for rows and False for columns
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:return matx(a.gele(b,r,chk,r),False,'c');
        except Exception as e:print("Invalid command: matutils.gele()");retrn(ret,e);

    # returns the transpose of the matrix
    @classmethod
    def tpose(cls,a:matx,chk:bool=True,ret:str='a')->matx:
        '''
#### Get the transpose matrix as matx object.
- **a**: matx object
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:return matx(tuple(zip(*a.matx)),False,'c');
                case True:
                    if tmatx(a) is None:raise Exception;
                    return matx(tuple(zip(*a.matx)),False,'c')
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
        except Exception as e:print("Invalid command: matutils.tpose()");retrn(ret,e);

    # returns the co-factor of the matrix element
    @classmethod
    def cofac(cls,a:matx,b:int,c:int,chk:bool=True,ret:str='a')->Decimal:
        '''
#### Get the cofactor of a matrix for an element.
- **a**: matx object
- **b**: row index
- **c**: column index
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case True:
                    if tmatx(a) is None or (b:=tint.ele([b,c],a.rowlen,True)) is None:raise Exception;
                    else:b,c=b;
                    if a.sqmatx is False:raise Exception("Error: Not a square matrix");
                case False:pass;
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            a=matx(a,False,'c');a.pop(c,False,False,'c');a.pop(b,chk=False,ret='c');
            setpr(getpr()+1)
            dnant = cls.dnant(a,False,'c')
            setpr(getpr()-1)
            if (p:=alg.div((b+c),2))==int(p):return deciml(dnant);
            else:return alg.mul('-1',dnant);
        except Exception as e:print("Invalid command: matutils.cofac()");retrn(ret,e);

    # returns the determinant of the matrix
    @classmethod
    def dnant(cls,a:matx,chk:bool=True,ret:str='a')->Decimal:
        '''
#### Get the determinant of a matrix.
- **a**: matx object
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx(a) is None:raise Exception;
                    if a.sqmatx is False:raise Exception("Error: Not a square matrix");
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            a=matx(a,False,'c')
            if (lr:=a.rowlen)==1:return a.mele(0,0,False,'c');
            else:
                ep=None;ele=a.mele(0,0,False,'c');li=a.mrow(0,False,'c');
                if ele==0:
                    for i in range(lr):
                        if i>0:
                            if li[i]!=0:e=li[i];ep=i;
                    if ep is None:return Decimal('0');
                else:ep=0;e=ele;
                setpr(getpr()+1)
                for i in range(lr):
                    if i!=ep:setpr(getpr()+1);ele=li[i];fac=alg.div(alg.mul('-1',ele,pr=getpr()+1),e);a.matx=cls.tform(a,i,ep,fac,False,False,'c');setpr(getpr()-1)
                cofac=cls.cofac(a,0,ep,False,'c')
                setpr(getpr()-1)
                return alg.mul(e,cofac)
        except Exception as e:print("Invalid command: matutils.dnant()");retrn(ret,e);

    # returns adjoint matrix of the matrix
    @classmethod
    def adjnt(cls,a:matx,chk:bool=True,ret:str='a')->matx:
        '''
#### Get the adjoint matrix as a matx object for a matrix.
- **a**: matx object
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:m=tuple([tuple([cls.cofac(a,j,i,False,'c') for j in range(a.collen)]) for i in range(a.rowlen)]);return matx(m,False,'c');
                case True:
                    if tmatx(a) is None:raise Exception;
                    if a.sqmatx is False:raise Exception("Error: Not a square matrix");
                    m=tuple([tuple([cls.cofac(a,j,i,False,'c') for j in range(a.collen)]) for i in range(a.rowlen)]);return matx(m,False,'c');
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
        except Exception as e:print("Invalid command: matutils.adjnt()");retrn(ret,e);

    # returns inverse matrix of the matrix
    @classmethod
    def invse(cls,a:matx,chk:bool=True,ret:str='a')->matx:
        '''
#### Get the inverse matrix of a matrix as a matx object.
- **a**: matx object
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx(a) is None:raise Exception;
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            setpr(getpr()+2)
            if (det:=cls.dnant(a,False,'c')) is None:raise Exception;
            setpr(getpr()-2)
            if det==0:raise Exception("Error: Determinant is 0,\nInverse DNE!");
            setpr(getpr()+1);v=alg.div(1,det);adj=cls.adjnt(a,False,'c');setpr(getpr()-1)
            return cls.smult(v,adj,chk=False,ret='c')
        except Exception as e:print("Invalid command: matutils.invse()");retrn(ret,e);
    
    # returns inverse matrix of the matrix using matrix transformation
    # det(A^-1) = det(B/L^(1/n)) or det(-B/L^(1/n))
    @classmethod
    def invsednant(cls,a:matx,chk:bool=True,ret:str='a')->Decimal:
        '''
#### Get the determinant of the inverse matrix for a matrix.
- **a**: matx object
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case True:
                    if tmatx(a) is None:raise Exception;
                case False:pass;
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            setpr(getpr()+1)
            a=matx(a,False,'c');
            b=cls.sclrm(a.rowlen,Decimal('1.0'),False,'c')
            l=list()
            for i in range(a.collen):
                ele=a.mele(i,i,False,'c')
                if ele==0:
                    el=0
                    for j in range(i+1,a.rowlen):
                        el=a.mele(i,j,False,'c')
                        if el!=0:a.matx=cls.tform(a,i,j,alg.div('1',el,getpr()+1),False,False,'c');b.matx=cls.tform(b,i,j,alg.div('1',el,getpr()+1),False,False,'c');break;
                    if el==0:
                        raise Exception("Error: Invalid Matrix Inverse");
                l.append(ele:=a.mele(i,i,False,'c'));row=a.mrow(i,False,'c');col=a.mcol(i,False,'c');
                for j in range(i+1,a.rowlen):
                    el=row[j];e=col[j];
                    a.matx=cls.tform(a,j,i,alg.div(alg.mul('-1',el,pr=getpr()+2),ele,getpr()+1),False,False,'c');b.matx=cls.tform(b,j,i,alg.div(alg.mul(-1,el,pr=getpr()+2),ele,getpr()+1),False,False,'c');a.matx=cls.tform(a,j,i,alg.div(alg.mul('-1',e,pr=getpr()+2),ele,getpr()+1),True,False,'c');b.matx=cls.tform(b,j,i,alg.div(alg.mul('-1',e,pr=getpr()+2),ele,getpr()+1),True,False,'c');del e;del el;
                del ele
            if (lam:=alg.div('1',alg.mul(*l)))==0:raise Exception("Error: Invalid Matrix Inverse");
            else:ret=alg.mul(lam,cls.dnant(b,False,'c'))
            setpr(getpr()-1)
            return deciml(ret)
        except Exception as e:print("Invalid command: matutils.invsednant()");retrn(ret,e);

    # returns matrix after row or column tranformation
    @classmethod
    def tform(cls,a:matx,b:int,c:int,d:Decimal,r:bool=False,chk:bool=True,ret:str='a')->matx:
        '''
#### Get the row or column transformation for a matrix as a matx object.
- **a**: matx object
- **b**: Row or column index to transform
- **c**: Row or column index for transformation
- **d**: Number to multiply with elements of *"c"*
##### Note - [b] -> [b] + d*[c]
- **r**: True for row transformation and False for column transformation
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx(a) is None or str(d:=deciml(d,getpr()))=='NaN':raise Exception;
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            if (m:=a.gele([b,c],r,chk,'c')) is None:raise Exception;
            a=list(a.matx)
            match r:
                case True:a[b]=galg.add(m[0],galg.mulsg(d,m[1],getpr()+1));
                case False:
                    for i in enumerate(galg.add(m[0],galg.mulsg(d,m[1],getpr()+1))):a1=list(a[i[0]]);a1[b]=i[1];a[i[0]]=tuple(a1);
                case _:raise Exception;
            return matx(tuple(a),False,'c');
        except Exception as e:print("Invalid command: matutils.tform()");retrn(ret,e);

    # returns sum of two matrices
    @staticmethod
    def madd(a:matx,b:matx,sumr:bool|None=None,chk:bool=True,ret:str='a')->matx|tuple[Decimal,...]:
        '''
#### Get the added matrix of two matrices as a matx object.
- **a**: matx object
- **b**: matx object
- **sumr**: Return sum of rows or columns as a tuple instead of a matx object
    - ***None***: matx object
    - ***True***: sum of elements in each column
    - ***False***: sum of elements in each row
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx([a,b],True) is None:raise Exception;
                    if eqval([a.collen,a.rowlen],[b.collen,b.rowlen]) is None:raise Exception;
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            if sumr != None:setpr(getpr()+1)
            r=[galg.add(*i) for i in zip(a.matx,b.matx)];
            if sumr != None:setpr(getpr()-1)
            match sumr:
                case None:return matx(tuple(r),False,'c');
                case True:return galg.add(*r);
                case False:return tuple([alg.add(*i) for i in r]);
                case _:raise Exception("invalid argument: sumr => None/bool, got {}".format(sumr.__class__.__name__));
        except Exception as e:print("Invalid command: matutils.madd()");retrn(ret,e);
    
    @classmethod
    def saddcnst(cls,a:tuple[Decimal,...]|list[Decimal]|Decimal,b:matx,r:bool|None=False,sumr:bool|None=None,chk:bool=True,ret:str='a')->matx|tuple[Decimal,...]:
        '''
#### Get the matrix on addition of a single constant to each row or column as a matx object.
- **a**: A number or list/tuple of numbers to add
- **b**: matx object
- **r**: 
    - ***None***: Add a number to all elements
    - ***True***: Add a number to each row
    - ***False***: Add a number to each column
- **sumr**: Return sum of rows or columns as a tuple instead of a matx object
    - ***None***: matx object
    - ***True***: sum of elements in each column
    - ***False***: sum of elements in each row
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if r is not None:
                        if (a:=tdeciml.dall(a,getpr()) if not tdeciml.deciml(a,True) else a) is None:raise Exception;
                    else:
                        if str(a:=deciml(a,getpr()) if a.__class__.__name__!='Decimal' else a)=='NaN':raise Exception;
                    if tmatx(b) is None:raise Exception;
                    match r:
                        case True:
                            if eqval(len(a),b.collen) is None:raise Exception;
                        case False:
                            if eqval(len(a),b.rowlen) is None:raise Exception;
                        case None:pass;
                        case _:raise Exception("Invalid argument: r => bool, got {}".format(r.__class__.__name__));
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            if sumr != None:setpr(getpr()+1)
            match r:
                case True:r=[galg.addsg(i[0],i[1]) for i in zip(a,b.matx)];
                case False:r=[galg.add(a,i) for i in b.matx];
                case None:r=[galg.addsg(a,i) for i in b.matx];
                case _:raise Exception("Invalid argument: r => bool/None, got {}".format(r.__class__.__name__));
            if sumr != None:setpr(getpr()-1)
            match sumr:
                case None:return matx(tuple(r),False,'c');
                case True:return galg.add(*r);
                case False:return tuple([alg.add(*i) for i in r]);
                case _:raise Exception("Invalid argument: sumr => None/bool, got {}".format(sumr.__class__.__name__));
        except Exception as e:print("Invalid command: matutils.saddcnst()");retrn(ret,e);

    # returns difference of two matrices
    @staticmethod
    def msub(a:matx,b:matx,sumr:bool|None=None,chk:bool=True,ret:str='a')->matx|tuple[Decimal,...]:
        '''
#### Get the subtracted matrix of two matrices as a matx object.
- **a**: matx object
- **b**: matx object
- **sumr**: Return sum of rows or columns as a tuple instead of a matx object
    - ***None***: matx object
    - ***True***: sum of elements in each column
    - ***False***: sum of elements in each row
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx([a,b],True) is None:raise Exception;
                    if eqval([a.collen,a.rowlen],[b.collen,b.rowlen]) is None:raise Exception;
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            if sumr != None:setpr(getpr()+1)
            r=[galg.sub(*i) for i in zip(a.matx,b.matx)];
            if sumr != None:setpr(getpr()-1)
            match sumr:
                case None:return matx(tuple(r),False,'c');
                case True:return galg.add(*r);
                case False:return tuple([alg.add(*i) for i in r]);
                case _:raise Exception("invalid argument: sumr => None/bool, got {}".format(sumr.__class__.__name__));
        except Exception as e:print("Invalid command: matutils.msub()");retrn(ret,e);

    # returns matrix after scalar multiplication
    @staticmethod
    def smult(a:Decimal,b:matx,sumr:bool|None=None,chk:bool=True,ret:str='a')->matx|tuple[Decimal,...]:
        '''
#### Get the matrix for elements of a matrix multiplied by a number as a matx object.
- **a**: Number
- **b**: matx object
- **sumr**: Return sum of rows or columns as a tuple instead of a matx object
    - ***None***: matx object
    - ***True***: sum of elements in each column
    - ***False***: sum of elements in each row
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if not str(a:=deciml(a,getpr()+1) if a.__class__.__name__!='Decimal' else a):raise Exception;
                    if tmatx(b) is None:raise Exception;
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            if sumr != None:setpr(getpr()+1)
            r=[galg.mulsg(a,i) for i in b.matx]
            if sumr != None:setpr(getpr()-1)
            match sumr:
                case None:return matx(tuple(r),False,'c');
                case True:return galg.add(*r);
                case False:return tuple([alg.add(*i) for i in r]);
                case _:raise Exception("Invalid argument: sumr => None/bool, got {}".format(sumr.__class__.__name__));
        except Exception as e:print("Invalid command: matutils.smult()");retrn(ret,e);

    @classmethod
    def smultfac(cls,a:tuple[Decimal,...]|list[Decimal],b:matx,r:bool=True,sumr:bool|None=None,chk:bool=True,ret:str='a')->matx|tuple[Decimal,...]:
        '''
#### Get the matrix for rows or columns of a matrix multiplied by a number as a matx object.
- **a**: List or tuple of numbers
- **b**: matx object
- **r**: True for row multiplied by a single number and False for column multiplied by a simgle number
- **sumr**: Return sum of rows or columns instead of matx object
    - ***None***: matx object
    - ***True***: sum of elements in each column
    - ***False***: sum of elements in each row
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if (a:=tdeciml.dall(a,getpr()+1) if not tdeciml.deciml(a,True) else a) is None or tmatx(b) is None:raise Exception;
                    match r:
                        case True:
                            if eqval(len(a),b.collen) is None:raise Exception;
                        case False:
                            if eqval(len(a),b.rowlen) is None:raise Exception;
                        case _:raise Exception("Invalid argument: r => bool, got {}".format(r.__class__.__name__));
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            if sumr != None:setpr(getpr()+1)
            if r is True:r=[galg.mulsg(i[0],i[1]) for i in zip(a,b.matx)];
            else:r=[galg.mul(a,i) for i in b.matx];
            if sumr != None:setpr(getpr()-1)
            match sumr:
                case None:return matx(tuple(r),False,'c');
                case True:return galg.add(*r);
                case False:return tuple([alg.add(*i) for i in r]);
                case _:raise Exception("Invalid argument: sumr => None/bool, got {}".format(sumr.__class__.__name__));
        except Exception as e:print("Invalid command: matutils.smultfac()");retrn(ret,e);

    # returns matrix after matrix multiplication
    @classmethod
    def mmult(cls,a:matx,b:matx,t:tuple[bool,bool]=(False,False),sumr:bool|None=None,chk:bool=True,ret:str='a')->matx|tuple[Decimal,...]:
        '''
#### Get the multiplied matrix of two matrices as a matx object.
- **a**: matx object
- **b**: matx object
- **t**: tuple of two booleans
    - 1<sup>st</sup> boolean:
        - ***True***: multiply with *"a"* transpose instead
    - 2<sup>nd</sup> boolean:
        - ***True***: multiply with *"b"* transpose instead
- **sumr**: Return sum of rows or columns as a tuple instead of matx object
    - ***None***: matx object
    - ***True***: sum of elements in each column
    - ***False***: sum of elements in each row
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            if sumr != None:setpr(getpr()+1)
            match t:
                case (False,False):
                    match chk:
                        case False:r=[matutils.smultfac(i,b,True,True,False,'c') for i in a.matx];
                        case True:
                            if tmatx([a,b],True) is None or eqval(a.rowlen,b.collen) is None:raise Exception;
                            r=[matutils.smultfac(i,b,True,True,False,'c') for i in a.matx]
                        case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
                case (False,True):
                    match chk:
                        case False:r=[matutils.smultfac(i,b,False,False,False,'c') for i in a.matx];
                        case True:
                            if tmatx([a,b],True) is None or eqval(a.rowlen,b.rowlen) is None:raise Exception;
                            r=[matutils.smultfac(i,b,False,False,False,'c') for i in a.matx]
                        case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
                case (True,False):
                    match chk:
                        case False:r=[matutils.smultfac(i,b,True,True,False,'c') for i in zip(*a.matx)];
                        case True:
                            if tmatx([a,b],True) is None or eqval(a.collen,b.collen) is None:raise Exception;
                            r=[matutils.smultfac(i,b,True,True,False,'c') for i in zip(*a.matx)]
                        case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
                case (True,True):
                    match chk:
                        case False:r=[matutils.smultfac(i,b,False,False,False,'c') for i in zip(*a.matx)];
                        case True:
                            if tmatx([a,b],True) is None or eqval(a.collen,b.rowlen) is None:raise Exception;
                            r=[matutils.smultfac(i,b,False,False,False,'c') for i in zip(*a.matx)]
                        case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
                case _:raise Exception("Invalid argument: t => (bool, bool), got {}".format(t.__class__.__name__));
            if sumr != None:setpr(getpr()-1)
            match sumr:
                case None:return matx(tuple(r),False,'c');
                case False:return tuple([alg.add(*i) for i in r]);
                case True:return galg.add(*r);
                case _:raise Exception("Invalid argument: sumr => None/bool, got {}".format(sumr.__class__.__name__));
        except Exception as e:print("Invalid command: matutils.mmult()");retrn(ret,e);
    
    @staticmethod
    def melmult(a:matx,b:matx,t=(False,False),sumr:bool|None=None,chk:bool=True,ret:str='a')->matx|tuple[Decimal,...]:
        '''
#### Get the matrix as a matx object for elements of two matrices multiplied.
- **a**: matx object
- **b**: matx object
- **t**: Tuple of two booleans
    - 1<sup>st</sup> boolean:
        - ***True***: Transpose of *"a"* instead
    - 2<sup></sup> boolean:
        - ***True***: Transpose of *"b"* instead
- **sumr**: Return sum of rows or columns instead of matx object
    - ***None***: Return matx object
    - ***True***: sum of elements in each column
    - ***False***: sum of elements in each row
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            if sumr != None:setpr(getpr()+1)
            match t:
                case (False,False):
                    match chk:
                        case False:r=tuple([galg.mul(*i) for i in zip(a.matx,b.matx)]);
                        case True:
                            if tmatx([a,b],True) is None or eqval([a.collen,a.rowlen],[b.collen,b.rowlen]) is None:raise Exception;
                            r=tuple([galg.mul(*i) for i in zip(a.matx,b.matx)])
                        case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
                case (True,False):
                    match chk:
                        case False:r=tuple([galg.mul(*i) for i in zip(zip(*a.matx),b.matx)]);
                        case True:
                            if tmatx([a,b],True) is None or eqval([a.collen,a.rowlen],[b.collen,b.rowlen]) is None:raise Exception;
                            r=tuple([galg.mul(*i) for i in zip(zip(*a.matx),b.matx)])
                        case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
                case (False,True):
                    match chk:
                        case False:r=tuple([galg.mul(*i) for i in zip(a.matx,zip(*b.matx))]);
                        case True:
                            if tmatx([a,b],True) is None or eqval([a.collen,a.rowlen],[b.collen,b.rowlen]) is None:raise Exception;
                            r=tuple([galg.mul(*i) for i in zip(a.matx,zip(*b.matx))])
                        case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
                case (True,True):
                    match chk:
                        case False:r=tuple([galg.mul(*i) for i in zip(zip(*a.matx),zip(*b.matx))])
                        case True:
                            if tmatx([a,b],True) is None or eqval([a.collen,a.rowlen],[b.rowlen,b.collen]) is None:raise Exception;
                            r=tuple([galg.mul(*i) for i in zip(zip(*a.matx),zip(*b.matx))])
                        case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
                case _:raise Exception("Invalid argument: t => (bool, bool), got {}".format(t.__class__.__name__));
            if sumr != None:setpr(getpr()-1)
            match sumr:
                case None:return matx(r,False,'c');
                case True:return galg.add(*r);
                case False:return tuple([alg.add(*i) for i in r]);
                case _:raise Exception("Invalid argument: sumr => None/bool, got {}".format(sumr.__class__.__name__));
        except Exception as e:print("Invalid command: matutils.melmult()");retrn(ret,e);

    @staticmethod
    def uldcompose(a:matx,chk:bool=True,ret:str='a')->tuple:
        '''
#### Get the upper, lower, and diagonal matrices for a matrix as a tuple of matx objects.
- **a**: matx object
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case True:
                    if tmatx(a) is None or a.sqmatx is None:raise Exception;
                case False:pass;
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            ut=list();lt=list();dia=list();
            for i in range(a.collen):
                ut1=list();lt1=list();
                for j in range(a.rowlen):
                    if j<i:lt1.append(a.mele(i,j,False,'c'));ut1.append(Decimal('0.0'));
                    elif i==j:dia.append(a.mele(i,j,False,'c'));lt1.append(Decimal('0.0'));ut1.append(Decimal('0.0'));
                    else:ut1.append(a.mele(i,j,False,'c'));lt1.append(Decimal('0.0'));
                ut.append(tuple(ut1));lt.append(tuple(lt1));
            return matx(tuple(ut),False,'c'),matx(tuple(lt),False,'c'),matx((tuple(dia),),False,'c')
        except Exception as e:print("Invalid command: matutils.uldcompose()");retrn(ret,e);
    
    @classmethod
    def dpose(cls,a:matx,li:list[int]|tuple[int,...],r:bool=False,chk:bool=True,ret:str='a')->tuple[matx,...]:
        '''
#### Get the matrices as a tuple of matx objects for groups of rows or columns of a matrix.
- **a**: matx object
- **li**: List or tuple with number of rows or columns
- **r**: True to decompose rows and False to decompose columns
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case True:
                    if tmatx(a) is None:raise Exception;
                    match li.__class__.__name__:
                        case 'list':
                            if (li:=tint.iwgrp(li)) is None:raise Exception;
                    match r:
                        case False:
                            if eqval(sum(li),a.rowlen) is None:raise Exception;
                        case True:
                            if eqval(sum(li),a.collen) is None:raise Exception;
                        case _:raise Exception("Invalid argument: r => bool, got {}".format(r.__class__.__name__));
                case False:pass;
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            i=0;ln=list();
            for j in li:ln.append([i+k for k in range(j)]);i+=j;
            return tuple([cls.gele(a,i,r,False,'c') for i in ln])
        except Exception as e:print("Invalid command: matutils.dpose()");retrn(ret,e);

    def moperate(a:tuple[str,tuple[tuple|matx,...]],chk:bool=True,ret:str='a')->matx:
        '''
#### Get the matx object after all matrix operations.
- a: Tuple with operation and matx objects
    - **("add" or "sub" or "mul" or "inverse", (matx,...) or another level)**
    - ***"sub"***: subtract the matrices of matx objects following the first matx object from its matrix in tuple
- chk: Check arguments
- ret: Exit type
        '''
        try:
            match chk:
                case True:
                    def __check(t):
                        if not ttup(t):return
                        if len(t) != 2:print("Invalid argument: a => tuple[str,tuple[tuple|matx,...]], tuple {} length not 2.".format([i.__class__.__name__ for i in t]));return
                case False:pass
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__))
            def __operate(o:str,a:tuple[matx|tuple[tuple[Decimal,...]],...]):
                a=tuple(map(lambda m:m.matx if m.__class__.__name__=='matx' else m,a))
                match o:
                    case "add":return tuple(map(lambda x:galg.add(*x),zip(*a)))
                    case "sub":return tuple(map(lambda xy:galg.sub(xy[0],xy[1]),zip(a[0],__operate("add",a[1:]))))
                    case "mul":
                        a,b=a[0],a[1:]
                        for i in b:
                            i=tuple(zip(*i))
                            a=tuple(map(lambda x_1:tuple(map(lambda x:alg.add(*galg.mul(x,x_1,pr=getpr()+1)),i)),a))
                        return a
                    case "invse":
                        def __cofac(__a,__j):
                            setpr(getpr()+1)
                            res=__det(tuple(map(lambda i:i[:__j]+i[__j+1:],__a[1:]))) if len(__a)!=2 else __a[1][0 if __j==1 else 1]
                            setpr(getpr()-1)
                            return res
                        def __det(__a):
                            det=0
                            setpr(getpr()+1)
                            for i in range(len(__a)):
                                det=alg.add(det,alg.mul((-1)**i,__a[0][i],__cofac(__a,i),pr=getpr()+1))
                            setpr(getpr()-1)
                            return det
                        def __adj(__a):
                            li=list()
                            for i in range(len(__a)):
                                li1=list()
                                for j in range(len(__a)):
                                    x=tuple(map(lambda k:k[:j]+k[j+1:],__a[:i]+__a[i+1:]))
                                    li1.append(alg.mul((-1)**(i+j),__det(x),pr=getpr()+1))
                                li.append(tuple(li1))
                            return tuple(zip(*li))
                        def __inv(__a):
                            det=__det(__a)
                            return tuple(map(lambda x:galg.divgs(x,det),__adj(__a)))
                        return tuple(map(lambda m:__inv(m),a))
                    case "lxtox":return tuple(map(lambda m:tuple(zip(m)),a))
                    case "xtolx":return tuple(map(lambda m:m[0],a))
                    case "tpose":return tuple(map(lambda m:tuple(zip(*m)),a))
                    case _:
                        if o.__class__.__name__=='str':print("Invalid argument: a - {} not 'add'/'sub'/'mul'/'invse'/'lxtox'/'xtolx'/'tpose'.".format(o));return
                        else:print("Invalid argument: a - {} not a string.".format(o.__class__.__name__));return
            t=a
            def __calculate(t):
                if chk:__check(t)
                a=[]
                nt=[]
                for i in t[1]:
                    if i.__class__.__name__=='matx':a.append(i)
                    elif i.__class__.__name__=='tuple':nt.append(i)
                    else:raise Exception("Invalid argument: a => tuple[str,tuple[tuple|matx,...]], has {} {}".format(i.__class__.__name__, i))
                for i in nt:
                    setpr(getpr()+1)
                    res=__calculate(i)
                    if res:
                        if i[0] in ["add","sub","mul","xtolx"]:
                            a.append(res)
                        else:
                            for j in res:
                                a.append(j)
                    else:return
                    setpr(getpr()-1)
                if len(a) < 2:
                    if t[0] not in ["invse","lxtox","xtolx","tpose"]:
                        print("Invalid argument: a - require more than one matx object to {}".format(t[0]));return
                    if len(a) == 0:
                        print("Invalid argument: a - require at least one matx object to {}".format(t[0]));return
                return __operate(t[0],a)
            r=__calculate(t)
            if not r:raise Exception
            return matx(r, False, 'c') if t[0] in ["add","sub","mul","xtolx"] else r if len(r:=tuple(map(lambda m:matx(m, False, 'c'),r))) > 1 else r[0]
        except Exception as e:print("Invalid command: moperate()");retrn(ret,e);


class melutils:

    @staticmethod
    def add(a:matx,li:list[list[int]]|tuple[list[int]]|str,r:bool=False,chk:bool=True,ret:str='a')->matx:
        '''
#### Returns a matx object with matrix rows as sum of elements with same row/column indexes in columns/rows.
- **a**: matx object
- **li**: 'all' or a list/tuple of lists or tuples of row or column indexes
- **r**: True if row indexes or False if column indexes
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if not tmatx(a):raise Exception;
                    if li != 'all':
                        if (tli:=li.__class__.__name__) != 'list' and tli != 'tuple':raise Exception("Invalid argument: li => 'all'/list/tuple, got {}".format(tli));
                        for index,i in enumerate(li):
                            if not (i:=tint.ele(i, a.collen if r == True else a.rowlen,True)):raise Exception;
                            li[index]=i
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            if (tli:=li.__class__.__name__)=='tuple' or tli=='list':
                l=list()
                for i in li:
                    for j in i:
                        if j not in l:l.append(j);
                d=dict()
                for i in enumerate(a.gele(l,r,chk,'c')):d[l[i[0]]]=i[1];
                return matx(tuple([galg.add(*[d[j] for j in i]) for i in li]),False,'c')
            elif li=='all':
                match r:
                    case False:return matx(tuple([alg.add(*i) for i in a.matx]),False,'c');
                    case True:return matx(galg.add(*a.matx),False,'c');
                    case _:raise Exception("Invalid argument: r => bool, got {}".format(r.__class__.__name__));
            else:raise Exception("Invalid argument: li => 'all'/list/tuple, got {}".format(li.__class__.__name__))
        except Exception as e:print("Invalid command: melutils.add()");retrn(ret,e);
    
    @staticmethod
    def mult(a:matx,li:list[list[int]]|tuple[list[int]]|str,r:bool=False,chk:bool=True,ret:str='a')->matx:
        '''
#### Returns a matx object with matrix rows as multiplication of elements with same row/column indexes in columns/rows.
- **a**: matx object
- **li**: 'all' or list/tuple of lists or tuples of row or column indexes
##### [a b c d] -> ([a]+[b]+[c]+[d])^T if 'li' is 'all'.
- **r**: True if row indexes or False if column indexes
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if not tmatx(a):raise Exception
                    if li != 'all':
                        for index,i in enumerate(li):
                            if not (i:=tint.ele(i, a.collen if r == True else a.rowlen,True)):raise Exception;
                            li[index]=i
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            if (tli:=li.__class__.__name__)=='list' or tli=='tuple':
                l=list()
                for i in li:
                    for j in i:
                        if j not in l:l.append(j);
                d=dict()
                for i in enumerate(a.gele(l,r,chk,'c')):d[l[i[0]]]=i[1];
                return matx(tuple([galg.mul(*[d[j] for j in i]) for i in li]),False,'c')
            elif li=='all':
                match r:
                    case False:return matx(tuple([alg.mul(*i) for i in a.matx]),False,'c');
                    case True:return matx(galg.mul(*a.matx),False,'c');
                    case _:raise Exception("Invalid argument: r => bool, got {}".format(r.__class__.__name__));
            else:
                raise Exception("Invalid argument: li => 'all'/list/tuple, got {}".format(li.__class__.__name__))
        except Exception as e:print("Invalid command: melutils.mult()");retrn(ret,e);

    @staticmethod
    def pow(an:list|tuple[Decimal,Decimal],a:matx,li:list[int]|tuple[int]|str,r:bool=False,chk:bool=True,ret:str='a')->matx:
        '''
#### Returns a matx object with matrix rows as exponentiated rows or columns.
- **an**: Tuple with first element as factor multiplied and second element as power
##### (a*[x])<sup>n</sup>
- **li**: 'all' or list/tuple of row or column indexes
- **r**: True if row indexes or False if column indexes
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if not tmatx(a):raise Exception
                    if eqval(len(an),2) is None:raise Exception;
                    match an.__class__.__name__:
                        case 'tuple':
                            if (an:=tdeciml.dall(an,getpr()) if not tdeciml.deciml(an,True) else an) is None:raise Exception;
                        case 'list':
                            if (an:=tdeciml.dall(an,getpr()) if not tdeciml.deciml(an,True) else an) is None:raise Exception;
                        case _:raise Exception("Invalid argument: a => tuple/list, got {}".format(a.__class__.__name__));
                    if li != 'all':
                        if not (li:=tint.ele(li, a.collen if r else a.rowlen,True)):raise Exception
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            if (tli:=li.__class__.__name__)=='tuple' or tli=='list':
                if an[0]!=1:return matx(tuple([galg.pwrgs(galg.mulsg(an[0],i,getpr()+1),an[1]) for i in a.gele(li,r,chk,'c')]),False,'c');
                else:return matx(tuple([galg.pwrgs(i,an[1]) for i in a.gele(li,r,chk,'c')]),False,'c');
            elif li=='all':
                if an[0]!=1:return matx(tuple([galg.pwrgs(galg.mulsg(an[0],i,getpr()+1),an[1]) for i in a.matx]),False,'c');
                else:return matx(tuple([galg.pwrgs(i,an[1]) for i in a.matx]),False,'c');
            else:
                raise Exception("Invalid argument: li => 'all'/tuple/list, got {}".format(li.__class__.__name__))
        except Exception as e:print("Invalid command: melutils.pow()");retrn(ret,e);

    @staticmethod
    def log(an:list|tuple[Decimal,Decimal],a:matx,li:list[int]|tuple[int]|str,r:bool=False,chk:bool=True,ret:str='a')->matx:
        '''
#### Returns a matx object with matrix rows as logarithm of elements of rows or columns.
- **an**: Tuple with first element as the factor multiplied and second element as the base for logarithm
##### log<sub>n</sub>(a*[x])
- **a**: matx object
- **li**: 'all' or list/tuple of row or column indexes
- **r**: True if row indexes or False if column indexes
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if not tmatx(a):raise Exception
                    match an.__class__.__name__:
                        case 'tuple':
                            if (an:=tdeciml.dall(an,getpr()) if not tdeciml.deciml(an,True) else an) is None:raise Exception;
                        case 'list':
                            if (an:=tdeciml.dall(an,getpr()) if not tdeciml.deciml(an,True) else an) is None:raise Exception;
                        case _:raise Exception("Invalid argument: a => tuple/list");
                    if eqval(len(an),2) is None:raise Exception;
                    if li != 'all':
                        if not (li:=tint.ele(li, a.collen if r else a.rowlen,True)):raise Exception
                case _:raise Exception("Invalid argument: chk => bool");
            if an[1]==0 or an[0]==0:raise Exception("Base of logarithm or number cannot be zero.")
            if (tli:=li.__class__.__name__)=='tuple' or tli=='list':
                if an[0]!=1:return matx(tuple([tuple([alg.log(alg.mul(j,an[0],pr=getpr()+1),an[1]) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                else:return matx(tuple([tuple([alg.log(j,an[1]) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
            elif li=='all':
                if an[0]!=1:return matx(tuple([tuple([alg.log(alg.mul(j,an[0],pr=getpr()+1),an[1]) for j in i]) for i in a.matx]),False,'c');
                else:return matx(tuple([tuple([alg.log(j,an[1]) for j in i]) for i in a.matx]),False,'c');
            else:
                raise Exception("Invalid argument: li => 'all'/tuple/list, got {}".format(li.__class__.__name__))
        except Exception as e:print("Invalid command: melutils.log()");retrn(ret,e);

    @staticmethod
    def expo(an:list|tuple[Decimal,Decimal],a:matx,li:list[int]|tuple[int,...]|str,r:bool=False,chk:bool=True,ret:str='a')->matx:
        '''
#### Returns a matx object with matrix rows as number exponentiated by a factor of elements in rows or columns.
- **an**: Tuple with first element as number to exponentiate and second elementas factor multiplied
##### a<sup>n*[x]</sup>
- **a**: matx object
- **li**: 'all' or list/tuple of row or column indexes
- **r**: True if row indexes or False if column indexes
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if not tmatx(a):raise Exception
                    match an.__class__.__name__:
                        case 'tuple':
                            if (an:=tdeciml.dall(an,getpr()) if not tdeciml.deciml(an,True) else an) is None:raise Exception;
                        case 'list':
                            if (an:=tdeciml.dall(an,getpr()) if not tdeciml.deciml(an,True) else an) is None:raise Exception;
                        case _:raise Exception("Invalid argument: a => tuple/list");
                    if eqval(len(an),2) is None:raise Exception;
                case _:raise Exception("Invalid argument: chk => bool");
            if (tli:=li.__class__.__name__)=='tuple' or tli=='list':
                if an[1]!=1:return matx(tuple([tuple([alg.pwr(an[0],alg.mul(j,an[1],pr=getpr()+1)) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
                else:return matx(tuple([tuple([alg.pwr(an[0],j) for j in i]) for i in a.gele(li,r,chk,'c')]),False,'c');
            elif li=='all':
                if an[1]!=1:return matx(tuple([tuple([alg.pwr(an[0],alg.mul(j,an[1],pr=getpr()+1)) for j in i]) for i in a.matx]),False,'c');
                else:return matx(tuple([tuple([alg.pwr(an[0],j) for j in i]) for i in a.matx]),False,'c');
            else:
                raise Exception("Invalid argument: li => 'all'/tuple/list, got {}".format(li.__class__.__name__))
        except Exception as e:print("Invalid command: melutils.expo()");retrn(ret,e);

    @staticmethod
    def trig(n:Decimal,a:matx,li:list[int]|tuple[int,...]|str,r:bool=False,f:str='cos',chk:bool=True,ret:str='a')->matx:
        '''
#### Returns matx object with matrix rows as trignometric function values for elements of rows or columns.
- **n**: Factor to multiply with elements
- **a**: matx object
- **li**: 'all' or list/tuple of row or column indexes
- **r**: True if row indexes or False if column indexes
- **f**: Trignometric function
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if str(n:=deciml(n,getpr()))=='NaN':raise Exception;
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            if (tli:=li.__class__.__name__)=='tuple' or tli=='list':
                if n!=1:
                    x=tuple(map(lambda x:galg.mulsg(n,x,getpr()+1),a.gele(li,r,chk,'c')))
                else:
                    x=a.gele(li,r,chk,'c')
            elif li=='all':
                if n!=1:
                    x=tuple(map(lambda x:galg.mulsg(n,x,getpr()+1),a.matx if r else matutils.tpose(a).matx))
                else:
                    x=a.matx if r else matutils.tpose(a).matx
            else:
                raise Exception("Invalid argument: li => 'all'/list/tuple, got {}".format(li))
            match f:
                case 'cos':return matx(tuple(map(lambda x:gtrig.cosine(x),x)),False,'c');
                case 'sin':return matx(tuple(map(lambda x:gtrig.sine(x),x)),False,'c');
                case 'tan':return matx(tuple(map(lambda x:gtrig.tan(x),x)),False,'c');
                case 'sec':return matx(tuple(map(lambda x:gtrig.sec(x),x)),False,'c');
                case 'cosec':return matx(tuple(map(lambda x:gtrig.cosec(x),x)),False,'c');
                case 'cot':return matx(tuple(map(lambda x:gtrig.cot(x),x)),False,'c');
                case 'acos':return matx(tuple(map(lambda x:gtrig.acosine(x),x)),False,'c');
                case 'asin':return matx(tuple(map(lambda x:gtrig.asine(x),x)),False,'c');
                case 'atan':return matx(tuple(map(lambda x:gtrig.atan(x),x)),False,'c');
                case 'asec':return matx(tuple(map(lambda x:gtrig.asec(x),x)),False,'c');
                case 'acosec':return matx(tuple(map(lambda x:gtrig.acosec(x),x)),False,'c');
                case 'acot':return matx(tuple(map(lambda x:gtrig.acot(x),x)),False,'c');
                case 'sinh':return matx(tuple(map(lambda x:ghtrig.sinh(x),x)),False,'c');
                case 'cosh':return matx(tuple(map(lambda x:ghtrig.cosh(x),x)),False,'c');
                case 'tanh':return matx(tuple(map(lambda x:ghtrig.tanh(x),x)),False,'c');
                case 'cosech':return matx(tuple(map(lambda x:ghtrig.cosech(x),x)),False,'c');
                case 'sech':return matx(tuple(map(lambda x:ghtrig.sech(x),x)),False,'c');
                case 'coth':return matx(tuple(map(lambda x:ghtrig.coth(x),x)),False,'c');
        except Exception as e:print("Invalid command: melutils.trig()");retrn(ret,e);

class matstat:
    
    @staticmethod
    def amean(a:matx,el:str='row',chk:bool=True,ret:str='a')->tuple[Decimal,...]|Decimal:
        '''
#### Returns the arithmatic mean for all elements in matrix or all matrix rows/columns.
- **a**: matx object
- **el**: The arithmatic mean for,
    - ***'row'***: all rows of matrix
    - ***'col'***: all columns of matrix
    - ***'all'***: all matrix elements
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx(a) is None: raise Exception;
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            match el:
                case 'row':return tuple(map(lambda x:stat.amean(x),a.matx));
                case 'col':return tuple(map(lambda x:stat.amean(x),tuple(zip(*a.matx))));
                case 'all':
                    li=tuple();
                    for i in a.matx:li+=i;
                    return stat.amean(li);
                case _:raise Exception("Invalid argument: el => {} is not 'row'/'col'/'all'".format(el));
        except Exception as e:print("Invalid command: matstat.amean()");retrn(ret,e);
    
    @staticmethod
    def gmean(a:matx,el:str='row',chk:bool=True,ret:bool='a')->tuple[Decimal,...]|Decimal:
        '''
#### Returns the geometric mean for all elements in matrix or all matrix rows/columns.
- **a**: matx object
- **el**: The geometric mean for,
    - ***'row'***: all rows of matrix
    - ***'col'***: all columns of matrix
    - ***'all'***: all matrix elements
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx(a) is None:raise Exception;
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            match el:
                case 'row':return tuple(map(lambda i:stat.gmean(i),a.matx));
                case 'col':return tuple(map(lambda i:stat.gmean(i),tuple(zip(*a.matx))));
                case 'all':
                    li=tuple()
                    for i in a.matx:li+=i;
                    return stat.gmean(li);
                case _:raise Exception("Invalid argument: el => {} is not 'row'/'col'/'all'".format(el));
        except Exception as e:print("Invalid command: matstat.gmean()");retrn(ret,e);

    @staticmethod
    def hmean(a:matx,el:str='row',chk:bool=True,ret:str='a')->tuple[Decimal,...]|Decimal:
        '''
#### Returns the harmonic mean for all elements in matrix or all matrix row/columns.
- **a**: matx object
- **el**: The harmonic mean for,
    - ***'row'***: all rows of matrix
    - ***'col'***: all columns of matrix
    - ***'all'***: all matrix elements
- **chk**: Check arguments
- **ret**: Exit type 
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx(a) is None:raise Exception;
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            match el:
                case 'row':return tuple(map(lambda i:stat.hmean(i),a.matx));
                case 'col':return tuple(map(lambda i:stat.hmean(i),tuple(zip(*a.matx))));
                case 'all':
                    li=tuple()
                    for i in a.matx:li+=i;
                    return stat.hmean(li);
                case _:raise Exception("Invalid argument: el => {} is not 'row'/'col'/'all'".format(el));
        except Exception as e:print("Invalid command: matstat.hmean()");retrn(ret,e);

    @staticmethod
    def qmean(a:matx,el:str='row',chk:bool=True,ret:str='a')->tuple[Decimal,...]|Decimal:
        '''
#### Returns the quadratic mean for all elements in matrix or all matrix rows/columns.
- **a**: matx object
- **el**: The quadratic mean for,
    - ***'row'***: all rows of matrix
    - ***'col'***: all columns of matrix
    - ***'all'***: all matrix elements
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx(a) is None: raise Exception;
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            match el:
                case 'row':return tuple(map(lambda i:stat.gmean(i),a.matx));
                case 'col':return tuple(map(lambda i:stat.gmean(i),tuple(zip(*a.matx))));
                case 'all':
                    li=tuple()
                    for i in a.matx:li+=i
                    return stat.gmean(li);
                case _:raise Exception("Invalid argument: el => {} is not 'row'/'col'/'all'".format(el));
        except Exception as e:print("Invalid command: matstat.qmean()");retrn(ret,e);
    
    @staticmethod
    def var(a:matx,el:str='row',samp:bool=True,chk:bool=True,ret:str='a')->tuple[Decimal,...]|Decimal:
        '''
#### Returns the variance for all elements in matrix or all matrix rows/columns.
- **a**: matx object
- **el**: The variance for,
    - ***'row'***: all rows of matrix
    - ***'col'***: all columns of matrix
    - ***'all'***: all matrix elements
- **samp**: Variance type
    - ***True***: Sample variance
    - ***False***: Population variance
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass;
                case True:
                    if tmatx(a) is None:raise Exception;
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__));
            match el:
                case 'row':
                    match samp:
                        case True:return tuple(map(lambda i:stat.svar(i),a.matx));
                        case False:return tuple(map(lambda i:stat.pvar(i),a.matx));
                        case _:raise Exception("Invalid argument: samp => bool, got {}".format(samp.__class__.__name__));
                case 'col':
                    match samp:
                        case True:return tuple(map(lambda i:stat.svar(i),tuple(zip(*a.matx))));
                        case False:return tuple(map(lambda i:stat.pvar(i),tuple(zip(*a.matx))));
                        case _:raise Exception("Invalid argument: samp => bool, got {}".format(samp.__class__.__name__));
                case 'all':
                    li=tuple()
                    for i in a.matx:li+=i
                    match samp:
                        case True:return stat.svar(li);
                        case False:return stat.pvar(li);
                        case _:raise Exception("Invalid argument: samp => bool, got {}".format(samp.__class__.__name__));
                case _:raise Exception("Invalid argument: el => {} is not 'row'/'col'/'all'".format(el));
        except Exception as e:print("Invalid command: matstat.var()");retrn(ret,e);
    
    @staticmethod
    def sd(a:matx,el:str='row',samp:bool=True,chk:bool=True,ret:str='a')->tuple[Decimal,...]|Decimal:
        '''
#### Returns the standard deviation for all elements in matrix or all matrix rows/columns.
- **a**: matx object
- **el**: The standard deviation for,
    - ***'row'***: all rows of matrix
    - ***'col'***: all columns of matrix
    - ***'all'***: all matrix elements
- **samp**: Standard deviation type
    - ***True***: Sample standard deviation
    - ***False***: Population standard deviation
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:pass
                case True:
                    if tmatx(a) is None:raise Exception;
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__))
            match samp:
                case True:
                    match el:
                        case 'row':return tuple(map(lambda i:stat.sstd_dev(i),a.matx));
                        case 'col':return tuple(map(lambda i:stat.sstd_dev(i),tuple(zip(*a.matx))));
                        case 'all':
                            li=tuple()
                            for i in a.matx:li+=i
                            return stat.sstd_dev(li)
                        case _:raise Exception("Invalid argument: el => {} is not 'row'/'col'/'all'".format(el))
                case False:
                    match el:
                        case 'row':return tuple(map(lambda i:stat.pstd_dev(i),a.matx));
                        case 'col':return tuple(map(lambda i:stat.pstd_dev(i),tuple(zip(*a.matx))));
                        case 'all':
                            li=tuple()
                            for i in a.matx:li+=i
                            return stat.pstd_dev(li)
                        case _:raise Exception("Invalid argument: el => {} is not 'row'/'col'/'all'".format(el))
                case _:raise Exception("Invalid argument: samp => bool, got {}".format(samp.__class__.__name__))
        except Exception as e:print("Invalid command: matstat.sd()");retrn(ret,e);

    @staticmethod
    def median(a:matx,el:str='row',chk:bool=True,ret:str='a')->tuple[Decimal,...]|Decimal:
        '''
#### Returns the median of all elements in matrix or all matrix rows/columns.
- **a**: matx object
- **el**: The median for,
    - ***'row'***: all rows of matrix
    - ***'col'***: all columns of matrix
    - ***'all'***: all matrix elements
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case True:
                    if not tmatx(a):raise Exception;
                case False:pass
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__))
            match el:
                case 'row':return tuple(map(lambda i:stat.median(i),a.matx));
                case 'col':return tuple(map(lambda i:stat.median(i),tuple(zip(*a.matx))));
                case 'all':
                    li=tuple()
                    for i in a.matx:li+=i
                    return stat.median(li)
                case _:raise Exception("Invalid argument: el => {} is not 'row'/'col'/'all'".format(el))
        except Exception as e:print("Invalid command: matstat.median()");retrn(ret,e);

    @staticmethod
    def mode(a:matx,el:str='row',chk:bool=True,ret:str='a')->tuple[dict,...]|dict:
        '''
#### Returns the mode of all elements in matrix or all matrix rows/columns.
- **a**: matx object
- **el**: The mode for,
    - ***'row'***: all rows of matrix
    - ***'col'***: all columns of matrix
    - ***'all'***: all matrix elements
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case True:
                    if not tmatx(a):raise Exception;
                case False:pass
                case _:raise Exception("Invalid argument: chk => bool, got {}".format(chk.__class__.__name__))
            match el:
                case 'row':return tuple(map(lambda i:stat.mode(i),a.matx));
                case 'col':return tuple(map(lambda i:stat.mode(i),tuple(zip(*a.matx))))
                case 'all':
                    li=tuple()
                    for i in a.matx:li+=i
                    return stat.mode(li)
                case _:raise Exception("Invalid argument: el => {} is not 'row'/'col'/'all'".format(el))
        except Exception as e:print("Invalid command: matstat.mode()");retrn(ret,e);

# print("1")
# z=[1,2,3]
# a1 = [z,[5,2, int(6)], [5, 5, 8]]
# b = [[1, 3, 6], [8, 5, 6], [7, 4, 5]]
# a = matx(a1)
# a.pmatx
# print(a.dnant())
# a.pmatx
# matutils.saddcnst((1, 2, 3), a).pmatx
# melutils.add(a, [[0,1], [0,1,2]]).pmatx
# melutils.add(a, [[0,1], [0,1,2]], True).pmatx
# melutils.pow([1, 2], a, [0,2]).pmatx
# melutils.trig(100, a, [0, 1], f='cos').pmatx
# x = matutils.dpose(a, [1,2], True)
# for i in x:
#     i.pmatx
# a.matx = a.matx
# a.pmatx
# print(a.matxl())
# a.pmatx
# a.tpose().pmatx
# print(a.mele(0, 0))
# a.pmatx
# print(a.rowlen, a.collen)
# a1 = [0, 0, 0]
# a.pmatx
# c = a.matxl()
# c[0] = [0, 0, 0]
# a.pmatx
# print(c)
# a.matx = [[1, 2, 3], [5, 0, 6], [5, 5, 8]]
# a.pmatx
# print("2")
# b = matx(b)
# a.pmatx
# b.pmatx
# matutils.melmult(a, b).pmatx
# print(matutils.melmult(a, b, (True, False), False))
# print(matutils.melmult(a, b, (False, True), True))
# matutils.melmult(a, b, (True, True)).pmatx
# matutils.addmatx(a, b, matx([[1,],[1,],[1,]])).pmatx
# matutils.smultfac(tuple([2, 1, 2]), a).pmatx
# matutils.gele(a, [0, 1]).pmatx
# matutils.gele(a, [1, 0], True).pmatx
# print(a.sqmatx)
# c = [0, 0]
# print(matx(c).sqmatx)
# print(a.dnant(), b.dnant())
# a.invse().pmatx
# b.invse().pmatx
# print(b.invsednant(), matutils.dnant(b.invse()))
# matutils.madd(a, b).pmatx
# matutils.mmult(a, b).pmatx
# a = matx([11, 10, 100])
# matutils.matlxtox(a)
# matutils.maddval(a, Decimal('1.0')).pmatx
# matutils.matxtolx([matx([1,2,3]), matx([2,3,4])], False).pmatx
# a = matx([[1,2], [5,3]])
# a.pmatx
# print(matstat.amean(a), matstat.amean(a, 'col'), matstat.amean(a, 'all'))
# print(matstat.gmean(a), matstat.gmean(a, 'col'), matstat.gmean(a, 'all'))
# print(matstat.hmean(a), matstat.hmean(a, 'col'), matstat.hmean(a, 'all'))
# print(matstat.qmean(a), matstat.qmean(a, 'col'), matstat.qmean(a, 'all'))
# print(matstat.sd(a, samp=False), matstat.sd(a, 'col', False), matstat.sd(a, 'all'))
# a.cofacm().pmatx

