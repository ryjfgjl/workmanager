from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = "F:\\Python37\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "F:\\Python37\\tcl\\tk8.6"

# Dependencies are automatically detected, but it might need
# fine tuning.
base = None
# 判断Windows系统  
#if sys.platform == 'win32':  
#    base = 'Win32GUI'  
  
#packages = ["os", "idna", "numpy", "pymysql", "pandas"]
packages = ["os", "numpy", "pymysql", "pandas"]
  
for dbmodule in ['win32gui','win32api' ,'win32con' , 'cx_Freeze']:
  
    try:  
  
        __import__(dbmodule)  
  
    except ImportError:  
  
        pass  
  
    else:  
        packages.append(dbmodule)  
  
  
options = {  
                'build_exe':   
                        {  
                             'includes': 'atexit'  
                             # 依赖的包  
                             ,"packages": packages
                             # 额外添加的文件  
                             , 'include_files': ['reference_files', 'config.ini', 'events', 'common', 'tools']
                            }  
                  
                }  
  
executables = [  
                        Executable(  
                                        # 工程的 入口   
                                        'interface.py'
                                        , base=base  
                                        # 生成 的文件 名字  
                                        , targetName = 'Work Manager.exe'
                                        # 生成的EXE的图标  
                                       , icon = 'cream.ico' #图标, 32*32px
                                        )  
                    ]  
  
setup(  
            # 产品名称  
           name='workmanager',
            # 版本号  
            version='2.3',
            # 产品说明  
            description='workmanager',
            options=options,  
            executables=executables  
      )  

