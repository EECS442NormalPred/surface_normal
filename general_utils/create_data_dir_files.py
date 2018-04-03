f = open('test_files_dir', 'w')
for i in range(2000):
    f.write('/home/ubuntu/eecs442challenge/test_resize/color/{}\n'.format(i))
f.close()

f = open('train_files_dir', 'w')
for i in range(20000):
    f.write('/home/ubuntu/eecs442challenge/train_resize/color/{}\n'.format(i))
f.close()
