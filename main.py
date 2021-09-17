import matplotlib.pyplot as plt
import numpy as np
import skimage.io as skio
from glob import glob
import click
import os
from skimage import registration
import scipy.ndimage as ndi
from skimage.exposure import equalize_adapthist
import re
import cv2
from reliability.Other_functions import crosshairs

@click.group()
def cli():
    pass

refPt = []
@cli.command('makeBarcodeWithBead')
@click.argument('img647_dir',type=click.Path(exists=True))
@click.argument('img750_dir',type=click.Path(exists=True))
@click.argument('bead_dir',type=click.Path(exists=True))
@click.option('--n_ref',default=0,type=int)
@click.option('--pattern',default=None,type=str)
@click.option('--circle_size',default=15,type=int)
@click.option('--thresh',default=0.995,type=float)
@click.option('--window_size',default=100,type=int)
@click.option('--img_scale',default=10.0,type=float)
def makeBarcodeWithBead(img647_dir:str,img750_dir:str,bead_dir:str,n_ref:int,pattern:str,circle_size:int,thresh:float,window_size:int,img_scale:float):

    


    global refPt
    if pattern is None:
        pattern = "*.TIFF"
    pattern647 = os.path.join(img647_dir,pattern)
    pattern750 = os.path.join(img750_dir,pattern)
    file_list_647 = glob(pattern647)
    file_list_750 = glob(pattern750)
    
    file_list_647.sort(key=lambda f: int(re.sub('\D', '', f)))
    file_list_750.sort(key=lambda f: int(re.sub('\D', '', f)))

    bead_dir_pattern = os.path.join(bead_dir,pattern)
    bead_file_list = glob(bead_dir_pattern)
    bead_file_list.sort(key=lambda f: int(re.sub('\D', '', f)))

    #Register the beads
    bead_imgs = dict()
    for idx,fn in enumerate(bead_file_list):
        img = skio.imread(fn)
        bead_imgs[idx]=img
    #load images
    imgs = dict()
    file_list = file_list_647+file_list_750
    for idx,fn in enumerate(file_list):
        
        _img = skio.imread(fn)
        
        imgs[idx]=equalize_adapthist(_img, clip_limit=0.03)

    
    for idx in range(1,len(bead_imgs)):
        shift,_,_ = registration.phase_cross_correlation(bead_imgs[n_ref],bead_imgs[idx])
        
        imgs[idx] = ndi.shift(imgs[idx],shift)


    #Window size
    window_Size =window_size

    ref_img = imgs[n_ref]
    ref_img = ref_img*img_scale

    fig,ax = plt.subplots(num=1)
    cid = fig.canvas.mpl_connect('button_release_event', recordClickLoc_mpl)
    ax.imshow(ref_img,cmap='gray')
    crosshairs()
    plt.show()
    while True:
  
        if len(refPt)<2:
            if not plt.fignum_exists(num=1):
                fig,ax = plt.subplots(num=1)
                cid = fig.canvas.mpl_connect('button_release_event', recordClickLoc_mpl)
                ax.imshow(ref_img,cmap='gray')
                crosshairs()
                plt.show()
            continue
        else:
            print('Accepted')
            print(refPt)
            break
    
    #load and register all the images based on the bead registration


    #Draw a circle of a certain radius in the image
    img_circle = dict()

    n_cols = 3
    n_rows = int(np.ceil(len(imgs)/n_cols))
    plt.rcParams.update({'font.size': 22})
    f,ax = plt.subplots(n_rows,n_cols,figsize=(20,20),dpi=200)
    ax = ax.flatten()

    for idx in range(len(imgs)):
        img = imgs[idx]
        spot_thresh = calcSpotThresh(img,thresh_percent=thresh)
        canvas = np.zeros((img.shape[0],img.shape[1],3))
        circle_mask = cv2.circle(canvas,tuple(refPt),circle_size//2,(1,1,1),-1)
        circle_test = circleTest(img,circle_mask,spot_thresh)
        img_circle[idx] = centreCrop(cv2.circle(img,tuple(refPt),circle_size//2,(0,255,255),1),
                                    refPt,
                                    window_Size)
        ax[idx].imshow(img_circle[idx]*img_scale,vmin=0,cmap='gray')#,vmax=np.max(img[idx]),)
        ax[idx].axis('off')
        ax[idx].set_title(circle_test)
    plt.tight_layout()

    plt.savefig('./barcode_bead_example.png')




    

def recordClickLoc_mpl(event):
    global refPt
    refPt=[int(event.xdata),int(event.ydata)]

def centreCrop(img,centrePt,window_size):
    h=window_size//2

    
    y = np.maximum(centrePt[1] - h,0)
    x = np.maximum(centrePt[0] - h,0)

    crop_img = img[int(y):int(y+window_size), int(x):int(x+window_size)]
    return crop_img

def circleTest(img,circle_mask, thresh):
    res = np.multiply(img[:,:,np.newaxis].copy(),circle_mask)[:,:]
    test = res[res>thresh].sum()
    if test>0:
        return 1
    else:
        return 0

def calcSpotThresh(img:np.ndarray,thresh_percent:float = 0.9)->float:
    _img = img[:,:].flatten()

    sorted_img = np.sort(_img)

    idx = np.floor(thresh_percent*sorted_img.size).astype(int)

    _thresh = sorted_img[idx]
    
    return _thresh
    #create histogram of the image
    #find the threshpercentile. i.e. sort the list, and then find the thresh_percent*len(list)

if __name__=='__main__':
    cli()

    # img647_dir = '/Volumes/shahidsWORK/647nm, Raw'

    # img750_dir = '/Volumes/shahidsWORK/750nm, Raw'

    # beads_dir = '/Volumes/shahidsWORK/561nm, Raw'

    # makeBarcodeWithBead(img647_dir,img750_dir,beads_dir,n_ref=0,pattern="merFISH_*_002_01.TIFF",circle_size=9,thresh=0.995,window_size=50,img_scale=1)
