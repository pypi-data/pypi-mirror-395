"""
Entry point for the CLI inference of SPAGHETTI.
"""
import os
import argparse
from spaghetti import inferences
from PIL import Image


def inference(input, output, checkpoint):
    """
    The inference function for the CLI inference
    args:
        input: str, the input image or directory to translate
        output: str, the output directory to save the translated image(s)
        checkpoint: str, the path to the checkpoint file
    """
    # check if input is a directory
    if os.path.isdir(input):
        # get all images
        imgs = []
        names = []
        for path, _, files in os.walk(input):
            for f in files:
                if f.endswith((".jpg", ".jpeg", ".png", ".tiff", ".tif")):
                    imgs.append(os.path.join(path, f))
                    names.append(f.split(".")[0])
    else:
        imgs = [input]
        names = [str(os.path.basename(input)).split(".")[0]]
    # create the model
    model = inferences.Spaghetti(checkpoint)
    # perform the inference
    pil_imgs = [Image.open(img).convert("RGB") for img in imgs]
    processed_imgs = model.pre_processing(pil_imgs, transform="default")
    model.inference(processed_imgs, names, output)


def main():
    parser = argparse.ArgumentParser(description="CLI for translating PCM images using SPAGHETTI")
    parser.add_argument("--input", '-i', type=str, help="The input image or directory to translate")
    parser.add_argument("--output", '-o', type=str, help="The output directory to save the translated image(s)")
    parser.add_argument("--checkpoint", '-c', type=str, help="The path to the checkpoint file", required=True)
    args = parser.parse_args()
    assert os.path.exists(args.checkpoint), "The checkpoint file does not exist"
    print("Welcome to SPAGHETTI CLI Inference")
    print("Checkpoint file found at ", args.checkpoint, "will be used for inference")
    print("Starting Inference...")
    inference(args.input, args.output, args.checkpoint)
    print("Inference Completed. Images saved to ", args.output)


if __name__ == "__main__":
    main()
