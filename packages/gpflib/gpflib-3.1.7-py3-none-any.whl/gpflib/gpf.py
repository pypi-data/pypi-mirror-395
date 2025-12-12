from gpflib import GPF
g=GPF("Corpus")
#Ret=g.BCC("v历史f{}[(1,2);(2,3)]",Print="Lua")
Ret=g.BCC("u~{}",Command="Context",PageNo=0,WinSize=30,Number=10)
print(Ret)