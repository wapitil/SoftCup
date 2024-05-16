import os 

for root,subdirs,files in os.walk(r'imgs'):
    print('root:',root)
    print('dirs:',subdirs)
    print('files:',files)
    print('\n')