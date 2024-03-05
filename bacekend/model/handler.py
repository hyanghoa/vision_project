import os
import json
import torch
import cv2
import numpy as np
import albumentations as A
from albumentations.pytorch import ToTensorV2
from ts.torch_handler.base_handler import BaseHandler


class Handler(BaseHandler):
    """
    A custom model handler implementation.
    """

    def __init__(self):
        self._context = None
        self.initialized = False
        self.explain = False
        self.target = 0
        self.mapping = None

    def initialize(self, context):
        """
        Invoke by torchserve for loading a model
        :param context: context contains model server system properties
        :return:
        """

        #  load the model
        self.manifest = context.manifest

        properties = context.system_properties
        model_dir = properties.get("model_dir")
        self.device = torch.device(
            "cuda:" + str(properties.get("gpu_id"))
            if torch.cuda.is_available()
            else "cpu"
        )

        # Read model serialize/pt file
        serialized_file = self.manifest["model"]["serializedFile"]
        model_pt_path = os.path.join(model_dir, serialized_file)

        if not os.path.isfile(model_pt_path):
            raise RuntimeError("Missing the model.pt file")

        # load the mapping file
        mapping_file_path = os.path.join(model_dir, "yolov8_cls_label.json")
        if os.path.isfile(mapping_file_path):
            with open(mapping_file_path) as f:
                self.mapping = json.load(f)

        self.model = torch.jit.load(model_pt_path)
        self.model.eval()
        self.initialized = True

    def preprocess(self, data):
        """
        Transform raw input into model input data.
        :param batch: list of raw requests, should match batch size
        :return: list of preprocessed model input data
        """
        # Take the input data and make it inference ready
        preprocessed_data = data[0].get("data")
        if preprocessed_data is None:
            preprocessed_data = data[0].get("body")

        # Bytearray를 NumPy 배열로 변환합니다.
        image_array = np.frombuffer(preprocessed_data, dtype=np.uint8)

        # NumPy 배열을 OpenCV 이미지로 변환합니다.
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        # OpenCV 이미지를 BGR -> RGB 이미지로 변환합니다.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 이미지 전처리: 크기 조절, 정규화
        MEAN = (0.0, 0.0, 0.0)
        STD = (1.0, 1.0, 1.0)
        transform = A.Compose(
            [
                A.Resize(width=224, height=224),
                A.Normalize(mean=torch.tensor(MEAN), std=torch.tensor(STD)),
                ToTensorV2(),
            ]
        )
        transformed_image = transform(image=image)
        transformed_image = transformed_image["image"]

        preprocessed_data = torch.unsqueeze(transformed_image, 0)
        return preprocessed_data

    def inference(self, model_input):
        """
        Internal inference methods
        :param model_input: transformed model input data
        :return: list of inference output in NDArray
        """
        # Do some inference call to engine here and return output
        model_output = self.model(model_input)
        return model_output

    def postprocess(self, inference_output):
        """
        Return inference result.
        :param inference_output: list of inference output
        :return: list of predict results
        """
        # Take output from network and post-process to desired format
        postprocess_output = inference_output.argmax(-1).tolist()
        postprocess_output = [self.mapping[str(label)] for label in postprocess_output]
        return postprocess_output

    def handle(self, data, context):
        """
        Invoke by TorchServe for prediction request.
        Do pre-processing of data, prediction using model and postprocessing of prediciton output
        :param data: Input data for prediction
        :param context: Initial context contains model server system properties.
        :return: prediction output
        """
        model_input = self.preprocess(data)
        model_output = self.inference(model_input)
        return self.postprocess(model_output)
