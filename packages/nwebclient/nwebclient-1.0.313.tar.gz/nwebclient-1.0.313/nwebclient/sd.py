from nwebclient import sdb
from nwebclient import ticker
from nwebclient import runner
import json
import os
import os.path
import requests
import time
import base64

# Stable Diffusion Imports in ImageGen::__init__

class ImageGen:
    """
    python -m nwebclient.sd
    from nwebclient import sd
    ig = sd.ImageGen()
    ig.prompt = "photo"
    ig.loop(5)
  
    ig.executeFromUrl('https://...')
    """
    generator = 'diffusers' # diffusers or automatic1111 dummy cn_pose_1111 diffcn
    # scheduler
    pipe = None
    prompt = "photo"
    negative_prompt = "text, cartoon, anime, drawing, meme, postcard, painting, ((fuzzy)), ((blurred)), ((low resolution)), ((b&w)), ((monochrome)), ambiguous, ((deformed)), oversaturated, ((out of shot)), ((incoherent)), (((glitched))), (((3d render))), cgi, ((incorrect anatomy)), bad hands, lowres, long body, ((blurry)), double, ((duplicate body parts)), (disfigured), (extra limbs), fused fingers, extra fingers, malformed hands, ((((mutated hands and fingers)))), conjoined, ((missing limbs)), logo, signature, mutated, jpeg artifacts, low quality, bad eyes, oversized, disproportionate, (((incorrect proportions))), exaggerated, (((aliasing)))"
    guidance_scale = 7.5
    num_inference_steps=15
    height=800
    width=640
    num_images=1
    prefix = 'sd'
    dbfile='data.db'
    # sdb jpg
    save_mode='sdb'
    loaded_model = None
    gen_count = 0
    api = None
    cn_image = None
    diff_cn = None
    loop_count = 25
    a11_default = {}
    ssl_verify = False
    verbose = False
    def __init__(self, model_id="XpucT/Deliberate"):
        self.model_id = model_id
    def load(self):
        if self.loaded_model == self.model_id or self.generator == 'automatic1111':
            return
        self.info("Loading Stable Diffusion Dependencies...");
        from diffusers import PNDMScheduler, DDIMScheduler, LMSDiscreteScheduler, EulerDiscreteScheduler, DPMSolverMultistepScheduler
        from diffusers import UniPCMultistepScheduler
        import torch
        from diffusers import StableDiffusionPipeline
        from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
        self.scheduler = DPMSolverMultistepScheduler.from_pretrained(self.model_id, subfolder="scheduler")
        device = "cuda"
        model_revision = None
        if self.scheduler is None:
           self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, torch_dtype=torch.float16, revision=model_revision)
        else:
           self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, scheduler=self.scheduler,  torch_dtype=torch.float16, revision=model_revision, custom_pipeline="lpw_stable_diffusion")
        self.pipe = self.pipe.to(device)
        if self.model_id=="XpucT/Deliberate" or self.model_id == "SG161222/Realistic_Vision_V1.4_Fantasy.ai":
            self.pipe.safety_checker = lambda images, clip_input: (images, False)
        self.load_model = self.model_id
    def initA1111(self):
        import webuiapi
        if self.api is None:
            self.api = webuiapi.WebUIApi(sampler='DPM++ SDE Karras', steps=self.num_inference_steps)
    def initDiffCn(self):
        if self.diff_cn is None:
            self.controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-openpose")#, ) lllyasviel/sd-controlnet-canny
            self.diff_cn = StableDiffusionControlNetPipeline.from_pretrained(model_id, controlnet=controlnet) # , torch_dtype=torch.float16
            self.diff_cn.scheduler = UniPCMultistepScheduler.from_config(controlnet_pipe.scheduler.config)
            self.diff_cn.enable_model_cpu_offload()
            #controlnet_pipe.enable_xformers_memory_efficient_attention()
            self.diff_cn = self.diff_cn.to("cuda")
            if self.model_id=="XpucT/Deliberate" or self.model_id == "SG161222/Realistic_Vision_V1.4_Fantasy.ai":
                self.diff_cn.safety_checker = lambda images, clip_input: (images, False)
    def gen(self, loop_number=1):
        if self.generator == 'diffusers':
            self.genDiffusers(loop_number)
        elif self.generator == 'automatic1111':
            self.genA1111(loop_number)
        elif self.generator == 'cn_pose_1111':
            self.genA1111(loop_number)
        elif self.generator == 'diffcn':
            self.genDiffCn(loop_number)
        elif self.generator == 'dummy':
            time.sleep(1)
            print("Dummy Generation; " + str(loop_number))
            self.gen_count = self.gen_count + 1
        if self.gen_count%100 == 0:
            self.info("gen_count: " + str(self.gen_count))
    def genDiffCn(self, loop_number=1):
        self.initDiffCn()
        output= self.diff_cn(self.prompt, self.cn_image, negative_prompt=self.negative_prompt, num_inference_steps=25, num_images_per_prompt = 1, height = self.height, width = self.width)
        self.save_image(output[0][0], 0,loop_number)
        self.gen_count = self.gen_count + 1
    def genCnPose1111(self, loop_number=1):
        self.initA1111();
        result = self.api.txt2img(prompt=self.prompt,negative_prompt=self.negative_prompt, height=self.height, width=self.width, controlnet_units=[self.cn_image],cfg_scale=self.guidance_scale)
        self.save_image(result.image, 0,loop_number)
        self.gen_count = self.gen_count + 1
    def genA1111(self, loop_number=1):  
        self.initA1111();
        if self.model_id.endswith('.safetensors') and self.model_id != self.loaded_model:
             self.a1111setModel(self.model_id)
        params = self.a11_default.copy()
        params['prompt'] = self.prompt
        params['negative_prompt']=self.negative_prompt
        params['height']=self.height
        params['width']=self.width
        params['cfg_scale']=self.guidance_scale
        #result = self.api.txt2img(prompt=self.prompt,negative_prompt=self.negative_prompt, height=self.height, width=self.width, cfg_scale=self.guidance_scale)
        self.v(params)
        result = self.api.txt2img(**params)
        self.v(result.info) # .info .parameter
        self.save_image(result.image, 0, loop_number, result.info)
        self.gen_count = self.gen_count + 1
    def genDiffusers(self, loop_number=1):
        if self.pipe is None:
            self.load()
        images = self.pipe(self.prompt,
            height = self.height,
            width = self.width,
            num_inference_steps = self.num_inference_steps,      # higher better quali default=45
            guidance_scale = self.guidance_scale,                # Prioritize creativity  7.5  Prioritize prompt (higher)
            num_images_per_prompt = self.num_images,
            negative_prompt = self.negative_prompt,
        ).images
        self.gen_count = self.gen_count + 1
        for i in range(len(images)):
            #  images[i].save(prefix+str(i)+".jpg")
            self.save_image(images[i], i, loop_number)
    def save_image(self, image, i, loop_number, extra_data = None):
        if self.save_mode == 'sdb':
            sdb.sdb_write_pil(image, self.prompt, self.negative_prompt, self.guidance_scale, self.prefix, self.dbfile, extra_data)
        if self.save_mode == 'jpg':
            image.save(self.prefix+'_'+str(loop_number)+'_'+str(i)+'.jpg')
    def loop(self, count=6):
        self.loop_count = count
        for i in range(count):
            print("Loop "+str(i)+"/"+str(count))
            self.gen(loop_number=i)
    def execute(self, data):
        if "type" in data:
            t = data['type']
            if t == 'sdjobs':
                return self.executeJobs(data)
            elif t != 'sdjob':
                return data
        if "pb" in data:
            data['prompt'] = str(base64.b64decode(data['pb']))
        if "nb" in data:
            self.negative_prompt =  str(base64.b64decode(data['nb']))
        if "negative_prompt" in data:
            self.negative_prompt = data['negative_prompt']
        if "prefix" in data:
            self.prefix = data['prefix']
        if "guidance_scale" in data:
            self.guidance_scale = float(data['guidance_scale'])
        if "height" in data:
            self.height = int(data['height'])
        if "width" in data:
            self.width = int(data['width'])
        if "generator" in data:
            self.generator = data['generator']
        if "model" in data and data['model'] != 'default':
            self.model_id = data['model']
            self.info("Using model: " + data['model'])
            self.load()
        if "num_inference_steps" in data:
            self.num_inference_steps = int(data["num_inference_steps"])
        if "hires" in data and data['hires']=='1':
            self.a11_default['enable_hr']=True
            self.a11_default['hr_scale']=2
            self.a11_default['hr_upscaler']= 'Latent' #webuiapi.HiResUpscaler.Latent,
            self.a11_default['hr_second_pass_steps']=10
        if "hires" in data and data['hires']=='0':
            self.a11_default.pop('enable_hr', False)
            self.a11_default.pop('hr_scale', False)
            self.a11_default.pop('hr_upscaler', False)
            self.a11_default.pop('hr_second_pass_steps', False)
        self.v("Prefix: " + self.prefix)
        count = 10
        res = {}
        if "count" in data:
            count = int(data['count'])
        if "prompt" in data:
            self.prompt = data['prompt']
            self.loop(count)
            res = {'success': True}
        elif "jobs" in data:
            for job in data["jobs"]:
                self.execute(job)
            res = {'success': True}
        else:
            msg = "Unknown SD-Job"
            self.info(msg)
            self.info("Jobs-Keys: " + str(data.keys()))
            return {'success': False, 'message': msg, 'data': data}
        if "result_url" in data:
            self.uploadWork(data['result_url'], data)
        return res
    def executeJsonFile(self, file, delete=True):
        try:
            data = json.load(open(file))
            self.execute(data)
            if delete:
                os.remove(file)
        except Exception as e:
            self.info("Error: " + str(e))
            self.info("Faild to execute JSON-File "+str(file))
    def executeMany(self, data, count = 50):
        for key in data:
            self.prompt = data[key]
            self.prefix = key
            self.loop(count)
    def uploadWork(self, result_url, data, removeSdb=True):
        if result_url.startswith('http') and os.path.isfile('data.db'):
            self.info("Uploading...")
            with open('data.db', 'rb') as upfile:
                files = {'upload_file': upfile}
                params = {'name': data['worker_name'], 'g': data['group_id']}
                res = requests.post(result_url, params=params, files=files, verify=self.ssl_verify)
                if len(res.text) < 2000:
                    print(res.text)
            if removeSdb:
                self.removeData()
    def removeData(self):
        os.remove('data.db')
    def executeJobs(self, data):
        """
          data: {jobs:{...}, result_url:'', upload_after_job:0|1}
        """
        self.info("Start: "+time.strftime("%Y-%m-%d, %H:%M:%S", time.localtime()))
        if "verbose" in data and data["verbose"]=="1":
            self.verbose = True
        jobs = data['jobs']
        i = 0
        for job in jobs:
            self.info("Job " + str(i) + "/" + str(len(jobs)) )
            self.execute(job)
            i=i+1
            if 'upload_after_job' in data and data['upload_after_job']=='1':
                self.uploadWork(data['result_url'], data)    
        self.uploadWork(data['result_url'], data)
        self.info("End: "+time.strftime("%Y-%m-%d, %H:%M:%S", time.localtime()))
        return i
    def executeFromUrl(self, url, askForMore= True, ssl_verify = None):
        if not ssl_verify is None:
            self.ssl_verify = ssl_verify
        res = requests.get(url, verify=self.ssl_verify)
        try:
            data = json.loads(res.text)
        except:
            self.info("Error: JSON Decode Error");
            self.info(res.text)
            self.info("Error: JSON Decode Error");
            return 0
        i = self.executeJobs(data)
        if i > 0 and askForMore:
            self.info('Asking for more Work')
            i = i + self.executeFromUrl(url, True)
        elif i == 0 and askForMore:
            self.info("Nothing to do.");
            time.sleep(120)
            self.info("Asking again");
            i = i + self.executeFromUrl(url, True)
        return i
    def info(self, message):
        print("[INFO] " + str(message))
    def v(self, message):
        if self.verbose:
            print("[INFO] " + str(message))
    def a1111models(self):
        self.initA1111();
        result = self.api.util_get_model_names()
        return result
    def a1111setModel(self,model):
        self.info("Automatic1111: Load model")
        self.initA1111();
        options = {}
        options['sd_model_checkpoint'] = model # 'model.ckpt [7460a6fa]'
        self.loaded_model = model
        self.api.set_options(options)
    def __str__(self):
        return f'ImageGen {self.generator} {self.model_id} {self.prefix}'
    def __repr__(self):
        return f'ImageGen(generator=\'{self.generator}\', model_id=\'{self.model_id}\', prefix=\'{self.prefix}\')'
    def __call__(self, prefix, prompt=None):
        if not prompt is None:
            self.prompt = prompt
        if isinstance(prefix, str):
            self.prefix = prefix
            self.loop(self.loop_count)
            return "ImageGen"
        else:
            self.execute(prefix)
    def toSdJob(self, count=50, model = None, file = None):
        data = {'prefix':self.prefix, 'prompt':self.prompt, 'count':count, 'height': self.height, 'width':self.width}
        if not model is None:
            data['model'] = model
            self.prefix = self.prefix + '_' + model[0:4]
        if not file is None:
            text = json.dumps(data)
            with open(self.prefix +'.sdjob', 'w') as f:
                f.write(text)
        return data
    def p(self, prompt, append = False):
        if append:
            self.prompt = self.prompt + ' ' + prompt
        else:
            self.prompt = prompt
        return self
    def pb(self, prompt_b, append = False):
        self.p(str(base64.b64decode(prompt_b)), append)
        
