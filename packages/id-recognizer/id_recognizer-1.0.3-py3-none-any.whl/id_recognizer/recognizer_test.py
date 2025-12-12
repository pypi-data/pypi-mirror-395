from composition_id_recognizer import CompositionIdRecognizer, mat_to_b64, b64_to_mat
import asyncio
import cv2
from pathlib import Path


async def recognize_async(im):
    fn = Path(im).stem
    input_im = cv2.imread(filename=im, flags=cv2.IMREAD_COLOR)
    recognizer = CompositionIdRecognizer()
    result = await asyncio.to_thread(recognizer.recognize, input_im=input_im, enable_code=False)
    return result, fn


async def main(files: list):
    tasks = [
        asyncio.create_task(recognize_async(f))
        for f in files
    ]

    ret = await asyncio.gather(*tasks)
    return [(r[0].sid, r[1], r[0].sid == r[1]) for r in ret]


if __name__ == "__main__":
    im_dir_path = "/Users/asan/Downloads/作文批改2/10班应用文答题卡"
    directory = Path(im_dir_path)
    suffixes = [".JPG", ".JPEG", ".PNG", ".jpg", ".jpeg", ".png"]
    t_files = [f for f in directory.glob("*") if f.is_file() and f.suffix in suffixes]
    t_results = asyncio.run(main(files=t_files))

    print(t_results)
    # t_recognizer = CompositionIdRecognizer()
    # t_input = cv2.imread(t_files[0], flags=cv2.IMREAD_COLOR)
    # t_results = t_recognizer.recognize(input_im=t_input)
    # print(t_results)
