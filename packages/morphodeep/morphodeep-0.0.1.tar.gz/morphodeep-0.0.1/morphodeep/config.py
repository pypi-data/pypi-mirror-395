
from os.path import join

from morphodeep.DataManagement.extract_Arabidopsis import extract_Arabidopsis
from morphodeep.DataManagement.extract_CElegans import extract_CElegans_data
from morphodeep.DataManagement.extract_CellPose import extract_Cellpose_data
from morphodeep.DataManagement.extract_Phallusia import extract_Phallusia_data
from morphodeep.DataManagement.extract_PlantSeg import extract_PlantSeg_data
from morphodeep.DataManagement.predict_cellpose import predict_cellpose, predict_cellpose_files
from morphodeep.DataManagement.extract_SeaStar import extract_SeaStar_data
from morphodeep.DataManagement.predict_plantseg import predict_plantseg, predict_plantseg_files
from morphodeep.paths import WORK, SCRATCH, STORE, RESULT, EXE, plantseg_path, arabidopsis_path, phallusia_path, \
    seastar_path, cellpose_path, celegans_path
from morphodeep.tools.setdata import generate_paths
from morphodeep.tools.ground_truth import ground_truth, job_ground_truths, extract_2D
from morphodeep.tools.utils import launch_job_gpu, get_job_id, get_specie, launch_job_cpu
import argparse