class ImageGenProcess(ticker.FileExtObserver):
    ext = ".sdjob"
    def __init__(self, generator=None):
        if generator is None:
            generator = ImageGen()
        self.generator = generator
    def processFile(self, filename):
        self.generator.executeJsonFile(filename)
    def configure(self, arg):
        self.generator.generator = arg
class JobFetch(ticker.Ticker):
    """ 
      JobFetch(NWebClient(...), 42)  
      
      npy-ticker nwebclient.sd.JobFetch:42
    """
    key = None
    def __init__(self, nwebclient=None, group=None):
        super().__init__("jobfetch",60*60*23) 
        self.nweb = nwebclient
        self.group = group
    def configure(self, arg):
        from nwebclient import NWebClient
        self.nweb = NWebClient()
        self.group = arg
    def execute(self):
        docs = self.nweb.docs('group_id='+str(self.group))
        for doc in docs:
            self.download(doc)
    def decrypt(self, file):
        from cryptography.fernet import Fernet
        fernet = Fernet(self.key)
        with open(file, 'rb') as f:
            original = f.read()
        encrypted = fernet.decrypt(original)
        with open(file, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
    def download(self, doc):
        self.log("Start Download")
        file = str(doc.id()) + '.sdjob'
        doc.save(file)
        if not self.key is None:
            self.decrypt(file)
        self.nweb.deleteDoc(doc.id())
    def log(self, message):
        print("JobFetch: "+str(message))
class SdbUpload(ticker.Ticker):
    key = None
    filename = 'data.db'
    def __init__(self, nwebclient=None, group=None, minSize = None):
        super().__init__("jobfetch",60*60*23) 
        from nwebclient import crypt
        from cryptography.fernet import Fernet
        self.nweb = nwebclient
        self.group = group
        self.minSize = minSize
    def execute(self):
        self.log("Execute")
        if os.path.isfile(self.filename) and self.isBigEnough(self.filename):
            self.upload(self.filename)
    def log(self, message):
        print("SdbUpload: "+str(message))
    def isBigEnough(self, file):
        if self.minSize == None:
            return True
        else:
            file_stats = os.stat(file)
            return file_stats.st_size > self.minSize
    def prepare(self, jobs):
        self.info("Prepare Jobs.")        
    def upload(self, file, remove = True):
        self.log("Uploading")
        if not self.key is None:
            fernet = Fernet(self.key)
            with open(file, 'rb') as f:
                original = f.read()
            encrypted = fernet.encrypt(original)
            with open(file, 'wb') as encrypted_file:
                encrypted_file.write(encrypted)
        self.nweb.createFileDoc('result', self.group, open(file, 'rb'))
        if remove:
            os.remove(file)
            
   
class InterrogateJob(runner.ImageExecutor):
    def __init__(self):
        self.ig = ImageGen()
        self.ig.generator = 'automatic1111'
        self.ig.initA1111()
    def executeImage(self, image, data):
        result= self.ig.api.interrogate(image)
        print(result.info)
        data['prompt'] = result.info
        return data

            
if __name__ == '__main__':
    print("SD")