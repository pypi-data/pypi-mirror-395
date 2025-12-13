import numpy as np

def speed_direction_batch(dets, tracks):
    tracks = tracks[..., np.newaxis]
    CX1, CY1 = (dets[:,0] + dets[:,2])/2.0, (dets[:,1]+dets[:,3])/2.0
    CX2, CY2 = (tracks[:,0] + tracks[:,2]) /2.0, (tracks[:,1]+tracks[:,3])/2.0
    dx = CX1 - CX2 
    dy = CY1 - CY2 
    norm = np.sqrt(dx**2 + dy**2) + 1e-6
    dx = dx / norm 
    dy = dy / norm
    return dy, dx # size: num_track x num_det


def linear_assignment(cost_matrix):
    try:
        import lap
        _, x, y = lap.lapjv(cost_matrix, extend_cost=True)
        return np.array([[y[i],i] for i in x if i >= 0]) #
    except ImportError:
        from scipy.optimize import linear_sum_assignment
        x, y = linear_sum_assignment(cost_matrix)
        return np.array(list(zip(x, y)))


def associate(self, detects, trks, velocities, previous_obs, vdc_weight, use_feature):    
    trackers = trks[:, :5]
    detections = detects[:, :6] 
    if(len(trackers)==0): #沒有track則不需匹配, 直接return
        return np.empty((0,2),dtype=int), np.arange(len(detections)), np.empty((0,5),dtype=int)

    #計算detection和各個previous_det的距離差 dx, dy
    Y, X = speed_direction_batch(detections, previous_obs)
    inertia_Y, inertia_X = velocities[:,0], velocities[:,1]
    inertia_Y = np.repeat(inertia_Y[:, np.newaxis], Y.shape[1], axis=1)
    inertia_X = np.repeat(inertia_X[:, np.newaxis], X.shape[1], axis=1)
    diff_angle_cos = inertia_X * X + inertia_Y * Y 
    #np.clip(a, b) 比a小的都變a, 比b大的都變b, ex: A=[0,1,2,3] np.clip(A,1,2) ---> A=[1,1,2,2]
    diff_angle_cos = np.clip(diff_angle_cos, a_min=-1, a_max=1)
    #arccos(餘弦值),cos返回去
    diff_angle = np.arccos(diff_angle_cos)
    diff_angle = (np.pi /2.0 - np.abs(diff_angle)) / np.pi
    valid_mask = np.ones(previous_obs.shape[0])
    valid_mask[np.where(previous_obs[:,4]<0)] = 0
    
    #比較detect_box和tracker_box的IoU (可更換IoU選擇: IoU, GIoU, CIoU...)
    iou_matrix = self.asso_func(detections, trackers)

    #scores = np.repeat(detections[:,-1][:, np.newaxis], trackers.shape[0], axis=1) #-1為原code，但我認為寫錯了，-1=cls,會隨著cls逐漸放大，應該是conf才對（？
    scores = np.repeat(detections[:,-2][:, np.newaxis], trackers.shape[0], axis=1)
    
    # iou_matrix = iou_matrix * scores # a trick sometiems works, we don't encourage this
    valid_mask = np.repeat(valid_mask[:, np.newaxis], X.shape[1], axis=1)

    angle_diff_cost = (valid_mask * diff_angle) * vdc_weight
    angle_diff_cost = angle_diff_cost.T
    ##很有問題==（scores = class * conf?? but 人的class = 0???) 改了之後沒有比較好，故保留！
    # angle_diff_cost = angle_diff_cost * (1 - scores)
    angle_diff_cost = angle_diff_cost * scores
    #建立trk_list
    if (trks != None).any():
      trk_ids = np.array(trks[:,5])
      trk_ids = np.asarray(trk_ids, dtype = int)
    else:
        trk_ids = []

    
    #為了不改變原code (結合特徵)
    if use_feature:
        features = detects[:, 7:] #前0-6不是
        #計算特徵的距離，並加權平均 cost_matrix = lamda * appear_matrix + (1-lamda) * IoU_matrix
        if len(trk_ids) > 0:
            appear_1_matrix = self.distance(np.array(features), trk_ids)
            pos_gate = iou_matrix < self.iou_threshold
            app_gate = appear_1_matrix < self.appear_threshold
            cost_matrix = self.lamda * appear_1_matrix + (1-self.lamda) * iou_matrix
            cost_matrix[np.logical_and(pos_gate, app_gate)] = 0
            bound = cost_matrix < self.lamda * self.appear_threshold + (1-self.lamda) * self.iou_threshold
            cost_matrix[bound] = 0

        else:
            cost_matrix = iou_matrix 

    else:
        cost_matrix = iou_matrix
            #為了不改變原code (結合特徵)

    #下面先用threshold篩選cost_matrix，然後再看是否有唯一的匹配，若沒有的話用「linear_assignment」
    if min(cost_matrix.shape) > 0 and trk_ids is not None:
        if use_feature:
            a = (cost_matrix > self.lamda * self.appear_threshold + (1-self.lamda) * self.iou_threshold).astype(np.int32)
        else:
            a = (cost_matrix > self.iou_threshold).astype(np.int32)
        if a.sum(1).max() == 1 and a.sum(0).max() == 1 :
            matched_indices = np.stack(np.where(a), axis=1)
        else:
            matched_indices = linear_assignment(-(cost_matrix+angle_diff_cost))
    else:
        matched_indices = np.empty(shape=(0,2))

    unmatched_detections = []
    for d, det in enumerate(detections):
        if(d not in matched_indices[:,0]):
            unmatched_detections.append(d)

    unmatched_trackers = []
    for t, trk in enumerate(trackers):
        if(t not in matched_indices[:,1]):
            unmatched_trackers.append(t)

    # filter out matched with low IOU (避免因為匈牙利演算法而導致過低分也考慮進去)
    matches = []
    for m in matched_indices:
        if use_feature and trk_ids is not None:
            if(cost_matrix[m[0], m[1]]<self.lamda * self.appear_threshold + (1-self.lamda) * self.iou_threshold):
                unmatched_detections.append(m[0])
                unmatched_trackers.append(m[1])
            else:
                matches.append(m.reshape(1,2))          
        else:
            if(iou_matrix[m[0], m[1]]<self.iou_threshold):
                unmatched_detections.append(m[0])
                unmatched_trackers.append(m[1])
            else:
                matches.append(m.reshape(1,2))
    if(len(matches)==0):
        matches = np.empty((0,2),dtype=int)
    else:
        matches = np.concatenate(matches,axis=0)
    return matches, np.array(unmatched_detections), np.array(unmatched_trackers)

