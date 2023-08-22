import os
import platform
import shutil


####################################################################################################
def gen_exe():
    print('Start to generate, Please wait...\n\n')

    working_dir, _ = os.path.split(os.path.abspath(__file__))
    os.chdir(working_dir)
    py_file = 'excel2pdf.py'
    py_file_full = os.path.join(working_dir, py_file)
    ico_file = os.path.join(working_dir, 'icon', 'excel2pdf.ico')
    if not os.path.isfile(py_file_full):
        print(f'\nCan not find the entry py file [{py_file_full}]')
        os._exit(-1)
    if not os.path.isfile(ico_file):
        print(f'\nCan not find the ico file [{ico_file}]')
        os._exit(-1)

    cmd = rf'C:\Users\wangx\AppData\Local\Programs\Python\Python39\Scripts\pyinstaller.exe -F {py_file_full} -n s2p.exe -i {ico_file} --distpath=.'
    os.system(cmd)

    print('\n\nDone.')


####################################################################################################


if __name__ == '__main__':
    gen_exe()
