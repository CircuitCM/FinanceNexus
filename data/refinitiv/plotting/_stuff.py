import dash_core_components as dcc
import plotly.graph_objects as go
import numpy as np
from numpy import random as rand
import scipy.interpolate as interp
import os
import math as m

#--- everything here is my original code unless I explicitly say it's not mine


def point_surface_plot(nrdat,name='Test Plot',wlevel=.25,mlevel=.6):
    arr = nrdat[0]
    mm=nrdat[1]
    mx=nrdat[2]
    ad = (mx-mm)
    settings = dict(colorscale=[[0,'blue'],[wlevel,'green'],[mlevel,'grey'],[1,'white']],showscale=False,
                    lighting=dict(roughness=.75,ambient=0.97,diffuse=0.95,specular=0.025,fresnel=0.01))
    if arr.shape[0]==arr.shape[1]:
        surf = go.Surface(z=arr,**settings)
        vrs = arr.var(ddof=True)
        ad=ad/vrs
    else:
        z=arr[:,2]
        vrs = z.var(ddof=True)
        ad = ad/vrs
        surf = go.Mesh3d(x=arr[:,0],y=arr[:,1],z=z,intensity=z,**settings)#[[0, 'blue'],[1, 'peach']]
    fig = go.Figure(surf,layout=dict(plot_bgcolor='rgb(12,163,135)',scene=dict(zaxis=dict(nticks=4, range=[int(mm - ad), int(mx + ad)])),
                                     scene_aspectmode='manual',
                                     scene_aspectratio=dict(x=2, y=2, z=1)))
    print('True variance: '+str(vrs))
    #renderer='iframe'
    fig.show()
    return dcc.Graph(id=name,figure=fig)


def test_array(n,mag):
    return rand.normal(loc=5, scale=mag, size=n**2).reshape((n,n))

#Not my code
#for that continous brownian motion
def rho(x,y,R,alpha):

    if alpha <= 1.5:
        # alpha=2*H, where H is the Hurst parameter
        beta = 0
        c2 = alpha/2
        c0 = 1-alpha/2
    else:
        # parameters ensure piecewise function twice differentiable
        beta = alpha*(2-alpha)/(3*R*(R**2-1))
        c2 = (alpha-beta*(R-1)**2*(R+2))/2
        c0 = beta*(R-1)**3+1-c2

    # create continuous isotropic function
    r = np.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)
    if r<=1:
        out=c0-r**alpha+c2*r**2
    elif r<=R:
        out=beta*(R-r)**3/r
    else:
        out=0

    return out, c0, c2

