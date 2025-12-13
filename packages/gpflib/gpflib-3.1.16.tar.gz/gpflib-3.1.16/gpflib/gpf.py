from gpflib import GPF
g=GPF("Corpus")
Query="""
--Lua
OriOn()
Speedup(1)
Condition("$1=[得]")
Handle0=GetAS("欢_u|","喜欢","","","","","","1,0","","")
SetBase(Handle0,0,0)
ClearLimit()
Condition("$1=[得]")
Handle0=GetAS("<不","不得了","~","","","","0,1","","","")
Handle1=Context(Handle0,30,0,10)
Ret=Output(Handle1)
return Ret
"""
#Ret=g.BCC("u~{}[(0,713);(714,928)]",Command="Context",PageNo=0,WinSize=30,Number=10)
#Ret=g.BCC("u~{}[(0,713);(714,928)]",Command="Count")
#Ret=g.BCC("喜欢u{} NOT 我{}",Command="Context",PageNo=0,WinSize=30,Number=10)
#Ret=g.BCC("喜欢u{} NOT 我{}",Command="Context",PageNo=0,WinSize=30,Number=10,Print="Lua")
#Ret=g.BCC("喜欢u{} AND 我{}",Command="Context",PageNo=0,WinSize=30,Number=10)
#Ret=g.BCC("(~)不得了{$1=[得]} AND 喜欢(u){$1=[得]}",Command="Context",PageNo=0,WinSize=30,Number=10)
#Ret=g.BCC(Query)
#Ret=g.BCC("我(~){}",Command="Context",PageNo=0,WinSize=30,Number=10)
#Ret=g.BCC("语法{} AND 我(~){$1=[想]}",Command="Context",PageNo=0,WinSize=30,Number=10)
#Ret=g.BCC("u~{}[(0,713);(714,928)]",Command="Freq",Number=10)
print(Ret)