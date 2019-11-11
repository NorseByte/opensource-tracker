from pkg_resources import resource_filename

def pose_predictor_five_point_model_location():
    return resource_filename(__name__, "face_models/shape_predictor_5_face_landmarks.dat")

def face_recognition_model_location():
    return resource_filename(__name__, "face_models/dlib_face_recognition_resnet_model_v1.dat")

def cnn_face_detector_model_location():
    return resource_filename(__name__, "face_models/mmod_human_face_detector.dat")