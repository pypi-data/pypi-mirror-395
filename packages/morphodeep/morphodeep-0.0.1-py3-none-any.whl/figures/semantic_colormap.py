import numpy as np
import matplotlib.pyplot as plt



def get_semantic_colormap(only_colors=False):
    #Define Colors for Semantic
    #    0 : Background
    #    1 : Inside the Cell (Cytoplasm)
    #    2 : Junction Level 1 ( Cell Wall )
    #    3 : Junction Level 2 (Cell Junctions with 3 cells)
    #    4 : Junction Level 3 (Cell Junctions with 4 cells or more )
    cols = np.zeros([5,4])
    cols[0, :] = [0,0,0,1]  # Background (black)
    cols[1, :] = [0.5, 0.5, 0.5,1]   # Cytoplasm (gray)
    cols[2,:]=[0,0,1,1] #Cell Wal (blue)
    cols[3,:]=[1,0,1,1] # Level 2 (red)
    cols[4,:]=[0,1,1,1] # Level 3 (cyan)
    if only_colors: return cols
    return plt.cm.colors.ListedColormap(cols)


if __name__ == '__main__':
    from morphodeep.tools.image import imread
    cols = get_semantic_colormap()
    im=imread('/Users/efaure/SeaFile/MorphoDeep/semantic/DATA/GT_3D/SPIM-Phallusia-Mammillata/semantic/140317-Patrick-St8/140317-Patrick-St8_fuse_t097_JN.tiff.gz')

    im=im[250,...]
    print(im.shape)
    fig, axs = plt.subplots(figsize=(round(im.shape[1]/10),round(im.shape[0]/10)))
    plt.imshow(im,cmap=get_semantic_colormap(),interpolation='none')
    plt.axis('off')
    plt.savefig(f"SemanticColorMap.png")
    plt.close(fig)