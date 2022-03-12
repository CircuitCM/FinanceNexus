import numpy as np
from numpy import random as nran
import random as rd
import plotly.graph_objects as grap
from plotly import subplots as sub
from scipy import stats as st
RND=nran.default_rng()
#----
#for now I will begin with static population size using binary strings
#population will be embeded in 2d numpy array using uint8

#---- Population initialization and generation,

def _unitize(x,y):
    return x/y

def _gen_pop(popr,ranr):
    popr[ranr]=1


unit = np.vectorize(_unitize,[float])
pop_gen = np.vectorize(_gen_pop,[np.uint8])

def new_var_comb_pop(ar:np.ndarray,comb:int=25,pop=50):
    ar:np.ndarray=ar/ar[:,0:1]
    ash=ar.shape[0]
    popl=np.zeros((pop,ash),np.uint8)
    for i in popl:
        i[RND.choice(ash,size=comb,replace=False)]=1
    print(ar)
    return ar, popl


#---- Fitness procedure, fitness func factory based off of solution space

def sharpe_fitness_fac(ar:np.ndarray,comb=25):
    covar:np.ndarray=np.cov(ar)
    m=np.matrix([[1./comb for _ in range(comb)]],float)
    mt=m.transpose()
    nar:np.ndarray=ar[:,-1]
    print(covar)
    def fitness(ftr:np.ndarray,gen:np.ndarray):
        for i in range(ftr.shape[0]):
            vl=gen[i].nonzero()
            cv=covar[np.meshgrid(vl,vl,indexing='xy',copy=False)]
            ftr[i]=np.sum(nar[vl]/comb)/(m@(cv@cv)@mt).item()
    return fitness





#---- selection, could use linear distribution over whole population best to worst, or geometric

def generic_selec(pa:np.ndarray,fitr:np.ndarray):
    vl = np.all(pa[0,:]==pa,axis=0)
    #print(vl)
    #print(vl)
    inb = vl.sum() / vl.shape[0]
    #print(inb)
    sm=fitr.sum()
    crm=np.argmax(fitr)
    nep=np.zeros(pa.shape,dtype=np.uint8)
    nep[crm]=pa[crm]
    for p,v in zip(iter(RND.choice(fitr.shape[0],size=2,replace=False,p=fitr/sm) for _ in range(fitr.shape[0]-1)),iter(i+1 if i>=crm else i for i in range(fitr.shape[0]-1))):
        cross_combo_restricted(pa[p[0]],pa[p[1]],nep[v],inbred=inb)
    return crm,nep



#crossover func produces the new population and keeps it within constraints, also responsible for mutations
def cross_combo_restricted(p1:np.ndarray,p2:np.ndarray,nep:np.ndarray,mutation=0.075,inbred=.0):
    nep[:]=p1[:]
    ar=np.asarray(p1!=p2).nonzero()[0]
    nran.shuffle(ar)
    #print(ar)
    for v in range(0,ar.shape[0]-1,2):
        nep[ar[v:v+2]]=[0,1]
    vl=RND.binomial(nep.shape[0], (mutation+inbred)/2)
    #vl=rd.
    if vl>0:
        p1=np.argwhere(nep==1)
        p0=np.argwhere(nep==0)
        sh0=p0.shape[0]
        sh1=p1.shape[0]
        for i in range(vl):
            r0=rd.randint(0,sh0-1)
            r1=rd.randint(0,sh1-1)
            nep[p0[r0]]=1
            nep[p1[r1]]=0
            l,m = p1[r1].item(),p0[r0].item()
            p0[r0],p1[r1]=l,m


#--- loop with characteristics

def elite_1(pop:np.ndarray,fit,iterations=10000):
    ftr=np.zeros(pop.shape[0],float)
    omx=-1
    ofv=-1
    for i in range(iterations):
        fit(ftr, pop)
        mx,nep=generic_selec(pop,ftr)
        pop=nep
        if omx!=mx:
            omx=mx
            fv=ftr[omx]
            if fv>ofv:
                ofv=fv
                print(f'New best portfolio found, fit: {ofv}, value: {pop[omx]}, iteration: {i}')
    return ofv,pop[omx]


def combinations_genetic_procedure(ar:np.ndarray,comb:int=25,pop=50,iterations=10000):
    solp,popl=new_var_comb_pop(ar,comb,pop)
    fit=sharpe_fitness_fac(solp,comb)
    return elite_1(popl,fit,iterations)


def test_array(days=1000,q=50,tgr=1.19,vg=.022,sig=.01,sigv=.002):
    pm:np.ndarray=np.ones((q,days),dtype=np.float64)
    for i in range(q):
        rv=rd.normalvariate(0,sigv)
        rv=0.001-sig if rv+sig<0 else rv
        tv=rd.normalvariate(0,vg)
        tv=0.001-tgr if tv+tgr<0 else tv
        pm[i,1:]=RND.lognormal(mean=(tgr+tv)/days,sigma=(sig+rv),size=days-1)
        #pm[i,0]=1.
        for s in range(1,days): pm[i,s]=pm[i,s-1]*pm[i,s]
    #print(pm)
    return pm


def testing():
    # a:np.ndarray=np.matrix([[11,12,15,15,14,16,20,21],
    #             [25,26,29,24,26,28,29,31],
    #             [10,9,8,10,14,17,19,23],
    #             [34,38,37,39,40,9,46,50],
    #             [35,36,37,45,41,51,42,55],
    #             [15,14,16,10,19,18,22,25]],float)
    a=test_array()
    plt = sub.make_subplots(rows=1, cols=1)
    #plt.add_trace(grap.Scatter(y=a),row=1,col=1)
    for i in a:
        plt.add_trace(grap.Scatter(y=i), row=1, col=1)
    plt.show()
    mx,folio=combinations_genetic_procedure(a,25,40,4500)
    sub.make_subplots(rows=1, cols=1).add_trace(grap.Scatter(y=[i.sum()/25 for i in a[folio.nonzero()[0]].transpose()])).show()
    mx, folio = combinations_genetic_procedure(a, 25, 14, 20000)
    sub.make_subplots(rows=1, cols=1).add_trace(
        grap.Scatter(y=[i.sum() / 25 for i in a[folio.nonzero()[0]].transpose()])).show()
    return
    print(a.shape)
    a=unit(a,a[:,0])
    print(a)
    a=np.cov(a)
    print(a)

    m=np.matrix([[.25,.25,.25,.25,]])
    mt=m.transpose()
    print(m)
    print(mt)
    na:np.ndarray=a*a
    print(na)
    print(m@(a*a)@mt)
    print((a*na).trace())
    #print(na.)




if __name__=='__main__':
    testing()
    # t1=np.array([0,0,0,0,0,1,1,1,1,1],int)
    # t2=np.array([1,1,1,1,1,0,0,0,0,0],int)
    # print(t1[t1!=t2].nonzero()[0])
    # print(t2[t1!=t2].nonzero()[0])
    # print(cross_combo_restricted(t1,t2,np.zeros(t1.shape[0],int)))
    # print(cross_combo_restricted(t1,t2, np.zeros(t1.shape[0],int)))

    # t1 = np.array([0, 0, 0, 1, 1, 0, 1, 1, 1, 0], int)
    # t2 = np.array([0, 1, 1, 1, 1, 0, 1, 0, 0, 0], int)
    # #print(cross_combo_restricted(t1, t2, np.zeros(t1.shape[0], int)))
    # #print(cross_combo_restricted(t1, t2, np.zeros(t1.shape[0], int)))
    # print(nran.binomial(50,.25*2/(50),1000)//2)
    # print(st.binom.rvs(50,.5/50,))