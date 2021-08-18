x={"a":1,"b":2,"c":3,"d":4}
print(len(x))
y={i:j*j*j for  (i,j) in x.items() if j>1 }
print(y)
print(27 in y.values())
# print(x.slice[:"c"])
# filter(funct,list)



h="hhhhbbbbaaaaaaaaaaaaaaaaallllllllllllllllleeeeeeeeeeeeeee"
slit=[x for x in h]
sh=set(h)
#print(sh[0])

result=[]
for i in set(h):
    print(i)
    result.append(len([k for k in slit if k == i]))
    result.append(i)

result="".join([str(x) for x in result])
print(result)

# def fac(n):
#     if n==


# yx=[1,2,3]
# print(sum(yx)/len(yx))
#print(split(h))
