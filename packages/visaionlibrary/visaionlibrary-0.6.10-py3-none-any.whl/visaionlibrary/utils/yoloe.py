import os
import numpy as np
from PIL import Image
from ultralytics import YOLOE
from ultralytics.models.yolo.yoloe.predict_vp import YOLOEVPSegPredictor


class YoloE:
    def __init__(self, model_path="yoloe-v8l-seg.pt", device="cuda:0"):
        VISAION_DIR = os.getenv("VISAION_DIR")
        if VISAION_DIR is None:
            raise ValueError("VISAION_DIR is not set")
        self.model_path = os.path.join(VISAION_DIR, "weights", model_path)
        self.device = device

    def visual(self, images:list[Image.Image], prompt_images:list[Image.Image], prompt_boxes:dict[str, list[np.ndarray]], prompt_names:list[str], **kwargs):
        """
        Predict the visual prompt of the images.
        Args:
            images: list[Image.Image]
            prompt_images: list[Image.Image]
            prompt_boxes: dict[str, list[np.ndarray]]
            prompt_names: list[str]
            **kwargs: dict
        Returns:
            list[Image.Image]
            list[str]
            list[float]
            list[list[float]]
            list[list[list[float]]]
        """
        assert "bboxes" in prompt_boxes and "cls" in prompt_boxes, f"prompt_boxes must contain 'bboxes' and 'cls'"
        assert len(prompt_images) == len(prompt_boxes["bboxes"]) == len(prompt_boxes["cls"]) == len(prompt_names), f"the length of prompt_image, prompt_boxes['bboxes'], prompt_boxes['cls'], and prompt_names must be the same"

        for prompt_image, prompt_box, prompt_cls, prompt_name in zip(prompt_images, prompt_boxes["bboxes"], prompt_boxes["cls"], prompt_names):
            visual_prompt = dict(
                bboxes=prompt_box,
                cls=prompt_cls,
            )

            model = YOLOE(self.model_path)
            model.to(self.device)
            model.predict(prompt_image, prompts=visual_prompt, predictor=YOLOEVPSegPredictor, return_vpe=True, **kwargs)
            model.set_classes(prompt_name, model.predictor.vpe)
            model.predictor = None  # remove VPPredictor
            results = model.predict(images, save=False, **kwargs)
            for image_index,result in enumerate(results):
                classes_index = result.boxes.cls.detach().cpu().numpy()
                class_names = [prompt_name[int(class_index)] for class_index in classes_index]
                confidence = result.boxes.conf.detach().cpu().numpy()
                bboxes = result.boxes.xyxy.detach().cpu().numpy()
                if result.masks is not None:
                    masks = result.masks.cpu().numpy()
                else:
                    masks = None
                yield image_index, class_names, confidence, bboxes, masks


    def text(self, images:list[Image.Image], prompt:list[str], **kwargs):
        """
        Predict the visual prompt of the images.
        Args:
            images: list[Image.Image]
            prompt: list[str]
            **kwargs: dict
        Returns:
            list[Image.Image]
            list[str]
            list[float]
            list[list[float]]
            list[list[list[float]]]
        """
        model = YOLOE(self.model_path)
        model.to(self.device)
        model.set_classes(prompt, model.get_text_pe(prompt))
        results = model.predict(images, verbose=False, **kwargs)
        for image_index,result in enumerate(results):
            classes_index = result.boxes.cls.detach().cpu().numpy()
            class_names = [prompt[int(class_index)] for class_index in classes_index]
            confidence = result.boxes.conf.detach().cpu().numpy()
            bboxes = result.boxes.xyxy.detach().cpu().numpy()
            if result.masks is not None:
                masks = result.masks.cpu().numpy()
            else:
                masks = None
            yield image_index, class_names, confidence, bboxes, masks

AILabel = YoloE