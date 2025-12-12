from gpflib import GPF
g=GPF("Corpus")
Query="""
--Lua
OriOn()
Speedup(1)
Handle0=GetAS("<我","我","","","","","","","","")
SetBase(Handle0,0,0)
ClearLimit()
Handle2=GetAS("欢_n|","喜欢","","","","","","","","")
Handle3=Context(Handle2,30,0,10)
Ret=Output(Handle3)
return Ret
"""
#Ret=g.BCC("v历史f{}[(1,2);(2,3)]",Print="Lua")
#Ret=g.BCC("u~{}[(0,713);(714,928)]",Command="Context",PageNo=0,WinSize=30,Number=10,Print="Lua")
#Ret=g.BCC("喜欢{} NOT 我{}",Command="Context",PageNo=0,WinSize=30,Number=10,Print="Lua")
#Ret=g.BCC("喜欢n{} AND 我{}",Print="Lua",Command="Context",PageNo=0,WinSize=30,Number=10)
#Ret=g.BCC(Query)
Ret=g.BCC("喜欢{} AND 我{}",Command="Context",PageNo=0,WinSize=30,Number=10)
#Ret=g.BCC("u~{}[(0,713);(714,928)]",Command="Count")
#Ret=g.BCC("u~{}[(0,713);(714,928)]",Command="Freq",Number=10)
print(Ret)