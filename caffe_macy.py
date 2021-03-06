import caffe
import numpy as np
import glob
import os
import pandas as pd


def batch_images(image_path, batch_size):
	images = glob.glob(image_path + '/*jpg')
	for i in xrange(0, len(images), batch_size):
		print "now working on images %d through %d" %(i,i+batch_size)
		yield images[i:i+batch_size]

def extract_labels_features(images, counter, topk=5):
	net.blobs['data'].data[...] = map(lambda x: transformer.preprocess('data',caffe.io.load_image(x)), images)
	out = net.forward()

	idxpreds = np.argsort(-out['prob'], axis=1)
	fc7 = net.blobs['fc7']
	labels = []

	for i,j in enumerate(idxpreds):
		labels.append([images[i]])

	labels = np.array(labels)
	features_with_labels = np.column_stack((labels, fc7.data))
	df = pd.DataFrame(features_with_labels)
	df.to_csv('%s_macy_features_with_labels_%d.csv'%(model,counter),index=False,header=False)

def load_model(batchsize):
	caffe.set_mode_cpu()
	# setup net with ( structure definition file ) + ( caffemodel ), in test mode
	#net = caffe.Net('/home/ubuntu/caffe/models/%s/deploy.prototxt'%model,
				#   '/home/ubuntu/caffe/models/%s/%s.caffemodel'%(model,model), 
				 #   caffe.TEST)
	caffe_root = '../'
        model_def = caffe_root + 'models/bvlc_alexnet/deploy.prototxt'
        model_weights=caffe_root +'models/bvlc_alexnet/bvlc_alexnet.caffemodel'
        net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)


	# add preprocessing
	transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
	transformer.set_transpose('data', (2,0,1)) # height*width*channel -> channel*height*width
	mean_file = np.array([105.908874512, 114.063842773, 116.282836914]) 
	transformer.set_mean('data', mean_file) #### subtract mean ####
	transformer.set_raw_scale('data', 255) # pixel value range
	transformer.set_channel_swap('data', (2,1,0)) 
	if model.split('_')[0] == 'alexnet':
		net.blobs['data'].reshape(50,3,227,227)
		
	else: net.blobs['data'].reshape(50,3,224,224)
	# set test batchsize
	data_blob_shape = net.blobs['data'].data.shape
	data_blob_shape = list(data_blob_shape)
	net.blobs['data'].reshape(batchsize, data_blob_shape[1], data_blob_shape[2], data_blob_shape[3])
	return net, transformer

batchsize = 25
image_path = '/home/ryan/Dato_Proj/Macy/pics'
model = 'alexnet'
counter = 0
net, transformer = load_model(25)
failed = []



for images in batch_images(image_path,batchsize):
	counter+=1
	try:
		extract_labels_features(images, counter)
		print counter
	except:
		failed.append(images)
		print "failed on counter: %d" %counter
		continue
