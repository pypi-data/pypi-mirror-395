# -*- coding: latin-1 -*-
import os
from os import listdir
from os.path import join, isfile, isdir, dirname, basename

from tqdm import tqdm

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from morphodeep.paths import SCRATCH, RESULT, WORK, species
from skimage.transform import resize
import numpy as np
from morphodeep.config import Config
from morphodeep.tools.utils import get_last_epochs, get_weights_filename, printi, mkdir, \
    file_write, get_basename, printp, printe, get_slice, execute, read_txt_file, get_correspond_filename, \
    read_eval_file, write_eval_file
from morphodeep.tools.image import imsave, get_glasbey, imread, get_gaussian, get_border, re_label, \
    semantic_to_segmentation, normalize
from morphodeep.tools.plot import imshow, get_tb, get_smooth, colors, remove_axis,  histo_iou
from morphodeep.tools.examples import MorphoExamples
try:
    import matplotlib.pyplot as plt
    from morphodeep.networks.metrics import eval_metrics, metricS, ms, eval_file
    from morphodeep.networks.unet import JUNNET,DUNNET
    from morphodeep.networks.unettopix import UPixToSem
    from morphodeep.networks.unetpp import UNETPP,UNETPPSem
    from morphodeep.networks.pixtopix import PixToPix
    from morphodeep.networks.pixtosem import PixToSem
    from morphodeep.networks.ResUNet import RESJUNET,RESDUNET
    import tensorflow as tf

except Exception as e:
    print(f" --> cannot import {e}")
    #pass



