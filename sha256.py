import math
import threading

def SHA256(input):
    Blocks=[[]]
    i,e=0,0
    while i<len(input):
        e=4
        while e>0 and i<len(input):
            e-=1
            Blocks[-1].append(ord(input[i])*256**e)
            i+=1
        if e==0:
            if len(Blocks[-1]) == 16:
                 Blocks = Blocks + [[0]]
            else:
                Blocks[-1] = Blocks[-1] + [0]
    
    if e > 0:
        Blocks[-1][-1] = Blocks[-1][-1] + (2147483648/int(256**(4-e)))
    else:
        Blocks[-1][-1] = 2147483648

    if len(Blocks[-1]) == 16:
        Blocks = Blocks + [[0]]
    import time
    if len(Blocks[-1])<15:
        while len(Blocks[-1]) != 15:
            Blocks[-1] = Blocks[-1] + [0]

    Blocks[-1] = Blocks[-1] + [len(input)*8]
    #print(Blocks)

    def add(a, b):
        return (a + b) % 4294967296
	
    def XOR(a, b):
        A=int(math.floor(a/65536))^int(math.floor(b/65536))
        B=int((a%65536))^int((b%65536))
        return A*65536+B
	
    def AND(a, b):
        A=math.floor(a/65536)&math.floor(b/65536)
        B=int(a%65536)&int(b%65536)
        return A*65536+B
	
    def OR(a, b):
        A=math.floor(a/65536)|math.floor(b/65536)
        B=int(a%65536)|int(b%65536)
        return A*65536+B
	
    def NOT(n):
        return 4294967295-n
	
    def Ch(x, y, z):
        return OR(AND(x, y), AND(NOT(x), z))
	
    def Maj(x, y, z):
        return OR(OR(AND(x, y), AND(x, z)), AND(y, z))
	
    def shr(n, shifts):
        return math.floor(n/(2**shifts))
	
    def rotr(n, rots):
        rots = 2**rots
        return (n % rots) * (4294967296/rots) + math.floor(n/rots)
	
    def sigma0(n):
        return XOR(XOR(rotr(n, 7), rotr(n, 18)), shr(n, 3))
	
    def sigma1(n):
        return XOR(XOR(rotr(n, 17), rotr(n, 19)), shr(n, 10))
	
    def SIGMA0(n):
        return XOR(XOR(rotr(n, 2), rotr(n, 13)), rotr(n, 22))
	
    def SIGMA1(n):
        return XOR(XOR(rotr(n, 6), rotr(n, 11)), rotr(n, 25))
	
    K = []
    K = K + [1116352408, 1899447441, 3049323471, 3921009573, 961987163, 1508970993, 2453635748, 2870763221]
    K = K + [3624381080, 310598401, 607225278, 1426881987, 1925078388, 2162078206, 2614888103, 3248222580]
    K = K + [3835390401, 4022224774, 264347078, 604807628, 770255983, 1249150122, 1555081692, 1996064986]
    K = K + [2554220882, 2821834349, 2952996808, 3210313671, 3336571891, 3584528711, 113926993, 338241895]
    K = K + [666307205, 773529912, 1294757372, 1396182291, 1695183700, 1986661051, 2177026350, 2456956037]
    K = K + [2730485921, 2820302411, 3259730800, 3345764771, 3516065817, 3600352804, 4094571909, 275423344]
    K = K + [430227734, 506948616, 659060556, 883997877, 958139571, 1322822218, 1537002063, 1747873779]
    K = K + [1955562222, 2024104815, 2227730452, 2361852424, 2428436474, 2756734187, 3204031479, 3329325298]
        
    H = [1779033703, 3144134277, 1013904242, 2773480762, 1359893119, 2600822924, 528734635, 1541459225]

    for Block in Blocks:
        W = Block[0:]
		
        for i in range(16, 63):
            W = W + [add(add(add(sigma1(W[i-2]), W[i-7]), sigma0(W[i-15])), W[i-16])]
		
        a = H[0]
        b = H[1]
        c = H[2]
        d = H[3]
        e = H[4]
        f = H[5]
        g = H[6]
        h = H[7]
		
        for i in range(0, 63):
            T1 = add(add(add(add(SIGMA1(e), Ch(e, f, g)), h), K[i]), W[i])
            T2 = add(SIGMA0(a), Maj(a, b, c))
            h = g
            g = f
            f = e
            e = add(d, T1)
            d = c
            c = b
            b = a
            a = add(T1, T2)
        H[0] = add(a, H[0])
        H[1] = add(b, H[1])
        H[2] = add(c, H[2])
        H[3] = add(d, H[3])
        H[4] = add(e, H[4])
        H[5] = add(f, H[5])
        H[6] = add(g, H[6])
        H[7] = add(h, H[7])
    print("H[7]:",H[7])

    
    hexTable = "0123456789abcdef"
    hash = ""
    for i in range(len(H)):
        for j in range(7):
            hash = hash + hexTable[math.floor(H[i]/16**j) % 16]
    return hash

def xfrange(start, stop, step):
    i = 0
    while start + i * step < stop:
        yield start + i * step
        i += 1

result=SHA256("abcd")
print(result)

def calc(s,d,R):
    print(s,d)
    for k in R[s:d]:
        pass
        if int(385875968*k)==1468785591:
            print("ONE")
        if int(402653184*k)==1468785591:
            print("TWO")
        #print(int(385875968*k),"< H[7] <",int(402653184*k))
            
    return 0

def secret(hash):
    hash=hash[::-1]
    hexTable = "0123456789abcdef"
    print(hexTable.index(hash[0]))
    R=list(xfrange(2,4,0.00000001))

    threads=[]
    print("R:",len(R))
    n=16
    for i in range(n):
        t=threading.Thread(target=calc,args=[int((len(R)/n)*i),int((len(R)/n)*(i+1)),R])
        t.start()
        threads.append(t)
    for i in threads:
        t.join()


    #print(int(385875968*k),"< H[7] <",int(402653184*k))


    for j in range(7)[::-1]:
        pass
    return "ok"
special=secret(result)
print(special)
