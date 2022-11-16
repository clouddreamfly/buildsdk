#!/usr/bin/python
#-*-coding:utf8-*-


import os
import json
import threading
import Tkinter 
import tkFileDialog
import tkMessageBox
import shutil
import sitecustomize



class Json(object) : 

    """json read write"""
    
    def __init__(self):
        
        self.json_data = {}


    def read(self, path):
        """json file read"""

        try:
            fp = open(path,'r')
        except:
            print("open json file error!\n")
            return False
            
        with fp:
            try:
                check_bom = fp.read(3)
                if check_bom == '\xef\xbb\xbf':
                    fp.seek(3)
                else:
                    fp.seek(0)
                self.json_data = json.load(fp, "utf-8")
            except Exception, e:
                print(e)
                print("json file read error!\n")
                return False

        return True        
        

    def write(self, path):
        """json file read"""

        if self.json_data == None or len(self.json_data) == 0:
            return False

        try:
            fp = open(path,'w')
        except:
            print("open json file error!\n")
            return False
            
        with fp:
            try:
                json.dump(self.json_data,fp,indent=4,separators=(',',': '))
            except:
                print("json file write error!\n")
                return False
                
        return True
    
    
    

class BuildSdk(object) :  

    def __init__(self):
        
        self.bulid_sdk_dir = os.getcwdu() 
        self.bulid_sdk_config_file = "buildsdk.json"
        self.sdk_info = { "include":[], "lib":[], "include_ex":[], "lib_ex":[], "include_dir":".", "lib_dir":".", "target_dir":"."}
        self.dlg = Tkinter.Tk()
        self.dlg.title(u"生成SDK")
        self.dlg.geometry('%dx%d+%d+%d'%(580, 430, (self.dlg.winfo_screenwidth()-580)/2, (self.dlg.winfo_screenheight()-430)/2))
        self.dlg.minsize(580, 430)
        self.dlg.maxsize(580, 430)
        self.sdk_build = False
        self.thread = None
        
        #画布1
        self.paned1 = Tkinter.PanedWindow(self.dlg, orient=Tkinter.HORIZONTAL) 
        self.paned1.pack(expand=Tkinter.TRUE, fill=Tkinter.BOTH)
         
        self.paned1_1 = Tkinter.PanedWindow(self.paned1, orient=Tkinter.VERTICAL) 
        self.paned1_1.pack(expand=Tkinter.TRUE, fill=Tkinter.BOTH)       
        self.paned1_2 = Tkinter.PanedWindow(self.paned1, orient=Tkinter.VERTICAL) 
        self.paned1_2.pack(expand=Tkinter.TRUE, fill=Tkinter.BOTH)            
         
        self.paned1.add(self.paned1_1)  
        self.paned1.add(self.paned1_2)    
        
        #头文件
        label = Tkinter.Label(self.paned1_1, text=u"头文件：")
        self.paned1_1.add(label)
    
        self.frame1 = Tkinter.Frame(self.paned1_1)   
        self.frame1_sb = Tkinter.Scrollbar(self.frame1)
        self.frame1_sb.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
        self.frame1_list_box = Tkinter.Listbox(self.frame1, width=40, height=6)
        self.frame1_list_box.pack(side=Tkinter.LEFT, expand=Tkinter.TRUE, fill=Tkinter.BOTH)
        self.paned1_1.add(self.frame1)
        
        self.frame1_list_box.configure(yscrollcommand = self.frame1_sb.set)
        self.frame1_sb["command"] = self.frame1_list_box.yview       
        
        #库文件
        label = Tkinter.Label(self.paned1_2, text=u"库文件：")
        self.paned1_2.add(label)        
    
        self.frame2 = Tkinter.Frame(self.paned1_2)  
        self.frame2_sb = Tkinter.Scrollbar(self.frame2)
        self.frame2_sb.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
        self.frame2_list_box = Tkinter.Listbox(self.frame2, width=50, height=6)
        self.frame2_list_box.pack(side=Tkinter.RIGHT, expand=Tkinter.TRUE, fill=Tkinter.BOTH)
        self.paned1_2.add(self.frame2)   
    
        self.frame2_list_box.configure(yscrollcommand = self.frame2_sb.set)
        self.frame2_sb["command"] = self.frame2_list_box.yview            
        
        #画布2
        self.paned2 = Tkinter.PanedWindow(self.dlg, orient=Tkinter.VERTICAL) 
        self.paned2.pack(expand=Tkinter.TRUE, fill=Tkinter.BOTH)  
    
        #信息输出
        label = Tkinter.Label(self.paned2, text=u"信息输出：")
        self.paned2.add(label)        
    
        self.frame3 = Tkinter.Frame(self.paned2)  
        self.frame3_sb = Tkinter.Scrollbar(self.frame3)
        self.frame3_sb.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)        
        self.frame3_text = Tkinter.Text(self.frame3, width=1024, height=6)
        self.frame3_text.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH)
        self.paned2.add(self.frame3)   
        
        self.frame3_text.configure(yscrollcommand = self.frame3_sb.set)
        self.frame3_sb["command"] = self.frame3_text.yview          
        
        #画布3
        self.paned3 = Tkinter.PanedWindow(self.dlg, orient=Tkinter.VERTICAL)  
        self.paned3.pack()
        
        self.paned3_1 = Tkinter.PanedWindow(self.paned3, orient=Tkinter.HORIZONTAL)  
        self.paned3_1.pack()        
        self.paned3_2 = Tkinter.PanedWindow(self.paned3, orient=Tkinter.HORIZONTAL)  
        self.paned3_2.pack()
        self.paned3_3 = Tkinter.PanedWindow(self.paned3, orient=Tkinter.HORIZONTAL)  
        self.paned3_3.pack()          
        
        self.paned3.add(self.paned3_1)
        self.paned3.add(self.paned3_2)
        self.paned3.add(self.paned3_3)
        
        #头文件路径
        label = Tkinter.Label(self.paned3_1, text=u"头文件路径：")
        self.enter_include_path = Tkinter.Entry(self.paned3_1, width=50)
        self.btn_include_path = Tkinter.Button(self.paned3_1, text=u"浏览", command=self.OnBtnIncludePath)
        self.paned3_1.add(label)
        self.paned3_1.add(self.enter_include_path)
        self.paned3_1.add(self.btn_include_path)
        
        #库文件路径
        label = Tkinter.Label(self.paned3_2, text=u"库文件路径：")   
        self.enter_lib_path = Tkinter.Entry(self.paned3_2, width=50)
        self.btn_lib_path = Tkinter.Button(self.paned3_2, text=u"浏览", command=self.OnBtnLibPath)
        self.paned3_2.add(label)
        self.paned3_2.add(self.enter_lib_path)
        self.paned3_2.add(self.btn_lib_path)
        
        #生成的路径
        label = Tkinter.Label(self.paned3_3, text=u"生成的路径：")    
        self.enter_build_path = Tkinter.Entry(self.paned3_3, width=50)   
        self.btn_build_path = Tkinter.Button(self.paned3_3, text=u"浏览", command=self.OnBtnBuildPath)
        self.paned3_3.add(label)
        self.paned3_3.add(self.enter_build_path)
        self.paned3_3.add(self.btn_build_path)
        
        #生成
        self.btn_build = Tkinter.Button(self.dlg, text=u"生成", command=self.OnBtnBuild)
        self.btn_build.pack(pady=4, ipadx=40)
        
        self.OnReadJsonConfig()
        self.OnShowIncludeFile()
        self.OnShowLibFile()
        
        self.enter_include_path.insert(0,  self.sdk_info["include_dir"])
        self.enter_lib_path.insert(0,  self.sdk_info["lib_dir"])
        self.enter_build_path.insert(0,  self.sdk_info["target_dir"])
        
        self.enter_include_path["state"] = "readonly"
        self.enter_lib_path["state"] = "readonly"
        self.enter_build_path["state"] = "readonly" 
        
    def OnReadJsonConfig(self):
        
        bulid_sdk_path = os.path.join(self.bulid_sdk_dir, self.bulid_sdk_config_file)
        json = Json()
        if not json.read(bulid_sdk_path) :
            tkMessageBox.showinfo(u"提示", u"读取生成SDK配置：%s错误..."%(self.bulid_sdk_config_file))
        else:
            self.sdk_info["include"] = json.json_data["include"]
            self.sdk_info["include_ex"] = json.json_data["include_ex"]
            self.sdk_info["lib"] = json.json_data["lib"]
            self.sdk_info["lib_ex"] = json.json_data["lib_ex"]
            self.sdk_info["include_dir"] = json.json_data["include_dir"]
            self.sdk_info["lib_dir"] = json.json_data["lib_dir"]
            self.sdk_info["target_dir"] = json.json_data["target_dir"]
        
    def OnShowIncludeFile(self):
        
        self.frame1_list_box.delete(0, Tkinter.END)
            
        for file_name in self.sdk_info["include"]:
            self.frame1_list_box.insert(Tkinter.END, file_name)
        
    def OnShowLibFile(self):
        
        self.frame2_list_box.delete(0, Tkinter.END)
            
        for file_name in self.sdk_info["lib"]:
            self.frame2_list_box.insert(Tkinter.END, file_name)
        

    def run(self):
        
        self.dlg.mainloop()
        self.OnExit()
        
    def OnBtnIncludePath(self):
        
        select_dir = tkFileDialog.askdirectory()
        self.enter_include_path["state"] = "normal"
        self.enter_include_path.delete(0, Tkinter.END)
        self.enter_include_path.insert(0, select_dir) 
        self.enter_include_path["state"] = "readonly"
    
    def OnBtnLibPath(self):
        
        select_dir = tkFileDialog.askdirectory()
        self.enter_lib_path["state"] = "normal"
        self.enter_lib_path.delete(0, Tkinter.END)
        self.enter_lib_path.insert(0, select_dir) 
        self.enter_lib_path["state"] = "readonly"
    
    def OnBtnBuildPath(self):
        
        select_dir = tkFileDialog.askdirectory()
        self.enter_build_path["state"] = "normal"
        self.enter_build_path.delete(0, Tkinter.END)
        self.enter_build_path.insert(0, select_dir)   
        self.enter_build_path["state"] = "readonly"

    def OnBtnBuild(self):
        
        if not self.sdk_build:
            self.sdk_build = True
            
            self.include_dir = self.enter_include_path.get()
            self.lib_dir = self.enter_lib_path.get()
            self.target_dir = self.enter_build_path.get()            
            self.thread_quit = False
            self.thread_lock = threading.RLock()
            self.thread = threading.Thread(target=self.OnThreadBuild)
            self.thread.start()
            
            self.btn_build["state"] = Tkinter.DISABLED
            self.frame3_text.delete('1.0', Tkinter.END)
         
        else:
            tkMessageBox.showinfo(u"提示", u"SDK 正在生成中...")
        
    
    def Log(self, text):
    
        if text is not None and len(text) > 0:
            self.frame3_text.insert(Tkinter.END, text)  
            self.frame3_text.see(Tkinter.END)
            print(text.strip('\n'))
        
        
    def OnThreadBuild(self):
        
        quit = False
        finish = False
        sdk_include = self.sdk_info["include"]
        sdk_include_ex = self.sdk_info["include_ex"]
        sdk_lib = self.sdk_info["lib"]
        sdk_lib_ex = self.sdk_info["lib_ex"]
        include_dir = self.include_dir
        lib_dir = self.lib_dir
        target_dir = self.target_dir
        current_dir = self.bulid_sdk_dir  
        
        while True: 
            
            self.thread_lock.acquire()
            if self.thread_quit == True: quit = True
            self.thread_lock.release()
            
            if quit == True:
                break
            
            # 拷贝文件
            #include 
            include_path = os.path.join(current_dir, include_dir)
            target_include_path = os.path.join(current_dir, target_dir, "Include")
            if not os.path.exists(target_include_path) : 
                os.makedirs(target_include_path)

            for include_file_name in sdk_include :
                src_path = os.path.join(include_path, include_file_name)
                if not os.path.exists(src_path) :
                    self.Log(u"复制文件：%s 不存在！！！\n"%(include_file_name))
                    ret = False #tkMessageBox.askokcancel(u"提示", u"复制的文件 %s 不存在！！！ 是否同意继续复制？"%(include_file_name))
                    if ret != True :
                        quit = True
                        break  
                else:
                    file_name = os.path.basename(include_file_name)               
                    target_path = os.path.join(target_include_path, file_name)
                    try:
                        shutil.copy(src_path, target_path)
                        
                        old_lines = None
                        with open(target_path, "r") as fr:
                            old_lines = fr.readlines()
                        
                        is_replace = False 
                        lines = 0
                        for old_line in old_lines:
                            pos = old_line.find("#include")
                            if pos != -1:
                                pos1 = old_line.find("\"")
                                pos2 = old_line.rfind("\\")
                                #if pos2 == -1: pos2 = old_line.rfind("/")
                                if pos1 != -1 and pos2 != -1 :
                                    is_replace = True
                                    new_line = old_line[0 : pos1 + 1] + old_line[pos2 + 1 :]
                                    old_lines[lines] = new_line
                                    
                            lines += 1
                                    
                        if is_replace == True :
                            with open(target_path + ".bak", "w") as fw:
                                fw.writelines(old_lines)     
                            
                            os.remove(target_path)
                            os.rename(target_path + ".bak", target_path)
        
                        self.Log(u"复制文件：%s\n"%(include_file_name))  
           
                    except Exception, e:
                        self.Log(u"处理异常：%s\n"%(e.message))
                        quit = True
                        break            
            
            if quit == True:
                break              
            
            #include ex
            include_path = os.path.join(current_dir, include_dir)
            target_include_path = os.path.join(current_dir, target_dir, "Include")
            if not os.path.exists(target_include_path) : 
                os.makedirs(target_include_path)

            for include_file_name in sdk_include_ex :
                src_path = os.path.join(include_path, include_file_name)
                if not os.path.exists(src_path) :
                    self.Log(u"复制文件：%s 不存在！！！\n"%(include_file_name))
                    ret = False #tkMessageBox.askokcancel(u"提示", u"复制的文件 %s 不存在！！！ 是否同意继续复制？"%(include_file_name))
                    if ret != True :
                        quit = True
                        break  
                else:
                    dir_name = os.path.dirname(include_file_name)
                    if not os.path.exists(dir_name) :
                        os.makedirs(dir_name)
                    
                    target_path = os.path.join(target_include_path, include_file_name)
                    try:
                        shutil.copy(src_path, target_path)
                        self.Log(u"复制文件：%s\n"%(include_file_name))  
                    except Exception, e:
                        self.Log(u"处理异常：%s\n"%(e.message))
                        quit = True
                        break            
            
            if quit == True:
                break            
            
            #lib
            lib_path = os.path.join(current_dir, lib_dir)
            target_lib_path = os.path.join(current_dir, target_dir, "Lib")
            if not os.path.exists(target_lib_path) : 
                os.makedirs(target_lib_path)

            for lib_file_name in sdk_lib :
                src_path = os.path.join(lib_path, lib_file_name)
                if not os.path.exists(src_path) :
                    self.Log(u"复制文件：%s 不存在！！！\n"%(lib_file_name))
                    ret = False #tkMessageBox.askokcancel(u"提示", u"复制的文件 %s 不存在！！！ 是否同意继续复制？"%(lib_file_name))
                    if ret != True :
                        quit = True
                        break  
                else:
                    file_name = os.path.basename(lib_file_name)
                    target_path = os.path.join(target_lib_path, file_name)
                    try:
                        shutil.copy(src_path, target_path)
                        self.Log(u"复制文件：%s\n"%(lib_file_name))  
                    except Exception, e:
                        self.Log(u"处理异常：%s\n"%(e.message))
                        quit = True
                        break
            
            if quit == True:
                break   
            
            #lib ex
            lib_path = os.path.join(current_dir, lib_dir)
            target_lib_path = os.path.join(current_dir, target_dir, "Lib")
            if not os.path.exists(target_lib_path) : 
                os.makedirs(target_lib_path)

            for lib_file_name in sdk_lib_ex :
                src_path = os.path.join(lib_path, lib_file_name)
                if not os.path.exists(src_path) :
                    self.Log(u"复制文件：%s 不存在！！！\n"%(lib_file_name))
                    ret = False #tkMessageBox.askokcancel(u"提示", u"复制的文件 %s 不存在！！！ 是否同意继续复制？"%(lib_file_name))
                    if ret != True :
                        quit = True
                        break  
                else:
                    dir_name = os.path.dirname(lib_file_name)
                    if not os.path.exists(dir_name) :
                        os.makedirs(dir_name)
                    
                    target_path = os.path.join(target_lib_path, lib_file_name)
                    try:
                        shutil.copy(src_path, target_path)
                        self.Log(u"复制文件：%s\n"%(lib_file_name))
                    except Exception, e:
                        self.Log(u"处理异常：%s\n"%(e.message))
                        quit = True
                        break            
            
            if quit == True:
                break   
                    
            finish = True
            break
    
        if finish == True:
            self.thread_lock.acquire()
            self.sdk_build = False
            self.btn_build["state"] = Tkinter.NORMAL
            self.thread_lock.release()
            self.Log(u"SDK 生成完成.....\n")
            
        if quit == True :
            self.thread_lock.acquire()
            self.sdk_build = False
            self.btn_build["state"] = Tkinter.NORMAL
            self.thread_lock.release()            
            self.Log(u"SDK 生成中断.....\n")
        
    
    def OnExit(self):
        
        if self.thread != None :
            self.thread_lock.acquire()
            self.thread_quit = True
            self.thread_lock.release()        
            self.thread.join()
    

def main():
    
    """software start runing """
    
    app = BuildSdk()
    app.run()


if __name__=="__main__":
    
    main()