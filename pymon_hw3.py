import sys
from os.path import exists


class Record:
    def __init__(self,cate,title,value):
        self._cate=cate
        self._title=title
        self._val=value

    @property
    def cate(self):
        return self._cate
    @property
    def title(self):
        return self._title
    @property
    def value(self):
        return self._val
        
class Records:
    def __init__(self,d=[]):
        self.d=d #用self.d存取
        total = 0 #預設值為0
        if exists("pymon.txt"):
            with open("pymon.txt") as f:
                data = f.read().split("\n")
                for info in data:
                    if info:
                        try:
                            self.cate = info.split(',')[0]
                            self.title = info.split(',')[1]
                            self.val = int(info.split(',')[2])
                            #將讀入物件切開並計算

                        except:
                            print("check your file!")
                        else:
                            self.d.append([self.cate,self.title,self.val])


        else:
            while True: #有很多次輸錯的機會
                a=input("\nHow much money do you have?")
                try:
                    self.total = int(a)
                except ValueError:
                    sys.stderr.write("ValueError")
                else:
                    break
    def add(self,usinput,cate):
        data=usinput.split(', ') #可輸入多項
        total=0
        try:
            for i in data:
                self.cate, self.title, self.val=i.split()
                if cate.cate_valid(self.cate):
                    total+=int(self.val)
                    self.d.append([self.cate,self.title,self.val]) #存進self.d
                else:
                    print('Category is not exist')
                    return
        except ValueError:
            sys.stderr.write("Invalid value")
        else:
            print(f"Today increase {total} dollars") #顯示一次增減的總額
            return total


    def view(self):
        t=0
        for i in self.d:
            print(f'{t}. {i[0]:<15}{i[1]:^10}{i[2]:>10}') #將self.d按特定格式輸出並加上編號
            t+=1


    def delete(self,d_input):
        try:
            del self.d[d_input]
        except (KeyError,ValueError):
            sys.stderr.write("No such key")
        else:
            dollars=0
            for t in self.d:
                dollars += int(t[2]) #計算刪去特定項目後的剩餘總額
            print(f"{d_input} has been deleted, now you have {dollars} dollars")


    def find(self,key):
        result=list(filter(lambda rec:rec[0] in key, self.d))
        for i in result:
            print(f'{i[0]:<15}{i[1]:^10}{i[2]:>10}')

    def save(self):
        with open("pymon.txt", "w") as f:
            for i in self.d:
                f.write(f'{i[0]},{i[1]},{i[2]}\n') #以字串格式儲存

class Categories:
    def __init__(self):
        cate=['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]
        self.cate=cate
    def view(self):
        def vc(L, prefix=()):
            if type(L) in (list, tuple):
                i=0
                for v in L:
                    if type(v) not in (list, tuple):
                        i+=1
                    vc(v,prefix+(i,)) #遞迴
            else:
                s=' ' *3*(len(prefix)-1)
                s+='- '+L
                print(s)
        vc(self.cate)

    def cate_valid(self,cate):
        #檢查輸入的分類是否存在

        def valid(cate,categories):
            for i in categories:
                if type(i) == list:
                    if valid(cate,i):
                        #print('T')
                        return True
                elif i == cate:
                    #print(2)
                    return True
            #print(3)
            return False
        return valid(cate,self.cate)
    

    def find_sub(self,cate):
        def f_sub_gen(category, cate, found=False):
            if type(cate) == list:
                for index, child in enumerate(cate):
                    yield from f_sub_gen(category, child, found)
                    if child == category and index + 1 < len(cate) \
                        and type(cate[index + 1]) == list:
                # When the target category is found,recursively call this generator on the subcategories with the flag set as True.
                        yield from f_sub_gen(category,cate[index+1],True)
            else:
                if cate == category or found:
                    yield cate
        ans = [i for i in f_sub_gen(category,self.cate)]
        return ans


categ=Categories()
records=Records()

while True:
    command=input("\n a for add/ v for view/ f for find/ vc for view categories/ d for delete/ e for exit：")
    if command == 'a':
        record = input("Add an expense or income as [category name +-num, category...]\n category:food/ trans(transportation)/ inc(income): ")
        records.add(record, categ)
    elif command == 'v':
        records.view()
    elif command == 'd':
        d_input = int(input("which record do you want to delete? (input number)"))        
        records.delete(d_input)
    elif command == 'vc':
        categ.view()
    elif command == 'f':
        category = input('Which category do you want to find? ')
        target_categories = categ.find_sub(category)
        records.find(target_categories)
    elif command == 'e':
        records.save()
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')
