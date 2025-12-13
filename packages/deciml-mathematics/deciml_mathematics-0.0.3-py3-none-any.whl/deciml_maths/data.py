from matrix import matx, matutils, melutils
from compare.cmpr import tmatx, eqval, tdata, tint, tdeciml, tstr
from terminate import retrn
from deciml_maths import *

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

class data:
        
    def __init__(self,x:tuple[tuple[int|float|Decimal,...],...]|list[list[int|float|Decimal]]|matx|tuple[matx,...]|list[matx],y:list[int|float|Decimal]|tuple[int|float|Decimal]|tuple[matx,...]|list[matx]|matx,chk:bool=True,ret:str='a')->None:
        '''
#### Create a data object.
- **x**: X values of data
- **y**: Y values of data
- **chk**: Check the arguments
- **ret**: Exit type
        '''
        try:
            def __dataxy(x,y,chk:bool)->matx:
                def __xcheck(x)->tuple:
                    if (xt:=x.__class__.__name__)=='tuple' or xt=='list':
                        del xt
                        if x[0].__class__.__name__=='matx':return matutils.matxtolx(x,True,'c');
                        else:return matx(x,True,'c');
                    return matx(x,True,'c')
                def __ycheck(y)->tuple:
                    if (yt:=y.__class__.__name__)=='tuple' or yt=='list':
                        if (y1:=y[0].__class__.__name__)=='int' or y1=='float' or y1=='Decimal':return tdeciml.dall(y);
                        elif y1=='matx':return tuple(zip(*matutils.matxtolx(y,True,'c').matx));
                        elif y1=='tuple' or y1=='list':return tdeciml.dall(tuple(zip(*y)));
                        else:return None;
                    if yt=='matx':
                        if y.collen==1:return y.matx;
                        elif y.rowlen==1:return tuple(zip(*y));
                        else:return None;
                match chk:
                    case True:
                        x=__xcheck(x)
                        if x is None:raise Exception("Invalid argument: x");
                        y=__ycheck(y)
                        if y is None:raise Exception("Invalid argument: y");
                    case False:pass;
                    case _:raise Exception;
                return (x,y),x.collen,x.rowlen
            if (ndata:=__dataxy(x,y,chk)) is not None:self.__data,self.__datalen,self.__xvars=ndata;del ndata;self.__xlabels=None;self.__ylabel=None;
            else:raise Exception;
        except Exception as e:print("Invalid command: data()");retrn(ret,e);

    @property
    def data(self)->tuple[matx,tuple[Decimal,...]]:
        '''
#### Get the data as a tuple with x values as matx object and y values as a tuple.
        '''
        return (self.getax(),self.getay());
    
    @property
    def datalen(self)->int:
        '''
#### Get the number of data points.
        '''
        return self.__datalen;
    
    @property
    def xvars(self)->int:
        '''
#### Get the number of x variables.
        '''
        return self.__xvars;

    @property
    def x_labels(self)->tuple[str,...]|None:
        '''
#### Get the x labels for data.
        '''
        return self.__xlabels;

    @x_labels.setter
    def x_labels(self,labels:list[str]|tuple[str,...])->tuple[str,...]|None:
        '''
#### Set the labels for x values.
- **labels**: List of x labels
        '''
        try:
            if not tstr(labels,True):raise Exception("Invalid argument: labels => list[str]|tuple[str,...]")
            if len(labels)!=self.__xvars:raise Exception("{} is not equal to number of variables ({})".format(len(labels),self.__xvars))
            self.__xlabels=tuple(labels)
            return self.__xlabels
        except Exception as e:
            retrn('a',e)

    @property
    def y_label(self):
        '''
#### Get the y label.
        '''
        return self.__ylabel;
    
    @y_label.setter
    def y_label(self,s:str):
        '''
#### Set the y label.
- **s**: Y label
        '''
        if tstr(s):self.__ylabel=s
        else:retrn('a',"Invalid argument: s => str")
        return self.__ylabel

    def get_label_index(self,labels:list[str]|tuple[str,...],ret:str='a')->tuple[int,...]:
        '''
#### Get the index of x labels.
- **labels**: List of x labels
        '''
        try:
            if not tstr(labels, True):retrn('a',"")
            else:
                indexes=list()
                for i in labels:
                    if i not in self.__xlabels:raise Exception("{} not a label.".format(i))
                    indexes.append(self.__xlabels.index(i))
                return indexes
        except Exception as e:retrn(ret, e)
    
    def __getitem__(self, index):
        try:
            if len(index)!=2:raise Exception("Expected 2 slices got {}".format(len(index)))
            if (ti0:=index[0].__class__.__name__)=='int' or ti0=='slice':
                if (ti1:=index[1].__class__.__name__)=='slice' or ti1=='int':
                    ret=data(self.__data[0][index[0],index[1]], self.__data[1][index[0]] if ti0=='slice' else (self.__data[1][index[0]],))
                    ret.x_labels=[self.__xlabels[index[1]]] if ti1=='int' else self.__xlabels[index[1]]
                    ret.y_label=self.__ylabel
                    return ret
                elif ti1=='list' or ti1=='tuple':
                    indexes=self.get_label_index(index[1]);l=[]
                    for i in self.data[0][index[0]].matx:
                        l1=[]
                        for j in indexes:
                            l1.append(i[j])
                        l.append(tuple(l1))
                    ret=data(l, self.__data[1][index[0]])
                    ret.x_labels=[self.__xlabels[i] for i in indexes]
                    ret.y_label=self.__ylabel
                    return ret
                else:raise Exception("Expected slice, int, or list/tuple got {}".format(ti1))
            else:raise Exception("Expected slice or int got {}".format(ti0))
        except Exception as e:retrn('a', e)
        
    # prints the data
    @data.getter
    def pdata(self)->None:
        '''
#### Print the data.
##### **Note: Use print() instead.**
        '''
        x=self.__data[0].matx;y=self.__data[1];
        print("data[")
        for i in range(self.datalen):print("  "+str(i)+": "+str([str(j) for j in x[i]])[1:-1]+" | "+str(str(y[i])));
        print("]\n")

    def __str__(self):
        x=self.__data[0].matx;y=self.__data[1];
        x_labels = None
        if self.__xlabels:x_labels=list(self.__xlabels);
        else:x_labels=[str(i) for i in range(self.xvars)];
        if self.__ylabel:y_label=self.__ylabel;
        else:y_label="Y";
        max_lens=[]
        for i in matutils.tpose(self.data[0]).matx:
            max_lens.append(max([len(str(j)) for j in i]))
        for j,i in enumerate(max_lens):
            if i < 8:
                max_lens[j] = 8
        n=len(str(self.__datalen))
        max_y=len(str(max(self.__data[1]))) if len(str(max(self.__data[1]))) > 8 else 8
        s="data[\n"+"_"*(n+2)+"|"
        for i,j in zip(x_labels,max_lens):
            if (l:=len(i)) > j:
                s+="_{}_|".format(i[:j-1]+"*")
            else:
                s+="_"*(u:=((j-l)//2))+"_{}_".format(i)+"_"*(j-u-l)+"|"
        s+="|"+"_"*(u:=((max_y-len(y_label))//2 if len(y_label) <= max_y else 0))+"_{}_".format(y_label if len(y_label) <= max_y else y_label[:max_y-1]+"*")+("_"*(max_y-u-len(y_label)) if len(y_label) <= max_y else "")+"|\n"
        for i,(x,y) in enumerate(zip(self.__data[0].matx, self.__data[1])):
            s+=" "*(n-len(str(i)))+" {} |".format(i)
            for m,j in enumerate(x):
                s+=" "*(l:=((max_lens[m]-len(str(j)))//2))+" {} ".format(str(j))+" "*(max_lens[m]-l-len(str(j)))+"|"
            s+="|"+" "*(u:=((max_y-len(str(y)))//2))+" {} ".format(y)+" "*(max_y-u-len(str(y)))+"|\n"
        return s+"]"


    def __repr__(self):
        x=self.__data[0].matx;y=self.__data[1];
        x_labels = None
        if self.__xlabels:x_labels=list(self.__xlabels);
        else:x_labels=[str(i) for i in range(self.xvars)];
        if self.__ylabel:y_label=self.__ylabel;
        else:y_label="Y";
        max_lens=[]
        for i in matutils.tpose(self.data[0]).matx:
            max_lens.append(max([len(str(j)) for j in i]))
        for j,i in enumerate(max_lens):
            if i < 8:
                max_lens[j] = 8
        n=len(str(self.__datalen))
        max_y=len(str(max(self.__data[1]))) if len(str(max(self.__data[1]))) > 8 else 8
        s="data[\n"+"_"*(n+2)+"|"
        for i,j in zip(x_labels,max_lens):
            if (l:=len(i)) > j:
                s+="_{}_|".format(i[:j-1]+"*")
            else:
                s+="_"*(u:=((j-l)//2))+"_{}_".format(i)+"_"*(j-u-l)+"|"
        s+="|"+"_"*(u:=((max_y-len(y_label))//2 if len(y_label) <= max_y else 0))+"_{}_".format(y_label if len(y_label) <= max_y else y_label[:max_y-1]+"*")+("_"*(max_y-u-len(y_label)) if len(y_label) <= max_y else "")+"|\n"
        for i,(x,y) in enumerate(zip(self.__data[0].matx, self.__data[1])):
            s+=" "*(n-len(str(i)))+" {} |".format(i)
            for m,j in enumerate(x):
                s+=" "*(l:=((max_lens[m]-len(str(j)))//2))+" {} ".format(str(j))+" "*(max_lens[m]-l-len(str(j)))+"|"
            s+="|"+" "*(u:=((max_y-len(str(y)))//2))+" {} ".format(y)+" "*(max_y-u-len(str(y)))+"|\n"
        return s+"]"
    
    def _repr_html_(self):
        x=self.__data[0].matx;y=self.__data[1];
        x_labels = None
        if self.__xlabels:x_labels=list(self.__xlabels);
        else:x_labels=[str(i) for i in range(self.xvars)];
        if self.__ylabel:y_label=self.__ylabel;
        else:y_label="Y";
        max_lens=[]
        for i in matutils.tpose(self.data[0]).matx:
            max_lens.append(max([len(str(j)) for j in i]))
        for j,i in enumerate(max_lens):
            if i < 8:
                max_lens[j] = 8
        n=len(str(self.__datalen))
        max_y=len(str(max(self.__data[1]))) if len(str(max(self.__data[1]))) > 8 else 8
        s1=str()
        for i,j in zip(x_labels,max_lens):
            if (l:=len(i)) > j:
                s1+="_{}_|".format(i[:j-1]+"*")
            else:
                s1+="_"*(u:=((j-l)//2))+"_{}_".format(i)+"_"*(j-u-l)+"|"
        s1+="|"+"_"*(u:=((max_y-len(y_label))//2 if len(y_label) <= max_y else 0))+"_{}_".format(y_label if len(y_label) <= max_y else y_label[:max_y-1]+"*")+("_"*(max_y-u-len(y_label)) if len(y_label) <= max_y else "")+"|\n"
        s="<pre style='max-height:45vh;width:{}ch'>data[\n".format(len(s1)+10)+"_"*(n+2)+"|"
        s+=s1
        del s1
        for i,(x,y) in enumerate(zip(self.__data[0].matx, self.__data[1])):
            s+=" "*(n-len(str(i)))+" {} |".format(i)
            for m,j in enumerate(x):
                s+=" "*(l:=((max_lens[m]-len(str(j)))//2))+" {} ".format(str(j))+" "*(max_lens[m]-l-len(str(j)))+"|"
            s+="|"+" "*(u:=((max_y-len(str(y)))//2))+" {} ".format(y)+" "*(max_y-u-len(str(y)))+"|\n"
        return s+"]</pre>"

    # returns all x
    def getax(self)->matx:
        '''
#### Get all the x values as a matx object.
        '''
        return matx(self.__data[0].matx,False,'c');

    # returns all y
    def getay(self)->tuple[Decimal,...]:
        '''
#### Get all the y values as a tuple.
        '''
        return self.__data[1];

    # returns x values from data
    def getx(self,li:list[int]|tuple[int,...],chk:bool=True,ret:str='a') -> matx:
        '''
#### Get the x values at row indexes as a matx object.
- **li**: List of row indexes
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:return matutils.gele(self.__data[0],li,True,chk,'c');
        except Exception as e:print("Invalid command: data.getx()");retrn(ret,e);

    # returns y values from data
    def gety(self,li:list[int]|tuple[int,...],chk:bool=True,ret:str='a')->tuple[Decimal,...]:
        '''
#### Get the y values at row indexes as a tuple.
- **li**: List of row indexes.
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:return tuple([self.__data[1][i] for i in li]);
                case True:
                    if (li:=tint.ele(li,self.__datalen,True)) is None:raise Exception;
                    return tuple([self.__data[1][i] for i in li])
                case _:raise Exception("Invalid argument: chk => bool")
        except Exception as e:print("Invalid command: data.gety()");retrn(ret,e);

    # returns data values from data
    def getd(self,li:list[int]|tuple[int,...],chk:bool=True,ret:str='a')->tuple[matx,tuple[Decimal,...]]:
        '''
#### Get the data points at row indexes as a tuple.
- **li**: List of row indexes
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:return tuple([matutils.gele(self.__data[0],li,True,False,'c'),tuple([self.__data[1][i] for i in li])]);
                case True:
                    if (li:=tint.ele(li,self.__datalen,True)) is None:raise Exception;
                    return tuple([matutils.gele(self.__data[0],li,True,False,'c'),tuple([self.__data[1][i] for i in li])]);
                case _:raise Exception("Invalid argument: chk => bool")
        except Exception as e:print("Invalid command: data.getd()");retrn(ret,e);

    # return listed x
    def getlx(self,li:list[int]|tuple[int,...],chk:bool=True,ret:str='a')->matx:
        '''
#### Get the x columns.
- **li**: List column indexes
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:return matutils.tpose(matutils.gele(self.__data[0],li,False,chk,'c'),False,'c');
        except Exception as e:print("Invalid command: data.getlx()");retrn(ret,e);


class datautils:
    
    @staticmethod
    def dataval(d:data,x:Decimal,chk:bool=True,ret:str='a')->data:
        '''
#### Add a column with the same value and get the data object.
- **d**: Data object
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:return data(matutils.maddval(d.getax(),x,False,'c'),d.getay(),False,'c');
                case True:
                    if tdata(d) is None:raise Exception;
                    if str(x:=deciml(x))=='NaN':raise Exception;
                    return data(matutils.maddval(d.getax(),x,False,'c'),d.getay(),False,'c');
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: datautils.dataval()");retrn(ret,e);

    # add the listed x to data
    @staticmethod
    def addata(d:data,*a:matx,chk:bool=True,ret:str='a')->data:
        '''
#### Add multiple matx objects as x columns to the data object.
- **d**: Data object
- **\*a**: matx objects
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:return data(matutils.addmatx(d.getax(),*a,r=False,chk=False,ret='c'),d.getay(),False,'c');
                case True:
                    if tdata(d) is None or tmatx(a,True) is None:raise Exception;
                    for i in a:
                        if eqval(d.datalen,i.collen) is None:raise Exception;
                    return data(matutils.addmatx(d.getax(),*a,r=False,chk=False,ret='c'),d.getay(),False,'c')
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: datautils.addata()");retrn(ret,e);

    # retuns a new data object with x of listed positions
    @staticmethod
    def datalx(d:data,li:list[int]|tuple[int,...],chk:bool=True,ret:str='a')->data:
        '''
#### Get a data object with listed x columns.
- **d**: Data object
- **li**: Column indexes
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:return data(d.getlx(li,False,'c'),d.getay(),False,'c');
                case True:
                    if tdata(d) is None:raise Exception;
                    return data(d.getlx(li,True,'c'),d.getay(),False,'c')
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: datautils.datalx()");retrn(ret,e);

    # add multiplication of x at listed positions to data
    @staticmethod
    def multlx(d:data,li:list[list[int]]|tuple[tuple[int,...]]|str,chk:bool=True,ret:str='a')->data:
        '''
#### Get the data object after multiplication of x columns as added x columns.
- **d**: Data object
- **li**: List with list of column indexes to multiply
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.mult(d.getax(),li,False,False,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c');
                case True:
                    if tdata(d) is None:raise Exception;
                    return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.mult(d.getax(),li,False,True,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c')
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: datautils.multlx()");retrn(ret,e);

    # add addition of x at listed positions to data
    @staticmethod
    def addlx(d:data,li:list[list[int]]|tuple[tuple[int,...]]|str,chk:bool=True,ret:str='a')->data:
        '''
#### Get the data object after addition of x columns as added x columns.
- **d**: Data object
- **li**: List with list of column indexes to add
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.add(d.getax(),li,False,False,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c');
                case True:
                    if tdata(d) is None:raise Exception;
                    return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.add(d.getax(),li,False,True,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c')
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: datautils.addlx()");retrn(ret,e);

    # add powers of x at listed positions to data
    @staticmethod
    def powlx(d:data,an:tuple[Decimal, Decimal],li:list[int]|tuple[int,...]|str,chk:bool=True,ret:str='a')->data:
        '''
#### Get the data object after exponentiation of x columns as added x columns.
- **d**: Data object
- **an**: Tuple of multiplication factor and exponent
##### (a*[x])<sup>n</sup>
- **li**: List of column indexes to exponentiate
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.pow(an,d.getax(),li,False,False,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c');
                case True:
                    if tdata(d) is None:raise Exception;
                    return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.pow(an,d.getax(),li,False,True,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c')
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: datautils.powlx()");retrn(ret,e);

    # append log of x at listed positions to data
    @staticmethod
    def loglx(d:data,an:tuple[Decimal,Decimal],li:list[int]|tuple[int,...]|str,chk:bool=True,ret:str='a')->data:
        '''
#### Get the data object after logarithm of x columns as added x columns.
- **d**: Data object
- **an**: Tuple of multiplication factor and base
##### log<sub>n</sub>(a*[x])
- **li**: List of column indexes to perform logarithm
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.log(an,d.getax(),li,False,False,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c');
                case True:
                    if tdata(d) is None:raise Exception;
                    return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.log(an,d.getax(),li,False,True,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c')
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: datautils.loglx()");retrn(ret,e);

    # append x at listed positions as a power to data
    @staticmethod
    def expolx(d:data,an:tuple[Decimal,Decimal],li:list[int]|tuple[int,...]|str,chk:bool=True,ret:str='a')->data:
        '''
#### Get the data object after exponentiated to x columns as added x columns.
- **d**: Data object
- **an**: Tuple of base and multiplication factor
##### a<sup>n*[x]</sup>
- **li**: List of column indexes to perform logarithm
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.expo(an,d.getax(),li,False,False,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c');
                case True:
                    if tdata(d) is None:raise Exception;
                    return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.expo(an,d.getax(),li,False,True,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c')
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: datautils.expolx()");retrn(ret,e);
    
    @staticmethod
    def triglx(d:data,n:Decimal,li:list[int]|tuple[int,...]|str,f:str='cos',chk:bool=True,ret:str='a')->data:
        '''
#### Get the data object after trignometric operation of x columns as added x columns.
- **d**: Data object
- **n**: Multiplication factor
- **li**: List of column indexes to perform logarithm
- **f**: Function
- **chk**: Check arguments
- **ret**: Exit type
        '''
        try:
            match chk:
                case False:return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.trig(n,d.getax(),li,False,f,False,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c');
                case True:
                    if tdata(d) is None:raise Exception;
                    return data(matutils.addmatx(d.getax(),matutils.tpose(melutils.trig(n,d.getax(),li,False,f,True,'c')),r=False,chk=False,ret='c'),d.getay(),False,'c')
                case _:raise Exception("Invalid argument: chk => bool");
        except Exception as e:print("Invalid command: datautils.triglx()");retrn(ret,e);
 

# a = [[1,2,2],[2,3,4],[7.9999999,3,2]]
# b = [3,]
# c = [2, ]
# y = data(a, [2, 3, 4])
# y.pdata
# y.getax().pmatx
# print(y.getay())
# y = datautils.dataval(y, deciml('1.0'))
# y.pdata
# z = y.getlx([1, 0])
# q = datautils.addata(y, z)
# q.pdata
# y = datautils.powlx(y, [1, 2], [1, 0])
# y.pdata
# y = datautils.multlx(y, [[1, 0], ])
# y.pdata
# y = datautils.addlx(y, [[0, 4], ])
# y.pdata
# y = datautils.loglx(y, [1, 10], [5, 6])
# y.pdata
# y = datautils.expolx(y, [2, 1], [1, 8])
# y = datautils.triglx(y, 1, [1, 8])
# n = datautils.datalx(y, [7, 8, 10])
# y.pdata
# n.pdata