class MorphoModel(Config):

    def __init__(self,*args, **kwargs):
        self.epochs_loaded = 0
        self.model=None
        super().__init__(*args,**kwargs)

    def process(self):
        if not super().process():
            if not self._eval_files:
                self.load_model(show=self._train)
                self.load_weights()
                if self.epochs_loaded>0 and not self._train:
                    if self.epochs<self.epochs_loaded and self.epochs!=1000: #Look for a sepcifc epochs
                        self.load_weights(epochs=self.epochs)
                    self.export_epochs_path = join(self.export_path, "EPOCHS_" + str(self.epochs_loaded))
                    mkdir(self.export_epochs_path)
            if self._train:
                self.train()
            elif self._export:
                self.export()
            elif self._plot_loss:
                self.plot_loss()
            elif self._plot:
                self.plot_loss()
                self.export()
            elif self._predict_test or self._eval:
                file_test=[join(self.dataset_file + "_test.txt")]
                species_topredict=[self.get_ms()]
                '''if self.microscope=="ALL":
                    species_topredict=species
                    file_test=[]
                    for s in species:
                        ft=join(WORK, "Semantic", "NETWORKS_" + str(self.img_size) + "_" + self.mode,s,"tf_test.txt")
                        file_test.append(ft)
                print(file_test)
                quit()
                '''
                if self._predict_test:
                    self.predict_test(species_topredict,file_test)
                    #self.eval(species_topredict, file_test)
                if self._eval: self.eval(species_topredict,file_test)
            elif self._predict_files:
                self.predict_files(self.filename,patches=self._patches,remove_zeros=self._remove_zeros)
            elif self._eval_files:
                self.eval_files(self.filename)

    def load_model(self,show=False):
        self.set_dimensions()
        print(f" --> compil {self.mode} {self.network}  with inputs={self.input_shape} to outputs={self.output_shape}")
        if self.network=="JUNNET":
            self.model = JUNNET(mode=self.mode, inputs=self.input_shape, outputs=self.output_shape)
        if self.network=="DUNNET":
            self.model = DUNNET(mode=self.mode, inputs=self.input_shape, outputs=self.output_shape)
        elif self.network=="UPixToSem":
            self.model = UPixToSem(mode=self.mode, inputs=self.input_shape, outputs=self.output_shape)
        elif self.network=="PixToPix":
            self.model = PixToPix(mode=self.mode, inputs=self.input_shape, outputs=self.output_shape)
        elif self.network=="PixToSem":
            self.model = PixToSem(mode=self.mode, inputs=self.input_shape, outputs=self.output_shape)
        elif self.network=="UNETPP":
            self.model = UNETPP(mode=self.mode, inputs=self.input_shape, outputs=self.output_shape)
        elif self.network=="UNETPPSem":
            self.model = UNETPPSem(mode=self.mode, inputs=self.input_shape, outputs=self.output_shape)
        elif self.network=="RESJUNET":
            self.model = RESJUNET(mode=self.mode, inputs=self.input_shape, outputs=self.output_shape)
        elif self.network=="RESDUNET":
            self.model = RESDUNET(mode=self.mode, inputs=self.input_shape, outputs=self.output_shape)
        if show:  self.model.summary(line_length=150)


    def load_weights(self, epochs=None,verbose=True):
        '''
        load the last weights
        if epochs is specify load the weight at this specific epochs
        '''
        if self.weight_files is None:
            return self.epochs_loaded
        if epochs is None:
            epochs = get_last_epochs(self.weight_files)
        filename=get_weights_filename(self.weight_files, epochs)
        if filename is not None and isfile(filename):
            if verbose: printi("load at epochs " + str(epochs) + " weights file " + filename)
            self.epochs_loaded=epochs
            if self.model is not None:
                self.model.load_weights(filename)
            else:
                printi("please load model first ....")
                return -1
        else:
            if verbose: printi("nothing weights found at " + self.weight_files)
            return -1
        return self.epochs_loaded

    def set_dimensions(self):
        v = 2 if self.mode == "2D" else 3
        self.net_size=self.img_size
        ims = (self.img_size,) * v
        self.input_shape = ims + (1,)
        self.output_shape = ims + (2+v,) #  5 Ouput Classes in 3D , 4 in 2D

    ##################### TRAINING
    def data_loader(self,examples):
        while True:
            b=self.batch_size
            if self.mode=="2D":
                batch_input = np.zeros([self.batch_size] + list(self.input_shape))
                batch_output = np.zeros([self.batch_size] + list(self.output_shape))
            else:
                b=1
                batch_input= np.zeros([1]+list(self.input_shape)) #Real Batch Size is only one
                batch_output = np.zeros([1] + list(self.output_shape))
            i=0
            nb_loop=0
            #print(f"batch_input: {batch_input.shape}")
            #print(f"batch_output: {batch_output.shape}")

            while i < b and nb_loop <  50: #ONLY 50 tests with no valid images...
                if self.mode=="2D":
                    data_input, data_output=examples.get_next(batch_size=1) #To have only unique images
                else:
                    data_input, data_output = examples.get_next(batch_size=self.batch_size)
                #print(f"data_input: {data_input.shape}")
                #print(f"bdata_output: {data_output.shape}")
                if data_input is not None and data_output is not None:
                    batch_input[i,...] = data_input
                    batch_output[i,...] = data_output
                    #print(f"{i} input {np.unique(data_input)}")
                    #print(f"{i} output {np.unique(data_output)}")
                    #imsave(join(SCRATCH,"PATCHES",f"data_input{i}.tiff"),data_input)
                    #imsave(join(SCRATCH, "PATCHES", f"data_output{i}.tiff"), data_output)
                    #quit()
                    i+=1
                else:
                    nb_loop+=1
                if nb_loop>=50:
                    print(" --> Error in the data loader....")
                    #quit()
            yield batch_input, batch_output

    def train(self):
        try:
            os.system('nvidia-smi')
        except:
            print(" --> ERROR nvidia or gpu card ...")

        printi('train with batch size '+str( self.batch_size)+ " on TF record file " + self.dataset_file)

        callbacks=[ tf.keras.callbacks.ModelCheckpoint(filepath=self.weight_files) ]
        if self.log_path is not None: # Create a TensorBoard callback
             callbacks.append(tf.keras.callbacks.TensorBoard(log_dir= self.log_path,histogram_freq=1,profile_batch='500,520'))


        file_write(join(self.weight_path,"parameters.txt"),self._get_cmd()) #Store the Parameters

        end_file=".txt"

        train_dataset =self.data_loader( MorphoExamples(self.dataset_file + "_train"+end_file, self.mode, self.img_size,self.input_shape, self.output_shape,  self._augmentation,shuffle=True))
        valid_dataset =self.data_loader( MorphoExamples(self.dataset_file + "_valid"+end_file, self.mode, self.img_size, self.input_shape, self.output_shape, self._augmentation,shuffle=True))
        history = self.model.fit(train_dataset,validation_data=valid_dataset,validation_steps=100,initial_epoch=self.epochs_loaded, steps_per_epoch= self.steps_per_epoch, epochs= self.epochs,callbacks=callbacks)



    ##################### COMPUTE OUTPUT ACCURACY
    def _get_fig_name(self,name,epochs=None,ext="png"):
        if epochs is None: epochs=self.epochs_loaded
        return join(self.export_path,"EPOCHS_" + str(epochs),"FusedToSemantic"+ "-" + self.mode + "-" + str(self.img_size) + "-" + self.network+"_"+name+"."+ext)

    def _cell_errorname(self,name):
        error_type_name = {"error_seg_ious": "PRED Semantic",
                       "error_gt_ious": "GT Semantic",
                       "error_plantseg_ious": "PlantSeg",
                       "error_cellpose_ious": "CellPose"}
        if name in error_type_name: return error_type_name[name]
        return name

    def export(self):

        if self.epochs_loaded == 0:
            printi("cannot export anything..")
            return None


        results = []
        to_plot=["age","cell_counter","name"] #t  not used
        if self.mode=="2D": to_plot.append("z")
        what_else=to_plot+["segmented","filename","cellpose4","plantseg"]

        end_file = ".txt"
        self.batch_size=1 #Retrive Only One by one
        test_dataset = MorphoExamples(self.dataset_file + "_test"+end_file, self.mode,
                                      self.img_size, self.input_shape, self.output_shape,
                                      self._augmentation,reverse=False,shuffle=True)
        stop = 200
        if self.mode == "3D":  stop=50

        #stop=len(test_dataset.paths) #TO TEST ALL EXAMPLES
        nb_test=0
        while nb_test<stop:
            image_batch = test_dataset.get_next(what_else=what_else,batch_size=1)
            print(f"{nb_test}/{stop} --> Compute Accuracy for {image_batch['name']}")
            result=self.compute_accuracy(image_batch)
            if result is not None:
                for x in to_plot:
                    if x not in result: result[x]=image_batch[x]
                results.append(result)
            nb_test+=1



        ########################################
        # Write Evaluation Result
        ########################################

        # Write outputfiles with all evaluations
        file_eval = self._get_fig_name("eval", ext="txt")
        f = open(file_eval, 'w')
        errors = {}
        error_types=[]
        for result in results:
            tw=result['name']+";"
            for error_type in result:
                if error_type not in error_types:error_types.append(error_type)
                tw+=error_type+"="+str(result[error_type])+";"
            f.write(tw+ "\n")
        f.close()

        error_str=" -> epochs "+str(self.epochs_loaded)+" : "+str(len(results))+ " tested examples  \n"
        print("\n"+error_str)
        error_types_mean={}
        for error_type in error_types: errors[error_type] = []

        for error_type in error_types:
            if errors[error_type] is not None:
                error_types_mean[error_type]=""
                if len(errors[error_type])>0:
                    error_types_mean[error_type]="        -->" +error_type+" :  Mean "+str(round(np.array(errors[error_type]).mean(),10)) + " --> STD "+str(round(np.array(errors[error_type]).std(),10))+"\n"
                    print(error_types_mean[error_type])


        ########################################
        # PLOT Evaluation Result
        ########################################



        metrics_plot =['er','ap','p','r','iou']
        methods_plot=["gt", "pred", "cp", "ps"]

        legends = {}
        legends['ap'] = "Average Precision"
        legends['er'] = "Error Rate"
        legends['p'] = "Precision"
        legends['r'] = "Recall"
        legends['iou'] = "Intersection over union"
        legends['gt'] = "Semantic Ground Truth"
        legends['pred'] = "Semantic Prediction "
        legends['cp'] = "CellPose"
        legends['ps'] = "PlantSeg"
        legends['age']="Embryo Age"
        legends['z']="z slice"
        legends['name'] = "Embryo Name"
        legends['cell_counter'] = "Number of Cells"
        legends['error_raw'] = "Semantic Prediction Error"
        legends['gt'] = "Semantic Ground Truth"
        legends['pred'] = "Semantic Prediction"
        legends['cp'] = "CellPose"
        legends['ps'] = "PlantSeg"
        for w in methods_plot:
            for mp in metrics_plot:
                legends[w+"_"+mp]=legends[w]+ " "+mp


        ####X AXIS
        figure_types = {}
        figure_types['raw']=to_plot
        figure_types['segmentation']=to_plot
        figure_types['compare'] =metrics_plot

        ####Y AXIS
        yfigure_types={}
        yfigure_types['raw'] = ["error_raw"]
        yfigure_types['segmentation'] = ["pred_er","pred_ap","pred_p","pred_r","pred_iou"]
        yfigure_types['compare'] = methods_plot

        #Count nb of embryos (to color by name)
        embryos=[]
        colors_embryos={}
        from matplotlib.colors import TABLEAU_COLORS as col
        for c in col:
            colors_embryos[len(colors_embryos)]=col[c]
        for result in results:
            if 'name' in result:
                xx = result['name'].split("_fuse")[0]
                if xx not in embryos:
                    embryos.append(xx)


        for figure_type in figure_types:
            print(f" --> Create Figure {figure_type} ")
            nb_x=len(figure_types[figure_type])
            nb_y=len(yfigure_types[figure_type])
            fig, axs = plt.subplots(nb_x, nb_y, figsize=(nb_y*5, nb_x*5))
            fig.suptitle( figure_type+" "+error_str)#+error_types_mean[figure_type])
            fig.subplots_adjust(hspace=0.5)
            case_in_str={}
            x_ax=0
            for xplot in figure_types[figure_type]:
                #print(f" --> Plot X {xplot}")
                y_ax=0
                case_in_str[xplot]={}
                for yplot in yfigure_types[figure_type]:
                    #print(f" -------> Y {yplot}")
                    ax=axs[x_ax,y_ax] if nb_y>1 else axs[x_ax]
                    X = []
                    Y = []
                    colors = []
                    xl = xplot
                    yl = yplot
                    if figure_type == "compare":
                        xl = yplot + "_" + xplot
                        yl = "pred_" + xplot

                    for result in results:
                        if xl in result and result[xl] is not None and yl in result and result[yl] is not None:
                            xx = result[xl]
                            yy = result[yl]
                            if xplot == "name":
                                xx = xx.split("_fuse")[0]  # just keep embryo name
                                if xx not in case_in_str[xplot]:
                                    case_in_str[xplot][xx] = len(case_in_str[xplot])
                                xx = case_in_str[xplot][xx]
                            if type(xx) == str: xx = float(xx)
                            X.append(xx)

                            Y.append(yy)
                            idx_embryo=embryos.index(result['name'].split("_fuse")[0])%len(colors_embryos)
                            colors.append(colors_embryos[idx_embryo])


                    #print(f" --> Plot {xl}={len(X)} with {yl}={len(Y)} ")
                    if len(X)>1:
                        #print(f"X={X}")
                        #print(f"Y={Y}")
                        ax.scatter(X,Y,s=10,color=colors)
                        if len(case_in_str[xplot])>0: #Change axis labels for string
                            x_labels=[]
                            x_ticks=[]
                            for xx in case_in_str[xplot]:
                                x_ticks.append(case_in_str[xplot][xx])
                                x_labels.append(xx)
                            ax.set_xticks(x_ticks)
                            ax.set_xticklabels(x_labels,rotation=45,ha='right')

                        if figure_type=="compare":
                            ax.set_xlim(0, 1)
                            ax.set_ylim(0, 1)
                            ax.plot([0, 1], [0, 1], '-r')
                            ax.set_title(legends[xplot])
                            ax.set(xlabel=legends[yplot], ylabel=legends["pred"])
                        else:
                            for m in metrics_plot:
                                if yl.endswith('_'+m):
                                    ax.set_title(legends[yplot.split("_")[0]])
                                    yl=m
                            ax.set(xlabel=legends[xl], ylabel=legends[yl])

                    y_ax+=1
                x_ax+=1

            print("--> create " + str(self._get_fig_name(figure_type)))
            plt.savefig(self._get_fig_name(figure_type))
            plt.close(fig)

        '''
        #Cell Histograme IOU OVER
        cell_errors_type={}
        for result in results:
            for k in result:
                if k.endswith("_ious"):
                    if k not in cell_errors_type:
                        cell_errors_type[k]=[]
                    cell_errors_type[k]+=list(result[k])

        if len(cell_errors_type)>0:
            fig, axs = plt.subplots(1,  len(cell_errors_type), figsize=( len(cell_errors_type)*4, 5))
            i=0
            max_bins = 0
            for error_type in cell_errors_type:
                bins = histo_iou(axs[i],self._cell_errorname(error_type),cell_errors_type[error_type],with_bar=False)
                max_bins = max(max_bins, bins[0].max())
                i+=1

            i=0
            for error_type in cell_errors_type:
                axs[i].set_ylim(0, max_bins)
                axs[i].plot([1, 1], [0, max_bins], "-r")  # Vertical Bar to separare element
                axs[i].text(1.5, max_bins / 2, 'under')
                axs[i].text(0.3, max_bins / 2, 'over')
                i += 1

            print("--> create " + fig_name.replace('raw.png', 'cellerrors.png'))
            plt.savefig(fig_name.replace('raw.png', 'cellerrors.png'))
            plt.close(fig)

        '''
        #If everything is calculated we can remove  results from previous epochs
        for e in range(self.epochs_loaded-1,0,-1):
            previous_path=join(self.export_path, "EPOCHS_" + str(e))
            if isdir(previous_path):
                execute(" rm -rf "+previous_path)


    def compute_accuracy(self,image_batch,stat_name=True,v=False):
        temp_path = self.export_epochs_path.replace(RESULT, join(SCRATCH, "TEMP_GT"))
        mkdir(temp_path)


        filename= ""
        name = image_batch['name']
        if "filename" in image_batch:
            filename=image_batch['filename']
            name = get_basename(filename)

        ########################################
        # DATA PREPARATION
        ########################################

        cmap = get_glasbey(100000)
        vmin = None
        vmax = None
        cmap_gt = "junctions"

        #print(image_batch)
        ######  RAW DATA
        input_image = image_batch['input']
        if v: print(f"input_image shape={input_image.shape}")

        ###### GROUND TRUTH  SEMANTIC
        output_image = image_batch['output']
        if v: print(f"output_image shape={output_image.shape}")
        if output_image is None: return None

        ###### GROUND TRUTH SEGMENTED
        gt_segmented=None
        if 'segmented' in image_batch:   gt_segmented = image_batch['segmented']
        if v and gt_segmented is not None : print(f"gt_segmented.shape={gt_segmented.shape}")
        if gt_segmented is None: return None

        ###### CELLPOSE
        cellpose = None
        if 'cellpose4' in image_batch:  cellpose = image_batch['cellpose4']
        if v and cellpose is not None : print(f"cellpose.shape={cellpose.shape}")

        ###### PLANTSEG
        plantseg = None
        if 'plantseg' in image_batch:    plantseg = image_batch['plantseg']
        if v and plantseg is not None : print(f"plantseg.shape={plantseg.shape}")

        ###### PREDICTION
        image_predict = self._predict_img(input_image)
        if image_predict is None:
            print(" --> ERROR during prediction")
            return None

        error_raw=np.abs(image_predict - output_image).mean()
        if np.isnan(error_raw):  #Issue somewhere on the prediction
            print(" --> ERROR with predition values "+str(np.unique(image_predict)))
            return None

        if v: print(f"image_predict shape={image_predict.shape}")
        image_predict = np.uint8(np.argmax(image_predict, axis=-1))  # FOR 4 LAYERS (PREDICTED IMAGE)
        if v: print(f"Arg Max image_predict shape={image_predict.shape}")

        predict_segmented = semantic_to_segmentation(image_predict)
        if v: print(f"predict_segmented shape={predict_segmented.shape}")

        output_image = np.uint8(np.argmax(output_image, axis=-1))  # FOR 4 LAYERS (GROUND TRUTH)
        if v: print(f"output_image shape={output_image.shape}")

        output_segmented = semantic_to_segmentation(output_image)
        if v: print(f"output_segmented shape ={output_segmented.shape}")

        ########################################
        # COMPUTE  PERCENTAGE ERROR
        ########################################

        '''imsave('/lustre/fsn1/projects/rech/dhp/uhb36wd/TEMP/TEST/gt_segmented.tiff',gt_segmented)
        imsave('/lustre/fsn1/projects/rech/dhp/uhb36wd/TEMP/TEST/output_segmented.tiff', output_segmented)
        imsave('/lustre/fsn1/projects/rech/dhp/uhb36wd/TEMP/TEST/predict_segmented.tiff', predict_segmented)
        imsave('/lustre/fsn1/projects/rech/dhp/uhb36wd/TEMP/TEST/cellpose.tiff', cellpose)
        imsave('/lustre/fsn1/projects/rech/dhp/uhb36wd/TEMP/TEST/plantseg.tiff', plantseg)'''

        result={}
        result["error_raw"] = error_raw

        #Error Rate, Average Precision , Precision, Recall, IOU, iou_over
        result["gt_er"], result["gt_ap"], result["gt_p"], result["gt_r"], result["gt_iou"] , result["gt_iou_over"] = eval_metrics(gt_segmented, output_segmented)
        result["pred_er"], result["pred_ap"], result["pred_p"], result["pred_r"], result["pred_iou"] , result["pred_iou_over"] = eval_metrics(gt_segmented, predict_segmented)

        if cellpose is not None:
            result["cp_er"], result["cp_ap"],result["cp_p"], result["cp_r"], result["cp_iou"] , result["cp_iou_over"]  = eval_metrics(gt_segmented, cellpose)
        if plantseg is not None:
            result["ps_er"], result["ps_ap"],result["ps_p"], result["ps_r"], result["ps_iou"], result["ps_iou_over"] = eval_metrics( gt_segmented, plantseg)


        print("FusedToSemantic --> " + name + ": "+metricS(result["pred_er"], result["pred_ap"], result["pred_iou"]))


        ########################################
        # PLOT FIGURES
        ########################################
        x_shape = 3 if gt_segmented is not None else 1
        window_size = 5 * x_shape + 2

        y_shape=4
        if cellpose is not None: y_shape += 1
        if plantseg is not None: y_shape += 1

        if self.mode == "3D":
            z = int(round(output_image.shape[2] / 2.0))
            if gt_segmented is not None  :
                #if len(np.unique(gt_segmented[:,:,z]))<5: #Look for the slice with the maximum number of element
                max_elts=0
                best_z=0
                for zi in range(gt_segmented.shape[2]):
                    nb=len(np.unique(gt_segmented[:,:,zi]))
                    if nb>max_elts:
                        max_elts=nb
                        best_z=zi
                if v: print(" --> found best slice at "+str(best_z)+ " with "+str(max_elts)+" elements ")
                z=best_z
                if z<0 or z>=output_image.shape[2]: z = int(round(output_image.shape[2] / 2.0)) #BLACK IMAGES

            if v : print(f" --> EXTRACT Z {z}")

            input_image = get_slice(input_image, z)
            output_image = get_slice(output_image, z)
            image_predict = get_slice(image_predict, z)
            gt_segmented=get_slice(gt_segmented, z)
            output_segmented = get_slice(output_segmented, z)
            predict_segmented = get_slice(predict_segmented, z)
            cellpose = get_slice(cellpose, z)
            plantseg = get_slice(plantseg, z)


        fig, axs = plt.subplots(x_shape, y_shape, figsize=(25, window_size))
        fig.suptitle("FusedToSemantic on epochs:" + str(self.epochs_loaded) + " -> " + name)
        imshow(axs, 0, 0, input_image, "Input")
        imshow(axs, 0, 1, output_image, "GT FusedToSemantic",cmap=cmap_gt,vmin=vmin,vmax=vmax)
        imshow(axs, 0, 2, image_predict, "PRED FusedToSemantic"+ " '(Pixels Error : " + str(error_raw)+")",cmap=cmap_gt,vmin=vmin,vmax=vmax)
        if type(image_predict)!=str and image_predict is not None and output_image is not None:
            imshow(axs, 0, 3, image_predict - output_image, "Difference (GT,PRED)",cmap=cmap_gt,vmin=vmin,vmax=vmax)


        if gt_segmented is not None:
           imshow(axs, 1, 0, gt_segmented, "Gold Truth", cmap=cmap, interpolation=None)
           imshow(axs, 1, 1, re_label(gt_segmented,output_segmented), "GT Semantic \n " + metricS( result["gt_er"], result["gt_ap"], result["gt_iou"] ), cmap=cmap, interpolation=None)
           imshow(axs, 1, 2, re_label(gt_segmented,predict_segmented),  "PRED Semantic \n" + metricS(result["pred_er"], result["pred_ap"], result["pred_iou"]), cmap=cmap, interpolation=None)
           remove_axis(axs, 1, 3)

           iy_shape=3
           if cellpose is not None:
               iy_shape+=1
               imshow(axs, 1, iy_shape, re_label(gt_segmented,cellpose), "CellPose \n"+ metricS(result["cp_er"], result["cp_ap"], result["cp_iou"]), cmap=cmap, interpolation=None)
               remove_axis(axs, 0, iy_shape) #Just to remove the blank panel upper

           if plantseg is not None:
               iy_shape += 1
               imshow(axs, 1, iy_shape, re_label(gt_segmented, plantseg),"PlantSeg \n" + metricS(result["ps_er"], result["ps_ap"], result["ps_iou"]), cmap=cmap, interpolation=None)
               remove_axis(axs, 0, iy_shape)  # Just to remove the blank panel upper

        #####HISTOGRAM FOR IOUS FOR EACH CELLS
        max_bins=0
        remove_axis(axs, 2, 0)

        if gt_segmented is not None:
            bins=histo_iou(axs[2, 1],"IOU Quality ", result["gt_iou_over"],with_bar=False)
            max_bins = max(max_bins, bins[0].max())
            bins=histo_iou(axs[2, 2],"IOU Quality ", result["pred_iou_over"],with_bar=False)
            max_bins = max(max_bins, bins[0].max())

        iy_shape = 3
        if cellpose is not None:
            iy_shape+=1
            bins=histo_iou(axs[2,iy_shape],"IOU Quality " ,result["cp_iou_over"],with_bar=False)
            max_bins = max(max_bins, bins[0].max())
        if plantseg is not None:
            iy_shape+=1
            bins=histo_iou(axs[2, iy_shape],"IOU Quality ", result["ps_iou_over"],with_bar=False)
            max_bins = max(max_bins, bins[0].max())

        for iiy_shape in range(iy_shape+1): #Scale all histogramme to the same scale bar
            if iiy_shape!=3 and iiy_shape!=0:
                axs[2, iiy_shape].set_ylim(0,max_bins)
                axs[2, iiy_shape].plot([1, 1], [0, max_bins], "-r")  # Vertical Bar to separare element
                axs[2, iiy_shape].text(1.5, max_bins / 2, 'under')
                axs[2, iiy_shape].text(0.3, max_bins / 2, 'over')
        remove_axis(axs, 2, 3)

        filenameplot = name + '_compare.png'
        if stat_name and error_raw is not None :  filenameplot=str(round(error_raw, 5)) +"_"+filenameplot
        print(' ->>> Save Figure  To '+join(self.export_epochs_path,filenameplot))
        plt.savefig(join(self.export_epochs_path,filenameplot))
        plt.close(fig)
        result['figname']=filenameplot


        if v :
            for m in result:  print(f" -> {m} == {result[m]}")

        return result



    ##################### PLOT LOSS
    def plot_loss(self, smoothing=0.1):
        filename = join(self.export_epochs_path, self.jobname[len(self.todo)+1:] + "_measure.png")
        if isfile(filename): return True #No need to recompute

        if not isdir(self.log_path):
            printe(" miss log path " + self.log_path)
            return
        if self.epochs_loaded == 0:
            printe(" didnt find any epochs")
            return

        print(" --> plot " + filename)
        self.all_plots = {}
        for step in listdir(self.log_path):  # Train and Valid
            if isdir(join(self.log_path, step)):
                for event_file in listdir(join(self.log_path, step)): #For each events
                    if isfile(join(self.log_path, step, event_file)): #Only files
                        event_name = event_file.split(".")[4]
                        step_tb = get_tb(join(self.log_path, step, event_file))
                        if step not in self.all_plots:  self.all_plots[step] = {}
                        for measure in step_tb:
                             if measure.find("evaluation_")==-1:
                                if measure not in self.all_plots[step]:
                                    self.all_plots[step][measure] = step_tb[measure]
                                else:  # Already in a previous Measure
                                    for x in step_tb[measure]:
                                        self.all_plots[step][measure][x] = step_tb[measure][x]

        #Just some prints:
        '''step="validation"
        measure="epoch_accuracy"
        for x in range(256,317):
            print(f"{step}, {measure} {x}: {self.all_plots[step][measure][x]}")
        quit()
        '''
        # ALL -> 230
        '''
        AT   -> 3497
        rm -f /lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_3D/CONF-Arabidopsis-Thaliana/JUNNET_256/JUNNET_256.35??.h5
        rm -f /lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_3D/CONF-Arabidopsis-Thaliana/JUNNET_256/JUNNET_256.3498.h5
        rm -f /lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_3D/CONF-Arabidopsis-Thaliana/JUNNET_256/JUNNET_256.3499.h5
        '''
        '''
        CE '''
        '''
        LP -> 280
        rm -rf /lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_3D/CONF-LateralRootPrimordia/JUNNET_256/JUNNET_256.3??.h5
        rm -rf /lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_3D/CONF-LateralRootPrimordia/JUNNET_256/JUNNET_256.29?.h5
        rm -rf /lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_3D/CONF-LateralRootPrimordia/JUNNET_256/JUNNET_256.28?.h5
        '''
        '''
        OV -> 348
        rm -rf /lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_3D/CONF-Ovules/JUNNET_256/JUNNET_256.4??.h5
        rm -rf /lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_3D/CONF-Ovules/JUNNET_256/JUNNET_256.39?.h5
        ...
        rm -rf /lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_3D/CONF-Ovules/JUNNET_256/JUNNET_256.35?.h5
        rm -rf /lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_3D/CONF-Ovules/JUNNET_256/JUNNET_256.349.h5
        rm -rf /lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_3D/CONF-Ovules/JUNNET_256/JUNNET_256.348.h5
        '''
        '''
        SS -> 288
        rm -f /lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_3D/CONF-SeaStar/JUNNET_256/JUNNET_256.3??.h5
        rm -f /lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_3D/CONF-SeaStar/JUNNET_256/JUNNET_256.29?.h5
        rm -f /lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_3D/CONF-SeaStar/JUNNET_256/JUNNET_256.289.h5
        '''
        # Get Smoothing Value
        smooth_plots = get_smooth(self.all_plots, smoothing)

        # Now Plot in a figure
        nb_fig = 0
        for step in self.all_plots:
            nb_fig = max(nb_fig, len(self.all_plots[step]))
        fig, axs = plt.subplots(1, nb_fig, figsize=(5 * nb_fig, 7))
        fig.suptitle(self.jobname)
        #Get the last epcohs for all plot
        max_epochs = 0
        for step in self.all_plots:
            for measure in self.all_plots[step]:
                max_epochs = max(max_epochs, np.array(list(self.all_plots[step][measure].keys())).max())
        for step in self.all_plots:
            fig_Y = 0
            for measure in self.all_plots[step]:
                X = []
                Y = []
                S = []
                for x in sorted(self.all_plots[step][measure]):
                    X.append(x)
                    Y.append(self.all_plots[step][measure][x])
                    if smooth_plots is not None:
                        S.append(smooth_plots[step][measure][x])
                axsfig = axs if nb_fig == 1 else axs[fig_Y]
                if smooth_plots is not None:
                    axsfig.plot(X, S, label=step, color=colors[step])
                    axsfig.plot(X, Y, color=colors[step], alpha=0.2)
                else:
                    axsfig.plot(X, Y, label=step, color=colors[step])
                axsfig.legend()
                axsfig.set_title(measure.replace('epoch_', ''))
                axsfig.set_xlim(0,max_epochs) #We resacale everythin plot to the same number of epocs
                fig_Y += 1

        # plt.show()
        mkdir(self.export_epochs_path)
        plt.savefig(filename)
        plt.close(fig)



    ##################### EVAL TEST DATABASE

    def predict_test(self,species_topredict,filenames,patches=True):
        for filename,specie in zip(filenames,species_topredict):
            files=read_txt_file(filename)
            for filename in files:
                output_filename = filename.replace("/GT", "/PD").replace("/membrane/", f"/predict_{self.network}_EPOCHS_{self.epochs_loaded}/").replace(  "_M.tiff", "_PS.tiff")
                #if specie!=self.get_ms():   output_filename=output_filename.replace(specie,self.get_ms())
                if output_filename.find(specie)==-1:
                    first=output_filename.split("/PD_"+str(self.mode)+"/")
                    last=first[1].split("/predict_"+self.network+"_EPOCHS")
                    output_filename =first[0]+"/PD_"+str(self.mode)+"/"+self.get_ms()+"/predict_"+self.network+"_EPOCHS"+last[1]
                if not isfile(filename):
                    print(f"miss input {filename}")
                elif not isfile(output_filename):
                    print(f"Predict {output_filename}")
                    mkdir(dirname(output_filename))
                    image_input=imread(filename)
                    pred_sem=self.predict(image_input,patches=patches)
                    pred_seg=semantic_to_segmentation(pred_sem)
                    imsave(output_filename,pred_seg)


    def eval(self,species_topredict,filenames):
        # SEMANTIC EVALUATION
        for filename, specie in zip(filenames, species_topredict):
            files = read_txt_file(filename)
            for epochs in range(1, self.epochs_loaded + 1):
                txt_filename=join(self.export_path, "EVAL_"+self.network+"_EPOCHS_" + str(epochs)+".txt")
                evals = read_eval_file(txt_filename)
                for f in files:
                    output_filename = f.replace("/GT", "/PD").replace("/membrane/", "/predict_"+self.network+"_EPOCHS_" + str(epochs) + "/").replace("_M.tiff", "_PS.tiff")
                    #if specie!=self.get_ms():   output_filename=output_filename.replace(specie,self.get_ms())
                    if output_filename.find(specie) == -1:
                        first = output_filename.split("/PD_" + str(self.mode) + "/")
                        last = first[1].split("/predict_"+self.network+"_EPOCHS")
                        output_filename = first[0] + "/PD_" + str(
                            self.mode) + "/" + self.get_ms() + "/predict_"+self.network+"_EPOCHS" + last[1]
                    if  output_filename not in evals:
                        if isfile(output_filename):
                            print(f"-> evals semantic prediction {output_filename}")
                            seg_filename = get_correspond_filename(f, "segmented")
                            evals[output_filename] =eval_file(seg_filename,output_filename)
                            print(f"{output_filename} ->{evals[output_filename]}")
                            write_eval_file(txt_filename,evals)
                        #elif not isfile(output_filename):  print(f"miss ouput {output_filename}")
        print("--> all semantic evaluation done")

        # CELLPOSE EVALUATION
        eval_path= join(RESULT,  "NETWORKS_" + str(self.img_size) + "_" + self.mode, self.get_ms())
        for cp_version in [3,4]:

            txt_filename = join(eval_path, f"EVAL_CELLPOSE{cp_version}.txt")
            evals = read_eval_file(txt_filename)
            for filename  in filenames:
                files = read_txt_file(filename)
                for f in files:
                    seg_filename = get_correspond_filename(f, "segmented")
                    output_filename = get_correspond_filename(f, f"cellpose{cp_version}")
                    if not isfile(output_filename):
                        print(f"--> miss {output_filename}")
                    else:
                        print(f"-> evals cellpose prediction {output_filename}")
                        if output_filename not in evals:
                            evals[output_filename] =eval_file(seg_filename,output_filename)
                            print(f"{output_filename} ->{evals[output_filename]}")
                            write_eval_file(txt_filename, evals)
            print("--> all cellpose evaluation done")

        # PLANTSEG EVALUATION
        txt_filename = join(eval_path, "EVAL_PLANTSEG.txt")
        evals = read_eval_file(txt_filename)
        for filename  in filenames:
            files = read_txt_file(filename)
            for f in files:
                seg_filename = get_correspond_filename(f, "segmented")
                output_filename = get_correspond_filename(f, "plantseg")
                if not isfile(output_filename):
                    print(f"--> miss {output_filename}")
                else:
                    print(f"-> evals plantseg prediction {output_filename}")
                    if output_filename not in evals:
                        evals[output_filename] = eval_file(seg_filename, output_filename)
                        print(f"{output_filename} ->{evals[output_filename]}")
                        write_eval_file(txt_filename, evals)
        print("--> all plantseg evaluation done")


    ##################### PREDICTION EXTERNAL FILE

    def predict_files(self,filename,patches=True,remove_zeros=False):
        if not isfile(filename):
            print(f" --> this file {filename} does not exist ...")
            quit()
        for f in open(filename,"r"):
            if not f.startswith("#"):
                tab=f.split(";")
                if len(tab)<3:
                    print(f"Not well define {f} ")
                    print("Should be, input_file,ground_truth_file,spacing")
                    quit()
                input_filename=tab[0]
                if not isfile(input_filename):
                    print(f"--> Miss  image file {input_filename}")
                else:
                    extension=os.path.splitext(input_filename)[1]
                    if extension == ".gz":  extension = os.path.splitext(os.path.splitext(input_filename)[0])[
                                                            1] + extension

                    output_filename = input_filename.replace(extension, f"_{self.network}_EPOCHS_{self.epochs_loaded}_SEG"+extension)
                    output_filename_sem=input_filename.replace(extension, f"_{self.network}_EPOCHS_{self.epochs_loaded}_SEM"+extension)
                    print(f"Predict {output_filename}")
                    #os.system(f"rm -f {output_filename}")
                    if not isfile(output_filename):
                        image_input = imread(input_filename)
                        pred_sem = self.predict(image_input, patches=patches,remove_zeros=remove_zeros)
                        imsave(output_filename_sem, pred_sem)
                        pred_seg = semantic_to_segmentation(pred_sem)
                        imsave(output_filename, pred_seg)

    def eval_files(self,filename):
        methods = ["JUNNET","DUNNET", "CellPose 3", "CellPose 4", "PlantSeg"]
        replacement = {"JUNNET": "S", "DUNNET": "S", "PlantSeg": "PS", "CellPose 3": "CP3", "CellPose 4": "CP4"}

        if not isfile(filename):
            print(f" --> this file {filename} does not exist ...")
            quit()

        eval_path = join(RESULT, "NETWORKS_" + str(self.img_size) + "_" + self.mode, self.get_ms())
        for f in open(filename, "r"):
            if not f.startswith("#"):
                tab = f.split(";")
                if len(tab) < 3:
                    print(f"Not well define {f}")
                    quit()
                input_filename = tab[0]
                print(f"Eval {input_filename}")
                gt_filename = tab[1]
                extension = os.path.splitext(input_filename)[1]
                if extension==".gz":  extension=os.path.splitext(os.path.splitext(input_filename)[0])[1]+extension
                #print(f"Extension {extension}")
                input_path = os.path.dirname(os.path.abspath(input_filename))
                for method in methods:
                    method_name = method.replace(" ", "").lower()
                    print(f" -> with {method}")
                    ouput_filenames = []
                    eval_filenames = []
                    if method.startswith("CellPose") or method.startswith("PlantSeg"):
                        ouput_filenames = [input_filename.replace(extension, f"_" + replacement[method] + extension)]
                        eval_filenames = [f"{eval_path}/EVAL_external_data_{method_name}.txt"]
                    else:
                        for ouput_filename in listdir(input_path):
                            #print(f" -> {ouput_filename} ")
                            #print(ouput_filename.startswith(basename(input_filename).replace(extension, f"_{method}_EPOCHS_")))
                            #print(ouput_filename.endswith("_SEG"+extension))
                            if ouput_filename.startswith(basename(input_filename).replace(extension, f"_{method}_EPOCHS_")) and ouput_filename.endswith("_SEG"+extension):

                                ouput_filenames.append(join(input_path,ouput_filename))
                                epochs=ouput_filename.split("_")[-2] #045_img_DUNNET_EPOCHS_3578_SEG.png
                                print(f" ---> epochs={epochs}")
                                eval_filenames.append(f"{eval_path}/EVAL_external_data_{method}_EPOCHS_{epochs}.txt")
                    #print(ouput_filenames)
                    for ouput_filename,eval_filename in zip(ouput_filenames,eval_filenames):
                        if isfile(ouput_filename):
                            evals = read_eval_file(eval_filename)  # READ PREVIOUS EVALUATION
                            if input_filename not in evals:
                                evaluation = eval_file(gt_filename, ouput_filename)
                                print(f"Evaluating {method} for {input_filename} -> {evaluation}")
                                evals[input_filename] = evaluation
                                write_eval_file(eval_filename, evals) #WRITE RESULT
                            else:
                                print(f"Evaluation done {method} for {input_filename} -> {evals[input_filename]}")
                        else:
                            print(f"Miss  image file {ouput_filename}")



    ##################### PREDICTION
    def _predict_img(self,image_input): #INTERNAL PREDICTION FOR IMAGES
        image_predict = self.model.predict(np.reshape(image_input, (1,)+self.input_shape))
        return image_predict[0,...]

    def predict(self, im, patches=False,remove_zeros=False):
        if not patches:
            return self.predict_full(im,remove_zeros=remove_zeros)
        else:
            return self.predict_patches(im,remove_zeros=remove_zeros)


    def predict_full(self,image_input,remove_zeros=False):
        original_shape = image_input.shape
        if self.mode=="3D":
            image_input = resize(image_input, [self.img_size, self.img_size, self.img_size], preserve_range=True).astype(image_input.dtype)
        else:
            image_input = resize(image_input, [self.img_size, self.img_size],  preserve_range=True).astype(image_input.dtype)
        output = self._predict_img(normalize(image_input,clip=True,remove_zeros=remove_zeros))
        output = np.uint8(np.argmax(output, axis=-1))
        output = resize(output, original_shape, preserve_range=True,order=0).astype(output.dtype)
        return output

    def predict_patches(self,image_input,remove_zeros=False):
        #print(f"Predict with patches")
        #When one of the dimension is lower than the patch, we increase the size
        image_shape=np.array(image_input.shape)
        #print(f"image_shape: {image_shape}")
        new_shape=np.array(image_input.shape)
        dim=int(self.mode[0])
        patches_shape=np.array(self.input_shape[0:dim])
        if (np.array(image_input.shape) <patches_shape).any():
            new_shape[np.array(image_input.shape)<patches_shape] =self.img_size
            print(f"--> the image is too small ({image_input.shape}) for patches , resize to {new_shape}")
            image_input=resize(image_input,new_shape,preserve_range=True).astype(image_input.dtype)

        image_input=normalize(image_input,clip=True,remove_zeros=remove_zeros)

        # PREDICT TILES
        predict_shape = image_input.shape[0:dim] + (self.output_shape[-1],)
        image_predict = np.zeros(predict_shape, dtype=np.float32)
        print(f"--> predict shape {predict_shape} with patches {self.img_size}")
        nb_image_predict = np.ones(predict_shape, dtype=np.uint16)
        borders = get_gaussian(self.img_size, mode=self.mode, shape=self.output_shape)
        slidingWindow = int(round(self.img_size / 2))

        if dim==3:
            nbTotal = float(len(range(0, image_input.shape[0], slidingWindow)) * len(range(0, image_input.shape[1], slidingWindow)) * len(range(0, image_input.shape[2], slidingWindow)))
            with tqdm(total=nbTotal, desc=f"Predict {self.mode} from tiles") as pbar:
                for x in range(0, image_input.shape[0], slidingWindow):
                    for y in range(0, image_input.shape[1], slidingWindow):
                        for z in range(0, image_input.shape[2], slidingWindow):
                            bx, ex = get_border(x, x + self.img_size, image_input.shape[0])
                            by, ey = get_border(y, y + self.img_size, image_input.shape[1])
                            bz, ez = get_border(z, z + self.img_size, image_input.shape[2])
                            input = image_input[bx:ex, by:ey, bz:ez, ...]
                            original_shape=input.shape
                            if original_shape[0]<self.img_size or original_shape[1]<self.img_size  or original_shape[2]<self.img_size : #Need To Resize Image
                                input = resize(input, [self.img_size, self.img_size, self.img_size], preserve_range=True).astype(input.dtype)
                                if ex-bx>  original_shape[0]:ex=original_shape[0]
                                if ey-by > original_shape[1]: ey = original_shape[1]
                                if ez-bz > original_shape[2]: ez = original_shape[2]
                            patch_predict = self.model.predict(np.reshape(input, (1,) + self.input_shape), verbose=0)
                            patch_predict=patch_predict[0, ...]* borders
                            borders_reshape=borders
                            if original_shape[0] < self.img_size or original_shape[1] < self.img_size or original_shape[2] < self.img_size:  # Need To Resize Image
                                patch_predict = resize(patch_predict, original_shape+ (self.output_shape[-1],), preserve_range=True).astype(patch_predict.dtype)
                                borders_reshape = resize(borders, original_shape ,preserve_range=True).astype(borders.dtype)

                            image_predict[bx:ex, by:ey, bz:ez] +=patch_predict
                            nb_image_predict[bx:ex, by:ey, bz:ez] += borders_reshape
                            pbar.update(1)

        elif dim == 2:
            nbTotal = float(len(range(0, image_input.shape[0], slidingWindow)) * len(   range(0, image_input.shape[1], slidingWindow)) )
            with tqdm(total=nbTotal, desc=f"Predict {self.mode} from tiles") as pbar:
                for x in range(0, image_input.shape[0], slidingWindow):
                    for y in range(0, image_input.shape[1], slidingWindow):
                            bx, ex = get_border(x, x + self.img_size, image_input.shape[0])
                            by, ey = get_border(y, y + self.img_size, image_input.shape[1])
                            input = image_input[bx:ex, by:ey, ...]
                            original_shape = input.shape
                            if original_shape[0] < self.img_size or original_shape[1] < self.img_size:  # Need To Resize Image
                                input = resize(input, [self.img_size, self.img_size],  preserve_range=True).astype(input.dtype)
                                if ex - bx > original_shape[0]: ex = original_shape[0]
                                if ey - by > original_shape[1]: ey = original_shape[1]
                            patch_predict = self.model.predict(np.reshape(input, (1,) + self.input_shape), verbose=0)
                            patch_predict = patch_predict[0, ...] * borders
                            borders_reshape = borders
                            if original_shape[0] < self.img_size or original_shape[1] < self.img_size :  # Need To Resize Image
                                patch_predict = resize(patch_predict, original_shape + (self.output_shape[-1],),  preserve_range=True).astype(patch_predict.dtype)
                                borders_reshape = resize(borders, original_shape, preserve_range=True).astype(borders_reshape.dtype)

                            image_predict[bx:ex, by:ey] += patch_predict
                            nb_image_predict[bx:ex, by:ey] += borders_reshape
                            pbar.update(1)

        image_predict /= nb_image_predict
        del nb_image_predict
        del image_input
        image_predict = np.uint8(np.argmax(image_predict, axis=-1))

        if (image_shape!=np.array(image_predict.shape)).any():
            print(f"--> resize image to orignal size {image_shape})")
            image_predict = resize(image_predict, image_shape, preserve_range=True,order=0).astype(image_predict.dtype)

        return image_predict



if __name__ == '__main__':
    mm = MorphoModel()
    mm.parse()
