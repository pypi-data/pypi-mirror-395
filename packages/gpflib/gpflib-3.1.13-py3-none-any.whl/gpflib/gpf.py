from gpflib import GPF
g=GPF("Corpus")
#Ret=g.BCC("v历史f{}[(1,2);(2,3)]",Print="Lua")
#Ret=g.BCC("u~{}[(0,713);(714,928)]",Command="Context",PageNo=0,WinSize=30,Number=10,Print="Lua")
#Ret=g.BCC("喜欢{} NOT 我{}",Command="Context",PageNo=0,WinSize=30,Number=10,Print="Lua")
Ret=g.BCC("喜欢{$1=[大家]}[(1,2);(3,5)] AND 我{}",Command="Context",PageNo=0,WinSize=30,Number=10,Print="Lua")
#Ret=g.BCC("u~{}[(0,713);(714,928)]",Command="Count")
#Ret=g.BCC("u~{}[(0,713);(714,928)]",Command="Freq",Number=10)
print(Ret)