class Config:
    def __init__(self,*args, **kwargs):

        self._init_var()
        self.kwargs=kwargs

        # SET DEFAULT PARAMETERS
        self.parser = argparse.ArgumentParser()

        # JOBS
        self._set_arg("job", help='Launch the corresponding job ')
        self._set_arg("exe", help="Execute directly the method ( used inside job for ground_truth, etc .. )")
        # JOBS ARRAY
        self._set_arg("job_number", short="ja", help='Launch a sepecif job in job array list')
        self._set_arg("job_filename", short="jaf", help='The file of the job array list')


        # TRAINING
        self._set_arg('train', help='Launch the training')
        self._set_arg("batch_size", short="b", default=20, help="batch_size")
        self._set_arg("steps_per_epoch", short="s", default=1000, help="steps_per_epoch")
        self._set_arg("epochs", short="e", default=10000, help="number of epochs")
        self._set_arg("log_path", short="lo", help="log path for tensorboard")
        self._set_arg('augmentation', default=True,help='Use Data Augmentation ? Default is True')
        self._set_arg('pondere', help='Keep only the worst element (10%) for training ')
        self._set_arg("export_path", short="ep", help="The export path for the results")
        self._set_arg("network", short="n", default="JUNNET", help="which network architecture to use")

        # OPTIONS
        self._set_arg("mode", short="t", default="3D", help="2D or 3D")
        self._set_arg("img_size", short="i", default=256, help="image size")
        self._set_arg("weight_files", short="w", help="weight files")

        #ANALYSIS RESULT
        self._set_arg("export", help='Compute the testing set and plot the results in figures')
        self._set_arg("eval", help='Evaluation of testing database ')
        self._set_arg("plot", help='Compute export and plot loss')
        self._set_arg("plot_loss", help='Plot the loss and accuracy')


        #PREDICTION
        self._set_arg('predict', help='Launch the prediction')
        self._set_arg('predict_test', help='Launch the prediction of the test data')
        self._set_arg('predict_files', help='Launch the prediction for a given txt file')
        self._set_arg('filename', short="f", help='filename to predict')
        self._set_arg('eval_files', help='Launch the evaluation for a given txt file')
        self._set_arg('patches', help='Predict Using Patches')
        self._set_arg("input_file", short="if", help="Input Filename to predict")
        self._set_arg("output_file", short="of", help="Output Filename of the predicted image")
        self._set_arg("remove_zeros",  help="when you have a new empty background at 0 after registration")

        #DATABASE PREPARATION
        self._set_arg("plantseg_data", help='Download and Prepare plant dataset')
        self._set_arg("seastar_data", help='Download and Prepare Sea Star')
        self._set_arg("arabidopsis_data", help='Download and Prepare Arabidopsis dataset')
        self._set_arg("cellpose_data", help='Download and Prepare Cellpose dataset')
        self._set_arg("phallusia_data", help='Download and Prepare Phallusia dataset')
        self._set_arg("celegans_data", help='Download and Caenorhabditis elegans dataset')
        self._set_arg("extract_2D", help='Extract 2D images from the 3D DB')

        #OTHER MODELS
        self._set_arg("predict_cellpose", help='Predict Cell Pose On Test Data')
        self._set_arg("predict_cellpose_files", help='Predict CellPose for a given txt file')
        self._set_arg("predict_plantseg", help='Predict PlantSeg On Test Data')
        self._set_arg("predict_plantseg_files", help='Predict PlantSeg for a given txt file')
        self._set_arg("what", short="wh", default=None, help='test/train/eval')


        # MICROSCOPIE AND SPECIES
        self._set_arg("specie", short="sp", default="all",help="which specie ? (PM,DR,AT,DM,all")
        self._set_arg("microscope", short="mo", default="ALL", help="which microscope ? (SPIM (for lightsheet), CONF (for confocal),ALL (for both))")

        # GROUND TRUTH
        self._set_arg("ground_truth", help='Generate all the ground truth')
        self._set_arg("input_path", short="ip", help="Input Path (depend on the called method )") #Other than automaticlly specified
        self._set_arg("output_path", short="op", help="Output Path (depend on the called method ") #Other than automaticlly specified

        # SPLIT DATABSE IN TRAIN/PRED/VALID
        self._set_arg("setdata", help='Generate the data list files used for train/test/predict ')
        self._set_arg("dataset_file", short="o", help="Dataset File without .train, .valid and .test")
        self._set_arg('test_split', short="ts", default=0.10,help="Float between 0 and 1. Fraction of the data to be used as test data.")
        self._set_arg('validation_split', short="vs", default=0.10,help="Float between 0 and 1. Fraction of the data to be used as validate data.")

        #ADD OTHER ARGS DIRECTLTY CALL FROM THE FUNCTION
        execute=False
        for name in self.kwargs:
            if name=="process" or name=="parse":
                execute=True
            else:
                try:
                    if eval("type(self._" + name + ") is bool"):
                        self._set(name, self.kwargs.get(name), True)
                        if self.kwargs.get(name): #If one action is true we have to execute the process
                            execute=True
                except:
                    self._set(name,self.kwargs.get(name),False)

        if execute or self._job:
            self.parse()
        else:
            self._complete_args()

    def _init_var(self):
        self.params=[] #List of all parameters
        self.validation_split = None
        self.test_split=None
        self._plot = None
        self._plot_loss = None
        self._predict_test=None
        self._predict_files=None
        self._eval_files=None
        self._eval = None
        self._export = None
        self._predict = None
        self._patches = None
        self._ground_truth = None
        self._extract_2D=None
        self._job = None
        self._train = None
        self.job_number = None
        self.job_filename = None
        self.dataset_file=None
        self._setdata = None
        self._phallusia_data = None
        self._augmentation = None
        self._pondere=None
        self.mode = None
        self.network = None
        self.specie = None
        self.microscope=None
        self.img_size = None
        self.batch_size = None
        self.steps_per_epoch=None
        self.output_segmented=None
        self.predict_segmented=None
        self.input_file=None
        self.output_file=None
        self.epochs=None
        self.log_path=None
        self._exe=None
        self.filename=None
        self._plantseg_data=None
        self._remove_zeros=None
        self._seastar_data=None
        self._arabidopsis_data=None
        self._celegans_data = None
        self._cellpose_data=None
        self._predict_cellpose = None
        self._predict_cellpose_files=None
        self._predict_plantseg_files=None
        self.what=None
        self._predict_plantseg=None

    def _set(self, name, default, action):
        if name not in self.params:
            self.params.append(name)
        if action:
            v = False if default == "" or default == "False" or default == False else True
            exec('self._' + name + "="+str(v))
        else:
            dtype = type(default)
            try:
                if eval('self.'+name+' is not None'):
                    dtype=eval('type(self.'+name+')')
            except:
                dtype = type(default)

            if dtype is str:
                exec('self.' + name + "='" + default + "'")
            else:
                exec('self.' + name + "=" + str(default))

    def _set_arg(self, name, short=None, default=None, help=""):
        if default is None:
            default = ""
        if short is not None:
            self.parser.add_argument("-" + short, '--' + name, default=default, help=help)
            self._set(name, default, False)
        else:
            self.parser.add_argument('--' + name, default=default, help=help, action='store_true')
            self._set(name, default,True)

    def get_ms(self):
        return self.microscope + "-" +get_specie(self.specie)

    def combine_path(self,path,One=True):
        if One:
            return join(path,self.get_ms())
        else:
            all_paths = []
            for ms in self.get_ms():
                all_paths.append(join(path, ms))
            return all_paths

    def path_gt(self,One=True): #GROUND TRUTH PATH
        return self.combine_path(join(SCRATCH, "Semantic", "GT_" + self.mode), One=One)

    def path_pd(self,One=True): #PREDICTION PATH (For CellPose or PlantSeg)
        return self.combine_path(join(SCRATCH, "Semantic",  "PD_" + self.mode), One=One)

    def path_networks(self,One=True):
        return  self.combine_path(join(WORK, "Semantic", "NETWORKS_" + str(self.img_size) + "_" + self.mode), One=One)

    def _complete_args(self):
        '''
        Complete all empty args
        '''
        self._set_todo() #Set Default Values


        # TRAIN / TEST FILE
        if self.dataset_file == "": self.dataset_file = join(self.path_networks(), "tf")


        ########################
        # ACTION
        ########################

        # PREPARE DATASET
        if self._phallusia_data :
            if self.input_path == "":  self.input_path = phallusia_path
            if self.output_path == "": self.output_path = self.path_gt()

        if self._plantseg_data :
            if self.input_path == "":  self.input_path =plantseg_path
            if self.output_path == "": self.output_path = self.path_gt()

        if self._seastar_data :
            if self.input_path == "":  self.input_path =seastar_path
            if self.output_path == "": self.output_path = self.path_gt()

        if self._arabidopsis_data:
            if self.input_path == "": self.input_path=arabidopsis_path
            if self.output_path == "": self.output_path = self.path_gt()

        if self._celegans_data:
            if self.input_path == "": self.input_path=celegans_path
            if self.output_path == "": self.output_path = self.path_gt()

        if self._cellpose_data:
            if self.input_path == "": self.input_path=cellpose_path
            if self.output_path == "": self.output_path=self.path_gt()

        # GENERATE VARIOUS GROUND TRUTH  FROM PREPARRED DATA
        if self._ground_truth:
            if self.input_path == "":  self.input_path =self.path_gt()
            if self.output_path == "": self.output_path = self.path_gt()

        # EXTRACT 3D TO 2D
        if self._extract_2D:
            if self.input_path == "": self.input_path = self.dataset_file

        # CREATE TEST/TRAIN/PREDICT TXT FILES
        if self._setdata:
            if self.input_path == "": self.input_path =self.path_gt(One=True)
            if self.output_path == "": self.output_path = self.dataset_file

        #CELL POSE PATHS
        if self._predict_cellpose:
            if self.input_path == "": self.input_path = self.dataset_file
            if self.output_path == "": self.output_path = self.path_pd()
            if self.what is None or self.what=="": self.what="test"
            self.jobname="CellPose4_"+str(self.get_ms())

        #PLANT SEG PATH
        if self._predict_plantseg:
            if self.what is None or self.what=="": self.what="test"
            if self.input_path == "": self.input_path = self.dataset_file
            if self.output_path == "": self.output_path = self.path_pd()

        # AUTOMATIC DATA AUGMENTATION
        # WORK PATH
        self.file_path = self.path_networks()
        self.weight_path= join(self.file_path, self.network+"_" + str(self.img_size))

        #WEIGHT FILES
        if self.weight_files == "":
            self.weight_files = join(self.weight_path, self.network+"_" + str(self.img_size)  + '.{epoch:02d}.h5')

        #TENSORBOARD LOG
        if self.log_path == "":  # To Visualize result launch the command : tensorboard --logdir <log>
            self.log_path = join(self.weight_path, 'LOG')

        #EXPORT PATH
        if self.export_path == "":
            self.export_path = join(RESULT,  "NETWORKS_" + str(self.img_size) + "_" + self.mode, self.get_ms(), self.network+"_" + str(self.img_size) )

        # JOB NAME
        self.jobname = "Semantic" + self.microscope+"_"+self.specie+"_" + self.mode + "_" + self.network+"_" + str( self.img_size)
        if not self._train and self.todo != "":  self.jobname = self.todo + "-" + self.jobname


    def parse(self):
        args = self.parser.parse_args()
        self.vargs = vars(args)
        for name in self.vargs:
            if name not in self.kwargs: #Priority give on the args defined in the function
                try:
                    if eval("type(self._"+name+") is bool"):
                        self._set(name,self.vargs[name],True)
                except:
                    self._set(name,self.vargs[name],False)
        self._complete_args()

        if self._exe:
            self.process()
        else:
            self.jobs()

    def _set_todo(self):
        self.todo=""
        if self._extract_2D:
            self.todo="extract_2D"
        if self._ground_truth:
            self.todo = "ground_truth"
        if self._setdata:
            self.todo = "setdata"
        if self._train:
            self.todo ="train"
        if self._predict:
            self.todo ="predict"
        if self._export:
            self.todo ="export"
        if self._eval:
            self.todo="eval"
        if self._plot:
            self.todo ="plot"
        if self._plot_loss:
            self.todo ="plot_loss"
        if self._predict_test:
            self.todo ="predict_test"
        if self._predict_files:
            self.todo="predict_files"
        if self._eval_files:
            self.todo="eval_files"
        if self._plantseg_data:
            self.todo="plantseg_data"
        if self._seastar_data:
            self.todo="seastar_data"
        if self._predict_cellpose:
            self.todo="predict_cellpose"
        if self._predict_cellpose_files:
            self.todo="predict_cellpose_files"
        if self._predict_plantseg:
            self.todo="predict_plantseg"
        if self._predict_plantseg_files:
            self.todo="predict_plantseg_files"

    def _get_cmd(self):
        # common_cmd = get_cmd(vargs)
        common_cmd =join(EXE, 'morphodeep.py')
        for name in self.params:
            if name!="job":
                try:
                    if eval("self._" + name): #Action to perform
                        common_cmd += " --" + str(name)
                except:
                    if eval("self." + name)!="": #Skip Empty Parameters
                        common_cmd += " --" + str(name) + " " + str(eval("self." + name))

        return common_cmd

    def jobs(self):   # RUN THE JOBS
        #print("---> job ")
        common_cmd =self._get_cmd()+" --exe "
        if self._ground_truth:
            job_ground_truths(common_cmd,self.mode,self.input_path,self.microscope,self.specie,not self._job)
        elif self._setdata:
            self.process()
        else:  # TRAIN, PREDICT ..
            long = False
            # memory 0 v100-16g ou v100-32g
            # memory 1 v100-32g
            # memory 2 a100
            memory = 1
            if self.mode == "3D" and (self.network=="DUNNET" or self.network=="RESDUNET"):  memory=2
            if self._plot or  self._plot_loss:
                launch_job_cpu(self.jobname, cmd=common_cmd,launch=not self._job,cpus_per_task=10,prepost=True,tensorflow_load=True)
            else :
                launch_job_gpu(self.jobname, memory=memory, long=long, cmd=common_cmd,launch=not self._job)

    def process(self): #PERFORM THE ACTION
        print("---> process ")
        if self._ground_truth:
            if self.job_number is not None and  self.job_number!="" and self.job_filename is not None and  self.job_filename!="" : #JOB ARRAY
                input_file,input_method=get_job_id(self.job_filename ,self.job_number ).split(";")
                ground_truth(input_method, input_file)
        elif self._extract_2D:
            extract_2D(self.input_path,self.what)
        elif self._setdata:
            generate_paths(self.specie,self.microscope,self.input_path, self.output_path,self.test_split, self.validation_split)
        elif self._phallusia_data:
            extract_Phallusia_data( self.input_path, gt_path=self.output_path)
        elif self._plantseg_data:
            extract_PlantSeg_data(self.get_ms(), self.input_path,gt_path=self.output_path)
        elif self._seastar_data:
            extract_SeaStar_data(self.input_path, gt_path=self.output_path)
        elif self._arabidopsis_data:
            extract_Arabidopsis(self.input_path, gt_path=self.output_path)
        elif self._cellpose_data:
            extract_Cellpose_data(self.get_ms(), self.input_path, gt_path=self.output_path)
        elif self._celegans_data:
            extract_CElegans_data( self.input_path, gt_path=self.output_path)
        elif self._predict_cellpose:
            predict_cellpose(self.specie,self.input_path,self.mode,self.what) #output path is automaclliy define
        elif self._predict_cellpose_files:
            predict_cellpose_files(self.filename)
        elif self._predict_plantseg:
            predict_plantseg(self.specie,self.input_path,self.what) #output path is automaclliy define
        elif self._predict_plantseg_files:
            predict_plantseg_files(self.filename)
        else: #Directly called from process  in morphomodel TRAIN, PREDICT,EXPORT, PLOT  etc ...
            return False
        return True




