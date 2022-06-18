# Доделать
# from __future__ import print_function
# import argparse

# import os
# import torch
# from torch.autograd import Variable
# from torch.utils.data import DataLoader
# from rbpn import Net as RBPN
# from data import get_test_set
# import numpy as np
# import utils
# import time
# import cv2
# import math
# import logger










# # этим заменить содержимое файла iSeeBetterTest.py




# # /content/iSeeBetter-pytorch/weights/RBPN_2x.pth
# # /content/iSeeBetter-pytorch/weights/netG_epoch_4_1_FullDataSet.pth
# # Training settings


# parser.add_argument('--future_frame', type=bool, default=True, help="Use future frame")



# gpus_list=range(1)
# chop_forward   = True 
# model_type     = 'RBPN'
# data_dir       = 'uploads/video/'
# nFrames        = 7
# upscale_factor = 2
# file_list      = 'uploads/video/' # указать нормальный
# other_dataset  = True
# future_frame   = True
# upscale_only   = True
# threads        = 1
# batch_size     = 1
# debug          = False
# model          = "weights/RBPN_2x.pth"
# output         = 'result/'

# test_set = get_test_set(data_dir, nFrames, upscale_factor, file_list, other_dataset, future_frame, upscale_only)
# testing_data_loader = DataLoader(dataset=test_set, num_workers=threads, batch_size=batch_size, shuffle=False)

# # print('==> Building model ', args.model_type)
# if model_type == 'RBPN':
#     model = RBPN(num_channels=3, base_filter=256,  feat = 64, num_stages=3, n_resblock=5, nFrames=nFrames, scale_factor=upscale_factor)


# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# if device != 'cpu':
#     model = model.cuda()
#     gpu_mode = True
# else:
#      gpu_mode = False   

# def eval():
#     # Initialize Logger
#     logger.initLogger(debug)


#     # load model
#     modelPath = os.path.join(model)
#     utils.loadPreTrainedModel(gpuMode=gpu_mode, model=model, modelPath=modelPath)

#     model.eval()
#     count = 0

#     for batch in testing_data_loader:
#         input, target, neigbor, flow, bicubic = batch[0], batch[1], batch[2], batch[3], batch[4]
        
#         with torch.no_grad():
#             if gpu_mode:
#                 input = Variable(input).cuda()
#                 bicubic = Variable(bicubic).cuda()
#                 neigbor = [Variable(j).cuda() for j in neigbor]
#                 flow = [Variable(j).cuda().float() for j in flow]
#             else:
#                 input = Variable(input).to(device=device, dtype=torch.float)
#                 bicubic = Variable(bicubic).to(device=device, dtype=torch.float)
#                 neigbor = [Variable(j).to(device=device, dtype=torch.float) for j in neigbor]
#                 flow = [Variable(j).to(device=device, dtype=torch.float) for j in flow]

#         t0 = time.time()
#         if chop_forward:
#             with torch.no_grad():
#                 prediction = chop_forward(input, neigbor, flow, model, upscale_factor)
#         else:
#             with torch.no_grad():
#                 prediction = model(input, neigbor, flow)
            
#         t1 = time.time()
#         print("==> Processing: %s || Timer: %.4f sec." % (str(count), (t1 - t0)))
#         save_img(prediction.cpu().data, str(count), True)

#         count += 1


# def save_img(img, img_name, pred_flag):
#     save_img = img.squeeze().clamp(0, 1).numpy().transpose(1,2,0)

#     # save img
#     save_dir=os.path.join(output, data_dir, os.path.splitext(file_list)[0]+'_'+str(upscale_factor)+'x')
#     if not os.path.exists(save_dir):
#         os.makedirs(save_dir)
        
#     if pred_flag:
#         save_fn = save_dir +'/'+ img_name+'_'+model_type+'F'+str(nFrames)+'.png'
#     else:
#         save_fn = save_dir +'/'+ img_name+'.png'
#     cv2.imwrite(save_fn, cv2.cvtColor(save_img*255, cv2.COLOR_BGR2RGB),  [cv2.IMWRITE_PNG_COMPRESSION, 0])

    
# def chop_forward(x, neigbor, flow, model, scale, shave=8, min_size=2000, nGPUs=1):
#     b, c, h, w = x.size()
#     h_half, w_half = h // 2, w // 2
#     h_size, w_size = h_half + shave, w_half + shave
#     inputlist = [
#         [x[:, :, 0:h_size, 0:w_size], [j[:, :, 0:h_size, 0:w_size] for j in neigbor], [j[:, :, 0:h_size, 0:w_size] for j in flow]],
#         [x[:, :, 0:h_size, (w - w_size):w], [j[:, :, 0:h_size, (w - w_size):w] for j in neigbor], [j[:, :, 0:h_size, (w - w_size):w] for j in flow]],
#         [x[:, :, (h - h_size):h, 0:w_size], [j[:, :, (h - h_size):h, 0:w_size] for j in neigbor], [j[:, :, (h - h_size):h, 0:w_size] for j in flow]],
#         [x[:, :, (h - h_size):h, (w - w_size):w], [j[:, :, (h - h_size):h, (w - w_size):w] for j in neigbor], [j[:, :, (h - h_size):h, (w - w_size):w] for j in flow]]]

#     if w_size * h_size < min_size:
#         outputlist = []
#         for i in range(0, 4, nGPUs):
#             with torch.no_grad():
#                 input_batch = inputlist[i]#torch.cat(inputlist[i:(i + nGPUs)], dim=0)
#                 output_batch = model(input_batch[0], input_batch[1], input_batch[2])
#             outputlist.extend(output_batch.chunk(nGPUs, dim=0))
#     else:
#         outputlist = [
#             chop_forward(patch[0], patch[1], patch[2], model, scale, shave, min_size, nGPUs) \
#             for patch in inputlist]

#     h, w = scale * h, scale * w
#     h_half, w_half = scale * h_half, scale * w_half
#     h_size, w_size = scale * h_size, scale * w_size
#     shave *= scale

#     with torch.no_grad():
#         output = Variable(x.data.new(b, c, h, w))
#     output[:, :, 0:h_half, 0:w_half] \
#         = outputlist[0][:, :, 0:h_half, 0:w_half]
#     output[:, :, 0:h_half, w_half:w] \
#         = outputlist[1][:, :, 0:h_half, (w_size - w + w_half):w_size]
#     output[:, :, h_half:h, 0:w_half] \
#         = outputlist[2][:, :, (h_size - h + h_half):h_size, 0:w_half]
#     output[:, :, h_half:h, w_half:w] \
#         = outputlist[3][:, :, (h_size - h + h_half):h_size, (w_size - w + w_half):w_size]

#     return output

# ##Eval Start!!!!
# eval()