#NOT my code, appears to make terrain similar to square midpoint displacement but with some continuous transformation
# The main control is the Hurst parameter: H should be between 0 and
# 1, where 0 is very noisy, and 1 is smoother.
def brownian_surface(N=1000, H=0.95):
    R = 2  # [0,R]^2 grid, may have to extract only [0,R/2]^2

    # size of grid is m*n; covariance matrix is m^2*n^2
    M = N

    # create grid for field
    tx = np.linspace(0, R, M)
    ty = np.linspace(0, R, N)
    rows = np.zeros((M,N))


    for i in range(N):
        for j in range(M):
            # rows of blocks of cov matrix
            rows[j,i] = rho([tx[i],ty[j]],
                            [tx[0],ty[0]],
                            R, 2*H)[0]

    BlkCirc_row = np.vstack(
        [np.hstack([rows, rows[:,-1:1:-1]]),
         np.hstack([rows[-1:1:-1,:], rows[-1:1:-1, -1:1:-1]])])

    # compute eigen-values
    lam = np.real(np.fft.fft2(BlkCirc_row))/(4*(M-1)*(N-1))
    lam = np.sqrt(lam)

    # generate field with covariance given by block circular matrix
    Z = np.vectorize(complex)(np.random.randn(2*(M-1), 2*(M-1)),
                              np.random.randn(2*(M-1), 2*(M-1)))
    F = np.fft.fft2(lam*Z)
    F = F[:M, :N] # extract sub-block with desired covariance

    out,c0,c2 = rho([0,0],[0,0],R,2*H)

    field1 = np.real(F) # two independent fields
    #field2 = np.imag(F)
    field1 = field1 - field1[0,0] # set field zero at origin
    #field2 = field2 - field2[0,0] # set field zero at origin

    # make correction for embedding with a term c2*r^2
    field1 = field1 + np.kron(np.array([ty]).T * np.random.randn(),
                              np.array([tx]) * np.random.randn())*np.sqrt(2*c2)
    #field2 = field2 + np.kron(np.array([ty]).T * np.random.randn(),
     #                         np.array([tx]) * np.random.randn())*np.sqrt(2*c2)
    #X,Y = np.meshgrid(tx,ty)

    field1 = field1[:N//2, :M//2]
    #field2 = field2[:N//2, :M//2]
    return (field1,np.amin(field1),np.amax(field1))

#first concept terrain generator, before I understood midpoint displacement or brownian motion
def tri_fractal_test(n,st=(1,1,1),zamp=1/2,xyamp=1/2,ran=lambda:rand.uniform(-1,1)):
    ifs = np.asfarray([[0,1/2],
           [m.sqrt(3)/4,-1/4],
           [-m.sqrt(3)/4,-1/4]],dtype='float')
    alloc =4**n
    iters = [(4**i) for i in range(0,n)]
    print(alloc)
    print(iters)
    pts = np.zeros((alloc,3),dtype='float')
    fp = pts[0]
    fp[0],fp[1],fp[2]=st[0],st[1],st[2]
    for i in range(0,n):
        ipos = iters[i]
        am = xyamp ** i
        for s in range(0,ipos):
            op = pts[s]
            for l in range(0,3):
                fp=pts[ipos+l]
                fi = ifs[l]
                xamp,yamp,zmp = fi[0]*am,fi[1]*am,ran()*(zamp**i)
                fp[0], fp[1], fp[2] = op[0]+xamp, op[1]+yamp, op[2]+zmp
            ipos += 3
    return (pts,np.amin(pts[:,2]),np.amax(pts[:,2]))

#line displacement
def midpt2D(N:int=0,H:float=1/2,R:int=2,var1:float=1,start=None,seed=rand.randint(0,1000000)):
    rand.seed(seed)
    if start is None:
        start =rand.normal(size=2)*var1
    if N <1:
        N = int((17/m.log2(R)))
        print('N: '+str(N))
    TN = (R**N)
    pts = np.zeros(TN+1,dtype='float64')
    pts[0]=start[0]
    pts[TN]=start[1]
    delta = m.sqrt(1-R**(2*H-2))*var1
    D=TN
    d=D//R
    for i in range(0,N):
        dev = delta*(R**(-i*H))
        for k in range(0,TN,D):
            x0=pts[k]
            x1=pts[k+D]
            for z in range(k+d,k+D,d):
                rp=(z-k)/D
                pts[z]=((1-rp)*x0 + rp*x1)+dev*rand.normal()
        D=d
        d=d//R
    return (pts,np.arange(0,TN+1))

#Stands for midpoint square step, H hurst factor, R lacunarity, var1 variance
def midpt3D_s(N:int=0,H:float=1/2,R:int=2,var1:float=1,start=None,seed=rand.randint(0,1000000)):
    rand.seed(seed)
    if start is None:
        start =rand.normal(size=4)*var1
    if N <1:
        N = int((10/m.log2(R)))
        print('N: '+str(N))
    TN = (R**N)
    pts = np.zeros((TN+1,TN+1),dtype='float64')
    pts[0][0],pts[0][TN],pts[TN][0],pts[TN][TN]=start[0],start[1],start[2],start[3]
    delta = m.sqrt(1-R**(2*H-2))*var1
    D=TN
    d=D//R
    for i in range(0,N):
        dev = delta*(R**(-i*H))
        #side point loop
        for v in range(0,TN+1,D):
            for k in range(0,TN,D):
                #horizontal get
                x0=pts[v][k]
                x1=pts[v][k+D]
                for z in range(k+d,k+D,d):
                    rp=(z-k)/D
                    pts[v][z]=((1-rp)*x0 + rp*x1)+dev*rand.normal()
                #vertical get
                x0=pts[k][v]
                x1=pts[k+D][v]
                for z in range(k+d,k+D,d):
                    rp=(z-k)/D
                    pts[z][v]=((1-rp)*x0 + rp*x1)+dev*rand.normal()
        #inner point loop
        #loop length
        for v in range(0,TN,D):
            #loop width
            for k in range(0,TN,D):
                #loop inner points
                for u in range(d,D,d):
                    y0,y1=pts[v][k+u],pts[v+D][k+u]
                    ry=u/D
                    yf = (1-ry)*y0+ry*y1
                    for z in range(d,D,d):
                        x0,x1=pts[v+z][k],pts[v+z][k+D]
                        rx=z/D
                        pts[v+z][k+u]=(yf+ (1-rx)*x0 + rx*x1)*.5 +dev*rand.normal()
        D=d
        d=d//R
    print('Dim: ' + str(pts.shape))
    print('Points: ' + str(pts.size))
    return (pts,np.amin(pts),np.amax(pts))

#NOT USED in presentation
#additive midpoint square step, turns out to be barely different from square midpoint
def midpt3D_sa(N:int=0,H:float=1/2,R:int=2,var1:float=1,start=None,seed=rand.randint(0,1000000)):
    rand.seed(seed)
    if start is None:
        start =rand.normal(size=4)*var1*m.sqrt(.5)
    if N <1:
        N = int((10/m.log2(R)))
        print('N: '+str(N))
    TN = (R**N)
    pts = np.zeros((TN+1,TN+1),dtype='float64')
    pts[0][0],pts[0][TN],pts[TN][0],pts[TN][TN]=start[0],start[1],start[2],start[3]
    delta = m.sqrt((.5)*(1-R**(2*H-2)))*var1
    D=TN
    d=D//R
    for i in range(0,N):
        dev = delta*(R**(-i*H))
        #side point loop
        for v in range(0,TN+1,D):
            for k in range(0,TN,D):
                #horizontal get
                x0=pts[v][k]
                x1=pts[v][k+D]
                for z in range(k+d,k+D,d):
                    rp=(z-k)/D
                    pts[v][z]=((1-rp)*x0 + rp*x1)+dev*rand.normal()
                #the additive randoms
                pts[v][k]=pts[v][k]+dev*rand.normal()
                pts[v][k+D]=pts[v][k+D]+dev*rand.normal()
                #vertical get
                x0=pts[k][v]
                x1=pts[k+D][v]
                for z in range(k+d,k+D,d):
                    rp=(z-k)/D
                    pts[z][v]=((1-rp)*x0 + rp*x1)+dev*rand.normal()
                # the additive randoms
                pts[k][v]=pts[k][v]+dev*rand.normal()
                pts[k+D][v]=pts[k+D][v]+dev*rand.normal()
        #inner point loop
        #loop length
        for v in range(0,TN,D):
            #loop width
            for k in range(0,TN,D):
                #loop inner points
                for u in range(d,D,d):
                    y0,y1=pts[v][k+u],pts[v+D][k+u]
                    ry=u/D
                    yf = (1-ry)*y0+ry*y1
                    pts[v][k+u]=y0+ dev*rand.normal()
                    for z in range(d,D,d):
                        x0,x1=pts[v+z][k],pts[v+z][k+D]
                        rx=z/D
                        pts[v+z][k+u]=(yf+ (1-rx)*x0 + rx*x1)*.5 +dev*rand.normal()
        D=d
        d=d//R
    print('Dim: '+str(pts.shape))
    print('Points: ' + str(pts.size))
    return (pts,np.amin(pts),np.amax(pts))

#wrap around square diamond displacement
def midpt3D_sd(N:int=10,H:float=1/2,var1:float=1,start=None,seed=rand.randint(0,1000000)):
    #R = 2
    rand.seed(seed)
    if start is None:
        start =rand.normal(size=4)*var1
    TN = (2**N)
    pts = np.zeros((TN+1,TN+1),dtype='float64')
    pts[0][0],pts[0][TN],pts[TN][0],pts[TN][TN]=start[0],start[1],start[2],start[3]
    delta = m.sqrt(1-2**(2*H-2))*var1
    D=TN
    d=D//2
    #code is short despite method being more complex because R is always 2
    for i in range(0,N):
        dev = delta*(2**(-i*H))
        #diamond step
        for v in range(0,TN,D):
            for k in range(0,TN,D):
                #set diagonal midpoint
                x0,x1,x2,x3=pts[v][k],pts[v][k+D],pts[v+D][k],pts[v+D][k+D]
                pts[v+d][k+d] = (x0+x1+x2+x3)*.25 +dev*rand.normal()

        #square step
        for v in range(0,TN+1,D):
            for k in range(0,TN,D):
                #loop inner points
                # - horizontally local midpts only mod y-axis
                x0,x1,x2,x3=pts[v][k],pts[v][k+D],pts[(v-d)%TN][k+d],pts[(v+d)%TN][k+d]
                pts[v][k+d] = (x0+x1+x2+x3)*.25 +dev*rand.normal()

                # - vertically local midpts only mod x-axis
                y0,y1,y2,y3=pts[k][v],pts[k+D][v],pts[k+d][(v-d)%TN],pts[k+d][(v+d)%TN]
                pts[k+d][v] = (y0+y1+y2+y3)*.25 +dev*rand.normal()
        D=d
        d=d//2
    print('Dim: '+str(pts.shape))
    print('Points: ' + str(pts.size))
    return (pts,np.amin(pts),np.amax(pts))

#No Wrap around 3 point sides,
def midpt3D_sd3(N:int=10,H:float=1/2,var1:float=1,start=None,seed=rand.randint(0,1000000)):
    #R = 2
    rand.seed(seed)
    if start is None:
        start =rand.normal(size=4)*var1
    TN = (2**N)
    pts = np.zeros((TN+1,TN+1),dtype='float64')
    pts[0][0],pts[0][TN],pts[TN][0],pts[TN][TN]=start[0],start[1],start[2],start[3]
    delta = m.sqrt(1-2**(2*H-2))*var1
    D=TN
    d=D//2
    #code is short despite method being more complex because R is always 2
    for i in range(0,N):
        dev = delta*(2**(-i*H))
        #diamond step
        for v in range(0,TN,D):
            for k in range(0,TN,D):
                #set diagonal midpoint
                x0,x1,x2,x3=pts[v][k],pts[v][k+D],pts[v+D][k],pts[v+D][k+D]
                pts[v+d][k+d] = (x0+x1+x2+x3)*.25 +dev*rand.normal()

        #square step
        for v in range(0,TN+1,D):
            for k in range(0,TN,D):
                #loop inner points
                # - crude implementation to prevent wrap around
                if v==0:
                    x0,x1,x3=pts[v][k],pts[v][k+D],pts[v+d][k+d]
                    pts[v][k+d] =((x0+x1+x3)/3) +dev*rand.normal()

                    y0,y1,y3=pts[k][v],pts[k+D][v],pts[k+d][v+d]
                    pts[k+d][v] = ((y0+y1+y3)/3) +dev*rand.normal()
                elif v==TN:
                    x0,x1,x2=pts[v][k],pts[v][k+D],pts[v-d][k+d]
                    pts[v][k+d] = ((x0+x1+x2)/3) +dev*rand.normal()

                    y0,y1,y2=pts[k][v],pts[k+D][v],pts[k+d][v-d]
                    pts[k+d][v] = ((y0+y1+y2)/3) +dev*rand.normal()
                else:
                    x0,x1,x2,x3=pts[v][k],pts[v][k+D],pts[v-d][k+d],pts[v+d][k+d]
                    pts[v][k+d] = (x0+x1+x2+x3)*.25 +dev*rand.normal()

                    y0,y1,y2,y3=pts[k][v],pts[k+D][v],pts[k+d][v-d],pts[k+d][v+d]
                    pts[k+d][v] = (y0+y1+y2+y3)*.25 +dev*rand.normal()
        D=d
        d=d//2
    print('Dim: '+str(pts.shape))
    print('Points: ' + str(pts.size))
    return (pts,np.amin(pts),np.amax(pts))

#adds water by filling in the z axis as a percentage from the min-z to max-z
def add_base(nrdat,wstart=.3):
    arr=nrdat[0]
    mm=nrdat[1]
    mx=nrdat[2]
    m = (mx-mm)*wstart +mm
    if arr.shape[1]==arr.shape[0]:
        for ix, iy in np.ndindex(arr.shape):
            if arr[ix, iy] <m:
                arr[ix, iy]=m
    else:
        for iz in np.ndindex(arr.shape[1]):
            if arr[iz, 2] <m:
                arr[iz,2]=m
    return (arr,m,mx)

#deprecated use variance:var1 in midpoint functions
def _amp(nrdat,amp=2.0):
    arr = nrdat[0]
    mm = nrdat[1]*amp
    mx = nrdat[2]*amp
    if arr.shape[1]==arr.shape[0]:
        arr=arr*amp
    else:
        arr[:, 2] = arr[:, 2] * amp
    return (arr,mm,mx)

def interp_array(arrdat,w,h):
    arr = arrdat[0]
    W, H = arr.shape[:2]
    xrange = lambda x: np.linspace(0, 1, x)

    f = interp.interp2d(xrange(W), xrange(H), arr, kind="linear")
    new_arr = f(xrange(w), xrange(h))
    return (new_arr,arrdat[1],arrdat[2])


def rename_figure(name=rand.randint(1,10000)):
    # because my computer was crashing, put figures into iframe folder
    #if in pycharm right click the figure in the iframes figure folder,select open in browser
    pth=__file__[:__file__.rfind('/')]
    if os.path.exists(pth+'/iframe_figures/figure_'+str(name)+'.html'):
        os.remove(pth+'/iframe_figures/figure_'+str(name)+'.html')
    os.renames(pth+'/iframe_figures/figure_0.html',pth+'/iframe_figures/figure_'+str(name)+'.html')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #app = dash.Dash()
    #nrdat = tri_fractal_test(5,zamp=1/1.6,xyamp=1/2,ran=lambda: rand.normal(0,1))
    #point_surface_plot(nrdat,name='Tri Test',wlevel=.4)
    #f1=brownian_surface(1200,.78)
    #f1=add_base(_amp(f1,3.5),.5)
    #point_surface_plot(f1, name='Brown Test',wlevel=.005,mlevel=.45)
    R=2
    ar = midpt2D(R=R,H=.7,start=np.zeros(2))
    fig =go.Figure(data=go.Scatter(y=ar[0],x=ar[1]))
    fig.show()
    #print(midpt_2D(N=3, R=2, seed=10))
    #------ to make realistic water set water wlevel=.005, mountain mlevel=maybe around .5
    #------ r=2 looks the best by far, r>2
    #------ to send straight to browser delete renderer='iframe' in the first def top of file
    # pts = add_base(interp_array(midpt3D_s(N=10, H=.7, R=2, var1=2.5),500,500), .45)
    # p1=point_surface_plot(pts, wlevel=.005, mlevel=.4,name='plot 1')
    # #rename_figure(1)
    #pts=add_base(midpt3D_s(N=4,H=.7,R=4,var1=3.5),.45)
    #point_surface_plot(pts,wlevel=.005,mlevel=.4,name='plot 2')
    #point_surface_plot(add_base(midpt3D_sd(N=8, H=.7, var1=3.5),.45),wlevel=.005,mlevel=.45)
    #point_surface_plot(add_base(midpt3D_sd3(N=8, H=.7, var1=3.5), .45), wlevel=.005, mlevel=.45)
    #app.layout = html.Div([p1, p2])
    #app.run_server(debug=True)
    #rename_figure(2)
