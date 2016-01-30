import os
import urllib
import time
import sys
import ftplib
from contextlib import closing
import threading
import os
import tarfile

global done
done = False

def progress_print(filename, size_to_dl):
    global done
    this_file_start = time.time()
    while not done:
        percent = (os.path.getsize(filename)/float(size_to_dl))
        rows, columns = os.popen('stty size', 'r').read().split()
        barLengthMax = int(int(columns)/2)
        pleft = int(percent*(barLengthMax))
        pright = barLengthMax-pleft
        #print(pleft,pright, barLengthMax)
        sys.stdout.write("\r{0}% [ {1}>{2} ] {3} seconds elapsed".format('%.2f'%(percent*100),'='*pleft, " "*pright, '%.2f'%(time.time()-this_file_start)))
        sys.stdout.flush()
    sys.stdout.write("\r{0}% [ {1}{2} ] {3} seconds elapsed".format('%.2f'%(100),'='*(pleft+pright), " "*0, '%.2f'%(time.time()-this_file_start)))
    print("\nDownloading {0} finished...".format(filename))

def download(urls, extract_tar=True):
    global done
    for url in urls:
        done = False
        print("Downloading {0}".format(url))
        with closing(ftplib.FTP()) as ftp:

            local_filename = url.split('/')[-1]
            local_filename_folder = ".".join(local_filename.split('.')[:-2])
            print(local_filename_folder)
            ftp_filename = '/'+"/".join(url.split('/')[3:])


            ftp.connect('ftp.ncbi.nlm.nih.gov', 21, 30*5) #5 mins timeout
            ftp.login('', '')
            ftp.set_pasv(True)
            ftp.sendcmd("TYPE i")
            ftp_size = ftp.size(ftp_filename)


            with open(local_filename, 'w+b') as f:
                t1 = threading.Thread(target=progress_print, args=(url.split('/')[-1], ftp_size))
                t1.start()
                res = ftp.retrbinary('RETR '+ftp_filename, f.write)
                done = True
                t1.join()

                #IF FAILURE
                if not res.startswith('226 Transfer complete'):
                    print('Download of file {0} failed...'.format(local_filename))
                    os.remove(local_filename)
                elif extract_tar:
                    print("Extracting {0} to {1}!".format(local_filename, local_filename_folder))
                    local_filename_folder = local_filename_folder
                    tfile = tarfile.open(local_filename)
                    if not os.path.exists(local_filename):
                        os.makedirs(local_filename)
                    tfile.extractall('./'+local_filename_folder+"/")
                    print("Extraction done...")

if __name__ == "__main__":
    print("Started download-script")
    dl_time = time.time()
    urls = [
        'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/articles.txt.0-9A-B.tar.gz',
        'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/articles.txt.C-H.tar.gz',
        'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/articles.txt.I-N.tar.gz',
        'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/articles.txt.O-Z.tar.gz'
    ]

    download(urls, False)
    print("Done in {0} seconds...".format('%.2f')%(time.time()-dl_time))
